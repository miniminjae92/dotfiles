import json
import hashlib
import os
from pathlib import Path
import re
import subprocess
import tempfile
import unittest


FRAGMENT = Path(__file__).parents[1] / "agents" / "claude" / "settings-fragment.json"
INSTALL = Path(__file__).parents[1] / "install.sh"


class ClaudeHookConfigTests(unittest.TestCase):
    def test_markdown_post_tool_hook_uses_guarded_ko_style_wrapper(self):
        fragment = json.loads(FRAGMENT.read_text(encoding="utf-8"))
        groups = fragment["hooks"]["PostToolUse"]
        group = next(group for group in groups if group.get("matcher") == "Write|Edit|MultiEdit")
        hook = next(hook for hook in group["hooks"] if "ko-style" in hook["command"])

        self.assertEqual(hook["timeout"], 15)
        self.assertEqual(
            hook["command"],
            'if [ -x "$HOME/.local/bin/ko-style-hook" ]; then "$HOME/.local/bin/ko-style-hook"; fi',
        )

    def test_installer_replaces_legacy_inline_ko_style_without_duplicate(self):
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary) / "home"
            mock_bin = Path(temporary) / "bin"
            mock_bin.mkdir()
            launchctl = mock_bin / "launchctl"
            launchctl.write_text("#!/bin/sh\n[ \"$1\" = print ] && exit 1\nexit 0\n",
                                 encoding="utf-8")
            launchctl.chmod(0o755)
            git = mock_bin / "git"
            git.write_text("#!/bin/sh\n[ \"$1\" = config ] && exit 0\nexit 1\n",
                           encoding="utf-8")
            git.chmod(0o755)
            settings = home / ".claude" / "settings.json"
            settings.parent.mkdir(parents=True)
            settings.write_text(json.dumps({"hooks": {"PostToolUse": [{
                "matcher": "Write|Edit|MultiEdit",
                "hooks": [
                    {"type": "command", "command": "$HOME/.local/bin/ko-style", "timeout": 15},
                    {"type": "command", "command": "$HOME/.local/bin/ko-style-hook", "timeout": 15},
                ],
            }]}}, ensure_ascii=False), encoding="utf-8")

            source_gitconfig = FRAGMENT.parents[2] / ".gitconfig"
            before = hashlib.sha256(source_gitconfig.read_bytes()).hexdigest()
            result = subprocess.run(
                [str(INSTALL)],
                env={**os.environ, "HOME": str(home), "DOTFILES_DIR": str(FRAGMENT.parents[2]),
                     "PATH": f"{mock_bin}:{os.environ['PATH']}"},
                capture_output=True, text=True, check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(before, hashlib.sha256(source_gitconfig.read_bytes()).hexdigest())
            merged = json.loads(settings.read_text(encoding="utf-8"))
            group = next(group for group in merged["hooks"]["PostToolUse"]
                         if group.get("matcher") == "Write|Edit|MultiEdit")
            commands = [hook["command"] for hook in group["hooks"]]
            self.assertEqual(sum("ko-style-hook" in command for command in commands), 1)
            self.assertFalse(any(re.search(r"bin/ko-style(?:[\"' ;]|$)", command)
                                 for command in commands))

            first_bytes = settings.read_bytes()
            first_mtime = settings.stat().st_mtime_ns
            repeat = subprocess.run(
                [str(INSTALL)],
                env={**os.environ, "HOME": str(home), "DOTFILES_DIR": str(FRAGMENT.parents[2]),
                     "PATH": f"{mock_bin}:{os.environ['PATH']}"},
                capture_output=True, text=True, check=False,
            )
            self.assertEqual(repeat.returncode, 0, repeat.stderr)
            self.assertIn("claude settings already configured", repeat.stdout)
            self.assertEqual(first_bytes, settings.read_bytes())
            self.assertEqual(first_mtime, settings.stat().st_mtime_ns)
            self.assertEqual(before, hashlib.sha256(source_gitconfig.read_bytes()).hexdigest())


if __name__ == "__main__":
    unittest.main()
