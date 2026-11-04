---
title: "Detecting and Validating Ecosystem Temporal Memory in Photosynthetic and Respiratory Carbon Fluxes Using Explainable Deep Learning"
title_zh: "用可解释深度学习检验生态碳通量的时间记忆（方法迁移参考）"
authors: "Teng Ma, Wei He, Shuangxi Fang, Jingfeng Xiao, Ngoc Tu Nguyen, Hua Yang, Peipei Xu, Yi Lin, Yuanyuan Chen, Meihong Fang, Chengcheng Huang, Mengyao Zhao, Xinhui Lei, Ziyi Huang"
date: "2026-10-23"
tags: ["paper:速读区", "query:deposition-surrogates"]
score: 8.0
evidence: "阅读判断：可把时间打乱和月份消融迁移到沉降替代实验，检验月度地表输入是否提供有效信息，而不是只展示注意力或特征重要性。"
tldr: "以LSTM注意力模型预测生态碳通量，并验证其时间归因。"
source: "Journal of Geophysical Research: Biogeosciences"
selection_source: "codex-subscription"
method: "结合输入时间顺序打乱、月份消融与集成归因比较。"
result: "作者发现不同通量和生态类型的时间响应有差异，扰动试验可检验模型对历史输入的依赖。"
conclusion: "仅核对摘要。对象是生态碳交换，并非沉降模块或遥感基础模型；归因与扰动结果也不单独构成物理因果证明，需独立观测和过程检验。"
motivation: "时序网络的归因图未必代表真实过程记忆，需要额外检验。"
---

[原文](https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2026JG010198) · 近期文献 · 仅核对摘要

## 研究内容
以LSTM注意力模型预测生态碳通量，并验证其时间归因。

## 方法与结果
结合输入时间顺序打乱、月份消融与集成归因比较。

作者发现不同通量和生态类型的时间响应有差异，扰动试验可检验模型对历史输入的依赖。

## 与当前实验的联系（阅读判断）
阅读判断：可把时间打乱和月份消融迁移到沉降替代实验，检验月度地表输入是否提供有效信息，而不是只展示注意力或特征重要性。

## 局限与待验证问题
仅核对摘要。对象是生态碳交换，并非沉降模块或遥感基础模型；归因与扰动结果也不单独构成物理因果证明，需独立观测和过程检验。
