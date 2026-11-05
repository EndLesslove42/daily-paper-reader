---
title: "TESSERA: Temporal Embeddings of Surface Spectra for Earth Representation and Analysis"
title_zh: "TESSERA：离线地表表征与轻量任务头，分离遥感骨干和在线过程计算"
authors: "Zhengpeng Feng, Clement Atzberger, Sadiq Jaffer, Jovana Knezevic, Silja Sormunen, Robin Young, Madeline C. Lisaius, Markus Immitzer, Toby Jackson, James Ball, David A. Coomes, Anil Madhavapeddy, Andrew Blake, Srinivasan Keshav"
date: "2025-06-25"
tags: ["paper:速读区", "query:geospatial-surface", "query:deposition-surrogates"]
score: 8.8
evidence: "阅读判断：将AEF/TESSERA先聚合到CMAQ网格并缓存，与动态气象输入交给小型Vd头；对地表变量、AEF和TESSERA做等容量比较，分别计离线准备与在线推理成本。"
tldr: "从Sentinel-1/2时序生成预计算地表嵌入，用轻量任务头适配下游问题，提供开放代码与年度产品。"
source: "CVPR 2026；日期为首版arXiv预印本，核查v7"
selection_source: "codex-subscription"
method: "双模态时序编码结合采样不变性学习，默认生成年度128维嵌入，并以int8压缩存储。"
result: "论文报告多个分类、分割和回归任务的有效性；预计算产品使使用者无需重复运行遥感骨干。"
conclusion: "速读：核查摘要、表征生成和量化章节，未逐节通读。时序编码不等于月度产品，年度嵌入不能直接提供天气尺度状态；int8存储不代表任务头采用INT8推理，论文未验证Vd或CMAQ加速。"
motivation: "遥感骨干的昂贵计算不一定需要出现在物理模型每个时间步内。"
---

[原文](https://arxiv.org/abs/2506.20380) · 非近期文献（按研究价值选入） · 仅核对摘要

## 研究内容
从Sentinel-1/2时序生成预计算地表嵌入，用轻量任务头适配下游问题，提供开放代码与年度产品。

## 方法与结果
双模态时序编码结合采样不变性学习，默认生成年度128维嵌入，并以int8压缩存储。

论文报告多个分类、分割和回归任务的有效性；预计算产品使使用者无需重复运行遥感骨干。

## 与当前实验的联系（阅读判断）
阅读判断：将AEF/TESSERA先聚合到CMAQ网格并缓存，与动态气象输入交给小型Vd头；对地表变量、AEF和TESSERA做等容量比较，分别计离线准备与在线推理成本。

## 局限与待验证问题
速读：核查摘要、表征生成和量化章节，未逐节通读。时序编码不等于月度产品，年度嵌入不能直接提供天气尺度状态；int8存储不代表任务头采用INT8推理，论文未验证Vd或CMAQ加速。
