const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');

async function main() {
  const html = fs.readFileSync(require.resolve('../index.html'), 'utf8');
  const loader = [...html.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/gi)]
    .map((m) => m[1]).find((script) => script.includes('function shouldLoadScriptFromCdn'));
  assert.ok(loader);
  const nodes = [];
  const document = {
    createElement: (tag) => ({ tag, remove() {} }),
    head: { appendChild(node) { nodes.push(node); if (node.tag === 'script') queueMicrotask(() => node.onload()); } },
  };
  const window = { setTimeout: () => 1, clearTimeout() {} };
  vm.runInNewContext(loader, { window, document, location: { hostname: 'endlesslove42.github.io' }, console });
  await window.DPRLoadAssets([
    { type: 'script', path: 'app/llm-config-utils.js' },
    { type: 'script', path: 'app/secret.session.js' },
    { type: 'script', path: 'app/vendor/docsify/4/lib/docsify.min.js' },
  ]);
  const expected = [
    'app/llm-config-utils.js', 'app/secret.session.js',
    'https://cdn.zwwen.online/app/vendor/docsify/4/lib/docsify.min.js',
  ];
  assert.deepEqual(nodes.filter((n) => n.tag === 'script').map((n) => n.src), expected);
  assert.deepEqual(nodes.filter((n) => n.as === 'script').map((n) => n.href), expected);
  console.log('asset origin integration tests passed');
}
main().catch((error) => { console.error(error); process.exitCode = 1; });
