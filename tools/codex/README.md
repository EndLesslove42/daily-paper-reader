# Codex 文献日报

此入口保留现有 Docsify 网页及日期归档，由已登录的 Codex 订阅完成检索、筛选和摘要。发布脚本仅使用 Python 标准库和 Git，不加载 `.env`，不调用大模型、embedding 或 reranker API。

每天北京时间 09:00 在原聊天触发定时任务，读取 `DAILY_PROMPT.txt`。本机必须开机、联网且应用运行。订阅额度不足、机器离线或发布失败时不能保证准点完成；失败不会用旧 API 补跑。

## 生成与发布

1. 读取五个订阅主题和去重记录；用 Codex 内置网页工具检索期刊与预印本，阅读原文。
2. 把结构化 JSON 写到仓库外的聊天工作目录 `work/`。字段见 `DAILY_PROMPT.txt`。
3. `python tools/codex/publish_daily.py check --input <report.json>` 检查。
4. `python tools/codex/publish_daily.py publish --input <report.json>` 安全提交到 `main`。

发布器保留历史侧边栏，生成日期目录、单篇页面、可下载元数据及原始 JSON，并记录 DOI/arXiv 去重台账。一天只发布一次；即使零篇也保留日期和真实检索说明。检索服务失败不可作为零篇日报发布。摘要核对和全文阅读必须区分。

五个方向为过程模块AI替代、沉降与陆气交换、观测约束与反演、遥感与地表表征、过程耦合与数值方法。沉降保留为重要应用主线，非沉降研究可凭具体的输入表示、模块设计、约束或验证价值独立入选；不设每日沉降比例或方法论文数量上限。结合近7天记录保持覆盖，避免同类沉降研究连续占满。历史机器tag保持兼容，以 `DAILY_PROMPT.txt` 和 `config.yaml` 中的新定义解释。

日报是每日选读，不限近期发表。不设检索年份窗口、旧文数量上限或新旧比例；按研究价值、证据质量和对当前问题的帮助程度选择经典、方法演进或近期研究。可以一整期都是值得读的较早文献。保留真实发表日期并解释当前阅读价值；JSON的 `recent` / `method-backfill` 仅兼容既有日期标识，不决定优先级。

`render --repo <临时预览目录> --input <report.json>` 只生成预览，不联网、不提交。预览目录需包含原 `docs/_sidebar.md`，`check` 不写文件。

## 旧流程

`daily-paper-reader.yml` 的旧 API 日程已移除，且作业只有在仓库变量 `DPR_ENABLE_LEGACY_API` 显式设为 `true` 时才允许手动运行。原密钥保持原位。Windows 菜单检测本入口后不会触发旧 API 作业。

恢复旧模式时需手工启用上述仓库变量、恢复原 workflow 日程，并暂停 Codex 日报任务，避免同时生成两份日报。与上游同步若恢复了旧 workflow 的触发器，作业的变量开关仍可阻止运行；合并时请保留这个开关和 Codex 入口。

不运行 `git add .`、不重写历史、不强推。仓库有其他已跟踪改动、未推送提交、日期文件已存在或重复文献时停止，保留现场并汇报。
