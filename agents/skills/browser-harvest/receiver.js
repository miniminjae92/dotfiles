#!/usr/bin/env node
// 로컬 수신 서버: 브라우저 페이지가 POST한 수확 데이터를 파일로 저장한다.
// 데이터가 모델 컨텍스트를 거치지 않게 하는 우회로 — 토큰 소모 0의 핵심.
// 사용: node receiver.js <출력경로> [포트=4199]
//
//   POST /save    전체 수확본 1건을 <출력경로>에 쓰고 종료   (모드 A)
//   POST /append  문서 1건을 <출력경로>에 JSONL로 덧붙임      (모드 B)
//   POST /done    수확 종료 선언 → 서버 종료                 (모드 B 마무리)
//
// 무수신 5분이면 자동 종료한다(요청이 올 때마다 갱신).
const http = require('http');
const fs = require('fs');

const OUT = process.argv[2];
const PORT = Number(process.argv[3] ?? 4199);
const IDLE_MS = 300_000;
if (!OUT) {
  console.error('usage: node receiver.js <out.json|out.jsonl> [port]');
  process.exit(1);
}

let idleTimer;
const bumpIdle = () => {
  clearTimeout(idleTimer);
  idleTimer = setTimeout(() => {
    console.log('idle timeout, exiting');
    process.exit(1);
  }, IDLE_MS);
};

let appended = 0;

const server = http.createServer((req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'content-type');
  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    return res.end();
  }

  const reply = (obj) => {
    res.writeHead(200, { 'content-type': 'application/json' });
    res.end(JSON.stringify(obj));
  };

  if (req.method === 'POST' && (req.url === '/save' || req.url === '/append')) {
    const mode = req.url === '/save' ? 'save' : 'append';
    let body = '';
    req.on('data', (c) => {
      body += c;
      if (body.length > 20e6) req.destroy();
    });
    req.on('end', () => {
      if (mode === 'save') {
        fs.writeFileSync(OUT, body);
        reply({ ok: true, bytes: body.length });
        console.log('saved', body.length, 'bytes ->', OUT);
        return setTimeout(() => process.exit(0), 500);
      }
      fs.appendFileSync(OUT, body.replace(/\n/g, ' ') + '\n');
      appended += 1;
      reply({ ok: true, bytes: body.length, count: appended });
      console.log('appended', body.length, 'bytes (#' + appended + ') ->', OUT);
      bumpIdle();
    });
    return;
  }

  if (req.method === 'POST' && req.url === '/done') {
    reply({ ok: true, count: appended });
    console.log('done,', appended, 'docs ->', OUT);
    return setTimeout(() => process.exit(0), 500);
  }

  res.writeHead(404);
  res.end();
});

server.listen(PORT, '127.0.0.1', () => console.log(`receiver on 127.0.0.1:${PORT} -> ${OUT}`));
bumpIdle();
