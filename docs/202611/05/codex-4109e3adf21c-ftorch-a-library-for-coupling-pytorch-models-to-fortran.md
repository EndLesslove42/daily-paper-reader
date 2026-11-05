---
title: "FTorch: a library for coupling PyTorch models to Fortran"
title_zh: "FTorch：把PyTorch模型原位接入Fortran的工程参考"
authors: "Jack Atkinson, Athena Elafrou, Elliott Kasoar, Joseph G. Wallwork, Thomas Meltzer, Simon Clifford, Dominic Orchard, Chris Edsall"
date: "2025-03-05"
tags: ["paper:精读区", "query:deposition-surrogates", "query:source-sink-coupling"]
score: 9.0
evidence: "阅读判断：可作CPU部署基线，比较原有接口与直接调用的完整成本。模型常驻、缓冲区复用及本地网格块批量调用仍需具体实现，不能只换接口便假定提速。"
tldr: "FTorch通过LibTorch连接Fortran与PyTorch，运行时不依赖Python，支持CPU和GPU。"
source: "Journal of Open Source Software（软件论文）"
selection_source: "codex-subscription"
method: "以iso_c_binding封装C++接口并加载TorchScript模型，条件允许时共享内存中的数组数据。"
result: "提供可检查的接口、示例和软件评审记录，但本文没有给出完整CMAQ模拟的加速倍率。"
conclusion: "已阅读原始软件论文，未编译复现。共享内存不等于CPU与独立显存免传输，也不能消除Transformer本身的运算成本；软件评审不替代目标CMAQ工况的性能验证。"
pdf: "https://www.theoj.org/joss-papers/joss.07602/10.21105.joss.07602.pdf"
motivation: "减少Fortran宿主调用代理时的跨语言运行时与数据复制负担。"
---

[原文](https://joss.theoj.org/papers/10.21105/joss.07602) · 非近期文献（按研究价值选入） · 已阅读全文

## 研究内容
FTorch通过LibTorch连接Fortran与PyTorch，运行时不依赖Python，支持CPU和GPU。

## 方法与结果
以iso_c_binding封装C++接口并加载TorchScript模型，条件允许时共享内存中的数组数据。

提供可检查的接口、示例和软件评审记录，但本文没有给出完整CMAQ模拟的加速倍率。

## 与当前实验的联系（阅读判断）
阅读判断：可作CPU部署基线，比较原有接口与直接调用的完整成本。模型常驻、缓冲区复用及本地网格块批量调用仍需具体实现，不能只换接口便假定提速。

## 局限与待验证问题
已阅读原始软件论文，未编译复现。共享内存不等于CPU与独立显存免传输，也不能消除Transformer本身的运算成本；软件评审不替代目标CMAQ工况的性能验证。
