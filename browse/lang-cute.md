# Kernel language: CuTe

[← README](../README.md) · 11 entries, newest first

## 2026

- **CompoundingKernel: Self-Improving from Zero to First** [![arXiv](https://img.shields.io/badge/arXiv-26.11-red)](https://arxiv.org/abs/2611.19230) [![Artifacts](https://img.shields.io/badge/Artifacts-HuggingFace-lightgrey)](https://huggingface.co/spaces/QianQu/CompoundingKernel-Explorer)
  - **Institution:** Amazon
  - **Type:** Search & evolution · **Kernel:** `CUDA` `CuTe` `Triton` · **Hardware:** NVIDIA · **Benchmark:** SOL-ExecBench
- **Warpline: Binary-Level Tracing and Unified Evidence for Agentic GPU Kernel Optimization** [![arXiv](https://img.shields.io/badge/arXiv-26.11-red)](https://arxiv.org/abs/2611.04331)
  - **Institution:** George Mason University, NVIDIA
  - **Type:** Tool · **Kernel:** `Triton` `CuTe` `CUDA` `PTX` · **Hardware:** NVIDIA · **Benchmark:** SOL-ExecBench
- **JustGoal: With Only a Goal, the AI Baseline Is Above the Expert Kernels** [![arXiv](https://img.shields.io/badge/arXiv-26.10-red)](https://arxiv.org/abs/2610.36434) [![Stars](https://img.shields.io/github/stars/OpenBMB/JustGoal)](https://github.com/OpenBMB/JustGoal)
  - **Institution:** Tsinghua University, ModelBest, Harbin Institute of Technology, University of Chinese Academy of Sciences
  - **Type:** Empirical study · **Kernel:** `Triton` `CUDA` `CuTe` · **Hardware:** NVIDIA · **Benchmark:** FlashInfer-Bench
- **Evolving Agent Teams** [![NeurIPS 2026](https://img.shields.io/badge/NeurIPS-26-green)](https://arxiv.org/abs/2610.36848) [![Stars](https://img.shields.io/github/stars/caoshiyi/EAT)](https://github.com/caoshiyi/EAT) [![Artifacts](https://img.shields.io/badge/Artifacts-GitHub-lightgrey)](https://github.com/caoshiyi/eat-kernels)
  - **Institution:** UC Berkeley
  - **Type:** General-purpose system · **Kernel:** `CUDA` `CuTe` `HIP` · **Hardware:** NVIDIA, AMD, Apple · **Benchmark:** FlashInfer-Bench
- **MetaKernelBench: Measuring GPU Kernel Knowledge Transfer Beyond Code** [![arXiv](https://img.shields.io/badge/arXiv-26.10-red)](https://arxiv.org/abs/2610.05014) [![Stars](https://img.shields.io/github/stars/YIGE24/MetaKernelBench)](https://github.com/YIGE24/MetaKernelBench) [![Project](https://img.shields.io/badge/Project-Page-blue)](https://yige24.github.io/MetaKernelBench)
  - **Institution:** Westlake University, Shanghai Jiao Tong University, Zhejiang University
  - **Type:** Benchmark · **Kernel:** `CuTe` `TIRx` · **Hardware:** NVIDIA
- **ForgeKernel: Self-Evolving Kernels Catching and Surpassing Experts and Agents** [![arXiv](https://img.shields.io/badge/arXiv-26.11-red)](https://arxiv.org/abs/2611.04998) [![Stars](https://img.shields.io/github/stars/OpenBMB/ForgeKernel)](https://github.com/OpenBMB/ForgeKernel)
  - **Institution:** Tsinghua University, ModelBest, University of Chinese Academy of Sciences, Harbin Institute of Technology
  - **Type:** Agentic workflow · **Kernel:** `CUDA` `CuTe` · **Hardware:** NVIDIA, Ascend · **Benchmark:** CANN-Bench, SOL-ExecBench, FlashInfer-Bench
- **KernelPro: Optimizing CUDA like a Human: Micro-Profiling Tools as Expert Surrogates for LLM-Based GPU Kernel Optimization** [![arXiv](https://img.shields.io/badge/arXiv-26.06-red)](https://arxiv.org/abs/2606.26453) [![Artifacts](https://img.shields.io/badge/Artifacts-arXiv-lightgrey)](https://arxiv.org/abs/2606.26453)
  - **Institution:** AWS, Siemens, University of Minnesota
  - **Type:** Search & evolution · **Kernel:** `CUDA` `CUTLASS` `CuTe` · **Hardware:** NVIDIA · **Benchmark:** KernelBench
- **Atrex Kernel Agent (AKA): Are LLM-Generated GPU Kernels Production-Ready? A Trace-Driven Benchmark and Optimization Agent** [![arXiv](https://img.shields.io/badge/arXiv-26.07-red)](https://arxiv.org/abs/2607.14541) [![Stars](https://img.shields.io/github/stars/alibaba/atrex-kernel-agent)](https://github.com/alibaba/atrex-kernel-agent) [![Release notes](https://img.shields.io/badge/Release-Notes-blue)](https://github.com/alibaba/atrex-kernel-agent/releases/tag/v0.3.0)
  - **Institution:** ATREX Team, Alibaba Group
  - **Type:** Agentic workflow · **Kernel:** `FlyDSL` `Triton` `CUDA` `Gluon` `CUTLASS` `CuTe` `TileLang` · **Hardware:** NVIDIA, AMD, T-Head PPU
- **AKO4X: AKO: Agentic Kernel Optimization** [![Stars](https://img.shields.io/github/stars/TongmingLAIC/AKO4X)](https://github.com/TongmingLAIC/AKO4X)
  - **Institution:** TLAIC
  - **Type:** Open-source / industry system · **Kernel:** `Triton` `CUDA` `TileLang` `CUTLASS` `CuTe` · **Hardware:** NVIDIA · **Benchmark:** FlashInfer-Bench
- **CuTeGen: An LLM-Based Agentic Framework for Generation and Optimization of High-Performance GPU Kernels using CuTe** [![arXiv](https://img.shields.io/badge/arXiv-26.04-red)](https://arxiv.org/abs/2604.01489) [![Stars](https://img.shields.io/github/stars/taratt/cutegen)](https://github.com/taratt/cutegen)
  - **Institution:** University of Toronto, Standard Kernel
  - **Type:** Agentic workflow · **Kernel:** `CuTe` · **Hardware:** NVIDIA · **Benchmark:** KernelBench
- **Cursor Multi-Agent Kernel Optimization** [![Blog](https://img.shields.io/badge/Blog-Cursor-blue)](https://cursor.com/blog/multi-agent-kernels) [![Artifacts](https://img.shields.io/badge/Artifacts-GitHub-lightgrey)](https://github.com/anysphere/kernel-optimization-results)
  - *Planner + autonomous parallel workers optimized 235 kernels from 124+ open-source models (CUDA C w/ inline PTX and CuTe DSL) on 27x Blackwell B200 over 3 weeks using NVIDIA's SOL-ExecBench test-debug-.*
  - **Institution:** Cursor, NVIDIA
  - **Type:** Open-source / industry system · **Kernel:** `CUDA` `CUTLASS` `CuTe` `PTX` · **Hardware:** NVIDIA · **Benchmark:** SOL-ExecBench
