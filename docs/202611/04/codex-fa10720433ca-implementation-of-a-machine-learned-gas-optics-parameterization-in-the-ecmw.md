---
title: "Implementation of a machine-learned gas optics parameterization in the ECMWF Integrated Forecasting System: RRTMGP-NN 2.0"
title_zh: "CPU模块代理如何嵌回ECMWF：RRTMGP-NN的Fortran批量推理与长期在线验证（定向方法补充）"
authors: "Peter Ukkonen, Robin J. Hogan"
date: "2023-06-09"
tags: ["paper:精读区", "query:deposition-surrogates", "query:source-sink-coupling"]
score: 9.8
evidence: "阅读判断：优先试CPU小型前馈网络或蒸馏学生，按本地网格块批量输出共享Vd通道；把数据布局与物理接口一起设计，再测完整CMAQ耗时。学习的是可移植的部署方法，不照搬辐射网络结构。"
tldr: "仅替换气体光学参数化，保留辐射传输方程，并接入ecRad和ECMWF IFS；这是物理系数模块替代，与保留浓度更新、只学习Vd的思路相近。"
source: "Geoscientific Model Development"
selection_source: "codex-subscription"
method: "Fortran前馈网络用BLAS批量矩阵乘法，同时预测多谱点，减少重复小循环；各配置开展四组13个月海气耦合模拟，去掉首月后评价全年结果。"
result: "ECMWF的AMD平台离线计时显示气体光学近3倍、ecRad约1.5倍加速；在线年度气候与物理基线接近。1.5倍不是IFS整模型的实测加速。"
conclusion: "核查原始正文的接口、批量实现、效率和在线验证，未复现代码。与前篇同属一条研究路线，非独立交叉验证；过程与数据依赖不同，倍率不可直接迁移到Vd。IFS中的辐射占比本就较小，局部收益仍受整体上限约束。"
motivation: "在保留物理求解器的前提下，把准确的系数代理做成能嵌入宿主模型的高效模块。"
---

[原文](https://gmd.copernicus.org/articles/16/3241/2023/) · 方法补充（非今日新发表） · 已核查论文正文关键章节

## 研究内容
仅替换气体光学参数化，保留辐射传输方程，并接入ecRad和ECMWF IFS；这是物理系数模块替代，与保留浓度更新、只学习Vd的思路相近。

## 方法与结果
Fortran前馈网络用BLAS批量矩阵乘法，同时预测多谱点，减少重复小循环；各配置开展四组13个月海气耦合模拟，去掉首月后评价全年结果。

ECMWF的AMD平台离线计时显示气体光学近3倍、ecRad约1.5倍加速；在线年度气候与物理基线接近。1.5倍不是IFS整模型的实测加速。

## 与当前实验的联系（阅读判断）
阅读判断：优先试CPU小型前馈网络或蒸馏学生，按本地网格块批量输出共享Vd通道；把数据布局与物理接口一起设计，再测完整CMAQ耗时。学习的是可移植的部署方法，不照搬辐射网络结构。

## 局限与待验证问题
核查原始正文的接口、批量实现、效率和在线验证，未复现代码。与前篇同属一条研究路线，非独立交叉验证；过程与数据依赖不同，倍率不可直接迁移到Vd。IFS中的辐射占比本就较小，局部收益仍受整体上限约束。
