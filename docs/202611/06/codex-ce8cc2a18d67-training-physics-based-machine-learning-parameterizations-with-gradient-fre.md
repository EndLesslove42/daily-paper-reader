---
title: "Training Physics-Based Machine-Learning Parameterizations With Gradient-Free Ensemble Kalman Methods"
title_zh: "不用逐步过程标签：从时间统计量反演嵌入式神经参数化"
authors: "Ignacio Lopez-Gomez, Costa Christopoulos, Haakon Ludvig Langeland Ervik, Oliver R. A. Dunbar, Yair Cohen, Tapio Schneider"
date: "2022-08-10"
tags: ["paper:精读区", "query:deposition-constraints", "query:deposition-surrogates"]
score: 9.5
evidence: "可先固定原有代理骨干，用少量共享通道校正参数试验：每次跑物理宿主，按站点真实采样窗口积分预测沉降量，再以窗口误差反演校正参数；先测有效可辨识维数及前向预算，再考虑放开更多网络权重。"
tldr: "将参数化训练写成逆问题：物理模型运行后，经空间和有限时间平均观测算子与数据比较，再更新闭合参数。"
source: "Journal of Advances in Modeling Earth Systems"
selection_source: "codex-subscription"
summary_format: "problem-oriented"
method: "采用EKI/UKI校准EDMF；包含LES资料和嵌入神经闭合实验。第2节说明观测映射，第4.3—4.4节比较部分观测及混合闭合。"
result: "部分观测仍可提供参数约束，但不同系数的可辨识性不同；混合模型共79个可校准参数。"
conclusion: "正文重点核查，未复现。作者指出UKI的2p+1个sigma点限制大参数模型，EKI集合塌缩也不能直接解释为参数后验不确定性；验证主要基于LES。"
motivation: "用部分状态或统计量训练过程参数化，减轻对逐时变化率标签和宿主梯度的依赖。"
critical_assessment: "阅读判断：有限时间平均能约束统计表现，却未必区分产生相同平均量的高频机制；文中不同系数受约束程度不一支持这一风险。迁移到月年沉降量时，应做多初值/先验敏感性、留窗口检验及独立通量或浓度验证，不能仅凭累计量拟合判定分钟Vd正确。"
differences: "文中学习EDMF湍流/对流闭合，不是Vd；LES场可设计观测映射，真实监测无法任意选变量。CMAQ训练需另处理浓度—Vd耦合、排放/输送误差和月年积分成本，79参数实验不能证明大型Transformer可直接集合反演。"
---

[原文](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2022MS003105) · 非近期文献（按研究价值选入） · 已阅读全文

## 本文研究了什么？
将参数化训练写成逆问题：物理模型运行后，经空间和有限时间平均观测算子与数据比较，再更新闭合参数。

采用EKI/UKI校准EDMF；包含LES资料和嵌入神经闭合实验。第2节说明观测映射，第4.3—4.4节比较部分观测及混合闭合。

部分观测仍可提供参数约束，但不同系数的可辨识性不同；混合模型共79个可校准参数。

## 有哪些局限或隐含问题？
正文重点核查，未复现。作者指出UKI的2p+1个sigma点限制大参数模型，EKI集合塌缩也不能直接解释为参数后验不确定性；验证主要基于LES。

**隐含问题分析（阅读者推断）**

阅读判断：有限时间平均能约束统计表现，却未必区分产生相同平均量的高频机制；文中不同系数受约束程度不一支持这一风险。迁移到月年沉降量时，应做多初值/先验敏感性、留窗口检验及独立通量或浓度验证，不能仅凭累计量拟合判定分钟Vd正确。

## 对我的研究有什么用，哪里不同？
可先固定原有代理骨干，用少量共享通道校正参数试验：每次跑物理宿主，按站点真实采样窗口积分预测沉降量，再以窗口误差反演校正参数；先测有效可辨识维数及前向预算，再考虑放开更多网络权重。

**差异与迁移前提**

文中学习EDMF湍流/对流闭合，不是Vd；LES场可设计观测映射，真实监测无法任意选变量。CMAQ训练需另处理浓度—Vd耦合、排放/输送误差和月年积分成本，79参数实验不能证明大型Transformer可直接集合反演。
