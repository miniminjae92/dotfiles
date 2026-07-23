#!/usr/bin/env node
// 1회용 로컬 수신 서버: 브라우저 페이지가 POST한 수확 JSON을 파일로 저장하고 종료한다.
// 사용: node receiver.js <출력.json> [포트=4199]
// 데이터가 모델 컨텍스트를 거치지 않게 하는 우회로 — 토큰 소모 0의 핵심.
const http = require('http');
const fs = require('fs');

const OUT = process.argv[2];
const PORT = Number(process.argv[3] ?? 4199);
if (!OUT) {
  console.error('usage: node receiver.js <out.json> [port]');
  process.exit(1);
}

const server = http.createServer((req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'content-type');
  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    return res.end();
  }
  if (req.method === 'POST' && req.url === '/save') {
    let body = '';
    req.on('data', (c) => {
      body += c;
      if (body.length > 20e6) req.destroy();
    });
    req.on('end', () => {
      fs.writeFileSync(OUT, body);
      res.writeHead(200, { 'content-type': 'application/json' });
      res.end(JSON.stringify({ ok: true, bytes: body.length }));
      console.log('saved', body.length, 'bytes ->', OUT);
      setTimeout(() => process.exit(0), 500);
    });
    return;
  }
  res.writeHead(404);
  res.end();
});

server.listen(PORT, '127.0.0.1', () => console.log(`receiver on 127.0.0.1:${PORT}`));
// 5분 안에 수신 없으면 자동 종료
setTimeout(() => {
  console.log('timeout, exiting');
  process.exit(1);
}, 300_000);
