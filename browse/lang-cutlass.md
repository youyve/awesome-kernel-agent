# Kernel language: CUTLASS

[← README](../README.md) · 13 entries, newest first

## 2026

- **RESOLVE: Language-Agnostic Validation of GPU Kernels Through Testing, Reduction, and Proof** [![arXiv](https://img.shields.io/badge/arXiv-26.10-red)](https://arxiv.org/abs/2610.05683)
  - **Institution:** UC Riverside, Math Inc., Microsoft Research
  - **Type:** Empirical study · **Kernel:** `CUTLASS` `Triton` `Gluon` · **Hardware:** NVIDIA
- **KernelArc: A Multi-Agent Framework for GPU Kernel Optimization** [![arXiv](https://img.shields.io/badge/arXiv-26.08-red)](https://arxiv.org/abs/2608.17071)
  - **Institution:** AI Labs, imec
  - **Type:** Search & evolution · **Kernel:** `CUDA` `PTX` `Triton` `CUTLASS` · **Hardware:** NVIDIA · **Benchmark:** SOL-ExecBench
- **Harness Engineering for LLM-Driven GPU Kernel Generation** [![arXiv](https://img.shields.io/badge/arXiv-26.07-red)](https://arxiv.org/abs/2607.17979) [![Stars](https://img.shields.io/github/stars/syhya/mlsys26-flashinfer-contest)](https://github.com/syhya/mlsys26-flashinfer-contest)
  - **Institution:** Baidu
  - **Type:** Agentic workflow · **Kernel:** `CUDA` `Triton` `CUTLASS` · **Hardware:** NVIDIA · **Benchmark:** FlashInfer-Bench
- **KernelPro: Optimizing CUDA like a Human: Micro-Profiling Tools as Expert Surrogates for LLM-Based GPU Kernel Optimization** [![arXiv](https://img.shields.io/badge/arXiv-26.06-red)](https://arxiv.org/abs/2606.26453) [![Artifacts](https://img.shields.io/badge/Artifacts-arXiv-lightgrey)](https://arxiv.org/abs/2606.26453)
  - **Institution:** AWS, Siemens, University of Minnesota
  - **Type:** Search & evolution · **Kernel:** `CUDA` `CUTLASS` `CuTe` · **Hardware:** NVIDIA · **Benchmark:** KernelBench
- **Atrex Kernel Agent (AKA): Are LLM-Generated GPU Kernels Production-Ready? A Trace-Driven Benchmark and Optimization Agent** [![arXiv](https://img.shields.io/badge/arXiv-26.07-red)](https://arxiv.org/abs/2607.14541) [![Stars](https://img.shields.io/github/stars/alibaba/atrex-kernel-agent)](https://github.com/alibaba/atrex-kernel-agent) [![Release notes](https://img.shields.io/badge/Release-Notes-blue)](https://github.com/alibaba/atrex-kernel-agent/releases/tag/v0.3.0)
  - **Institution:** ATREX Team, Alibaba Group
  - **Type:** Agentic workflow · **Kernel:** `FlyDSL` `Triton` `CUDA` `Gluon` `CUTLASS` `CuTe` `TileLang` · **Hardware:** NVIDIA, AMD, T-Head PPU
- **KDA-Pilot** [![Stars](https://img.shields.io/github/stars/BBuf/KDA-Pilot)](https://github.com/BBuf/KDA-Pilot)
  - *Evidence-first autonomous SGLang kernel-optimization campaigns with production baselines, strict correctness gates, NCU/KernelWiki evidence, and replayable logs.*
  - **Institution:** RadixArk
  - **Type:** Open-source / industry system · **Kernel:** `Triton` `CUDA` `CUTLASS` · **Hardware:** NVIDIA
- **Houmao Agentic Kernel Optimization: Agentic Kernel Optimization: Generating State-of-the-Art GPU Kernels Without Hand-Written CUDA** [![arXiv](https://img.shields.io/badge/arXiv-26.08-red)](https://arxiv.org/abs/2608.14560) [![Stars](https://img.shields.io/github/stars/igamenovoer/houmao)](https://github.com/igamenovoer/houmao) [![Artifacts](https://img.shields.io/badge/Artifacts-GitHub-lightgrey)](https://github.com/CodeGandee/flashinfer-bench-starter-kit/tree/main/solution/cuda)
  - **Institution:** Intellifusion
  - **Type:** Agentic workflow · **Kernel:** `CUDA` `CUTLASS` · **Hardware:** NVIDIA · **Benchmark:** FlashInfer-Bench
- **AKO4X: AKO: Agentic Kernel Optimization** [![Stars](https://img.shields.io/github/stars/TongmingLAIC/AKO4X)](https://github.com/TongmingLAIC/AKO4X)
  - **Institution:** TLAIC
  - **Type:** Open-source / industry system · **Kernel:** `Triton` `CUDA` `TileLang` `CUTLASS` `CuTe` · **Hardware:** NVIDIA · **Benchmark:** FlashInfer-Bench
- **FACT: Compositional Kernel Synthesis with a Three-Stage Agentic Workflow** [![arXiv](https://img.shields.io/badge/arXiv-26.04-red)](https://arxiv.org/abs/2604.26666)
  - **Institution:** Virginia Tech
  - **Type:** Agentic workflow · **Kernel:** `CUTLASS` · **Hardware:** NVIDIA · **Benchmark:** KernelBench
- **Cursor Multi-Agent Kernel Optimization** [![Blog](https://img.shields.io/badge/Blog-Cursor-blue)](https://cursor.com/blog/multi-agent-kernels) [![Artifacts](https://img.shields.io/badge/Artifacts-GitHub-lightgrey)](https://github.com/anysphere/kernel-optimization-results)
  - *Planner + autonomous parallel workers optimized 235 kernels from 124+ open-source models (CUDA C w/ inline PTX and CuTe DSL) on 27x Blackwell B200 over 3 weeks using NVIDIA's SOL-ExecBench test-debug-.*
  - **Institution:** Cursor, NVIDIA
  - **Type:** Open-source / industry system · **Kernel:** `CUDA` `CUTLASS` `CuTe` `PTX` · **Hardware:** NVIDIA · **Benchmark:** SOL-ExecBench
- **muCUTLASS + Speed-of-Light Guidance: Improving Efficiency of GPU Kernel Optimization Agents using a Domain-Specific Language and Speed-of-Light Guidance** [![arXiv](https://img.shields.io/badge/arXiv-26.03-red)](https://arxiv.org/abs/2603.29010)
  - **Institution:** NVIDIA, Stanford University
  - **Type:** Agentic workflow · **Kernel:** `CUTLASS` · **Hardware:** NVIDIA · **Benchmark:** KernelBench

## 2025

- **KernelEvolve: Scaling Agentic Kernel Coding for Heterogeneous AI Accelerators at Meta** [![ISCA 2026](https://img.shields.io/badge/ISCA-26-green)](https://arxiv.org/abs/2512.23236) [![Blog](https://img.shields.io/badge/Blog-Meta-blue)](https://engineering.fb.com/2026/04/02/developer-tools/kernelevolve-how-metas-ranking-engineer-agent-optimizes-ai-infrastructure)
  - **Institution:** Meta
  - **Type:** Trained model · **Kernel:** `CUDA` `Triton` `TileLang` `CUTLASS` `HIP` · **Hardware:** NVIDIA, Meta MTIA · **Benchmark:** KernelBench
- **KForge: A Multi-Agent System for Cross-Platform Kernel Synthesis** [![ICML Workshop 2026](https://img.shields.io/badge/ICML_Workshop-26-green)](https://arxiv.org/abs/2606.02963)
  - **Institution:** Gimlet Labs
  - **Type:** Agentic workflow · **Kernel:** `Triton` `CUDA` `CUTLASS` `HIP` `SYCL` `Metal` · **Hardware:** NVIDIA, AMD, Intel, Apple · **Benchmark:** KernelBench
