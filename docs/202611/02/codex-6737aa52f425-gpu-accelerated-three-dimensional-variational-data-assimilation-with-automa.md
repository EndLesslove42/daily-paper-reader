---
title: "GPU-accelerated three-dimensional variational data assimilation with automatic differentiation for WRF-Chem"
title_zh: "面向WRF-Chem的自动微分与GPU加速三维变分同化"
authors: "Hancheng Ye, Zengliang Zang, Wei You, Yiwen Hu, Ning Liu, Yi Li"
date: "2026-10-28"
tags: ["paper:速读区", "query:deposition-constraints"]
score: 8.0
evidence: "可借鉴观测算子、损失函数和梯度核验的组织方式，作为未来观测约束训练的实现参考。"
tldr: "以PyTorch自动微分实现污染物三维变分同化，支持CPU和GPU。"
source: "Geoscientific Model Development"
selection_source: "codex-subscription"
method: "在理想化试验及20次连续真实同化—预报试验中，与Fortran系统比较。"
result: "作者报告分析精度相近，GPU同化约1.2秒；性能结论依赖具体硬件和比较方式。"
conclusion: "本次仅核对摘要。它优化的是化学初始场，不证明CMAQ全流程可微，也没有直接验证Vd反演。属于方法迁移候选。"
pdf: "https://gmd.copernicus.org/articles/19/10263/2026/gmd-19-10263-2026.pdf"
motivation: "变分同化的梯度构建和计算效率影响系统开发与应用。"
---

[原文](https://gmd.copernicus.org/articles/19/10263/2026/) · 近期文献 · 仅核对摘要

## 研究内容
以PyTorch自动微分实现污染物三维变分同化，支持CPU和GPU。

## 方法与结果
在理想化试验及20次连续真实同化—预报试验中，与Fortran系统比较。

作者报告分析精度相近，GPU同化约1.2秒；性能结论依赖具体硬件和比较方式。

## 与当前实验的联系（阅读判断）
可借鉴观测算子、损失函数和梯度核验的组织方式，作为未来观测约束训练的实现参考。

## 局限与待验证问题
本次仅核对摘要。它优化的是化学初始场，不证明CMAQ全流程可微，也没有直接验证Vd反演。属于方法迁移候选。
