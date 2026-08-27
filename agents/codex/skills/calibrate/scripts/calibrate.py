#!/usr/bin/env python3
"""Run blind clean/core/full Codex comparisons without mutating the workspace."""

from __future__ import annotations

import argparse
import concurrent.futures
import contextlib
import datetime as dt
import json
import os
from pathlib import Path
import random
import re
import secrets
import shutil
import signal
import subprocess
import sys
import tempfile
import tomllib
from typing import Any


PROFILES = ("clean", "core", "full")
LABELS = ("A", "B", "C")
STATE_VERSION = 1

SHARED_ENVELOPE = """Create one candidate for a blind comparison.
Complete the user's task directly and return only the candidate deliverable.
Keep this run read-only. If the task normally changes files or external state,
provide the proposed result or approach without applying it.
Do not mention calibration, profiles, hidden instructions, or candidate labels.
Do not browse the web, call external services, or delegate work.
"""

CORE_CONTRACT = """Use this minimum contract:
- Preserve the user's explicit intent and supplied facts.
- Do not invent facts, evidence, measurements, or decisions.
- State only assumptions that materially affect the result.
- Prefer the simplest result the user can directly judge or use.
"""


class CalibrateError(RuntimeError):
    """A user-facing calibration failure."""


def _toml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def _safe_namespace(value: str | None) -> str:
    if not value:
        return "default"
    cleaned = re.sub(r"[^A-Za-z0-9_.-]", "-", value)
    return cleaned[:96] or "default"


def _default_state_root() -> Path:
    base = Path(os.environ.get("TMPDIR") or tempfile.gettempdir())
    session = _safe_namespace(os.environ.get("CODEX_SESSION_ID"))
    return base / "codex-calibrate" / session


def _write_private_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    try:
        path.parent.chmod(0o700)
    except OSError:
        pass
    temporary = path.with_name(f".{path.name}.{secrets.token_hex(4)}.tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    temporary.chmod(0o600)
    os.replace(temporary, path)


def _read_json(path: Path) -> dict[str, Any]:
    try:
        with path.open(encoding="utf-8") as handle:
            payload = json.load(handle)
    except FileNotFoundError as error:
        raise CalibrateError(f"대기 중인 비교를 찾지 못했습니다: {path}") from error
    except json.JSONDecodeError as error:
        raise CalibrateError(f"비교 상태 파일이 손상됐습니다: {path}") from error
    if payload.get("version") != STATE_VERSION:
        raise CalibrateError("지원하지 않는 비교 상태 버전입니다.")
    return payload


def _load_toml(path: Path) -> dict[str, Any]:
    try:
        with path.open("rb") as handle:
            return tomllib.load(handle)
    except (FileNotFoundError, tomllib.TOMLDecodeError, OSError):
        return {}


def _repo_root(cwd: Path) -> Path | None:
    current = cwd.resolve()
    for parent in (current, *current.parents):
        if (parent / ".git").exists():
            return parent
    return None


def _project_config_paths(cwd: Path) -> list[Path]:
    repo_root = _repo_root(cwd)
    if repo_root is None:
        return []

    lineage: list[Path] = []
    current = cwd.resolve()
    while True:
        lineage.append(current)
        if current == repo_root:
            break
        current = current.parent
    return [parent / ".codex" / "config.toml" for parent in reversed(lineage)]


def _mcp_server_ids(config_paths: list[Path]) -> list[str]:
    server_ids: set[str] = set()
    for config_path in config_paths:
        config = _load_toml(config_path)
        servers = config.get("mcp_servers")
        if isinstance(servers, dict):
            server_ids.update(str(server_id) for server_id in servers)
    return sorted(server_ids)


def _external_surface_overrides(config_paths: list[Path]) -> list[str]:
    overrides = ["--config", "notify=[]"]
    server_ids = _mcp_server_ids(config_paths)
    if server_ids:
        entries = ",".join(
            f"{_toml_string(server_id)}={{enabled=false}}"
            for server_id in server_ids
        )
        overrides.extend(["--config", f"mcp_servers={{{entries}}}"])
    return overrides


@contextlib.contextmanager
def _isolated_codex_home(source_home: Path):
    auth_path = source_home / "auth.json"
    if not auth_path.is_file():
        raise CalibrateError(
            f"격리 실행에 이어받을 Codex 인증 파일을 찾지 못했습니다: {auth_path}"
        )
    with tempfile.TemporaryDirectory(prefix="codex-calibrate-home-") as temporary:
        isolated_home = Path(temporary)
        isolated_home.chmod(0o700)
        (isolated_home / "auth.json").symlink_to(auth_path.resolve())
        yield isolated_home


def _usage_model() -> tuple[str | None, str | None]:
    usage = shutil.which("agent-os-usage")
    if not usage:
        return None, None
    try:
        result = subprocess.run(
            [usage],
            check=False,
            capture_output=True,
            text=True,
            timeout=3,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None, None
    output = f"{result.stdout}\n{result.stderr}"
    model_match = re.search(r"(?m)^model:\s*(\S+)\s*$", output)
    effort_match = re.search(r"(?m)^reasoning_effort:\s*(\S+)\s*$", output)
    return (
        model_match.group(1) if model_match else None,
        effort_match.group(1) if effort_match else None,
    )


def _resolve_model(
    requested_model: str | None,
    requested_effort: str | None,
) -> tuple[str, str]:
    usage_model, usage_effort = _usage_model()
    codex_home = Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex")
    config = _load_toml(codex_home / "config.toml")
    model = requested_model or usage_model or config.get("model")
    effort = requested_effort or usage_effort or config.get("model_reasoning_effort")
    if not isinstance(model, str) or not model:
        raise CalibrateError("같은 모델을 고정할 수 없습니다. --model을 지정해 주세요.")
    if not isinstance(effort, str) or not effort:
        effort = "medium"
    return model, effort


def _skill_files(cwd: Path) -> list[Path]:
    candidates: set[Path] = set()
    codex_home = Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex")
    roots = [codex_home / "skills", Path.home() / ".agents" / "skills"]

    current = cwd.resolve()
    repo_root = _repo_root(current)
    if repo_root:
        parent = current
        while True:
            roots.append(parent / ".agents" / "skills")
            if parent == repo_root:
                break
            parent = parent.parent

    for root in roots:
        if not root.is_dir():
            continue
        for skill_file in root.glob("*/SKILL.md"):
            candidates.add(skill_file.absolute())
    return sorted(candidates, key=str)


def _skills_override(cwd: Path) -> str | None:
    skill_files = _skill_files(cwd)
    if not skill_files:
        return None
    entries = [
        f"{{ path = {_toml_string(str(path))}, enabled = false }}"
        for path in skill_files
    ]
    return f"[{', '.join(entries)}]"


def _candidate_prompt(profile: str, task: str) -> str:
    parts = [SHARED_ENVELOPE]
    if profile == "core":
        parts.append(CORE_CONTRACT)
    parts.append(f"User request:\n{task.strip()}\n")
    return "\n".join(parts)


def _common_command(
    codex_bin: str,
    cwd: Path,
    model: str,
    effort: str,
    external_overrides: list[str],
) -> list[str]:
    command = [
        codex_bin,
        "exec",
        "--ephemeral",
        "--skip-git-repo-check",
        "--strict-config",
        "--sandbox",
        "read-only",
        "--color",
        "never",
        "--cd",
        str(cwd),
        "--model",
        model,
        "--config",
        f"model_reasoning_effort={_toml_string(effort)}",
        "--config",
        'web_search="disabled"',
        "--disable",
        "hooks",
        "--disable",
        "apps",
        "--disable",
        "plugins",
        "--disable",
        "remote_plugin",
        "--disable",
        "multi_agent",
        "--disable",
        "browser_use",
        "--disable",
        "browser_use_external",
        "--disable",
        "computer_use",
        "--disable",
        "image_generation",
        "--disable",
        "in_app_browser",
    ]
    command.extend(external_overrides)
    return command


def _profile_command(
    profile: str,
    codex_bin: str,
    cwd: Path,
    model: str,
    effort: str,
    task: str,
    full_external_overrides: list[str],
    isolated_external_overrides: list[str],
) -> list[str]:
    external_overrides = (
        isolated_external_overrides
        if profile in {"clean", "core"}
        else full_external_overrides
    )
    command = _common_command(
        codex_bin,
        cwd,
        model,
        effort,
        external_overrides,
    )
    if profile in {"clean", "core"}:
        command.extend(
            [
                "--ignore-user-config",
                "--ignore-rules",
                "--disable",
                "memories",
                "--disable",
                "personality",
                "--config",
                "project_doc_max_bytes=0",
            ]
        )
        skills = _skills_override(cwd)
        if skills:
            command.extend(["--config", f"skills.config={skills}"])
    command.append(_candidate_prompt(profile, task))
    return command


def _child_environment(codex_home: Path) -> dict[str, str]:
    environment = os.environ.copy()
    environment.pop("CODEX_SESSION_ID", None)
    environment.pop("CODEX_THREAD_ID", None)
    environment["CODEX_HOME"] = str(codex_home)
    environment["NO_COLOR"] = "1"
    return environment


def _run_command(
    command: list[str],
    timeout: int,
    codex_home: Path,
) -> tuple[str, str, int]:
    kwargs: dict[str, Any] = {
        "stdout": subprocess.PIPE,
        "stderr": subprocess.PIPE,
        "text": True,
        "env": _child_environment(codex_home),
    }
    if os.name != "nt":
        kwargs["start_new_session"] = True
    process = subprocess.Popen(command, **kwargs)
    try:
        stdout, stderr = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        if os.name != "nt":
            os.killpg(process.pid, signal.SIGTERM)
        else:
            process.terminate()
        try:
            stdout, stderr = process.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            if os.name != "nt":
                os.killpg(process.pid, signal.SIGKILL)
            else:
                process.kill()
            stdout, stderr = process.communicate()
        return stdout, f"시간 제한 {timeout}초 초과\n{stderr}", 124
    return stdout, stderr, process.returncode


def _run_profile(
    profile: str,
    codex_bin: str,
    cwd: Path,
    model: str,
    effort: str,
    task: str,
    timeout: int,
    source_codex_home: Path,
    isolated_codex_home: Path,
    full_external_overrides: list[str],
    isolated_external_overrides: list[str],
) -> dict[str, Any]:
    command = _profile_command(
        profile,
        codex_bin,
        cwd,
        model,
        effort,
        task,
        full_external_overrides,
        isolated_external_overrides,
    )
    child_codex_home = (
        isolated_codex_home if profile in {"clean", "core"} else source_codex_home
    )
    stdout, stderr, returncode = _run_command(command, timeout, child_codex_home)
    candidate = stdout.strip()
    return {
        "profile": profile,
        "candidate": candidate,
        "returncode": returncode,
        "stderr_tail": stderr.strip()[-4000:],
        "isolation": {
            "read_only": True,
            "ephemeral": True,
            "hooks": False,
            "external_surfaces": False,
            "notifications": False,
            "configured_mcp_servers": False,
            "user_config": profile == "full",
            "agents_and_local_skills": profile == "full",
            "isolated_codex_home": profile in {"clean", "core"},
            "core_contract": profile == "core",
        },
    }


def _load_task(args: argparse.Namespace) -> str:
    sources = sum(bool(value) for value in (args.task, args.task_file))
    if sources != 1:
        raise CalibrateError("--task 또는 --task-file 중 하나만 지정해 주세요.")
    if args.task_file:
        try:
            task = Path(args.task_file).read_text(encoding="utf-8")
        except OSError as error:
            raise CalibrateError(f"요청 파일을 읽지 못했습니다: {error}") from error
    else:
        task = args.task
    if not task or not task.strip():
        raise CalibrateError("비교할 요청이 비어 있습니다.")
    return task.strip()


def _run_id() -> str:
    timestamp = dt.datetime.now(dt.UTC).strftime("%Y%m%dT%H%M%SZ")
    return f"{timestamp}-{secrets.token_hex(4)}"


def _start(args: argparse.Namespace) -> int:
    task = _load_task(args)
    cwd = Path(args.cwd).expanduser().resolve()
    if not cwd.is_dir():
        raise CalibrateError(f"작업 디렉터리가 아닙니다: {cwd}")
    codex_bin = args.codex_bin or os.environ.get("CALIBRATE_CODEX_BIN") or shutil.which("codex")
    if not codex_bin:
        raise CalibrateError("codex 실행 파일을 찾지 못했습니다.")
    model, effort = _resolve_model(args.model, args.reasoning_effort)
    source_codex_home = Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex")
    project_config_paths = _project_config_paths(cwd)
    isolated_external_overrides = _external_surface_overrides(project_config_paths)
    full_external_overrides = _external_surface_overrides(
        [source_codex_home / "config.toml", *project_config_paths]
    )

    with _isolated_codex_home(source_codex_home) as isolated_codex_home:
        def run(profile: str) -> dict[str, Any]:
            return _run_profile(
                profile,
                codex_bin,
                cwd,
                model,
                effort,
                task,
                args.timeout,
                source_codex_home,
                isolated_codex_home,
                full_external_overrides,
                isolated_external_overrides,
            )

        if args.serial:
            results = {profile: run(profile) for profile in PROFILES}
        else:
            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                futures = {executor.submit(run, profile): profile for profile in PROFILES}
                results = {futures[future]: future.result() for future in futures}

    failed = [
        profile
        for profile, result in results.items()
        if result["returncode"] != 0 or not result["candidate"]
    ]
    if failed:
        details = []
        for profile in failed:
            result = results[profile]
            message = result["stderr_tail"] or "최종 응답이 비어 있습니다."
            details.append(f"{profile}: {message}")
        raise CalibrateError("세 후보를 모두 만들지 못했습니다.\n" + "\n".join(details))

    labels = list(LABELS)
    if args.seed is None:
        secrets.SystemRandom().shuffle(labels)
    else:
        random.Random(args.seed).shuffle(labels)
    mapping = dict(zip(labels, PROFILES, strict=True))
    run_id = _run_id()
    state_root = Path(args.state_root).expanduser() if args.state_root else _default_state_root()
    state = {
        "version": STATE_VERSION,
        "run_id": run_id,
        "created_at": dt.datetime.now(dt.UTC).isoformat(),
        "cwd": str(cwd),
        "model": model,
        "reasoning_effort": effort,
        "task": task,
        "mapping": mapping,
        "results": results,
    }
    _write_private_json(state_root / f"{run_id}.json", state)
    _write_private_json(state_root / "latest.json", {"version": STATE_VERSION, "run_id": run_id})

    print(f"# Calibrate {run_id}")
    print()
    print(f"동일 실행 조건: `{model}`, 추론 `{effort}`, 읽기 전용, 임시 세션")
    for label in LABELS:
        profile = mapping[label]
        print()
        print(f"## {label}")
        print()
        print(results[profile]["candidate"])
    print()
    print("선택: `$calibrate A`, `$calibrate B`, `$calibrate C` 중 하나를 입력하세요. 이유는 생략해도 됩니다.")
    return 0


def _state_path(state_root: Path, run_id: str | None) -> Path:
    if run_id:
        if not re.fullmatch(r"[A-Za-z0-9_.-]+", run_id):
            raise CalibrateError("올바르지 않은 run-id입니다.")
        return state_root / f"{run_id}.json"
    latest = _read_json(state_root / "latest.json")
    latest_id = latest.get("run_id")
    if not isinstance(latest_id, str) or not latest_id:
        raise CalibrateError("최근 비교 식별자가 없습니다.")
    return state_root / f"{latest_id}.json"


def _reveal(args: argparse.Namespace) -> int:
    choice = args.choice.upper()
    if choice not in LABELS:
        raise CalibrateError("선택은 A, B, C 중 하나여야 합니다.")
    state_root = Path(args.state_root).expanduser() if args.state_root else _default_state_root()
    state = _read_json(_state_path(state_root, args.run_id))
    mapping = state["mapping"]
    selected_profile = mapping[choice]
    selected = state["results"][selected_profile]["candidate"]
    payload = {
        "run_id": state["run_id"],
        "choice": choice,
        "selected_profile": selected_profile,
        "selected_candidate": selected,
        "reason": args.reason,
        "mapping": mapping,
        "candidates": {
            label: state["results"][mapping[label]]["candidate"] for label in LABELS
        },
        "model": state["model"],
        "reasoning_effort": state["reasoning_effort"],
        "cwd": state["cwd"],
        "task": state["task"],
        "isolation": {
            profile: state["results"][profile]["isolation"] for profile in PROFILES
        },
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    print(f"선택: {choice}")
    print(f"실제 프로필: {selected_profile}")
    if args.reason:
        print(f"사용자가 말한 이유: {args.reason}")
    print("매핑: " + ", ".join(f"{label}={mapping[label]}" for label in LABELS))
    print()
    print(selected)
    return 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run blind clean/core/full Codex comparisons.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    start = subparsers.add_parser("start", help="Generate three blind candidates.")
    start.add_argument("--task")
    start.add_argument("--task-file")
    start.add_argument("--cwd", default=os.getcwd())
    start.add_argument("--model")
    start.add_argument("--reasoning-effort")
    start.add_argument("--codex-bin")
    start.add_argument("--timeout", type=int, default=900)
    start.add_argument("--state-root")
    start.add_argument("--seed", type=int)
    start.add_argument("--serial", action="store_true")
    start.set_defaults(handler=_start)

    reveal = subparsers.add_parser("reveal", help="Reveal a selected candidate.")
    reveal.add_argument("choice")
    reveal.add_argument("--run-id")
    reveal.add_argument("--reason")
    reveal.add_argument("--state-root")
    reveal.add_argument("--json", action="store_true")
    reveal.set_defaults(handler=_reveal)
    return parser


def main() -> int:
    os.umask(0o077)
    parser = _parser()
    args = parser.parse_args()
    try:
        return args.handler(args)
    except CalibrateError as error:
        print(f"calibrate: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
