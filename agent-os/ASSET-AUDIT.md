# Existing Asset Audit

## Keep

| Asset | Role | Constraint |
| --- | --- | --- |
| `.codex/AGENTS.md` | global safety and routing | keep concise; no project-specific workflow |
| `work` skill | explicit Builder workflow | do not auto-trigger or pause unless plan-first was requested |
| `codex-session-export` and `arc` | manual raw-session export | use only when a durable archive is explicitly needed |
| archive skills | manual source refinement | never run after every task; high context cost |
| `fast_worker` | bounded low-cost delegation | use only when handoff saves net context |
| `critical_reviewer` | independent high-risk review | read-only and conditional |

## Exclude From The Default Path

| Asset | Reason |
| --- | --- |
| `vault-ai-classify` | tied to the legacy Yggdrasil layout and an Ollama classification workflow |
| raw/keyword/structure/source archive chain | duplicates normal Run records and costs extra tokens when invoked automatically |
| legacy vault organization rules | not validated for Developer OS taxonomy |

## Re-evaluate After Pilot

- Disable assets that are not used during the first 10 real tasks.
- Promote only assets with evidence of saved time, reduced rework, or improved understanding.
- Do not build compatibility layers solely to preserve an unused legacy workflow.
