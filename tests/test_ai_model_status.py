import importlib.machinery
import importlib.util
import subprocess
import unittest
from pathlib import Path
from unittest import mock


SCRIPT_PATH = Path(__file__).parents[1] / "bin" / "ai-model-status"
LOADER = importlib.machinery.SourceFileLoader("ai_model_status", str(SCRIPT_PATH))
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
ai_model_status = importlib.util.module_from_spec(SPEC)
LOADER.exec_module(ai_model_status)


class AiModelStatusTest(unittest.TestCase):
    def test_loads_all_task_bindings_from_registry(self):
        registry_path = Path(__file__).parents[1] / "ai-tools" / "models.json"

        registry = ai_model_status.load_registry(registry_path)
        bindings = ai_model_status.collect_bindings(registry)

        self.assertIn(
            ai_model_status.Binding(
                "git_plan", "agy", "agy_gemini_fast", "Gemini 3.5 Flash (Low)"
            ),
            bindings,
        )
        self.assertIn(
            ai_model_status.Binding("video_summary", "codex", None, None),
            bindings,
        )

    def test_environment_override_is_reported_as_effective_model(self):
        bindings = [
            ai_model_status.Binding(
                "git_plan", "agy", "agy_gemini_fast", "agy-default"
            )
        ]

        with mock.patch.dict(
            ai_model_status.os.environ,
            {"GIT_PLAN_AI_AGY_MODEL": "agy-override"},
        ):
            effective = ai_model_status.effective_bindings(bindings)

        self.assertEqual(effective[0].model, "agy-override")
        self.assertEqual(
            effective[0].model_ref,
            "env:GIT_PLAN_AI_AGY_MODEL",
        )

    @mock.patch.object(ai_model_status.shutil, "which", return_value="/fake/codex")
    @mock.patch.object(ai_model_status.subprocess, "run")
    def test_codex_static_check_does_not_run_inference(self, run, _which):
        run.side_effect = [
            subprocess.CompletedProcess(
                ["codex", "--version"], 0, stdout="codex-cli 1.0\n", stderr=""
            ),
            subprocess.CompletedProcess(
                ["codex", "login", "status"],
                0,
                stdout="Logged in using ChatGPT\n",
                stderr="",
            ),
        ]

        status = ai_model_status.static_provider_status(
            "codex", ("gpt-test", None)
        )

        self.assertTrue(status["installed"])
        self.assertEqual(status["auth"], "Logged in using ChatGPT")
        commands = [call.args[0] for call in run.call_args_list]
        self.assertNotIn("exec", [part for command in commands for part in command])

    @mock.patch.object(ai_model_status.shutil, "which", return_value="/fake/agy")
    @mock.patch.object(ai_model_status.subprocess, "run")
    def test_agy_probe_uses_plan_mode_in_empty_directory(self, run, _which):
        run.return_value = subprocess.CompletedProcess(
            ["agy"], 0, stdout="OK\n", stderr=""
        )

        result = ai_model_status.probe_model("agy", "Gemini test")

        self.assertEqual(result["status"], "ok")
        command = run.call_args.args[0]
        self.assertEqual(command[0], "agy")
        self.assertIn("--mode", command)
        self.assertIn("plan", command)
        self.assertIn("--sandbox", command)
        self.assertEqual(run.call_args.kwargs["env"]["CI"], "1")
        self.assertNotEqual(Path(run.call_args.kwargs["cwd"]), Path.cwd())


if __name__ == "__main__":
    unittest.main()
