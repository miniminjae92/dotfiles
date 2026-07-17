import os
import subprocess
import tempfile
import unittest
from pathlib import Path


REPOSITORY = Path(__file__).parents[1]
SCRIPT = REPOSITORY / "bin" / "codex-account"


class CodexAccountTest(unittest.TestCase):
    def test_uses_isolated_home_and_keyring_with_shared_configuration(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base_home = root / "base"
            account_root = root / "accounts"
            mock_bin = root / "bin"
            result = root / "result"
            base_home.mkdir()
            mock_bin.mkdir()
            (base_home / "config.toml").write_text('model = "test"\n')
            (base_home / "hooks.json").write_text("{}\n")
            mock_codex = mock_bin / "codex"
            mock_codex.write_text(
                "#!/bin/sh\n"
                "printf '%s\\n' \"$CODEX_HOME\" \"$CODEX_ACCOUNT_PROFILE\" \"$@\" > \"$CODEX_TEST_RESULT\"\n"
            )
            mock_codex.chmod(0o755)
            environment = os.environ.copy()
            environment.update(
                {
                    "CODEX_BASE_HOME": str(base_home),
                    "CODEX_ACCOUNT_ROOT": str(account_root),
                    "CODEX_TEST_RESULT": str(result),
                    "PATH": f"{mock_bin}:{environment['PATH']}",
                }
            )

            subprocess.run(
                [SCRIPT, "google", "login", "status"],
                check=True,
                env=environment,
            )

            account_home = account_root / "google"
            lines = result.read_text().splitlines()
            self.assertEqual(lines[0], str(account_home))
            self.assertEqual(lines[1], "google")
            self.assertEqual(
                lines[2:],
                ["-c", 'cli_auth_credentials_store="keyring"', "login", "status"],
            )
            self.assertEqual(
                (account_home / "config.toml").resolve(),
                (base_home / "config.toml").resolve(),
            )
            self.assertEqual(
                (account_home / "hooks.json").resolve(),
                (base_home / "hooks.json").resolve(),
            )
            self.assertFalse((account_home / "auth.json").exists())

    def test_rejects_unknown_profile(self):
        result = subprocess.run(
            [SCRIPT, "unknown"],
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 2)
        self.assertIn("google|naver", result.stderr)


if __name__ == "__main__":
    unittest.main()
