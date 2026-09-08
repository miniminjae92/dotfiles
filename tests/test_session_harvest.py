import importlib.machinery
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT_PATH = Path(__file__).parents[1] / "bin" / "session-harvest"
LOADER = importlib.machinery.SourceFileLoader("session_harvest", str(SCRIPT_PATH))
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
session_harvest = importlib.util.module_from_spec(SPEC)
LOADER.exec_module(session_harvest)


class SessionHarvestTest(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.home = Path(self.temporary_directory.name)
        self.home_patch = mock.patch.object(session_harvest, "HOME", self.home)
        self.home_patch.start()

    def tearDown(self):
        self.home_patch.stop()
        self.temporary_directory.cleanup()

    def test_agy_model_falls_back_to_gemini_37_when_registry_is_missing(self):
        self.assertEqual(session_harvest.agy_model(), "Gemini 3.7 Flash (Low)")

    def test_agy_model_falls_back_to_gemini_37_when_registry_is_invalid(self):
        registry = self.home / ".config/ai-tools/models.json"
        registry.parent.mkdir(parents=True)
        registry.write_text("not json", encoding="utf-8")

        self.assertEqual(session_harvest.agy_model(), "Gemini 3.7 Flash (Low)")

    def test_agy_model_uses_registry_value(self):
        registry = self.home / ".config/ai-tools/models.json"
        registry.parent.mkdir(parents=True)
        registry.write_text(
            json.dumps({"models": {"agy_gemini_fast": "registry-model"}}),
            encoding="utf-8",
        )

        self.assertEqual(session_harvest.agy_model(), "registry-model")


if __name__ == "__main__":
    unittest.main()
