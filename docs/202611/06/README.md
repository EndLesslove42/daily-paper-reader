# 日报 · 2026-11-06

- 生成时间：2026-11-06T09:35:22+08:00
- 当次推荐总数：3
- 精读区：2
- 速读区：1

## 今日简报
今天围绕“稀疏观测怎样反馈到过程模块的神经参数”选读3篇：JAMES用时间统计量校准嵌入式闭合，JFM用稀疏速度观测学习闭合网络，HESS检验动态参数是否真的优于简单基线。三篇均保留物理宿主，按研究问题、局限与隐含风险、对当前研究的用途和差异三问组织。这里提供可迁移路线，不声称任何一篇已解决月年沉降量反演分钟Vd，也不把无梯度训练等同于低计算成本。

## 精读区
1. [不用逐步过程标签：从时间统计量反演嵌入式神经参数化](/202611/06/codex-ce8cc2a18d67-training-physics-based-machine-learning-parameterizations-with-gradient-fre) — 可先固定原有代理骨干，用少量共享通道校正参数试验：每次跑物理宿主，按站点真实采样窗口积分预测沉降量，再以窗口误差反演校正参数；先测有效可辨识维数及前向预算，再考虑放开更多网络权重。
2. [从稀疏间接观测更新网络权重：保留物理求解器的集合学习](/202611/06/codex-cccdaf2b7298-ensemble-kalman-method-for-learning-turbulence-models-from-indirect-observa) — 对应你的问题，可把“闭合网络→RANS→速度观测”改成“Vd代理→CMAQ→站点浓度/累计沉降观测”，直接研究共享网络参数更新，而不是给稀疏站点插值造全网格标签。

## 速读区
1. [观测真的支持动态参数吗？先把简单参数化基线做扎实](/202611/06/codex-5641a6c79feb-an-argument-for-parsimony-in-differentiable-hydrologic-models) — 在稀疏沉降监督前，先比较少量固定校正参数、静态地表编码加动态物理输入，以及动态校正头，并保持相同观测损失与划分。参数静态不意味着把随气象变化的Vd设成常数。

## 检索记录
不设年份窗口，检索时间积分/平均观测算子、神经参数化反演、集合Kalman学习及参数可辨识性。打开并核查JAMES 2022原始正文、Cambridge JFM 2022正文、HESS 2026正文及预印本讨论页；用Caltech作者库、arXiv与EGUsphere交叉核对日期和身份。JAMES和JFM按正文重点阅读归档，HESS按摘要及关键方法/讨论核查的速读归档，未复现代码。特别区分：LES/合成观测与真实监测、空间稀疏与时间累计、日径流监督与月年沉降量监督。没有将月径流端到端预测、短连续记录校准或一般少样本标签当作本题直接解答。三篇均非近期新发表，已检查历史DOI/arXiv去重。

- [检索来源 1](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2022MS003105)
- [检索来源 2](https://authors.library.caltech.edu/records/1q6gn-mvc46)
- [检索来源 3](https://www.cambridge.org/core/journals/journal-of-fluid-mechanics/article/ensemble-kalman-method-for-learning-turbulence-models-from-indirect-observation-data/1017FA12DF01850C1579ABCFB09405E2)
- [检索来源 4](https://arxiv.org/abs/2202.05122)
- [检索来源 5](https://hess.copernicus.org/articles/30/5173/2026/)
- [检索来源 6](https://egusphere.copernicus.org/preprints/2026/egusphere-2026-756/)
