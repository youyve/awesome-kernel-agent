# Kernel language: HIP

[← README](../README.md) · 15 entries, newest first

## 2026

- **TileCas: Cascading Kernel Development Across Programming Abstractions** [![arXiv](https://img.shields.io/badge/arXiv-26.10-red)](https://arxiv.org/abs/2610.14740) [![Stars](https://img.shields.io/github/stars/TongmingLAIC/tilecas)](https://github.com/TongmingLAIC/tilecas)
  - **Institution:** Fudan University, University of Texas at Dallas, Peking University, Beijing Tongming Lake Information Technology Application Innovation Center
  - **Type:** Agentic workflow · **Kernel:** `TileLang` `Ascend C` `HIP` · **Hardware:** AMD, Ascend · **Benchmark:** KernelBench
- **SHADB: From Custom-Fit to Portable: Bridging the Gap Between Synthesized and Engineered GPU Query Execution** [![arXiv](https://img.shields.io/badge/arXiv-26.07-red)](https://arxiv.org/abs/2607.07632) [![Stars](https://img.shields.io/gitlab/stars/dislab%2FSHADB?gitlab_url=https%3A%2F%2Fgitlab.eurecom.fr)](https://gitlab.eurecom.fr/dislab/SHADB)
  - **Institution:** EURECOM
  - **Type:** Agentic workflow · **Kernel:** `CUDA` `HIP` · **Hardware:** NVIDIA, AMD
- **GEAK v4** [![Stars](https://img.shields.io/github/stars/AMD-AGI/GEAK)](https://github.com/AMD-AGI/GEAK) [![Project](https://img.shields.io/badge/Project-Page-blue)](https://rocm.docs.amd.com/projects/geak/en/latest) [![Blog](https://img.shields.io/badge/Blog-AMD-blue)](https://www.amd.com/en/developer/resources/technical-articles/2026/geak-v4.html)
  - *AMD's multi-agent kernel optimizer spans HIP, Triton, FlyDSL, TileLang and Composable Kernel.*
  - **Institution:** AMD-AGI
  - **Type:** Open-source / industry system · **Kernel:** `HIP` `Triton` `FlyDSL` `TileLang` `Composable Kernel` · **Hardware:** AMD
- **AgentKernelArena: Generalization-Aware Benchmarking of GPU Kernel Optimization Agents** [![arXiv](https://img.shields.io/badge/arXiv-26.05-red)](https://arxiv.org/abs/2605.16819) [![Stars](https://img.shields.io/github/stars/AMD-AGI/AgentKernelArena)](https://github.com/AMD-AGI/AgentKernelArena)
  - **Institution:** AMD
  - **Type:** Benchmark · **Kernel:** `HIP` `Triton` · **Hardware:** AMD
- **AMDKernelVault: Large-Scale Datasets and Agentic Training for AMD GPU Kernel Optimization** [![arXiv](https://img.shields.io/badge/arXiv-26.09-red)](https://arxiv.org/abs/2609.12471) [![Stars](https://img.shields.io/github/stars/AMD-AGI/AMDKernelVault)](https://github.com/AMD-AGI/AMDKernelVault) [![Dataset](https://img.shields.io/badge/Dataset-HuggingFace-yellow)](https://huggingface.co/datasets/amd/AIG-Datasets)
  - **Institution:** AMD
  - **Type:** Trained model · **Kernel:** `HIP` `Triton` · **Hardware:** AMD · **Benchmark:** KernelBench, TritonBench
- **Ave: Guiding Agentic GPU Optimization Using Data-Flow Invariants** [![SOSP 2026](https://img.shields.io/badge/SOSP-26-green)](https://arxiv.org/abs/2604.18616)
  - **Institution:** CausalFlow, Hong Kong University of Science and Technology, University of Chinese Academy of Sciences, UC Riverside, Tsinghua University, Stanford University
  - **Type:** Agentic workflow · **Kernel:** `HIP` · **Hardware:** AMD · **Benchmark:** KernelBench
- **ROCm Hyperloom** [![Stars](https://img.shields.io/github/stars/AMD-AGI/Hyperloom)](https://github.com/AMD-AGI/Hyperloom) [![Project](https://img.shields.io/badge/Project-Page-blue)](https://rocm.docs.amd.com/projects/hyperloom/en/latest/index.html) [![Blog](https://img.shields.io/badge/Blog-AMD-blue)](https://rocm.blogs.amd.com/software-tools-optimization/hyperloom-optimization/README.html) [![Artifacts](https://img.shields.io/badge/Artifacts-GitHub-lightgrey)](https://github.com/AMD-AGI/Hyperloom/tree/79856335c65047ac11264132167def97047f83e5/.cursor/skills/inference-optimization/results/qwen3-14b-mi355x)
  - *Multi-agent inference optimization across serving settings, framework source, and generated GPU kernels, with independent end-to-end measurement and a reusable recipe knowledge base.*
  - **Institution:** AMD
  - **Type:** Open-source / industry system · **Kernel:** `HIP` `Triton` `FlyDSL` · **Hardware:** AMD
- **Apex** [![Stars](https://img.shields.io/github/stars/AMD-AGI/Apex)](https://github.com/AMD-AGI/Apex)
  - *Agent harness (Claude Code/Codex/Cursor Agent backends) that iterates HIP/Triton kernels against a compile+correctness+speedup grader across 12 LLM-serving kernel types (flash attn, MoE, GEMM, RoPE, K.*
  - **Institution:** AMD
  - **Type:** Open-source / industry system · **Kernel:** `HIP` `Triton` · **Hardware:** AMD
- **GEAK-HIP** [![Stars](https://img.shields.io/github/stars/AMD-AGI/GEAK)](https://github.com/AMD-AGI/GEAK) [![Blog](https://img.shields.io/badge/Blog-AMD-blue)](https://rocm.blogs.amd.com/software-tools-optimization/geak-hip-optimizations/README.html)
  - *GEAK extension for iterative HIP-kernel optimization on AMD GPUs.*
  - **Institution:** AMD-AGI
  - **Type:** Open-source / industry system · **Kernel:** `HIP` · **Hardware:** AMD

## 2025

- **KernelEvolve: Scaling Agentic Kernel Coding for Heterogeneous AI Accelerators at Meta** [![ISCA 2026](https://img.shields.io/badge/ISCA-26-green)](https://arxiv.org/abs/2512.23236) [![Blog](https://img.shields.io/badge/Blog-Meta-blue)](https://engineering.fb.com/2026/04/02/developer-tools/kernelevolve-how-metas-ranking-engineer-agent-optimizes-ai-infrastructure)
  - **Institution:** Meta
  - **Type:** Trained model · **Kernel:** `CUDA` `Triton` `TileLang` `CUTLASS` `HIP` · **Hardware:** NVIDIA, Meta MTIA · **Benchmark:** KernelBench
- **PEAK: A Performance Engineering AI-Assistant for GPU Kernels Powered by Natural Language Transformations** [![arXiv](https://img.shields.io/badge/arXiv-25.12-red)](https://arxiv.org/abs/2512.19018)
  - **Institution:** Stanford University, Microsoft Research
  - **Type:** Agentic workflow · **Kernel:** `CUDA` `HIP` · **Hardware:** NVIDIA, AMD
- **KForge: A Multi-Agent System for Cross-Platform Kernel Synthesis** [![ICML Workshop 2026](https://img.shields.io/badge/ICML_Workshop-26-green)](https://arxiv.org/abs/2606.02963)
  - **Institution:** Gimlet Labs
  - **Type:** Agentic workflow · **Kernel:** `Triton` `CUDA` `CUTLASS` `HIP` `SYCL` `Metal` · **Hardware:** NVIDIA, AMD, Intel, Apple · **Benchmark:** KernelBench
- **IntelliPerf** [![Stars](https://img.shields.io/github/stars/AMDResearch/intelliperf)](https://github.com/AMDResearch/intelliperf)
  - *Profiling-guided LLM framework for AMD GPUs.*
  - **Institution:** AMD Research
  - **Type:** Open-source / industry system · **Kernel:** `HIP` `Triton` · **Hardware:** AMD
- **QiMeng-Xpiler: Transcompiling Tensor Programs for Deep Learning Systems with a Neural-Symbolic Approach** [![OSDI 2025](https://img.shields.io/badge/OSDI-25-green)](https://arxiv.org/abs/2505.02146)
  - **Institution:** Institute of Computing Technology (CAS), University of Science and Technology of China, Cambricon
  - **Type:** Agentic workflow · **Kernel:** `CUDA` `HIP` · **Hardware:** NVIDIA, AMD, CPU, Cambricon
- **IntelliKit** [![Stars](https://img.shields.io/github/stars/AMDResearch/intellikit)](https://github.com/AMDResearch/intellikit)
  - *LLM-ready profiling toolkit for AMD GPUs.*
  - **Institution:** AMD Research
  - **Type:** Tool · **Kernel:** `HIP` · **Hardware:** AMD
