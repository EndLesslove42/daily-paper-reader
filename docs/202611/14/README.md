# 日报 · 2026-11-14

- 生成时间：2026-11-14T09:39:32+08:00
- 当次推荐总数：3
- 精读区：1
- 速读区：2

## 今日简报
今天选3篇可靠研究，补充“该让神经网络学习哪一层”与“遥感输入怎样进入过程模型”两条路线。分布式水文研究用保留的物理状态提供记忆，以小网络修正内部通量；生态学对照说明参数学习、残差校正和预训练适配的收益取决于跨站跨年任务；Prithvi-EO-2.0提供冻结遥感编码器与动态气象融合的具体通量案例。三篇均不提供CMAQ现成提速结论。对你更值得先测的是：宿主状态是否足以支持轻量代理、月年损失能辨识哪些内部量，以及遥感表征能否提前计算缓存。

## 精读区
1. [由出口观测学习内部通量：让物理状态承担记忆，再用小网络修正过程](/202611/14/codex-7314190468b6-a-distributed-hybrid-physics-ai-framework-for-learning-corrections-of-inter) — 先检验CMAQ已保留的状态和跨步缓存能否给小MLP提供足够记忆，再决定是否需要Transformer。将待学范围限制为明确的交换子过程或有界修正，在站点真实空间支持上积算月/年通量；以同参数量网络和不同状态输入作对照，同时实测CPU嵌回耗时。

## 速读区
1. [物理应放在哪一层：参数学习、残差校正与预训练适配的系统对照](/202611/14/codex-4f4d7085f4f3-process-informed-neural-networks-a-hybrid-modelling-approach-to-improve-pre) — 为沉降建立四个可比较版本：固定物理参数、轻量网络生成参数、仅作有界过程修正、二者组合。共享观测算子与划分，再比较留站留年表现和CPU成本。月年实测只用于对应窗口积分损失，保留原模型作预训练参考及约束，不把它当独立观测。
2. [冻结遥感表征再融合气象：一个小样本通量案例及其空间验证缺口](/202611/14/codex-a548e5acf1f7-prithvi-eo-2-0-a-versatile-multitemporal-foundation-model-for-earth-observa) — 把现有地表输入、AEF与Prithvi月/季节表征做同划分消融。遥感嵌入可预先提取、缓存，再与CMAQ动态气象共同输入小代理，避免每个分钟步调用大编码器；同时评估嵌入更新频率、聚合尺度及完整CPU耗时。

## 检索记录
检索不设年份窗口或新旧比例。已同步独立发布副本，读取DAILY_PROMPT与仓库规则，核对近7日覆盖和全部历史身份。近期已连续介绍CPU/GPU耦合与贝叶斯校准，本期优先补充内部过程修正、稀疏监督的架构对照、时序遥感输入。实际查阅HESS分布式混合水文正式论文与公开审稿记录、Ecology Letters过程信息网络正式论文、Prithvi-EO-2.0的Jülich机构库正式IEEE排版PDF和arXiv记录；另检索了海洋边界层神经闭合、生态混合建模和多时间尺度水文候选，未按标题贴合凑数。HESS正文和附录文本已完整阅读；Ecology Letters仅核读摘要及架构、采样、验证、结果关键段落；Prithvi仅核读摘要、GPP方法和结果，不把后两篇标成全文精读。PMC遇到浏览器检测，改读合法开放的出版社HTML；Freiburg机构库跳转失败，IEEE DOI入口未能打开，但正式排版PDF可读，不能把这些访问失败写成没有论文。保留正式日期：Ecology Letters首次上线2024-12-03；Prithvi首次正式上线2025-12-11、卷期为2026，早期arXiv始于2024，不包装为今天新文。三篇分别使用小时流量、从日值每周抽取一天、日均GPP产品，都不是仅有月年累计沉降的完整实证；迁移时必须另建真实时间积分与空间支持算子。未调用旧模型API或旧日报工作流。

- [检索来源 1](https://hess.copernicus.org/articles/29/3589/2025/)
- [检索来源 2](https://hess.copernicus.org/articles/29/3589/2025/hess-29-3589-2025-discussion.html)
- [检索来源 3](https://onlinelibrary.wiley.com/doi/full/10.1111/ele.70012)
- [检索来源 4](https://juser.fz-juelich.de/record/1050065/files/Prithvi-EO-2.0_A_Versatile_Multitemporal_Foundation_Model_for_Earth_Observation_Applications.pdf)
- [检索来源 5](https://arxiv.org/abs/2412.02732)
