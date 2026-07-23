// LMS+(techcourse-lms-plus-web.woowahan.com) 미션 스텝 수확기 — 페이지 컨텍스트에 주입해서 실행.
// javascript_tool로 이 파일 내용을 통째로 실행하면 window.__lmsHarvest가 설치된다.
// 이후 `await window.__lmsHarvest.run('http://127.0.0.1:4199/save')` 한 줄로:
//   사이드바 스텝 전수 클릭 순회 → 본문 md 변환 → 로컬 수신 서버로 POST.
// 반환값은 스텝별 {id, len} 요약뿐이라 모델 컨텍스트(토큰)를 거의 안 쓴다.
(() => {
  function toMd(node, depth = 0) {
    if (node.nodeType === Node.TEXT_NODE) return node.textContent.replace(/\s+/g, ' ');
    if (node.nodeType !== Node.ELEMENT_NODE) return '';
    const kids = () => [...node.childNodes].map((c) => toMd(c, depth)).join('');
    const tag = node.tagName.toLowerCase();
    switch (tag) {
      case 'h1': return `\n# ${kids().trim()}\n`;
      case 'h2': return `\n## ${kids().trim()}\n`;
      case 'h3': return `\n### ${kids().trim()}\n`;
      case 'h4': return `\n#### ${kids().trim()}\n`;
      case 'p': return `\n${kids().trim()}\n`;
      case 'strong': case 'b': return `**${kids().trim()}**`;
      case 'em': case 'i': return `*${kids().trim()}*`;
      case 'code': return node.closest('pre') ? kids() : `\`${kids().trim()}\``;
      case 'pre': return `\n\`\`\`\n${node.textContent}\n\`\`\`\n`;
      case 'a': {
        const href = (node.getAttribute('href') ?? '').split('?')[0];
        const t = kids().trim();
        return href && href.startsWith('http') ? `[${t}](${href})` : t;
      }
      case 'img': {
        const alt = node.getAttribute('alt') ?? 'image';
        const src = (node.getAttribute('src') ?? '').split('?')[0];
        return `![${alt}](${src})`;
      }
      case 'ul': case 'ol': {
        let i = 0;
        return '\n' + [...node.children].filter((c) => c.tagName === 'LI').map((li) => {
          const marker = tag === 'ol' ? `${++i}.` : '-';
          const inner = [...li.childNodes].map((c) => toMd(c, depth + 1)).join('').trim()
            .replace(/\n/g, '\n' + '  '.repeat(depth + 1));
          return '  '.repeat(depth) + `${marker} ${inner}`;
        }).join('\n') + '\n';
      }
      case 'blockquote': return '\n' + kids().trim().split('\n').map((l) => `> ${l}`).join('\n') + '\n';
      case 'table': {
        const rows = [...node.querySelectorAll('tr')].map(
          (tr) => '| ' + [...tr.children].map((td) => td.textContent.trim()).join(' | ') + ' |'
        );
        if (rows.length > 1) rows.splice(1, 0, '|' + ' --- |'.repeat(rows[0].split('|').length - 2));
        return '\n' + rows.join('\n') + '\n';
      }
      case 'br': return '\n';
      case 'script': case 'style': case 'nav': case 'button': case 'svg': return '';
      default: return kids();
    }
  }

  // React fiber를 타고 올라가며 step 데이터({id, title|name})를 찾는다.
  function fiberStep(el) {
    const k = Object.keys(el).find((k) => k.startsWith('__reactFiber$'));
    let f = k ? el[k] : null;
    for (let i = 0; i < 12 && f; i++) {
      const p = f.memoizedProps;
      if (p && typeof p === 'object') {
        for (const key of ['step', 'item', 'data']) {
          const o = p[key];
          if (o && typeof o === 'object' && 'id' in o && ('title' in o || 'name' in o)) {
            return { id: o.id, title: o.title ?? o.name };
          }
        }
        if ('id' in p && ('title' in p || 'name' in p)) return { id: p.id, title: p.title ?? p.name };
      }
      f = f.return;
    }
    return null;
  }

  const ITEM_SELECTOR = 'div.group.flex.flex-col'; // 사이드바 스텝 항목
  const GROUP_SELECTOR = 'div.mb-2'; // 사이드바 섹션 그룹

  async function grab(id) {
    const el = [...document.querySelectorAll(ITEM_SELECTOR)].find((e) => fiberStep(e)?.id === id);
    if (!el) return { id, error: 'sidebar item not found' };
    el.click();
    await new Promise((r) => setTimeout(r, 1200));
    const md = toMd(document.querySelector('main')).replace(/\n{3,}/g, '\n\n').trim()
      .replace(/^진행 단계\d*\s*/, '')
      .replace(/\[\]\(#[^)]*\)/g, '');
    return { id, md, len: md.length };
  }

  async function run(receiverUrl) {
    const groups = [...document.querySelectorAll(GROUP_SELECTOR)].map((g) => {
      const label = (g.firstElementChild?.textContent ?? '').trim().slice(0, 40).replace(/\d+$/, '').trim();
      const stepIds = [...g.querySelectorAll(ITEM_SELECTOR)].map((e) => fiberStep(e)?.id).filter(Boolean);
      return { label, stepIds };
    }).filter((g) => g.stepIds.length);

    const titles = {};
    [...document.querySelectorAll(ITEM_SELECTOR)].forEach((e) => {
      const s = fiberStep(e);
      if (s) titles[s.id] = s.title;
    });

    const steps = {};
    const status = [];
    for (const g of groups) {
      for (const id of g.stepIds) {
        const r = await grab(id);
        if (r.md) steps[id] = r.md;
        status.push({ id, title: titles[id], len: r.len ?? 0, error: r.error });
      }
    }

    const payload = {
      mission: Number(location.pathname.match(/missions\/(\d+)/)?.[1] ?? 0),
      url: location.origin + location.pathname,
      groups,
      titles,
      steps,
    };
    const resp = await fetch(receiverUrl, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const saved = await resp.json();
    return { saved, stepCount: Object.keys(steps).length, status };
  }

  window.__lmsHarvest = { run, grab, toMd, fiberStep };
  return 'installed: window.__lmsHarvest';
})();
