#!/usr/bin/env node
// 수확 JSON → 섹션 디렉터리별 스텝 md 파일 + README 인덱스.
// 사용: node split.js <harvest.json> <출력디렉터리> [수확일=오늘]
const fs = require('fs');
const path = require('path');

const [jsonPath, outBase, dateArg] = process.argv.slice(2);
if (!jsonPath || !outBase) {
  console.error('usage: node split.js <harvest.json> <outDir> [YYYY-MM-DD]');
  process.exit(1);
}
const harvested = dateArg ?? new Date().toISOString().slice(0, 10);
const data = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));

const slug = (t) => t.replace(/[\/\\:*?"<>|()!,]/g, '').trim().replace(/\s+/g, '-').slice(0, 50);
const index = [];

data.groups.forEach((g, gi) => {
  const secName = g.label.replace(/\d+$/, '').trim() || `섹션${gi}`;
  const dirName = `${String(gi).padStart(2, '0')}-${slug(secName)}`;
  const dir = path.join(outBase, dirName);
  fs.mkdirSync(dir, { recursive: true });
  index.push(`\n## ${secName}\n`);
  g.stepIds.forEach((id, i) => {
    if (!data.steps[id]) return;
    const title = data.titles[id] ?? `step-${id}`;
    const fname = `${String(i + 1).padStart(2, '0')}-${slug(title)}.md`;
    const fm = [
      '---',
      `source: ${data.url}?step=${id}`,
      `mission: missions/${data.mission}`,
      `section: ${secName}`,
      `step_id: ${id}`,
      `harvested: ${harvested}`,
      '---',
      '',
    ].join('\n');
    fs.writeFileSync(path.join(dir, fname), fm + data.steps[id] + '\n');
    index.push(`- [${title}](${dirName}/${fname})`);
  });
});

fs.writeFileSync(
  path.join(outBase, 'README.md'),
  `# LMS 미션 문서 (수확본)\n\n원본: ${data.url} · 수확일: ${harvested} · 총 ${Object.keys(data.steps).length}개 스텝\n` +
    index.join('\n') + '\n'
);
console.log('done:', outBase, '/', Object.keys(data.steps).length, 'steps');
