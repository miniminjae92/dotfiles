# Recovery

## Local history

- The vault is a local Git repository.
- `agent-os-vault-snapshot` commits changed notes every hour and best-effort pushes them to the private Git remote (for phone reading via the GitHub app); an offline run still commits locally.
- Restore a note by inspecting Git history and applying the selected version.

## Off-device backup

Local Git does not protect against device loss. Choose exactly one primary off-device path during the final setup interview:

- Obsidian Sync with end-to-end encryption
- a private Git remote
- an encrypted macOS backup such as Time Machine

Test restoration after choosing a provider. Do not treat synchronization alone as a verified backup until that test passes.
