---
title: "Technical note: AQMEII4 Activity 1: evaluation of wet and dry deposition schemes as an integral part of regional-scale air quality models"
title_zh: "AQMEII4：把干湿沉降放回空气质量宿主，建立可比较的过程诊断"
authors: "Stefano Galmarini, Paul Makar, Olivia E. Clifton, Christian Hogrefe, Jesse O. Bash, Roberto Bellasio, Roberto Bianconi, Johannes Bieser, Tim Butler, Jason Ducker, Johannes Flemming, Alma Hodzic, Christopher D. Holmes, Ioannis Kioutsioukis, Richard Kranenburg, Aurelia Lupascu, Juan Luis Perez-Camanyo, Jonathan Pleim, Young-Hee Ryu, Roberto San Jose, Donna Schwede, Sam Silva, Ralf Wolke"
date: "2021-10-20"
tags: ["paper:速读区", "query:surface-exchange", "query:source-sink-coupling", "query:deposition-constraints"]
score: 9.4
evidence: "迁移建议：在原模型与替代模块中同步保留参考浓度、实际沉降通量、Vd及可获得的过程诊断，先按真实采样窗聚合通量，再对比观测，避免用月均浓度乘月均Vd冒充累计量。湿沉降联合检查同窗降水及雨水化学；另做其他模块扰动对照，区分固定宿主条件下的改进与对干扰误差的稳健性。"
tldr: "提出区域空气质量模型内干湿沉降评估协议。重点是比较不同阻力结构和地表类型下的过程，而非只比较最终浓度；这是一篇技术协议，不是已完成的神经校准效果论文。"
source: "Atmospheric Chemistry and Physics"
selection_source: "codex-subscription"
summary_format: "problem-oriented"
method: "对干沉降输出地表类型分组诊断、路径有效导度及有效通量；有效导度之和对应Vd。路径通量须先按小时计算再聚合；湿沉降同时核查降水与沉降输出。"
result: "示例显示，白天某路径对Vd贡献大，并不保证其对累计沉降质量贡献大，因为浓度随时间变化。协议把这些不同诊断统一到可比较的接口。"
conclusion: "阅读范围：摘要、2.3节、4.1节相关正文及式(3)—(6)说明，未通读全文。共同输入与标准诊断用于减少比较差异，并不保证排放、边界、气象或地表输入本身正确。"
critical_assessment: "阅读者推断：即使按协议将各路径贡献加总得到正确Vd，只有总量观测时仍可能存在多种路径分配；这是总量到分量的识别风险，不是协议失败。可用独立通量与地表状态分组检验，并对路径控制参数做扰动，观察哪些变化能被观测区分。若不能区分，应报告可约束的总量或组合，不把模型内部路径诊断当独立机制证据。"
differences: "协议提供诊断设计，没有给出异质稀疏数据的联合似然、神经权重优化或模块归因保证。路径定义必须跟随实际阻力框架，气体路径不能直接套到颗粒物。当前单向交换可以先使用兼容部分；本文另列的NH3双向诊断不是当前工作的启动条件。"
---

[原文](https://acp.copernicus.org/articles/21/15663/2021/) · 非近期文献（按研究价值选入） · 仅核对摘要

## 本文研究了什么？
提出区域空气质量模型内干湿沉降评估协议。重点是比较不同阻力结构和地表类型下的过程，而非只比较最终浓度；这是一篇技术协议，不是已完成的神经校准效果论文。

对干沉降输出地表类型分组诊断、路径有效导度及有效通量；有效导度之和对应Vd。路径通量须先按小时计算再聚合；湿沉降同时核查降水与沉降输出。

示例显示，白天某路径对Vd贡献大，并不保证其对累计沉降质量贡献大，因为浓度随时间变化。协议把这些不同诊断统一到可比较的接口。

## 有哪些局限或隐含问题？
阅读范围：摘要、2.3节、4.1节相关正文及式(3)—(6)说明，未通读全文。共同输入与标准诊断用于减少比较差异，并不保证排放、边界、气象或地表输入本身正确。

**隐含问题分析（阅读者推断）**

阅读者推断：即使按协议将各路径贡献加总得到正确Vd，只有总量观测时仍可能存在多种路径分配；这是总量到分量的识别风险，不是协议失败。可用独立通量与地表状态分组检验，并对路径控制参数做扰动，观察哪些变化能被观测区分。若不能区分，应报告可约束的总量或组合，不把模型内部路径诊断当独立机制证据。

## 对我的研究有什么用，哪里不同？
迁移建议：在原模型与替代模块中同步保留参考浓度、实际沉降通量、Vd及可获得的过程诊断，先按真实采样窗聚合通量，再对比观测，避免用月均浓度乘月均Vd冒充累计量。湿沉降联合检查同窗降水及雨水化学；另做其他模块扰动对照，区分固定宿主条件下的改进与对干扰误差的稳健性。

**差异与迁移前提**

协议提供诊断设计，没有给出异质稀疏数据的联合似然、神经权重优化或模块归因保证。路径定义必须跟随实际阻力框架，气体路径不能直接套到颗粒物。当前单向交换可以先使用兼容部分；本文另列的NH3双向诊断不是当前工作的启动条件。
