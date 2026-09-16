import json
from pathlib import Path
import unittest


HOOKS = Path(__file__).parents[1] / "agents" / "codex" / "hooks.json"


class CodexHookConfigTests(unittest.TestCase):
    def test_post_tool_use_resolves_agent_notify_permission(self):
        config = json.loads(HOOKS.read_text(encoding="utf-8"))
        groups = config["hooks"]["PostToolUse"]
        commands = [
            hook["command"]
            for group in groups
            for hook in group["hooks"]
        ]

        self.assertEqual(
            sum("agent-notify" in command and "codex-hook" in command for command in commands),
            1,
        )


if __name__ == "__main__":
    unittest.main()
