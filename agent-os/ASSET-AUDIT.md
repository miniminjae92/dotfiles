# Existing Asset Audit

## Keep

| Asset | Role | Constraint |
| --- | --- | --- |
| `.codex/AGENTS.md` | global safety and routing | keep concise; no project-specific workflow |
| `codex-session-export` | manual raw-session export | use only when a durable archive is explicitly needed |
| `fast_worker` | bounded low-cost delegation | use only when handoff saves net context |
| `critical_reviewer` | independent high-risk review | read-only and conditional |

## Exclude From The Default Path

| Asset | Reason |
| --- | --- |
| `vault-ai-classify` | tied to the legacy Yggdrasil layout and an Ollama classification workflow |
| legacy vault organization rules | not validated for Developer OS taxonomy |

## Re-evaluate After Pilot

- `agent-os/schemas/` (event/run): 2026-07-25 실측에서 소비자 0 확인. 계측 트랙의 규범 승격(구현 리포 CONTEXT.md/ADR) 시 채택 또는 폐기 판정.
- Disable assets that are not used during the first 10 real tasks.
- Promote only assets with evidence of saved time, reduced rework, or improved understanding.
- Do not build compatibility layers solely to preserve an unused legacy workflow.
