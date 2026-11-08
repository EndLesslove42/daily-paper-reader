# 日报 · 2026-11-08

- 生成时间：2026-11-08T09:42:57+08:00
- 当次推荐总数：3
- 精读区：3
- 速读区：0

## 今日简报
今天选读3篇较早研究，围绕“替代边界如何满足收支闭合”“遥感时序能否在循环外编码”“稀疏观测下怎样检验真正的泛化”。建议先读Beucler的硬约束模块，再用Roberts设计留站、留年份检验；Presto补充动态地表输入与离线特征缓存的思路。均保留真实发表日期，不把参数少、FLOPs低或预算闭合写成CMAQ已提速、瞬时Vd已被观测验证。

## 精读区
1. [把解析约束写进神经网络：模块边界必须包含哪些收支项？](/202611/08/codex-edf9a8126da8-enforcing-analytic-constraints-in-neural-networks-emulating-physical-system) — 先画两种候选接口：①预测阻力或交换系数，保留宿主的通量与质量更新；②联合预测一组交换通道，并由固定更新层闭合空气与地表收支。用相同的小MLP比较软、硬约束的精度、非负性、CPU调用耗时和整模式误差。这能帮助确定哪些输出应一起替代，但边界增大后的速度必须另测。
2. [稀疏站点的“好精度”可信吗？按预测目标设计时空分块验证](/202611/08/codex-5f50e02b2a17-cross-validation-strategies-for-data-with-temporal-spatial-hierarchical-or) — 建议分别报告同站未来时段、新站同气候条件、新地区三个目标；用不重叠观测窗口分组，必要时设时间缓冲。调参采用训练内分块，最终测试站点和年份锁定。月累计沉降就评价相同窗口的累计量；高频Vd另需独立高频证据。比较AEF或时序表征时沿用同一划分，避免把地点记忆误判为地表机制增益。
3. [Presto：把慢变化地表时序编码留在CMAQ时间循环之外](/202611/08/codex-0d50b9ae770c-lightweight-pre-trained-transformers-for-remote-sensing-timeseries) — 可做“时间循环外编码＋循环内小MLP”的分层方案：预处理慢变化地表时序，按月或所需频率缓存网格特征，分钟级调用仅读缓存并结合即时气象与浓度。与AEF、常规LAI/土地类型和无编码基线比较；计时包含预处理摊销、缓存读取和MPI内存开销，实际验证能否降低总耗时。

## 速读区
- 本次无合适推荐。

## 检索记录
未设年份窗口。检索并打开过程代理硬约束、轻量遥感时序表征、时空依赖数据验证的原文，结合11月2–7日已推条目去重；今天补充输入表征与验证设计，不再重复集合反演和可微参数学习。PRL主文、Presto arXiv v4主文、Ecography正文均已阅读，补充材料与代码未运行或逐项复现。Presto明确为NeurIPS 2023气候机器学习workshop Spotlight，不标作NeurIPS主会；依据公开代码、跨任务对照和消融选入，定位为地表输入方法参考，非CMAQ加速证据。Ecography网页显示2016-12-08在线首发、2017年卷期，日期字段采用前者。APS DOI入口在工具内不可达，改读作者机构公开的正式版PDF；WSL的Roberts PDF返回404，但Wiley全文可读；一次组合请求连接失败后重试成功，未把访问失败当作文献空缺。未调用旧API或旧工作流。

- [检索来源 1](https://gentinelab.eee.columbia.edu/sites/gentinelab.eee.columbia.edu/files/content/PhysRevLett.126.098302.pdf)
- [检索来源 2](https://arxiv.org/abs/1909.00912)
- [检索来源 3](https://nsojournals.onlinelibrary.wiley.com/doi/full/10.1111/ecog.02881)
- [检索来源 4](https://epub.uni-regensburg.de/39299/)
- [检索来源 5](https://arxiv.org/abs/2304.14065)
- [检索来源 6](https://arxiv.org/html/2304.14065v4)
- [检索来源 7](https://github.com/nasaharvest/presto)
- [检索来源 8](https://gabrieltseng.github.io/publications)
