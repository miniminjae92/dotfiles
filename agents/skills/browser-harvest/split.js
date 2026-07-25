#!/usr/bin/env node
// 수확본(JSON 또는 JSONL) → 섹션 디렉터리별 md 파일 + README 인덱스.
// 사용: node split.js <harvest.json|harvest.jsonl> <출력디렉터리> [수확일=오늘] [제목]
//
// 입력 두 가지를 다 받는다.
//   모드 A: { url, title, meta, docs: [{id, title, section, source, md}] }
//   모드 B: 한 줄에 문서 하나씩인 JSONL (같은 doc 모양)
const fs = require('fs');
const path = require('path');

const [inPath, outBase, dateArg, titleArg] = process.argv.slice(2);
if (!inPath || !outBase) {
  console.error('usage: node split.js <harvest.json|jsonl> <outDir> [YYYY-MM-DD] [title]');
  process.exit(1);
}
const harvested = dateArg ?? new Date().toISOString().slice(0, 10);
const raw = fs.readFileSync(inPath, 'utf8').trim();

let docs = [];
let meta = {};
let sourceUrl = '';
let indexTitle = titleArg ?? '';

try {
  const data = JSON.parse(raw);
  docs = data.docs ?? [];
  meta = data.meta ?? {};
  sourceUrl = data.url ?? '';
  indexTitle = indexTitle || data.title || '';
} catch {
  docs = raw.split('\n').filter(Boolean).map((line) => JSON.parse(line));
}
if (!docs.length) {
  console.error('no docs in', inPath);
  process.exit(1);
}

const slug = (t) => String(t).replace(/[\/\\:*?"<>|()!,]/g, '').trim().replace(/\s+/g, '-').slice(0, 50);

// 등장 순서를 유지한 채 섹션별로 묶는다.
const sections = [];
for (const doc of docs) {
  const label = (doc.section ?? '').replace(/\d+$/, '').trim();
  let sec = sections.find((s) => s.label === label);
  if (!sec) sections.push((sec = { label, docs: [] }));
  sec.docs.push(doc);
}
const flat = sections.length === 1 && !sections[0].label;

const index = [];
let written = 0;

sections.forEach((sec, si) => {
  const name = sec.label || `섹션${si + 1}`;
  const dirName = flat ? '' : `${String(si).padStart(2, '0')}-${slug(name)}`;
  const dir = path.join(outBase, dirName);
  fs.mkdirSync(dir, { recursive: true });
  if (!flat) index.push(`\n## ${name}\n`);
  sec.docs.forEach((doc, i) => {
    if (!doc.md) return;
    const title = doc.title ?? `doc-${doc.id}`;
    const fname = `${String(i + 1).padStart(2, '0')}-${slug(title)}.md`;
    const fm = ['---', `source: ${doc.source ?? sourceUrl}`];
    for (const [k, v] of Object.entries(meta)) fm.push(`${k}: ${v}`);
    if (!flat) fm.push(`section: ${name}`);
    fm.push(`id: ${doc.id}`, `harvested: ${harvested}`, '---', '');
    fs.writeFileSync(path.join(dir, fname), fm.join('\n') + doc.md + '\n');
    index.push(`- [${title}](${path.join(dirName, fname)})`);
    written += 1;
  });
});

fs.writeFileSync(
  path.join(outBase, 'README.md'),
  `# ${indexTitle || '수확본'}\n\n` +
    `원본: ${sourceUrl || docs[0].source || '-'} · 수확일: ${harvested} · 총 ${written}개 문서\n` +
    (flat ? '\n' : '') + index.join('\n') + '\n'
);
console.log('done:', outBase, '/', written, 'docs in', sections.length, 'section(s)');
