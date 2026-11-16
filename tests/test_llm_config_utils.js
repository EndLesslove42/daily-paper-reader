const assert = require('node:assert/strict');

const {
  normalizeBaseUrlForStorage,
  buildChatCompletionsEndpoint,
  sanitizeModelList,
  resolveChatModels,
  resolveSummaryLLM,
  inferProviderType,
  getProviderPreset,
  buildProviderConfig,
  getDeepSeekPreset,
  inferChatApiProfile,
  resolveJsonResponseMode,
  isDeepSeekV4Model,
  resolveMaxOutputTokens,
  shouldUseXApiKeyHeader,
  buildStreamingChatPayload,
  buildConnectivityTestPayload,
} = require('../app/llm-config-utils.js');

function testNormalizeBaseUrlForStorage() {
  assert.equal(
    normalizeBaseUrlForStorage('https://api.example.com/v1/chat/completions'),
    'https://api.example.com/v1',
  );
  assert.equal(
    normalizeBaseUrlForStorage('https://api.example.com/v1/'),
    'https://api.example.com/v1',
  );
}

function testBuildChatCompletionsEndpoint() {
  assert.equal(
    buildChatCompletionsEndpoint('https://api.example.com/v1'),
    'https://api.example.com/v1/chat/completions',
  );
  assert.equal(
    buildChatCompletionsEndpoint('https://api.example.com/custom-root'),
    'https://api.example.com/custom-root/v1/chat/completions',
  );
}

function testSanitizeModelList() {
  assert.deepEqual(
    sanitizeModelList(['deepseek-v4-flash', ' deepseek-v4-flash ', 'deepseek-v4-pro', 'custom-model', 'extra'], 3),
    ['deepseek-v4-flash', 'deepseek-v4-pro', 'custom-model'],
  );
}

function testResolveChatModelsAndSummary() {
  const secret = {
    summarizedLLM: {
      apiKey: 'sk-summary',
      baseUrl: 'https://api.example.com/v1',
      model: 'gpt-4.1-mini',
    },
    chatLLMs: [
      {
        apiKey: 'sk-chat',
        baseUrl: 'https://api.example.com/v1/',
        models: ['gpt-4.1-mini', 'claude-sonnet-4'],
      },
    ],
  };

  const chatModels = resolveChatModels(secret);
  assert.equal(chatModels.length, 2);
  assert.deepEqual(chatModels.map((item) => item.name), [
    'gpt-4.1-mini',
    'claude-sonnet-4',
  ]);

  const summary = resolveSummaryLLM(secret);
  assert.equal(summary.model, 'gpt-4.1-mini');
  assert.equal(summary.baseUrl, 'https://api.example.com/v1');
}

function testInferProviderType() {
  assert.equal(
    inferProviderType({
      summarizedLLM: {
        apiKey: 'sk',
        baseUrl: 'https://api.deepseek.com',
        model: 'deepseek-v4-flash',
      },
    }),
    'deepseek',
  );
  assert.equal(
    inferProviderType({
      summarizedLLM: {
        apiKey: 'sk',
        baseUrl: 'https://example.com/v1',
        model: 'other-model',
      },
    }),
    'custom',
  );
}

function testGetDeepSeekPreset() {
  assert.deepEqual(
    getDeepSeekPreset('deepseek'),
    {
      key: 'deepseek',
      label: 'DeepSeek 官方',
      baseUrl: 'https://api.deepseek.com',
      models: ['deepseek-v4-flash', 'deepseek-v4-pro'],
    },
  );
  assert.equal(getDeepSeekPreset('other-a'), null);
  assert.equal(getDeepSeekPreset('other-b'), null);
  assert.equal(getDeepSeekPreset('other-c'), null);
  assert.equal(getDeepSeekPreset('other-d'), null);
}

function testInferChatApiProfile() {
  assert.equal(
    inferChatApiProfile('https://api.deepseek.com', 'deepseek-v4-flash'),
    'deepseek',
  );
  assert.equal(inferChatApiProfile('https://example.com/v1', 'other-model'), 'unsupported');
  assert.equal(inferChatApiProfile('https://example.com/v1', 'other-model'), 'unsupported');
}

function testResolveJsonResponseMode() {
  assert.equal(
    resolveJsonResponseMode({
      baseUrl: 'https://api.deepseek.com',
      model: 'deepseek-v4-flash',
    }),
    'json_object',
  );
  assert.equal(
    resolveJsonResponseMode({
      baseUrl: 'https://example.com/v1',
      model: 'other-model',
      preferSchema: false,
    }),
    'json_object',
  );
}

function testResolveMaxOutputTokens() {
  assert.equal(isDeepSeekV4Model('deepseek-v4-flash'), true);
  assert.equal(isDeepSeekV4Model('deepseek-v4-pro'), true);
  assert.equal(isDeepSeekV4Model('deepseek-chat'), false);
  assert.equal(
    resolveMaxOutputTokens({
      baseUrl: 'https://api.deepseek.com',
      model: 'deepseek-v4-flash',
    }),
    393216,
  );
  assert.equal(
    resolveMaxOutputTokens({
      baseUrl: 'https://api.deepseek.com',
      model: 'deepseek-v4-pro',
    }),
    393216,
  );
  assert.equal(
    resolveMaxOutputTokens({
      baseUrl: 'https://example.com/v1',
      model: 'other-model',
    }),
    null,
  );
}

function testShouldUseXApiKeyHeader() {
  assert.equal(
    shouldUseXApiKeyHeader({
      baseUrl: 'https://example.com/v1',
      model: 'other-model',
    }),
    true,
  );
  assert.equal(
    shouldUseXApiKeyHeader({
      baseUrl: 'https://example.com/v1',
      model: 'other-model',
    }),
    true,
  );
}

function testBuildStreamingChatPayload() {
  assert.deepEqual(
    buildStreamingChatPayload({
      baseUrl: 'https://api.deepseek.com',
      model: 'deepseek-v4-flash',
      messages: [{ role: 'user', content: 'hi' }],
    }),
    {
      model: 'deepseek-v4-flash',
      messages: [{ role: 'user', content: 'hi' }],
      stream: true,
      max_tokens: 393216,
    },
  );

  assert.deepEqual(
    buildStreamingChatPayload({
      baseUrl: 'https://api.deepseek.com',
      model: 'deepseek-v4-pro',
      messages: [{ role: 'user', content: 'hi' }],
    }),
    {
      model: 'deepseek-v4-pro',
      messages: [{ role: 'user', content: 'hi' }],
      stream: true,
      max_tokens: 393216,
    },
  );

}

function testBuildConnectivityTestPayload() {
  assert.deepEqual(
    buildConnectivityTestPayload({
      baseUrl: 'https://api.deepseek.com',
      model: 'deepseek-v4-pro',
    }),
    {
      model: 'deepseek-v4-pro',
      messages: [
        { role: 'system', content: 'Reply with exactly: hello world' },
        { role: 'user', content: 'hello world' },
      ],
      temperature: 0,
      max_tokens: 256,
    },
  );

  assert.deepEqual(
    buildConnectivityTestPayload({
      baseUrl: 'https://api.deepseek.com',
      model: 'deepseek-v4-flash',
    }),
    {
      model: 'deepseek-v4-flash',
      messages: [
        { role: 'system', content: 'Reply with exactly: hello world' },
        { role: 'user', content: 'hello world' },
      ],
      temperature: 0,
      max_tokens: 256,
    },
  );

}

function testParateraAndCustomConfiguration() {
  const preset = getProviderPreset('paratera');
  assert.equal(preset.baseUrl, 'https://llm.paratera.com');
  assert.deepEqual(preset.models, ['DeepSeek-V4-Pro-0813']);
  preset.models.push('local-mutation');
  assert.deepEqual(getProviderPreset('paratera').models, ['DeepSeek-V4-Pro-0813']);
  assert.equal(getProviderPreset('__proto__'), null);

  const config = buildProviderConfig({
    providerType: 'paratera', apiKey: 'test-key',
    baseUrl: 'https://llm.paratera.com/v1/chat/completions', model: 'DeepSeek-V4-Pro-0813',
  });
  assert.equal(config.providerType, 'paratera');
  assert.equal(config.summaryBaseUrl, 'https://llm.paratera.com/v1');
  assert.equal(buildChatCompletionsEndpoint(config.summaryBaseUrl), 'https://llm.paratera.com/v1/chat/completions');
  assert.deepEqual(config.chatModels, ['DeepSeek-V4-Pro-0813']);
  assert.equal(inferProviderType({
    llmProvider: { type: 'deepseek' },
    summarizedLLM: { apiKey: 'test-key', baseUrl: config.summaryBaseUrl, model: config.summaryModel },
  }), 'paratera');

  // A third-party DeepSeek model must not inherit the official endpoint's token limit.
  assert.equal(resolveMaxOutputTokens({ baseUrl: preset.baseUrl, model: 'deepseek-v4-pro' }), null);
  assert.equal(inferChatApiProfile(preset.baseUrl, 'deepseek-v4-pro'), 'unsupported');
  assert.equal(buildStreamingChatPayload({ baseUrl: preset.baseUrl, model: 'DeepSeek-V4-Pro-0813', messages: [] }).max_tokens, undefined);
  assert.equal(buildProviderConfig({ providerType: 'custom', apiKey: 'test-key', baseUrl: 'https://other.example/v1', model: 'Exact-Model-ID' }).summaryModel, 'Exact-Model-ID');
  assert.equal(inferProviderType({}), 'deepseek');
  assert.throws(() => buildProviderConfig({ providerType: 'paratera', apiKey: 'test-key', baseUrl: '', model: 'model' }), /Base URL/);
  assert.throws(() => buildProviderConfig({ apiKey: 'test-key', baseUrl: 'javascript:alert(1)', model: 'model' }), /http/);
  assert.throws(() => buildProviderConfig({ apiKey: 'test-key', baseUrl: 'https://name:password@example.com', model: 'model' }), /Base URL/);
  assert.throws(() => buildProviderConfig({ apiKey: 'test-key', baseUrl: 'https://example.com', model: '<img src=x onerror=alert(1)>' }), /模型 ID/);
}

testNormalizeBaseUrlForStorage();
testBuildChatCompletionsEndpoint();
testSanitizeModelList();
testResolveChatModelsAndSummary();
testInferProviderType();
testGetDeepSeekPreset();
testInferChatApiProfile();
testResolveJsonResponseMode();
testResolveMaxOutputTokens();
testShouldUseXApiKeyHeader();
testBuildStreamingChatPayload();
testBuildConnectivityTestPayload();
testParateraAndCustomConfiguration();

console.log('llm config utils tests passed');
