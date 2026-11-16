# 日报 · 2026-11-16

- 生成时间：2026-11-16T09:56:32+08:00
- 当次推荐总数：3
- 精读区：1
- 速读区：2

## 今日简报
今天选3篇较早但直接帮助实验设计的文章：先看O’Gorman与Dwyer怎样把多输出过程模块嵌回Fortran，以及扩大替代边界后为何还要重设特征和损失；再看PCL如何保留数值宿主、用间接观测学习模块中的神经关系；最后精读Fuentes与Raftery，处理稀疏站点和模型网格并非同一空间支持的问题。三篇分别解决接口、梯度和观测比较方式，不能把各自结果拼成已实现的CMAQ加速或月年观测辨识方案。

## 精读区
1. [稀疏站点怎样与CMAQ网格比较：空间支持、偏差与不确定性](/202611/16/codex-a6568b5b68a4-model-evaluation-and-spatial-interpolation-by-bayesian-combination-of-obser) — 在训练之前为每类数据明确空间支持：塔通量足迹、采样器局地代表性、遥感像元与CMAQ格网分别建算子，再与时间窗口积分组合。先比较最近网格匹配与显式支持匹配的观测损失和参数变化；将代表性误差纳入权重或协方差，避免把一个站点插值成许多高权重标签。

## 速读区
1. [多输出对流模块嵌回Fortran：共同约束与扩大替代边界的代价](/202611/16/codex-1287744db43a-using-machine-learning-to-parameterize-moist-convection-potential-for-model) — 为你的Transformer建立原位CPU的小型MLP和多输出RF对照，统一计算标准化、数组重排及调用开销；仅在公共输入计算或共同预算明确时扩边界。通量和浓度更新之间保留可核查的代数质量收支，按物种和湿润/干燥、昼夜等条件检查最差误差，再看完整CMAQ连续积分。
2. [保留PDE求解器，通过稀疏间接观测学习模块内的神经关系](/202611/16/codex-85f4216aca2b-physics-constrained-learning-for-data-driven-inverse-modeling-from-sparse-o) — 先做一个含浓度收支和沉降模块的可微柱模型：保留分钟级物理推进，网络只修正少量过程关系；按真实窗口计算累计沉降，并经空间支持算子组成损失。将这一观测算子的导数连到宿主再更新权重，用有限差分检查梯度。先检验小模型能否恢复预设关系，再评估完整CMAQ的离散伴随或其他梯度实现成本。

## 检索记录
北京时间2026-11-16执行；独立发布副本已安全同步，今天台账未发布，核查近7天覆盖及历史身份。检索不设年份窗口，查了Fortran原位模块替代、多输出随机森林的物理约束、辐射代理计时、保留PDE求解器的稀疏观测神经反演、可微水文方法和站点/网格空间融合。没有为了覆盖五个主题或近期年份凑数：昨天偏实际湿沉降观测，今天补模块边界与空间支持方法。入选依据分别是实际嵌回及扩大边界试验、隐式求解梯度与稀疏观测算例、明确空间积分算子和留站检验；并非单凭期刊名或引用量。O’Gorman论文按出版社First published记2018-10-03，PDF另列正式在线版本2018-10-27，arXiv首发2018-06-28；同文身份已合并。PCL期刊卷期日期为2022-03-15（JCP 453, 110938），首次在线日未核实，不能将该卷期日宣称首发；算例阅读使用2020-02-24的作者arXiv v1，与期刊摘要交叉核对，未逐项核实最终版改动。Fuentes按出版社首发2005-02-28记录，昨天只检索未推荐，今天完成开放作者版全文阅读后入选。Fuentes标精读/full_text；其余两篇核查摘要及相关正文但未完成全部补充材料，保守标速读/abstract。ScienceDirect全文入口及部分AGU入口返回403；使用合法作者/机构开放稿与可达出版社摘要，没有绕过检测，也没有把访问失败说成无文献。未运行旧工作流或调用原DeepSeek、embedding、rerank、summary API。本文献组合尚不提供仅凭月年观测训练全部网络权重、或CMAQ CPU整模型必然加速的证据。

- [检索来源 1](https://agupubs.onlinelibrary.wiley.com/doi/abs/10.1029/2018ms001351)
- [检索来源 2](https://pog.mit.edu/src/ogorman_convection_machine_learning_2018.pdf)
- [检索来源 3](https://arxiv.org/abs/1806.11037)
- [检索来源 4](https://arxiv.org/abs/2002.10521)
- [检索来源 5](https://arxiv.org/pdf/2002.10521)
- [检索来源 6](https://sites.stat.washington.edu/raftery/Research/PDF/fuentes2005.pdf)
- [检索来源 7](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.0006-341X.2005.030821.x)
