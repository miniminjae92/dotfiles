# java-blackjack reviews across cohorts

The `gh-mine` collection covers 1,054 merged PRs in `woowacourse/java-blackjack` from 2020~2026 and 40,489 review units. It excludes open PRs; 146 collected PRs have `truncated=1`, so their review tails may be missing. These are the recorded collection bounds, not a claim that every review was evaluated.

## Candidate status

- `asx show 6519adf2` is the original one-mission collection request. `asx show a4475347` records the 2026-08-14 iMac verification: 508 rule candidates across eight topics and 310 candidates with at least three supporting items in `work/checklist-run11-ms3.md`.
- User selection, `decide`, and `export` had not completed in that record. The iMac `ghmine.db` and checklist are the canonical run 11 artifacts. Verify their current state before treating any selection as final.
- The MacBook's `~/projects/gh-mine/ghmine.db` is a 2026-07-24 backup. Its `work/checklist-run8.md` has 42 unchecked candidates and its `decision` table has zero rows. The run 11 checklist is absent here. Candidate text, support counts, and repeated reviewer comments are evidence to examine, not approved Java rules.

## Read a relevant review

Read `~/projects/gh-mine/docs/taxonomy.md` for topic meanings. In a Java coding session, query any copy of `ghmine.db` with `sqlite3 -readonly`; the `ghmine` CLI opens the database through a schema-writing connection. Leave the database and `work/` artifacts untouched.

Choose a concrete code question and search term before querying. Use `test`, `design`, `arch`, `naming`, `error`, `idiom`, `readability`, or `perf` as the topic. First see which years have matches. Then inspect a small sample from at least two years before saying a review pattern spans cohorts. This example searches Java test comments containing `테스트` in 2024; repeat with another year and a term specific to the code under change.

```sh
sqlite3 -readonly -header -column ~/projects/gh-mine/ghmine.db \
  "SELECT u.id, u.thread_id, u.ref AS pr, p.truncated, u.path, u.url,
          substr(replace(u.body,char(10),' '),1,300) AS excerpt
   FROM annotation a
   JOIN unit u ON u.id=a.unit_id
   JOIN pr p ON p.repo=u.repo AND p.number=CAST(u.ref AS INTEGER)
   WHERE a.run_id=7 AND a.topic='test'
     AND a.type IN ('issue','question') AND u.path LIKE '%.java'
     AND u.body LIKE '%테스트%' AND substr(u.created_at,1,4)='2024'
   ORDER BY u.created_at DESC LIMIT 10;"
```

The example uses the MacBook backup's annotation run 7. Check the run and available years in any other copy before adapting it. `issue` and `question` are starting points; relevant `praise` and `info` comments can change the conclusion.

For each selected `thread_id`, read all its `unit` rows ordered by `created_at`, including replies, and inspect `body` and `diff_hunk`. Open the returned GitHub URL to inspect the PR's later code before calling a suggestion adopted. If GitHub or the final code is unavailable, report that follow-up as unverified. `is_resolved` is thread metadata, not proof of adoption. Check `pr.truncated` before making completeness claims. Read `ghmine/db.py` for the schema when a different lookup is needed. Review topics and machine clusters classify comments; they do not establish that the suggested code is correct for the current task.
