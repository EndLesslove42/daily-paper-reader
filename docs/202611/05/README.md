# 日报 · 2026-11-05

- 生成时间：2026-11-05T09:51:33+08:00
- 当次推荐总数：4
- 精读区：2
- 速读区：2

## 今日简报
今天选读4篇有具体方法或工程证据的较早研究：FTorch的Fortran原位接入、GRL的物理一致参数化与低精度边界、GEOS-Chem随机森林的负面计时案例，以及TESSERA的离线地表表征。前两篇按正文阅读归档，后两篇为摘要和关键章节核查的速读。重点是保留宿主物理框架，把可学习性转化为模块收益，不追求整模型端到端替代。

## 精读区
1. [FTorch：把PyTorch模型原位接入Fortran的工程参考](/202611/05/codex-4109e3adf21c-ftorch-a-library-for-coupling-pytorch-models-to-fortran) — 阅读判断：可作CPU部署基线，比较原有接口与直接调用的完整成本。模型常驻、缓冲区复用及本地网格块批量调用仍需具体实现，不能只换接口便假定提速。
2. [物理一致的模块输出与低精度：稳定嵌回大气模型的经典参考](/202611/05/codex-d3758020b2c7-use-of-neural-networks-for-stable-accurate-and-physically-consistent-parame) — 阅读判断：为Vd、交换系数或通量等边界选择提供结构依据，也支持在CPU小模型上逐级验证精度。保留原物理更新不妨碍模块学习，但应同时检查过程收支、非负性及多步误差。

## 速读区
1. [GEOS-Chem随机森林化学代理：能拟合但更慢的早期负面案例](/202611/05/codex-6cfb322a784b-application-of-random-forest-regression-to-the-calculation-of-gas-phase-che) — 阅读判断：对比共享通道与按物种分别推理，统计调用次数、MPI进程的模型副本与访存成本。选择轻量架构须测完整模块，不能从单个树或单次预测推断整体速度。
2. [TESSERA：离线地表表征与轻量任务头，分离遥感骨干和在线过程计算](/202611/05/codex-ae387c203a51-tessera-temporal-embeddings-of-surface-spectra-for-earth-representation-and) — 阅读判断：将AEF/TESSERA先聚合到CMAQ网格并缓存，与动态气象输入交给小型Vd头；对地表变量、AEF和TESSERA做等容量比较，分别计离线准备与在线推理成本。

## 检索记录
检索不设年份窗口，沿模块嵌入、守恒输出、低精度、化学代理及预计算遥感表征追踪原始文献。核查JOSS原始软件论文、GMD和AGU/GRL正文、arXiv版本记录及作者仓库。TESSERA首版为2025-06-25，2026会议版不作为今日新文；CVF HTML返回403，改读公开arXiv版本。FTorch是软件工程参考，不是CMAQ已提速的性能证明。四篇均检查历史DOI/arXiv身份，不重复昨日辐射文献；未运行旧模型API或论文代码。

- [检索来源 1](https://joss.theoj.org/papers/10.21105/joss.07602)
- [检索来源 2](https://www.theoj.org/joss-papers/joss.07602/10.21105.joss.07602.pdf)
- [检索来源 3](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2020GL091363)
- [检索来源 4](https://gmd.copernicus.org/articles/12/1209/2019/)
- [检索来源 5](https://arxiv.org/abs/2506.20380)
- [检索来源 6](https://arxiv.org/html/2506.20380v7)
- [检索来源 7](https://github.com/ucam-eo/tessera)
