# Kernel language: TileLang

[← README](../README.md) · 13 entries, newest first

## 2026

- **What Language Should LLMs Write GPU Kernels In? Disentangling Abstraction Level from Resource Level** [![NeurIPS Workshop 2026](https://img.shields.io/badge/NeurIPS_Workshop-26-green)](https://openreview.net/forum?id=9Ppcp9PK8i)
  - **Institution:** Pusan National University, Electronics and Telecommunications Research Institute
  - **Type:** Empirical study · **Kernel:** `CUDA` `PTX` `Triton` `TileLang` · **Hardware:** NVIDIA · **Benchmark:** KernelBench
- **TileCas: Cascading Kernel Development Across Programming Abstractions** [![arXiv](https://img.shields.io/badge/arXiv-26.10-red)](https://arxiv.org/abs/2610.14740) [![Stars](https://img.shields.io/github/stars/TongmingLAIC/tilecas)](https://github.com/TongmingLAIC/tilecas)
  - **Institution:** Fudan University, University of Texas at Dallas, Peking University, Beijing Tongming Lake Information Technology Application Innovation Center
  - **Type:** Agentic workflow · **Kernel:** `TileLang` `Ascend C` `HIP` · **Hardware:** AMD, Ascend · **Benchmark:** KernelBench
- **LLM4LLM: Bridging Kernel Benchmarks and Real Deployment via Closed-Loop Agentic Optimization** [![arXiv](https://img.shields.io/badge/arXiv-26.08-red)](https://arxiv.org/abs/2608.21836) [![Stars](https://img.shields.io/github/stars/hzeng2000/LLM4LLM)](https://github.com/hzeng2000/LLM4LLM)
  - **Institution:** Xidian University, Zhongguancun Academy
  - **Type:** Agentic workflow · **Kernel:** `Triton` `CUDA` `TileLang` · **Hardware:** NVIDIA · **Benchmark:** KernelBench
- **GEAK v4** [![Stars](https://img.shields.io/github/stars/AMD-AGI/GEAK)](https://github.com/AMD-AGI/GEAK) [![Project](https://img.shields.io/badge/Project-Page-blue)](https://rocm.docs.amd.com/projects/geak/en/latest) [![Blog](https://img.shields.io/badge/Blog-AMD-blue)](https://www.amd.com/en/developer/resources/technical-articles/2026/geak-v4.html)
  - *AMD's multi-agent kernel optimizer spans HIP, Triton, FlyDSL, TileLang and Composable Kernel.*
  - **Institution:** AMD-AGI
  - **Type:** Open-source / industry system · **Kernel:** `HIP` `Triton` `FlyDSL` `TileLang` `Composable Kernel` · **Hardware:** AMD
- **Atrex Kernel Agent (AKA): Are LLM-Generated GPU Kernels Production-Ready? A Trace-Driven Benchmark and Optimization Agent** [![arXiv](https://img.shields.io/badge/arXiv-26.07-red)](https://arxiv.org/abs/2607.14541) [![Stars](https://img.shields.io/github/stars/alibaba/atrex-kernel-agent)](https://github.com/alibaba/atrex-kernel-agent) [![Release notes](https://img.shields.io/badge/Release-Notes-blue)](https://github.com/alibaba/atrex-kernel-agent/releases/tag/v0.3.0)
  - **Institution:** ATREX Team, Alibaba Group
  - **Type:** Agentic workflow · **Kernel:** `FlyDSL` `Triton` `CUDA` `Gluon` `CUTLASS` `CuTe` `TileLang` · **Hardware:** NVIDIA, AMD, T-Head PPU
- **AKO4X: AKO: Agentic Kernel Optimization** [![Stars](https://img.shields.io/github/stars/TongmingLAIC/AKO4X)](https://github.com/TongmingLAIC/AKO4X)
  - **Institution:** TLAIC
  - **Type:** Open-source / industry system · **Kernel:** `Triton` `CUDA` `TileLang` `CUTLASS` `CuTe` · **Hardware:** NVIDIA · **Benchmark:** FlashInfer-Bench
- **DSL-Monkeys: Self-Generated In-Context Examples for Low-Resource GPU DSL Kernels** [![ICLR Workshop 2026](https://img.shields.io/badge/ICLR_Workshop-26-green)](https://openreview.net/forum?id=2yS4j1C3zi)
  - **Type:** Trained model · **Kernel:** `TileLang` `ThunderKittens` · **Hardware:** NVIDIA · **Benchmark:** KernelBench
- **CANNBot Skills** [![Code](https://img.shields.io/badge/Code-GitCode-blue)](https://gitcode.com/cann/cannbot-skills) [![Changelog](https://img.shields.io/badge/Changelog-GitCode-blue)](https://gitcode.com/cann/cannbot-skills/blob/master/CHANGELOG.md)
  - *Public plugin/agent/skill suite for staged NPU-operator development: architect, developer, reviewer and tester workflows cover direct and registered Ascend C kernels plus Catlass, PyPTO, TileLang and.*
  - **Institution:** Huawei CANN
  - **Type:** Open-source / industry system · **Kernel:** `Ascend C` `Catlass` `PyPTO` `TileLang` `Triton` · **Hardware:** Ascend
- **AKO / AKO4ALL** [![Stars](https://img.shields.io/github/stars/TongmingLAIC/AKO4ALL)](https://github.com/TongmingLAIC/AKO4ALL) [![Project](https://img.shields.io/badge/Project-Page-blue)](https://tongminglaic.github.io/AKO)
  - *Generic coding-agent harness for kernel optimization.*
  - **Institution:** TLAIC
  - **Type:** Open-source / industry system · **Kernel:** `Triton` `CUDA` `TileLang` · **Hardware:** NVIDIA · **Benchmark:** SOL-ExecBench
- **TileOPs (TOPS)** [![Stars](https://img.shields.io/github/stars/tile-ai/TileOPs)](https://github.com/tile-ai/TileOPs)
  - *Spec-driven operator library: AI agents read declarative manifests (signatures, workloads, roofline formulas), generate TileLang kernels, and self-validate against Speed-of-Light bounds.*
  - **Institution:** tile-ai
  - **Type:** Tool · **Kernel:** `TileLang` · **Hardware:** NVIDIA

## 2025

- **KernelEvolve: Scaling Agentic Kernel Coding for Heterogeneous AI Accelerators at Meta** [![ISCA 2026](https://img.shields.io/badge/ISCA-26-green)](https://arxiv.org/abs/2512.23236) [![Blog](https://img.shields.io/badge/Blog-Meta-blue)](https://engineering.fb.com/2026/04/02/developer-tools/kernelevolve-how-metas-ranking-engineer-agent-optimizes-ai-infrastructure)
  - **Institution:** Meta
  - **Type:** Trained model · **Kernel:** `CUDA` `Triton` `TileLang` `CUTLASS` `HIP` · **Hardware:** NVIDIA, Meta MTIA · **Benchmark:** KernelBench
- **AKG-AGENT: AKG kernel Agent: A Multi-Agent Framework for Cross-Platform Kernel Synthesis** [![arXiv](https://img.shields.io/badge/arXiv-25.12-red)](https://arxiv.org/abs/2512.23424) [![Code](https://img.shields.io/badge/Code-GitHub-blue)](https://github.com/mindspore-ai/akg/tree/master/akg_agents)
  - **Institution:** Huawei, Hunan University
  - **Type:** Agentic workflow · **Kernel:** `Triton` `TileLang` `Ascend C` `CUDA` · **Hardware:** NVIDIA, Ascend, CPU · **Benchmark:** KernelBench
- **TileLang-Ascend** [![Stars](https://img.shields.io/github/stars/tile-ai/tilelang-ascend)](https://github.com/tile-ai/tilelang-ascend)
  - *Adapter layer connecting TileLang to the Ascend backend (not an agent).*
  - **Institution:** tile-ai
  - **Type:** Tool · **Kernel:** `TileLang` · **Hardware:** Ascend
