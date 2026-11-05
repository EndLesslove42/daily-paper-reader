---
title: "Application of random forest regression to the calculation of gas-phase chemistry within the GEOS-Chem chemistry model v10"
title_zh: "GEOS-Chem随机森林化学代理：能拟合但更慢的早期负面案例"
authors: "Christoph A. Keller, Mat J. Evans"
date: "2019-03-29"
tags: ["paper:速读区", "query:deposition-surrogates", "query:source-sink-coupling"]
score: 9.0
evidence: "阅读判断：对比共享通道与按物种分别推理，统计调用次数、MPI进程的模型副本与访存成本。选择轻量架构须测完整模块，不能从单个树或单次预测推断整体速度。"
tldr: "以随机森林替换气相化学积分，保留GEOS-Chem其他过程，并考虑物种寿命和NOx家族关系。"
source: "Geoscientific Model Development"
selection_source: "codex-subscription"
method: "按物种建立森林，以Fortran接回模型；正文4.1节讨论串行评估和内存管理。"
result: "该实现平均约2.6毫秒，原积分器约1.4毫秒，即用时增加约85%；作者定位为尚未充分优化的概念验证。"
conclusion: "速读：核对摘要及正文计时与实现段落，未逐节通读或复现。负面结果仅针对该版实现，不能推出随机森林始终慢，也不是CPU/GPU搬运的受控实验。"
motivation: "即使替代昂贵的化学模块，算法与内存布局也可能使实际速度下降。"
---

[原文](https://gmd.copernicus.org/articles/12/1209/2019/) · 非近期文献（按研究价值选入） · 仅核对摘要

## 研究内容
以随机森林替换气相化学积分，保留GEOS-Chem其他过程，并考虑物种寿命和NOx家族关系。

## 方法与结果
按物种建立森林，以Fortran接回模型；正文4.1节讨论串行评估和内存管理。

该实现平均约2.6毫秒，原积分器约1.4毫秒，即用时增加约85%；作者定位为尚未充分优化的概念验证。

## 与当前实验的联系（阅读判断）
阅读判断：对比共享通道与按物种分别推理，统计调用次数、MPI进程的模型副本与访存成本。选择轻量架构须测完整模块，不能从单个树或单次预测推断整体速度。

## 局限与待验证问题
速读：核对摘要及正文计时与实现段落，未逐节通读或复现。负面结果仅针对该版实现，不能推出随机森林始终慢，也不是CPU/GPU搬运的受控实验。
