# Woowacourse Java evidence map

This map was checked on 2026-09-25. Verify a repository's current branch and files before using a historical example.

## Cross-cohort review evidence

- The requested one-mission collection is `~/projects/gh-mine`: reviews from merged PRs in `woowacourse/java-blackjack` across 2020~2026. Read its `README.md` for the pipeline and [the corpus guide](blackjack-prs.md) for safe, targeted retrieval. The README's claim that repeated comments are a team's true conventions is the project's hypothesis, not proof of team agreement or the user's preference. The original request is `asx show 6519adf2`; the latest recorded iMac verification is `asx show a4475347`.
- The corpus is comparative evidence, not a source of the user's approved conventions. The 2026-08-14 iMac checklist had 310 candidates awaiting user selection. The current MacBook copy has an older checklist and database; check which copy you are reading.

## Personal code and Obsidian evidence

- Main collection: `~/.obsidian/mimir/20 Knowledge/Programming/Java/Woowacourse-Evidence/`. Read `README.md` for scope and evidence order, then the relevant part of `java-programming-criteria.md`. `HANDOFF.md` records the state on 2026-09-20; read it when tracing an unresolved convention or updating the collection, and compare claimed decisions with current `~/.dotfiles/agent-os/DECISIONS.md` and project ADRs. Its `Work In Progress` and `Next Steps` are historical, not instructions for today's task.
- Review themes and original source locations: `analysis/review-themes.md` and `raw/source-index.md` under that collection. Consult `raw/pr-feedback.json` or `raw/patches/` only when a decision depends on the exact original text or change.
- Readable feedback for 14 mission PRs: `~/.obsidian/yggdrasil/1-knowledge/GitHub/PR Feedback/woowacourse/<repo>/PR-<number>/feedback.md`. The Mimir collection has a broader 2026-09-20 snapshot; neither count is a live GitHub total.
- Mission requirements and learning context: use `raw/source-index.md` to locate the matching original under `~/.obsidian/yggdrasil/3-stash/우테코-완료/` or `~/projects/ww-mission-learning/`. The completion hub starts at `00-기록-허브/README.md`. Open only the notes for the mission and behavior under change.
- If the Mimir directory is absent from the working tree, read files from its recorded commit without changing the vault branch. For example, from the Mimir repository run `git show '4e3837b:20 Knowledge/Programming/Java/Woowacourse-Evidence/README.md'` and replace `README.md` with the needed relative file. If that commit is unavailable, use the readable feedback and current repository, then report the missing source.

## User-authored mission code

These refs held implementation when checked. Inspect the actual target tree rather than assuming `main` contains the user's code. The personal coding draft uses the first six missions in recent-first order; the user excluded `java-http` from that draft.

| User code source | Historical ref | Useful entry point |
| --- | --- | --- |
| `java-blackjack` (GitHub PR heads; no local checkout) | [#1028 step1](https://github.com/miniminjae92/java-blackjack/tree/55f4ecac696a74ec9bae7508ef89f84f48380aca), [#1094 step2](https://github.com/miniminjae92/java-blackjack/tree/1dbbdec89f77b63b12485375cf4e1e2386b21b4b) | `Hand` and its test, `BettingBoard` and its test, `State`, `RefereeTest`; own PR feedback under the Yggdrasil path above |
| `java-janggi` | `e69a183` (`origin/step2`) | `src/main/java/janggi/domain/space/Position.java`, `README.md`, PR #269 and #338: creation invariants, collection exposure, and game state |
| `spring-roomescape-admin` | `2fb37ed` (`origin/miniminjae92`) | PR #427: early application and repository boundaries |
| `spring-roomescape-member` | `dd94d1b` (`origin/step2`) | `src/main/java/roomescape/domain/Reservation.java`, its test, PR #418 and #499: state transitions, API contracts, and DB constraints |
| `spring-roomescape-auth` | `85c1974` (`origin/miniminjae92`) | Code and tests; the collected PR had no human review |
| `spring-roomescape-waiting` | `03c112e` (`origin/step3`) | `src/main/java/roomescape/domain/reservation/ReservationSlot.java`, its test, `docs/README.md`, PR #415, #429 and #590: time boundaries and transaction behavior |

The Janggi mission's `else` and method-length limits were mission requirements, not general Java rules. The waiting and member package layouts also differ. In the user's blackjack feedback, `unresolved` is thread metadata and `outdated` marks an older code position; compare comments with the final PR head. `~/projects/ww-final-judge/pr_data/PR_*` contains other participants' PR code and is not evidence of the user's coding habits.
