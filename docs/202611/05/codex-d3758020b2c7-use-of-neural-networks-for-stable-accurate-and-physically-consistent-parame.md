---
title: "Use of Neural Networks for Stable, Accurate and Physically Consistent Parameterization of Subgrid Atmospheric Processes With Good Performance at Reduced Precision"
title_zh: "物理一致的模块输出与低精度：稳定嵌回大气模型的经典参考"
authors: "Janni Yuval, Paul A. O'Gorman, Chris N. Hill"
date: "2021-02-06"
tags: ["paper:精读区", "query:deposition-surrogates", "query:source-sink-coupling"]
score: 9.3
evidence: "阅读判断：为Vd、交换系数或通量等边界选择提供结构依据，也支持在CPU小模型上逐级验证精度。保留原物理更新不妨碍模块学习，但应同时检查过程收支、非负性及多步误差。"
tldr: "在SAM中学习次网格过程参数化，尽可能预测通量或扩散系数，再由物理关系计算变化率。"
source: "Geophysical Research Letters"
selection_source: "codex-subscription"
method: "分过程构建标签和输出，加入物理一致性与非负约束，开展在线模拟及输入输出精度扰动。"
result: "参数化可稳定运行，网络存储显著小于随机森林；降低输入输出精度后仍可保持相近气候统计。"
conclusion: "已核查正文，未复现。对象是理想化大气次网格过程，不是干沉降。低精度试验主要舍入输入输出，未证明全部权重和乘法已低精度执行，不能作为INT8 CPU提速的实测证据。"
motivation: "离线误差之外，输出边界和守恒结构会影响代理参数化的长期表现。"
---

[原文](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2020GL091363) · 非近期文献（按研究价值选入） · 已阅读全文

## 研究内容
在SAM中学习次网格过程参数化，尽可能预测通量或扩散系数，再由物理关系计算变化率。

## 方法与结果
分过程构建标签和输出，加入物理一致性与非负约束，开展在线模拟及输入输出精度扰动。

参数化可稳定运行，网络存储显著小于随机森林；降低输入输出精度后仍可保持相近气候统计。

## 与当前实验的联系（阅读判断）
阅读判断：为Vd、交换系数或通量等边界选择提供结构依据，也支持在CPU小模型上逐级验证精度。保留原物理更新不妨碍模块学习，但应同时检查过程收支、非负性及多步误差。

## 局限与待验证问题
已核查正文，未复现。对象是理想化大气次网格过程，不是干沉降。低精度试验主要舍入输入输出，未证明全部权重和乘法已低精度执行，不能作为INT8 CPU提速的实测证据。
