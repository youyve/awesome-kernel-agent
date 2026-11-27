# Infrastructure and tools

[← README](../README.md) · 11 entries, newest first

_Benchmarking isolation, tracing, and kernel libraries used by agents._

## 2026

- **KernelArmor: End-to-End Agentic System for Establishing Memory and Thread Safety for CUDA** [![arXiv](https://img.shields.io/badge/arXiv-26.11-red)](https://arxiv.org/abs/2611.18754)
  - **Institution:** NVIDIA, Stanford University
  - **Type:** Tool · **Kernel:** `CUDA` · **Hardware:** NVIDIA · **Benchmark:** KernelBench, SOL-ExecBench
- **Warpline: Binary-Level Tracing and Unified Evidence for Agentic GPU Kernel Optimization** [![arXiv](https://img.shields.io/badge/arXiv-26.11-red)](https://arxiv.org/abs/2611.04331)
  - **Institution:** George Mason University, NVIDIA
  - **Type:** Tool · **Kernel:** `Triton` `CuTe` `CUDA` `PTX` · **Hardware:** NVIDIA · **Benchmark:** SOL-ExecBench
- **LARK: Lean-Assisted Reasoning for LLM-Generated GPU Kernels** [![arXiv](https://img.shields.io/badge/arXiv-26.11-red)](https://arxiv.org/abs/2611.02028)
  - **Institution:** Imperial College London, University of Cambridge, Quettaflop AI, University of Edinburgh, EPFL
  - **Type:** Tool · **Kernel:** `PTX` `CUDA` `HIP` · **Hardware:** NVIDIA, AMD · **Benchmark:** KernelCraft
- **Lean and VerCors GPU Verification: Proving LLM-Generated GPU Kernels Correct and Safe: Floating-Point Verification in Lean and VerCors** [![arXiv](https://img.shields.io/badge/arXiv-26.10-red)](https://arxiv.org/abs/2610.24548)
  - **Institution:** Imperial College London, Logos Research
  - **Type:** Tool · **Kernel:** `CUDA` · **Hardware:** CPU · **Benchmark:** KernelBench
- **KREX** [![arXiv](https://img.shields.io/badge/arXiv-26.09-red)](https://arxiv.org/abs/2609.30057)
  - *Runtime for interference-controlled kernel benchmarking on shared GPUs.*
  - **Institution:** Hong Kong University of Science and Technology, Alibaba
  - **Type:** Tool · **Hardware:** NVIDIA, AMD
- **Xtrace** [![arXiv](https://img.shields.io/badge/arXiv-26.09-red)](https://arxiv.org/abs/2609.28769) [![Project](https://img.shields.io/badge/Project-Page-blue)](https://g-watch.github.io) [![Artifacts](https://img.shields.io/badge/Artifacts-g--watch.github.io-lightgrey)](https://g-watch.github.io/en/open-traces)
  - *Binary-instrumentation tracing infrastructure with GPU kernel-agent case studies.*
  - **Institution:** National University of Singapore, Meta
  - **Type:** Tool · **Hardware:** NVIDIA, AMD
- **BIEvolve: God Does Not Play Dice: Enforcing Batch Invariance in Agentic Kernel Generation** [![arXiv](https://img.shields.io/badge/arXiv-26.10-red)](https://arxiv.org/abs/2610.36623) [![Code unavailable](https://img.shields.io/badge/Code-unavailable-lightgrey)](https://github.com/STAR-Computing/BIEvolve)
  - **Institution:** George Mason University, National University of Singapore
  - **Type:** Tool · **Hardware:** NVIDIA · **Benchmark:** KernelBench.com, FlashInfer-Bench
- **Kernel Contracts: A Specification Language for ML Kernel Correctness Across Heterogeneous Silicon** [![arXiv](https://img.shields.io/badge/arXiv-26.04-red)](https://arxiv.org/abs/2604.22032) [![Stars](https://img.shields.io/github/stars/cv700/ashiba-verify)](https://github.com/cv700/ashiba-verify)
  - **Institution:** Ashiba Research
  - **Type:** Tool · **Hardware:** NVIDIA, AMD, Apple
- **TileOPs (TOPS)** [![Stars](https://img.shields.io/github/stars/tile-ai/TileOPs)](https://github.com/tile-ai/TileOPs)
  - *Spec-driven operator library: AI agents read declarative manifests (signatures, workloads, roofline formulas), generate TileLang kernels, and self-validate against Speed-of-Light bounds.*
  - **Institution:** tile-ai
  - **Type:** Tool · **Kernel:** `TileLang` · **Hardware:** NVIDIA

## 2025

- **TileLang-Ascend** [![Stars](https://img.shields.io/github/stars/tile-ai/tilelang-ascend)](https://github.com/tile-ai/tilelang-ascend)
  - *Adapter layer connecting TileLang to the Ascend backend (not an agent).*
  - **Institution:** tile-ai
  - **Type:** Tool · **Kernel:** `TileLang` · **Hardware:** Ascend
- **IntelliKit** [![Stars](https://img.shields.io/github/stars/AMDResearch/intellikit)](https://github.com/AMDResearch/intellikit)
  - *LLM-ready profiling toolkit for AMD GPUs.*
  - **Institution:** AMD Research
  - **Type:** Tool · **Kernel:** `HIP` · **Hardware:** AMD
