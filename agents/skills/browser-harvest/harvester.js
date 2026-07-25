// 브라우저 페이지 안에서 도는 수확 엔진 — 사이트 중립.
// javascript_tool로 이 파일 내용을 통째로 실행하면 window.__harvest가 설치된다.
// 본문은 페이지 안에서 md로 변환해 로컬 수신 서버로 직송하므로, 도구 출력(=모델 컨텍스트)에는
// 문서별 {id, len} 요약만 흐른다. 사이트별 셀렉터는 호출 시 config로 주입한다(presets/ 참고).
//
//   모드 A(목록 순회): await window.__harvest.run({ receiverUrl, itemSelector, ... })
//   모드 B(URL 1건):   await window.__harvest.grabPage({ receiverUrl, ... })
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

  // 기본 식별자 추출기: React fiber를 타고 올라가며 {id, title|name}을 찾는다.
  // id·href가 DOM에 안 드러나는 SPA 목록용. 평범한 <a href> 목록이면
  // config.identify를 갈아끼우는 편이 빠르다(presets/ 참고).
  function fiberIdentify(el) {
    const k = Object.keys(el).find((k) => k.startsWith('__reactFiber$'));
    let f = k ? el[k] : null;
    for (let i = 0; i < 12 && f; i++) {
      const p = f.memoizedProps;
      if (p && typeof p === 'object') {
        for (const key of ['step', 'item', 'data', 'node']) {
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

  const DEFAULTS = {
    receiverUrl: 'http://127.0.0.1:4199/save',
    itemSelector: null,       // 목록(사이드바/목차)의 한 항목 — 모드 A 필수
    groupSelector: null,      // 항목을 감싸는 섹션. null이면 전체가 한 섹션
    contentSelector: 'main',  // 본문 컨테이너
    waitMs: 1200,             // 클릭 후 본문 교체 대기(ms)
    identify: fiberIdentify,  // (el) => {id, title} | null
    strip: [],                // 본문에서 걷어낼 정규식 배열(머리말·앵커 찌꺼기 등)
    sourceOf: null,           // (id) => 원문 URL. null이면 현재 URL
    meta: {},                 // 수확본 전체에 붙일 부가 정보(frontmatter로 내려간다)
  };

  const cfgOf = (opts) => ({ ...DEFAULTS, ...(typeof opts === 'string' ? { receiverUrl: opts } : opts) });
  const here = () => location.origin + location.pathname;

  function readBody(cfg) {
    const root = document.querySelector(cfg.contentSelector);
    if (!root) return null;
    let md = toMd(root).replace(/\n{3,}/g, '\n\n').trim();
    for (const re of cfg.strip) md = md.replace(re, '');
    return md.replace(/\n{3,}/g, '\n\n').trim();
  }

  async function post(url, payload) {
    const resp = await fetch(url, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify(payload),
    });
    return resp.json();
  }

  const itemsOf = (cfg, root = document) => [...root.querySelectorAll(cfg.itemSelector)];

  async function grab(id, section, cfg) {
    const el = itemsOf(cfg).find((e) => cfg.identify(e)?.id === id);
    if (!el) return { id, error: 'list item not found' };
    el.click();
    await new Promise((r) => setTimeout(r, cfg.waitMs));
    const md = readBody(cfg);
    if (md == null) return { id, error: `content not found: ${cfg.contentSelector}` };
    return { id, section, source: cfg.sourceOf ? cfg.sourceOf(id) : here(), md, len: md.length };
  }

  // 모드 A — 한 페이지 안에서 목록 항목을 전수 클릭 순회한 뒤 통째로 한 번 POST.
  async function run(opts) {
    const cfg = cfgOf(opts);
    if (!cfg.itemSelector) throw new Error('itemSelector required');

    const ids = (root) => itemsOf(cfg, root).map((e) => cfg.identify(e)?.id).filter((v) => v != null);
    const sections = (cfg.groupSelector
      ? [...document.querySelectorAll(cfg.groupSelector)].map((g) => ({
          label: (g.firstElementChild?.textContent ?? '').trim().slice(0, 40).replace(/\d+$/, '').trim(),
          ids: ids(g),
        }))
      : [{ label: '', ids: ids(document) }]
    ).filter((s) => s.ids.length);

    const titles = {};
    itemsOf(cfg).forEach((e) => {
      const it = cfg.identify(e);
      if (it) titles[it.id] = it.title;
    });

    const docs = [];
    const status = [];
    for (const s of sections) {
      for (const id of s.ids) {
        const r = await grab(id, s.label, cfg);
        const title = titles[id] ?? String(id);
        if (r.md) docs.push({ id, title, section: s.label, source: r.source, md: r.md });
        status.push({ id, title, len: r.len ?? 0, error: r.error });
      }
    }

    const saved = await post(cfg.receiverUrl, { url: here(), title: document.title, meta: cfg.meta, docs });
    return { saved, docCount: docs.length, sections: sections.length, status };
  }

  // 모드 B — 지금 열린 페이지 1건만 수확해 수신 서버에 덧붙인다(URL 목록 순회용).
  // 페이지를 이동하면 이 스크립트는 사라지므로 매 URL마다 주입 → 호출한다.
  async function grabPage(opts) {
    const cfg = cfgOf(opts);
    const md = readBody(cfg);
    if (md == null) return { error: `content not found: ${cfg.contentSelector}` };
    const doc = {
      id: cfg.meta.id ?? location.pathname,
      title: String(cfg.meta.title ?? document.title).trim(),
      section: cfg.meta.section ?? '',
      source: location.href.split('#')[0],
      md,
    };
    const saved = await post(cfg.receiverUrl, doc);
    return { saved, id: doc.id, title: doc.title, len: md.length };
  }

  window.__harvest = { run, grabPage, grab, toMd, readBody, fiberIdentify, DEFAULTS };
  return 'installed: window.__harvest';
})();
