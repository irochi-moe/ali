const assert = require('node:assert/strict');
const {readFileSync} = require('node:fs');
const {join} = require('node:path');
const {test} = require('node:test');
const vm = require('node:vm');

const script = readFileSync(join(__dirname, '../site/app.js'), 'utf8');
const catalog = JSON.parse(readFileSync(join(__dirname, '../site/products.json'), 'utf8'));

async function page({data = catalog, ok = true} = {}) {
  const nodes = Object.fromEntries(['search', 'group', 'category', 'channel', 'count', 'updated', 'results']
    .map(id => [id, {
      value: id === 'group' ? 'products' : '', disabled: true, innerHTML: '', textContent: '', events: {},
      addEventListener(event, callback) { this.events[event] = callback; }
    }]));
  const requests = [];
  const errors = [];
  const context = vm.createContext({
    document: {getElementById: id => nodes[id]}, URL, Intl,
    console: {error: error => errors.push(error)},
    fetch: async (url, options) => {
      requests.push({url, options});
      return {ok, status: ok ? 200 : 503, json: async () => structuredClone(data)};
    }
  });
  await vm.runInContext(script, context);
  function set(id, value) {
    nodes[id].value = value;
    nodes[id].events[id === 'search' ? 'input' : 'change']();
  }
  return {nodes, requests, errors, set};
}

test('loads the complete catalog with relative paths and timestamped source links', async () => {
  const {nodes, requests, errors} = await page();
  assert.equal(errors.length, 0);
  assert.equal(requests[0].url, './products.json');
  assert.equal(nodes.count.textContent, `${catalog.products.length}종`);
  assert.equal((nodes.results.innerHTML.match(/<details /g) || []).length, catalog.products.length);
  assert.match(nodes.results.innerHTML, /&amp;t=4661s/);
  assert.match(nodes.results.innerHTML, /NPWGVK3SHZT8/);
  assert.match(nodes.results.innerHTML, /href="https:\/\/s\.click\.aliexpress\.com\/e\/[^"]+"[^>]*>[^<]+ 알리 링크<\/a> <span class="muted">\(유튜버 링크 그대로\)/);
  assert.match(nodes.updated.textContent, /2026/);
  assert.equal(nodes.search.disabled, false);
});

test('category, case-insensitive search, and empty results', async () => {
  const {nodes, set} = await page();
  set('category', 'CPU');
  assert.equal(nodes.count.textContent, '6종');
  assert.match(nodes.results.innerHTML, /<h2>CPU<\/h2>/);
  assert.doesNotMatch(nodes.results.innerHTML, /GMKtec/);
  set('category', '');
  set('search', ' gmkTEC M8 ');
  assert.equal(nodes.count.textContent, '1종');
  set('search', 'no-such-product-xyz');
  assert.equal(nodes.count.textContent, '0종');
  assert.match(nodes.results.innerHTML, /검색 결과가 없습니다/);
});

test('creator grouping narrows offers and keeps the product-specific code source', async () => {
  const {nodes, set} = await page();
  set('search', 'ORICO 마그네틱 허브');
  set('group', 'channels');
  set('channel', '알뜰직구');
  assert.equal(nodes.count.textContent, '1종');
  assert.match(nodes.results.innerHTML, /<h2>알뜰직구<\/h2>/);
  assert.match(nodes.results.innerHTML, /\[알뜰직구\]/);
  assert.doesNotMatch(nodes.results.innerHTML, /<h2>셀링포인트/);
  assert.match(nodes.results.innerHTML, /lc=Ugz-DwqWCpvTSqKjvbZ4AaABAg/);
});

test('escapes product, option and code text, and blocks executable code links', async () => {
  const data = structuredClone(catalog);
  data.products = [{category: 'CPU', name: '<img src=x onerror=alert(1)>', offers: [{
    video_id: data.videos[0].id, time: null, price: '', option: '<script>bad()</script>',
    code: '<b>COUPON</b>', code_url: 'javascript:alert(1)', url: 'javascript:alert(1)'
  }, {
    video_id: data.videos[0].id, time: '00:01', price: '', code: 'X',
    url: 'https://aliexpress.com.evil.example/item'
  }]}];
  const {nodes, errors} = await page({data});
  assert.equal(errors.length, 0);
  assert.match(nodes.results.innerHTML, /&lt;img/);
  assert.match(nodes.results.innerHTML, /&lt;script&gt;/);
  assert.match(nodes.results.innerHTML, /&lt;b&gt;COUPON/);
  assert.doesNotMatch(nodes.results.innerHTML, /<img|<script|href="javascript:|evil\.example|알리 링크/);
});

test('a failed data request leaves a visible recovery message', async () => {
  const {nodes, errors} = await page({ok: false});
  assert.equal(errors.length, 1);
  assert.match(nodes.results.textContent, /새로고침/);
  assert.equal(nodes.search.disabled, true);
});
