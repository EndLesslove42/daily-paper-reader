// Exercise the real setup handlers with an in-memory DOM and fake network/credentials.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const { webcrypto } = require('node:crypto');
const utils = require('../app/llm-config-utils.js');

async function main() {
  const nodes = new Map();
  class Element {
    constructor(id = '') {
      this.id = id;
      this.value = '';
      this.style = {};
      this.attrs = {};
      this.handlers = {};
      this.children = [];
      this.classList = { add() {}, remove() {}, toggle() {} };
    }
    set innerHTML(html) {
      this.html = html;
      if (this.id === 'secret-gate-modal') {
        for (const match of html.matchAll(/id="([^"]+)"/g)) nodes.set(match[1], new Element(match[1]));
      }
    }
    get innerHTML() { return this.html || ''; }
    addEventListener(name, fn) { (this.handlers[name] ||= []).push(fn); }
    async emit(name) { for (const fn of this.handlers[name] || []) await fn({ target: this }); }
    setAttribute(name, value) { this.attrs[name] = value; }
    getAttribute(name) { return this.attrs[name] || ''; }
    appendChild(child) { this.children.push(child); }
    closest() { return { style: {} }; }
    focus() {}
  }
  nodes.set('secret-gate-overlay', new Element('secret-gate-overlay'));
  nodes.set('secret-gate-modal', new Element('secret-gate-modal'));
  const document = {
    readyState: 'loading', addEventListener() {}, dispatchEvent() {},
    getElementById: (id) => nodes.get(id) || null,
    createElement: () => new Element(),
  };
  const storage = new Map([['dpr_secret_password_v1', 'Test-password1!']]);
  const window = {
    location: { hostname: 'localhost', protocol: 'http:', origin: 'http://localhost', pathname: '/' },
    DPRLLMConfigUtils: utils, crypto: webcrypto,
    SubscriptionsManager: { openOverlay() {} },
    localStorage: { getItem: (k) => storage.get(k) || null, setItem: (k, v) => storage.set(k, v), removeItem: (k) => storage.delete(k) },
  };
  const calls = [];
  const errors = [];
  let failAuth = false;
  let changeModelDuringTest = false;
  const fetch = async (url, options) => {
    calls.push({ url, options });
    if (url === 'https://llm.paratera.com/v1/chat/completions') {
      if (failAuth) return { ok: false, status: 401, statusText: 'Unauthorized', text: async () => 'invalid test key' };
      if (changeModelDuringTest) nodes.get('secret-setup-deepseek-model-select').value = 'Changed-Model';
      return { ok: true, json: async () => ({ choices: [{ message: { content: 'hello world' } }] }) };
    }
    if (url === 'http://localhost:8567/api/local/secret') return { ok: true, json: async () => ({ ok: true }) };
    throw new Error('Unexpected request: ' + url);
  };
  const context = { window, document, fetch, console: { ...console, error: (...args) => errors.push(args) }, crypto: webcrypto, URL,
    TextEncoder, TextDecoder, AbortController, Uint8Array,
    btoa: (s) => Buffer.from(s, 'binary').toString('base64'),
    setTimeout, clearTimeout, requestAnimationFrame: (fn) => fn(),
    CustomEvent: class { constructor(type, init) { this.type = type; this.detail = init?.detail; } },
  };
  const source = fs.readFileSync(require.resolve('../app/secret.session.js'), 'utf8')
    .replace('  function init() {', '  window.testSetupOverlay = setupOverlay;\n  function init() {');
  vm.runInNewContext(source, context);
  window.testSetupOverlay(false);
  window.DPRSecretSetup.openStep2();
  const get = (id) => { assert.ok(nodes.has(id), 'Missing UI control: ' + id); return nodes.get(id); };
  const provider = get('secret-setup-llm-provider');
  provider.value = 'paratera';
  await provider.emit('change');
  assert.equal(get('secret-setup-llm-base-url').value, 'https://llm.paratera.com');
  assert.equal(get('secret-setup-deepseek-model-select').value, 'DeepSeek-V4-Pro-0813');
  get('secret-setup-deepseek').value = 'test-key-not-real';
  await get('secret-setup-deepseek').emit('input');

  // Untested configuration is not saved or sent anywhere.
  await get('secret-setup-generate').emit('click');
  assert.equal(calls.length, 0);
  await get('secret-setup-deepseek-test').emit('click');
  assert.equal(calls.length, 1);
  assert.equal(calls[0].url, 'https://llm.paratera.com/v1/chat/completions');
  assert.equal(JSON.parse(calls[0].options.body).model, 'DeepSeek-V4-Pro-0813');
  assert.equal(calls[0].options.headers.Authorization, 'Bearer test-key-not-real');

  // Editing the address invalidates the test; normalization must not duplicate /v1.
  get('secret-setup-llm-base-url').value = 'https://llm.paratera.com/v1/';
  await get('secret-setup-llm-base-url').emit('input');
  await get('secret-setup-generate').emit('click');
  assert.equal(calls.length, 1);
  await get('secret-setup-deepseek-test').emit('click');
  await get('secret-setup-generate').emit('click');
  assert.equal(calls.length, 3);
  assert.deepEqual(errors, []);
  assert.ok(storage.has('dpr_local_secret_private_v1'), 'Encrypted config was not saved');
  assert.equal(window.decoded_secret_private.llmProvider.type, 'paratera');
  assert.equal(window.decoded_secret_private.summarizedLLM.baseUrl, 'https://llm.paratera.com/v1');
  assert.equal(window.decoded_secret_private.chatLLMs[0].baseUrl, 'https://llm.paratera.com/v1');
  assert.equal(window.decoded_secret_private.chatLLMs[0].models[0], 'DeepSeek-V4-Pro-0813');

  // Reopening the UI restores the actual saved provider, address and exact model ID.
  window.DPRSecretSetup.openStep2();
  assert.equal(get('secret-setup-llm-provider').value, 'paratera');
  assert.equal(get('secret-setup-llm-base-url').value, 'https://llm.paratera.com/v1');
  assert.equal(get('secret-setup-deepseek-model-select').value, 'DeepSeek-V4-Pro-0813');
  failAuth = true;
  await get('secret-setup-deepseek-test').emit('click');
  assert.match(get('secret-setup-deepseek-status').textContent, /401.*llm\.paratera\.com/);
  const afterFailure = calls.length;
  await get('secret-setup-generate').emit('click');
  assert.equal(calls.length, afterFailure, 'Failed authentication must prevent saving');
  assert.ok(calls.every((c) => !c.url.includes('api.deepseek.com')), 'Never retry a third-party key at the official endpoint');
  failAuth = false;
  changeModelDuringTest = true;
  await get('secret-setup-deepseek-test').emit('click');
  assert.equal(get('secret-setup-deepseek-status').textContent, '配置已变更，请重新测试。');
  const afterChange = calls.length;
  await get('secret-setup-generate').emit('click');
  assert.equal(calls.length, afterChange, 'A stale successful test must not validate changed configuration');
  console.log('provider setup integration tests passed (mock requests only)');
}
main().catch((error) => { console.error(error); process.exitCode = 1; });
