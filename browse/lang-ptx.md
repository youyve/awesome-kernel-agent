# Kernel language: PTX

[← README](../README.md) · 8 entries, newest first

## 2026

- **What Language Should LLMs Write GPU Kernels In? Disentangling Abstraction Level from Resource Level** [![NeurIPS Workshop 2026](https://img.shields.io/badge/NeurIPS_Workshop-26-green)](https://openreview.net/forum?id=9Ppcp9PK8i)
  - **Institution:** Pusan National University, Electronics and Telecommunications Research Institute
  - **Type:** Empirical study · **Kernel:** `CUDA` `PTX` `Triton` `TileLang` · **Hardware:** NVIDIA · **Benchmark:** KernelBench
- **Triton AI Compiler (TAIC): AI as a Compiler: Compiling Triton kernels without the Triton compiler** [![arXiv](https://img.shields.io/badge/arXiv-26.09-red)](https://arxiv.org/abs/2609.36800) [![Stars](https://img.shields.io/github/stars/francois141/triton_ai_compiler)](https://github.com/francois141/triton_ai_compiler)
  - **Institution:** Stanford University, EPFL
  - **Type:** Agentic workflow · **Kernel:** `PTX` · **Hardware:** NVIDIA
- **PTXBench: Evaluating and Adapting LLMs for GPU Kernel Optimization with Architecture-specific PTX** [![NeurIPS Workshop 2026](https://img.shields.io/badge/NeurIPS_Workshop-26-green)](https://arxiv.org/abs/2608.17379) [![Stars](https://img.shields.io/github/stars/zhang677/PTXBench)](https://github.com/zhang677/PTXBench) [![Model](https://img.shields.io/badge/Model-HuggingFace-yellow)](https://huggingface.co/collections/Genghan/ptxbench-qwen36-27b-sft-series) [![Dataset](https://img.shields.io/badge/Dataset-HuggingFace-yellow)](https://huggingface.co/datasets/AccRL/accrl-training) [![Blog](https://img.shields.io/badge/Blog-Stanford_University-blue)](https://zhang677.github.io/blog_md/ptxbench.html)
  - **Institution:** Stanford University, Carnegie Mellon University, RadixArk
  - **Type:** Trained model · **Kernel:** `CUDA` `PTX` `Triton` · **Hardware:** NVIDIA · **Benchmark:** FlashInfer-Bench
- **KernelArc: A Multi-Agent Framework for GPU Kernel Optimization** [![arXiv](https://img.shields.io/badge/arXiv-26.08-red)](https://arxiv.org/abs/2608.17071)
  - **Institution:** AI Labs, imec
  - **Type:** Search & evolution · **Kernel:** `CUDA` `PTX` `Triton` `CUTLASS` · **Hardware:** NVIDIA · **Benchmark:** SOL-ExecBench
- **CAKE: Compiler-Agent Co-Design for Frontier Kernel Evolution** [![arXiv](https://img.shields.io/badge/arXiv-26.08-red)](https://arxiv.org/abs/2608.12629) [![Artifacts](https://img.shields.io/badge/Artifacts-GitHub-lightgrey)](https://github.com/flashinfer-ai/flashinfer/issues/4254)
  - **Institution:** NVIDIA, Carnegie Mellon University
  - **Type:** Agentic workflow · **Kernel:** `CAKE IR` `CUDA` `PTX` · **Hardware:** NVIDIA
- **Cursor Multi-Agent Kernel Optimization** [![Blog](https://img.shields.io/badge/Blog-Cursor-blue)](https://cursor.com/blog/multi-agent-kernels) [![Artifacts](https://img.shields.io/badge/Artifacts-GitHub-lightgrey)](https://github.com/anysphere/kernel-optimization-results)
  - *Planner + autonomous parallel workers optimized 235 kernels from 124+ open-source models (CUDA C w/ inline PTX and CuTe DSL) on 27x Blackwell B200 over 3 weeks using NVIDIA's SOL-ExecBench test-debug-.*
  - **Institution:** Cursor, NVIDIA
  - **Type:** Open-source / industry system · **Kernel:** `CUDA` `CUTLASS` `CuTe` `PTX` · **Hardware:** NVIDIA · **Benchmark:** SOL-ExecBench
- **AVO: Agentic Variation Operators for Autonomous Evolutionary Search** [![arXiv](https://img.shields.io/badge/arXiv-26.03-red)](https://arxiv.org/abs/2603.24517) [![Project](https://img.shields.io/badge/Project-Page-blue)](https://github.com/austin1997/AVO)
  - **Institution:** NVIDIA, OctoML
  - **Type:** Search & evolution · **Kernel:** `CUDA` `PTX` · **Hardware:** NVIDIA
- **Standard Kernel** [![Blog](https://img.shields.io/badge/Blog-Standard_Kernel-blue)](https://standardkernel.com/blog/announcing-our-seed-round-is-kernel-generation-solved)
  - *Hybrid program-analysis + LLM reasoning at the PTX layer across Triton / TileLang / ThunderKittens / CUTLASS.*
  - **Institution:** Standard Kernel
  - **Type:** Open-source / industry system · **Kernel:** `PTX` · **Hardware:** NVIDIA
