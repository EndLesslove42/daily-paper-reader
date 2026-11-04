---
title: "Exploring Pathways to More Accurate Machine Learning Emulation of Atmospheric Radiative Transfer"
title_zh: "模块替代边界怎么选：辐射子过程代理的精度与实际速度比较（定向方法补充）"
authors: "Peter Ukkonen"
date: "2022-03-06"
tags: ["paper:精读区", "query:deposition-surrogates", "query:source-sink-coupling"]
score: 9.8
evidence: "阅读判断：为Vd-only、完整地表交换参数化等候选边界分别统计原始耗时、输入输出规模、调用次数和闭环误差。优先选择能消除重复过程计算、支持网格块与共享通道批量输出的边界；小网络本身不保证提速。"
tldr: "在同一辐射代码内比较不同替代边界，包括只替换气体光学、只替换反射透射计算及整个辐射参数化。这里重点借鉴前两种子模块实验，并非替代整套天气或化学传输模型。"
source: "Journal of Advances in Modeling Earth Systems"
selection_source: "codex-subscription"
method: "前馈网络在Fortran中批量推理，使用BLAS矩阵乘法并计入预后处理；CPU测试采用单核、单精度和经过优化的物理基线。"
result: "气体光学自身约快3倍，但整个短波辐射计算仅减少约25%用时；反射透射代理只有280个参数，却慢40%–45%。"
conclusion: "核查正文的方法、边界比较与计时结果，未复现代码。上述倍率是特定辐射计算实验，不是CMAQ整体加速；不能据此直接扩大到浓度更新或承诺Vd替代收益。"
motivation: "判断可学习的子过程是否也是值得替代的计算边界，不能仅看拟合精度和参数量。"
---

[原文](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2021MS002875) · 方法补充（非今日新发表） · 已核查论文正文关键章节

## 研究内容
在同一辐射代码内比较不同替代边界，包括只替换气体光学、只替换反射透射计算及整个辐射参数化。这里重点借鉴前两种子模块实验，并非替代整套天气或化学传输模型。

## 方法与结果
前馈网络在Fortran中批量推理，使用BLAS矩阵乘法并计入预后处理；CPU测试采用单核、单精度和经过优化的物理基线。

气体光学自身约快3倍，但整个短波辐射计算仅减少约25%用时；反射透射代理只有280个参数，却慢40%–45%。

## 与当前实验的联系（阅读判断）
阅读判断：为Vd-only、完整地表交换参数化等候选边界分别统计原始耗时、输入输出规模、调用次数和闭环误差。优先选择能消除重复过程计算、支持网格块与共享通道批量输出的边界；小网络本身不保证提速。

## 局限与待验证问题
核查正文的方法、边界比较与计时结果，未复现代码。上述倍率是特定辐射计算实验，不是CMAQ整体加速；不能据此直接扩大到浓度更新或承诺Vd替代收益。
