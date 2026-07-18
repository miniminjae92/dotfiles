import os
import subprocess
import tempfile
import unittest
from pathlib import Path


REPOSITORY = Path(__file__).parents[1]
SCRIPT = REPOSITORY / "bin" / "codex-account"
LOGIN_SCRIPT = REPOSITORY / "bin" / "codex-account-login"


class CodexAccountTest(unittest.TestCase):
    def test_uses_isolated_home_and_file_auth_with_shared_configuration(self):
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
                ["-c", 'cli_auth_credentials_store="file"', "login", "status"],
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


class CodexAccountLoginTest(unittest.TestCase):
    def test_opens_configured_chrome_profile_and_uses_device_auth(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            mock_bin = root / "bin"
            mock_bin.mkdir()
            codex_calls = root / "codex-calls"
            open_call = root / "open-call"
            mock_codex = mock_bin / "codex"
            mock_codex.write_text(
                "#!/bin/sh\n"
                "printf '%s\\n' \"$@\" >> \"$CODEX_TEST_CALLS\"\n"
                "if [ \"${3:-}\" = login ] && [ \"${4:-}\" = status ]; then exit 1; fi\n"
            )
            mock_codex.chmod(0o755)
            mock_open = mock_bin / "open"
            mock_open.write_text(
                "#!/bin/sh\nprintf '%s\\n' \"$@\" > \"$CODEX_TEST_OPEN_CALL\"\n"
            )
            mock_open.chmod(0o755)
            environment = os.environ.copy()
            environment.update(
                {
                    "CODEX_ACCOUNT_ROOT": str(root / "accounts"),
                    "CODEX_NAVER_CHROME_PROFILE": "Profile 9",
                    "CODEX_OPEN_COMMAND": str(mock_open),
                    "CODEX_TEST_CALLS": str(codex_calls),
                    "CODEX_TEST_OPEN_CALL": str(open_call),
                    "PATH": f"{mock_bin}:{environment['PATH']}",
                }
            )

            subprocess.run([LOGIN_SCRIPT, "naver"], check=True, env=environment)

            self.assertEqual(
                open_call.read_text().splitlines(),
                [
                    "-a",
                    "Google Chrome",
                    "--args",
                    "--profile-directory=Profile 9",
                    "https://auth.openai.com/codex/device",
                ],
            )
            self.assertIn("login\n--device-auth\n", codex_calls.read_text())

    def test_does_not_start_login_when_account_is_already_logged_in(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            mock_bin = root / "bin"
            mock_bin.mkdir()
            mock_codex = mock_bin / "codex"
            mock_codex.write_text("#!/bin/sh\nexit 0\n")
            mock_codex.chmod(0o755)
            environment = os.environ.copy()
            environment.update(
                {
                    "CODEX_ACCOUNT_ROOT": str(root / "accounts"),
                    "PATH": f"{mock_bin}:{environment['PATH']}",
                }
            )

            result = subprocess.run(
                [LOGIN_SCRIPT, "google"],
                check=True,
                capture_output=True,
                text=True,
                env=environment,
            )

            self.assertIn("already logged in", result.stdout)


if __name__ == "__main__":
    unittest.main()
