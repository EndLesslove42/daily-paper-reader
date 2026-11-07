# 日报 · 2026-11-07

- 生成时间：2026-11-07T09:51:49+08:00
- 当次推荐总数：3
- 精读区：2
- 速读区：1

## 今日简报
今天选读3篇经典与方法应用：臭氧干沉降综述帮助厘清通量观测究竟测到什么；dPL奠基工作解释如何跨站共享参数映射；FATES光合作用研究展示真实、非连续观测如何训练内部参数。后两篇属于同一方法路线的框架和应用，不是两项独立交叉验证。重点从“有稀疏数据”推进到“监督对象是否匹配、共享约束是否可信、未知站点是否真的泛化”。

## 精读区
1. [从逐站校准到共享参数学习：让稀疏站点借用跨区域信息](/202611/07/codex-8d0273237823-from-calibration-to-parameter-learning-harnessing-the-scaling-effects-of-bi) — 可以让共享的小网络从地表/气象特征预测有限校正参数，在多个站点的真实观测窗口上联合训练；无观测网格用同一映射。对能使用历史观测的站点与完全无观测网格，应分别规定网络输入。
2. [真实非连续观测如何学习内部参数？FATES光合作用模块的实例](/202611/07/codex-503fd41df41d-a-differentiable-physics-informed-ecosystem-modeling-and-learning-framework) — 可借鉴“已知参数合成恢复→真实稀疏观测训练→独立过程验证”的实验顺序。先检查哪些共享Vd校正参数在理想观测下可恢复，再增加缺测、窗口累计、噪声和宿主偏差，评估可辨识性如何退化。

## 速读区
1. [干沉降观测究竟约束什么？从臭氧测量与过程综述建立边界](/202611/07/codex-a6000c3ce840-dry-deposition-of-ozone-over-land-processes-measurement-and-modeling) — 建立观测元数据表，记录通量或累计量、窗口、参考浓度高度、单位、足迹与处理方法。先定义从CMAQ输出到观测的映射，再构造损失，避免只用最近网格和同名变量硬配。

## 检索记录
不设发表年份窗口，检索干沉降观测解释、跨站参数学习及可微生态模块反演。核查Reviews of Geophysics原始摘要与测量章节，Nature Communications原始论文的PMC全文，以及Biogeosciences原始正文。Nature直接页面重定向失败，改用公开PMC版本；JGR光合作用后续候选未取得足够内容，本期未选。综述按速读归档，其余两篇按正文阅读归档，未复现代码。明确区分：塔上湍流通量与地表沉降、叶片非连续快照与月年累计量、日径流监督与极稀疏长期监督、校准耗时与CMAQ部署提速。日期使用期刊首次在线日期，预印本身份用于去重。

- [检索来源 1](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2019RG000670)
- [检索来源 2](https://www.nature.com/articles/s41467-021-26107-z)
- [检索来源 3](https://pmc.ncbi.nlm.nih.gov/articles/PMC8514470/)
- [检索来源 4](https://arxiv.org/abs/2007.15751)
- [检索来源 5](https://bg.copernicus.org/articles/20/2671/2023/)
