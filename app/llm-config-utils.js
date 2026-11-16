(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) {
    module.exports = api;
  }
  if (root) {
    root.DPRLLMConfigUtils = api;
  }
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  const DEFAULT_DEEPSEEK_BASE_URL = 'https://api.deepseek.com';
  const DEFAULT_DEEPSEEK_CHAT_MODELS = [
    'deepseek-v4-flash',
    'deepseek-v4-pro',
  ];
  const DEEPSEEK_V4_MAX_OUTPUT_TOKENS = 393216;
  const DEEPSEEK_PRESETS = Object.freeze({
    deepseek: Object.freeze({
      key: 'deepseek',
      label: 'DeepSeek 官方',
      baseUrl: 'https://api.deepseek.com',
      models: Object.freeze(['deepseek-v4-flash', 'deepseek-v4-pro']),
    }),
  });
  const LLM_PROVIDER_PRESETS = Object.freeze({
    deepseek: DEEPSEEK_PRESETS.deepseek,
    paratera: Object.freeze({
      key: 'paratera',
      label: '并行智算云',
      baseUrl: 'https://llm.paratera.com',
      models: Object.freeze(['DeepSeek-V4-Pro-0813']),
    }),
  });

  const normalizeText = (value) => String(value || '').trim();

  const normalizeBaseUrlForStorage = (value) => {
    let text = normalizeText(value).replace(/\/+$/g, '');
    if (!text) return '';
    text = text.replace(/\/chat\/completions$/i, '');
    return text.replace(/\/+$/g, '');
  };

  const buildChatCompletionsEndpoint = (value) => {
    const raw = normalizeText(value).replace(/\/+$/g, '');
    if (!raw) return '';
    if (/\/chat\/completions$/i.test(raw)) return raw;
    const normalized = normalizeBaseUrlForStorage(raw);
    if (!normalized) return '';
    if (/\/v\d+$/i.test(normalized)) {
      return `${normalized}/chat/completions`;
    }
    return `${normalized}/v1/chat/completions`;
  };

  const sanitizeModelList = (values, maxCount = 3) => {
    const rawList = Array.isArray(values) ? values : [values];
    const out = [];
    const seen = new Set();
    for (const value of rawList) {
      const parts = String(value || '')
        .split(/[\n,]+/)
        .map((item) => normalizeText(item))
        .filter(Boolean);
      for (const name of parts) {
        const key = name.toLowerCase();
        if (!key || seen.has(key)) continue;
        seen.add(key);
        out.push(name);
        if (out.length >= Math.max(Number(maxCount) || 0, 1)) {
          return out;
        }
      }
    }
    return out;
  };

  const resolveChatModels = (secret) => {
    const safeSecret = secret && typeof secret === 'object' ? secret : {};
    const chatList = Array.isArray(safeSecret.chatLLMs) ? safeSecret.chatLLMs : [];
    const models = [];
    const seen = new Set();
    chatList.forEach((item) => {
      if (!item || typeof item !== 'object') return;
      const baseUrl = normalizeBaseUrlForStorage(item.baseUrl || '');
      const apiKey = normalizeText(item.apiKey || '');
      const modelNames = sanitizeModelList(item.models || [], 99);
      if (!baseUrl || !apiKey || !modelNames.length) return;
      modelNames.forEach((name) => {
        const dedupeKey = `${name.toLowerCase()}\u0000${baseUrl}\u0000${apiKey}`;
        if (seen.has(dedupeKey)) return;
        seen.add(dedupeKey);
        models.push({
          name,
          apiKey,
          baseUrl,
        });
      });
    });
    return models;
  };

  const resolveSummaryLLM = (secret) => {
    const safeSecret = secret && typeof secret === 'object' ? secret : {};
    const summarized = safeSecret.summarizedLLM || {};
    const baseUrl = normalizeBaseUrlForStorage(summarized.baseUrl || '');
    const apiKey = normalizeText(summarized.apiKey || '');
    const model = normalizeText(summarized.model || '');
    if (baseUrl && apiKey && model) {
      return { baseUrl, apiKey, model };
    }

    const chatModels = resolveChatModels(safeSecret);
    if (!chatModels.length) return null;
    return {
      baseUrl: normalizeBaseUrlForStorage(chatModels[0].baseUrl || ''),
      apiKey: normalizeText(chatModels[0].apiKey || ''),
      model: normalizeText(chatModels[0].name || ''),
    };
  };

  const inferProviderType = (secret) => {
    const safeSecret = secret && typeof secret === 'object' ? secret : {};
    const llmProvider = safeSecret.llmProvider || {};
    const explicit = normalizeText(llmProvider.type || llmProvider.provider || '').toLowerCase();
    const summary = resolveSummaryLLM(safeSecret);
    const baseUrl = summary ? summary.baseUrl : '';
    if (baseUrl) {
      let host = '';
      try { host = new URL(baseUrl).hostname.toLowerCase(); } catch { /* invalid URL */ }
      if (host === 'llm.paratera.com' || host === 'llmapi.paratera.com') return 'paratera';
      if (host === 'api.deepseek.com' || host === 'deepseek.com') return 'deepseek';
      return 'custom';
    }
    return ['deepseek', 'paratera', 'custom'].includes(explicit) ? explicit : 'deepseek';
  };

  const getProviderPreset = (key) => {
    const name = normalizeText(key).toLowerCase();
    const preset = Object.prototype.hasOwnProperty.call(LLM_PROVIDER_PRESETS, name)
      ? LLM_PROVIDER_PRESETS[name] : null;
    return preset ? { ...preset, models: [...preset.models] } : null;
  };

  const buildProviderConfig = ({ providerType, apiKey, baseUrl, model, chatModels = [] } = {}) => {
    const preset = getProviderPreset(providerType);
    const key = normalizeText(apiKey);
    const base = normalizeBaseUrlForStorage(baseUrl == null ? (preset && preset.baseUrl) : baseUrl);
    const name = normalizeText(model);
    if (!key) throw new Error('请填写当前服务商的 API Key。');
    if (!base) throw new Error('请填写当前服务商的 Base URL。');
    let url;
    try { url = new URL(base); } catch { throw new Error('Base URL 必须是完整的 http(s) 地址。'); }
    if (!['http:', 'https:'].includes(url.protocol) || url.username || url.password || url.search || url.hash) {
      throw new Error('Base URL 必须是无账号、查询参数及片段的 http(s) 地址。');
    }
    if (!name) throw new Error('请填写平台提供的准确模型 ID。');
    if (/[<>\r\n]/.test(name)) throw new Error('模型 ID 不能包含 HTML 或换行。');
    return {
      providerType: inferProviderType({ summarizedLLM: { apiKey: key, baseUrl: base, model: name } }),
      summaryApiKey: key,
      summaryBaseUrl: base,
      summaryModel: name,
      chatModels: sanitizeModelList([name, ...chatModels], 99),
    };
  };

  const getDeepSeekPreset = (key) => {
    const presetKey = normalizeText(key).toLowerCase();
    const preset = DEEPSEEK_PRESETS[presetKey];
    if (!preset) return null;
    return {
      key: preset.key,
      label: preset.label,
      baseUrl: preset.baseUrl,
      models: [...preset.models],
    };
  };

  const inferChatApiProfile = (baseUrl, model) => {
    const normalizedBaseUrl = normalizeBaseUrlForStorage(baseUrl || '').toLowerCase();
    if (/(^|\/\/)(api\.)?deepseek\.com(?:$|\/)/i.test(normalizedBaseUrl)) {
      return 'deepseek';
    }
    // A model name does not establish the endpoint's provider or token limits.
    return 'unsupported';
  };

  const resolveJsonResponseMode = ({ baseUrl, model, preferSchema = true }) => {
    return 'json_object';
  };

  const isDeepSeekV4Model = (model) => {
    const normalizedModel = normalizeText(model || '').toLowerCase();
    return normalizedModel === 'deepseek-v4-flash' || normalizedModel === 'deepseek-v4-pro';
  };

  const resolveMaxOutputTokens = ({ baseUrl, model } = {}) => {
    const profile = inferChatApiProfile(baseUrl, model);
    if (profile === 'deepseek' && isDeepSeekV4Model(model)) {
      return DEEPSEEK_V4_MAX_OUTPUT_TOKENS;
    }
    return null;
  };

  const shouldUseXApiKeyHeader = ({ baseUrl, model }) => {
    return true;
  };

  const buildStreamingChatPayload = ({ baseUrl, model, messages }) => {
    const payload = {
      model: normalizeText(model),
      messages: Array.isArray(messages) ? messages : [],
      stream: true,
    };
    const maxTokens = resolveMaxOutputTokens({ baseUrl, model });
    if (maxTokens) {
      payload.max_tokens = maxTokens;
    }
    return payload;
  };

  const buildConnectivityTestPayload = ({ baseUrl, model }) => {
    const normalizedModel = normalizeText(model);
    return {
      model: normalizedModel,
      messages: [
        {
          role: 'system',
          content: 'Reply with exactly: hello world',
        },
        {
          role: 'user',
          content: 'hello world',
        },
      ],
      temperature: 0,
      max_tokens: 256,
    };
  };

  return {
    DEFAULT_DEEPSEEK_BASE_URL,
    DEFAULT_DEEPSEEK_CHAT_MODELS,
    DEEPSEEK_PRESETS,
    LLM_PROVIDER_PRESETS,
    normalizeText,
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
  };
});
