# 日报 · 2026-11-09

- 生成时间：2026-11-09T10:16:51+08:00
- 当次推荐总数：3
- 精读区：2
- 速读区：1

## 今日简报
今天选读3篇：先看真正嵌回GEOS-Chem、在CPU上获得模块提速的化学代理案例；再看保留少量可调物理输入、利用长期统计校准神经参数化的方法；最后用剖面似然判断稀疏观测究竟约束了什么。重点区分模块速度与整模式速度、改善统计量与恢复真实参数。今天的组合可形成一条实验线：确定模块接口和计时范围→保留低维可调参数→按真实观测窗口校准→检验可辨识性。

## 精读区
1. [嵌回GEOS-Chem后化学积分提速5倍：CPU接口、分裂耦合与区域偏差](/202611/09/codex-cf48cbf4a166-an-online-learned-neural-network-chemical-solver-for-stable-long-term-globa) — 对你的Vd代理最直接的用处是先测清接口账：分别计时原沉降调用、纯CPU推理、数组整理/语言接口及整段CMAQ。再比较Vd-only与共享输入的多通道交换代理，确保输入在每个宿主步骤重新同步。CPU小MLP/残差网络加批量调用可作为Transformer的对照；是否更快由同一硬件、编译优化和误差容许范围下的实测决定。
2. [给神经参数化保留少量可调物理输入，用长期统计而非逐步标签校准](/202611/09/codex-c252edb94221-how-to-calibrate-a-dynamical-system-with-neural-network-based-physics) — 可先冻结已能逼近CMAQ的网络，保留少数有物理意义的阻力修正或通道系数作为条件输入；用真实站点和窗口算子生成模拟月累计/平均观测，在宿主外层做低维校准。先检查现有网络是否能表示这些参数变化；若训练只覆盖固定参数，需补采样训练，不能任意附加新输入。低维目标可试高斯过程辅助搜索，减少整段CMAQ调用。

## 速读区
1. [拟合月年累计量之后，哪些过程参数仍不可辨识？剖面似然提供的诊断](/202611/09/codex-4e123a7bdfeb-structural-and-practical-identifiability-analysis-of-partially-observed-dyn) — 先用少数通道系数做合成反演：保持真实稀疏站点和月年窗口，构造累计沉降损失；固定一个系数时允许其他系数及选定的排放扰动重新优化。收集同样拟合累计量的参数组，比较其日夜Vd、干湿分配和未观测站点预测。若分歧大，再比较增加浓度观测、短期通量观测或新增站点能否收紧可行范围。

## 检索记录
未设年份窗口。检索过程代理的CPU嵌回、在线训练/长期统计校准、部分观测动力系统可辨识性；核对近7天及历史条目，未重复推荐。Kelp与Balogh两篇已读出版社主文，代码归档页面已核查，未执行或复现代码；Raue的出版社入口发生重定向错误，作者机构及大学库PDF超时，故仅据出版社索引返回的摘要、方法与部分案例文字作保守速读，不标全文精读。EarthArXiv页面返回人机检测，未尝试绕过；同文关系据出版社/预印本检索记录核对。未把访问失败写成没有文献。Balogh日期采用期刊接受稿在线首发2022-04-11，正式版在线2022-04-14；Kelp采用期刊页面首发2022-05-19，未用代码归档或预印本日期替代。入选依据是明确模块边界、在线实验、公开实现与可检验方法；不因主题贴近而接受夸大加速或参数恢复结论。

- [检索来源 1](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2021MS002926)
- [检索来源 2](https://zenodo.org/records/5736524)
- [检索来源 3](https://eartharxiv.org/repository/view/2886/)
- [检索来源 4](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2022GL097872)
- [检索来源 5](https://agupubs.onlinelibrary.wiley.com/doi/abs/10.1029/2022GL097872)
- [检索来源 6](https://zenodo.org/records/6141165)
- [检索来源 7](https://academic.oup.com/bioinformatics/article/25/15/1923/213246)
- [检索来源 8](https://www.jeti.uni-freiburg.de/papers/Raue_Bioinformatics_printed_1923.pdf)
- [检索来源 9](https://opus.bibliothek.uni-augsburg.de/opus4/frontdoor/deliver/index/docId/113236/file/113236.pdf)
