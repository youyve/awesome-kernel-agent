# Awesome Kernel Agent [![Awesome](https://awesome.re/badge.svg)](https://awesome.re) [![Last Commit](https://img.shields.io/github/last-commit/youyve/awesome-kernel-agent)](https://github.com/youyve/awesome-kernel-agent/commits/main) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

> The living map of LLM-driven kernel generation and optimization: agents, trained models, benchmarks, and industry systems across NVIDIA, AMD, Ascend, TPU, and more. Continuously updated.

[Benchmark catalog](https://github.com/youyve/awesome-kernel-benchmark) · [Data](data/entries.yaml) · [Contributing](CONTRIBUTING.md)

**188 kernel agents** · **35 benchmarks** · **41 general-purpose systems** · **7 empirical studies** · **6 applications** · **5 tools** · research cutoff **2026-10-19**

## Browse

| Browse by | |
| --- | --- |
| **Type** | [Agentic workflows](browse/type-agentic-workflows.md) 72 · [Search and evolution](browse/type-search-and-evolution.md) 33 · [Trained kernel models](browse/type-trained-kernel-models.md) 50 · [Single-pass generation and developer tools](browse/type-single-pass-generation-and-developer-tools.md) 5 · [Open-source and industry systems](browse/type-open-source-and-industry-systems.md) 28 · [Benchmarks](browse/type-benchmarks.md) 35 · [General-purpose systems with kernel results](browse/type-general-purpose-systems-with-kernel-results.md) 41 · [Applications](browse/type-applications.md) 6 · [Infrastructure and tools](browse/type-infrastructure-and-tools.md) 5 · [Empirical studies](browse/type-empirical-studies.md) 7 |
| **Hardware** | [NVIDIA](browse/hw-nvidia.md) 188 · [AMD](browse/hw-amd.md) 29 · [Ascend](browse/hw-ascend.md) 25 · [Intel](browse/hw-intel.md) 3 · [Google TPU](browse/hw-google-tpu.md) 5 · [AWS Neuron](browse/hw-aws-neuron.md) 7 · [Apple](browse/hw-apple.md) 6 · [CPU](browse/hw-cpu.md) 3 · [RISC-V](browse/hw-risc-v.md) 6 · [Mobile GPU](browse/hw-mobile-gpu.md) 3 · [Meta MTIA](browse/hw-meta-mtia.md) 2 · [Moore Threads](browse/hw-moore-threads.md) 2 · [Cambricon](browse/hw-cambricon.md) 1 · [Tenstorrent](browse/hw-tenstorrent.md) 1 · [T-Head PPU](browse/hw-t-head-ppu.md) 2 · [Hygon DCU](browse/hw-hygon-dcu.md) 2 · [Cerebras](browse/hw-cerebras.md) 1 · [Research accelerators](browse/hw-research-accelerators.md) 3 · [Other](browse/hw-other.md) 1 |
| **Kernel language** | [CUDA](browse/lang-cuda.md) 95 · [Triton](browse/lang-triton.md) 71 · [HIP](browse/lang-hip.md) 15 · [TileLang](browse/lang-tilelang.md) 13 · [Ascend C](browse/lang-ascend-c.md) 13 · [CUTLASS](browse/lang-cutlass.md) 13 · [PTX](browse/lang-ptx.md) 8 · [CuTe](browse/lang-cute.md) 6 · [TVM](browse/lang-tvm.md) 4 · [NKI](browse/lang-nki.md) 4 · [Other](browse/lang-other.md) 15 |
| **Benchmark** | [KernelBench](browse/bench-kernelbench.md) 81 · [FlashInfer-Bench](browse/bench-flashinfer-bench.md) 18 · [TritonBench](browse/bench-tritonbench.md) 14 · [SOL-ExecBench](browse/bench-sol-execbench.md) 8 · [MultiKernelBench](browse/bench-multikernelbench.md) 6 · [NPUKernelBench](browse/bench-npukernelbench.md) 5 · [CANN-Bench](browse/bench-cann-bench.md) 4 |
| **Year** | [2026](browse/year-2026.md) 226 · [2025](browse/year-2025.md) 54 · [2024 and earlier](browse/year-2024-and-earlier.md) 2 |
| **Everything** | [All entries on one page](browse/all.md) |

**Badges:** ![arXiv](https://img.shields.io/badge/arXiv-YY.MM-red) preprint · ![Venue](https://img.shields.io/badge/Venue-YY-green) accepted at a peer-reviewed conference or workshop · ![OpenReview](https://img.shields.io/badge/OpenReview-YY.MM-lightgrey) OpenReview submission, not yet accepted · ![Blog](https://img.shields.io/badge/Blog-Org-blue) blog or technical report · ![Stars](https://img.shields.io/badge/stars-live-white) GitHub stars, updated automatically

## Contents

- [**Kernel agents**](#kernel-agents) (188)
  - **2026** — [Oct](#2026-10) 5 · [Sep](#2026-09) 35 · [Aug](#2026-08) 16 · [Jul](#2026-07) 8 · [Jun](#2026-06) 13 · [May](#2026-05) 20 · [Apr](#2026-04) 9 · [Mar](#2026-03) 20 · [Feb](#2026-02) 9 · [Jan](#2026-01) 9
  - **2025** — [Dec](#2025-12) 8 · [Nov](#2025-11) 9 · [Oct](#2025-10) 8 · [Sep](#2025-09) 2 · [Aug](#2025-08) 1 · [Jul](#2025-07) 5 · [Jun](#2025-06) 4 · [May](#2025-05) 4 · [Feb](#2025-02) 2
  - **2023** — [Nov](#2023-11) 1
- [**Benchmarks**](#benchmarks) (35)
- **Context** — [General-purpose systems with kernel results](#general-purpose-systems-with-kernel-results) (41) · [Applications](#applications) (6) · [Infrastructure and tools](#infrastructure-and-tools) (5) · [Empirical studies](#empirical-studies) (7)
- **Resources** — [Evaluation integrity and reward hacking](#evaluation-integrity-and-reward-hacking) · [Competitions and leaderboards](#competitions-and-leaderboards) · [Datasets](#datasets) · [Representations and infrastructure](#representations-and-infrastructure)

_Every section is a timeline: newest first, grouped by the month of first public release (arXiv v1, OpenReview submission, blog post, or repository)._

## Kernel agents

_LLM systems whose main contribution is generating or optimizing kernels. Filter by type, hardware, kernel language, or benchmark with **Browse** above._

### 2026-10

- **How to Train Your Little Dragon: Teaching a Small Language Model to Construct and Refine GPU Optimization Scripts** [![arXiv](https://img.shields.io/badge/arXiv-26.10-red)](https://arxiv.org/abs/2610.20980) [![Stars](https://img.shields.io/github/stars/Anna-Bele/How-To-Train-Your-Little-Dragon)](https://github.com/Anna-Bele/How-To-Train-Your-Little-Dragon)
  - **Institution:** UC San Diego, Amazon
  - **Type:** Trained model · **Kernel:** `TVM` · **Hardware:** NVIDIA
- **VibeKernel: Long-Horizon GPU Kernel Optimization with General-Purpose Coding Agents** [![NeurIPS Workshop 2026](https://img.shields.io/badge/NeurIPS_Workshop-26-green)](https://openreview.net/forum?id=WIihTnl976)
  - **Institution:** ETH Zurich
  - **Type:** Agentic workflow · **Kernel:** `Triton` · **Hardware:** NVIDIA · **Benchmark:** FlashInfer-Bench, SOL-ExecBench
- **Vessel: High-Utilization Megakernels by Construction** [![NeurIPS Workshop 2026](https://img.shields.io/badge/NeurIPS_Workshop-26-green)](https://openreview.net/forum?id=ZCNEnKYAIc) [![Code](https://img.shields.io/badge/Code-Anonymous-lightgrey)](https://anonymous.4open.science/r/vessel-artifact-5CE8)
  - **Type:** Single-pass / tooling · **Hardware:** NVIDIA
- **TileCas: Cascading Kernel Development Across Programming Abstractions** [![arXiv](https://img.shields.io/badge/arXiv-26.10-red)](https://arxiv.org/abs/2610.14740) [![Stars](https://img.shields.io/github/stars/TongmingLAIC/tilecas)](https://github.com/TongmingLAIC/tilecas)
  - **Institution:** Fudan University, University of Texas at Dallas, Peking University, Beijing Tongming Lake Information Technology Application Innovation Center
  - **Type:** Agentic workflow · **Kernel:** `TileLang` `Ascend C` `HIP` · **Hardware:** AMD, Ascend · **Benchmark:** KernelBench
- **ATRL: Compaction-Aware Reinforcement Learning For Ascend Triton Kernel Generation** [![arXiv](https://img.shields.io/badge/arXiv-26.10-red)](https://arxiv.org/abs/2610.23950)
  - **Institution:** Huawei
  - **Type:** Trained model · **Kernel:** `Triton` · **Hardware:** Ascend · **Benchmark:** KernelBench, NPUKernelBench

### 2026-09

- **Triton AI Compiler (TAIC): AI as a Compiler: Compiling Triton kernels without the Triton compiler** [![arXiv](https://img.shields.io/badge/arXiv-26.09-red)](https://arxiv.org/abs/2609.36800) [![Stars](https://img.shields.io/github/stars/francois141/triton_ai_compiler)](https://github.com/francois141/triton_ai_compiler)
  - **Institution:** Stanford University, EPFL
  - **Type:** Agentic workflow · **Kernel:** `PTX` · **Hardware:** NVIDIA
- **SAGE: From Experience to Expertise: Adoption-Aware Memory Learning for Data-Scarce NPU Kernel Synthesis** [![arXiv](https://img.shields.io/badge/arXiv-26.09-red)](https://arxiv.org/abs/2609.35568)
  - **Institution:** Fudan University, University of Science and Technology of China, Huawei
  - **Type:** Agentic workflow · **Hardware:** Ascend · **Benchmark:** NPUKernelBench
- **AReaL-TIK: Stateful Agentic Optimization of Unified RL Kernels through an Optimization IR** [![arXiv](https://img.shields.io/badge/arXiv-26.09-red)](https://arxiv.org/abs/2609.35140) [![Stars](https://img.shields.io/github/stars/areal-project/AReaL-TIK)](https://github.com/areal-project/AReaL-TIK)
  - **Institution:** Hong Kong University of Science and Technology, University of Cambridge, Ant Group, Reflection AI
  - **Type:** Agentic workflow · **Hardware:** NVIDIA
- **KernelZero: Co-Evolving Proposer and Coder for Continuously Improved GPU Kernel Generation** [![arXiv](https://img.shields.io/badge/arXiv-26.09-red)](https://arxiv.org/abs/2609.33074) [![Stars](https://img.shields.io/github/stars/kcxain/KernelZero)](https://github.com/kcxain/KernelZero) [![Model](https://img.shields.io/badge/Model-HuggingFace-yellow)](https://huggingface.co/collections/kcxain/kernelzero)
  - **Institution:** Institute of Computing Technology (CAS), University of Chinese Academy of Sciences, Institute of Software (CAS), Institute of AI for Industries (CAS)
  - **Type:** Trained model · **Kernel:** `CUDA` `Triton` · **Hardware:** NVIDIA · **Benchmark:** KernelBench
- **KernelOPT: Dispatch-Aware Agentic Search for GPU Kernel Optimization** [![arXiv](https://img.shields.io/badge/arXiv-26.09-red)](https://arxiv.org/abs/2609.30059) [![Code unavailable](https://img.shields.io/badge/Code-unavailable-lightgrey)](https://github.com/TorchedHat/KernelOPT)
  - **Institution:** Red Hat
  - **Type:** Search & evolution · **Kernel:** `Triton` `Helion` · **Hardware:** NVIDIA · **Benchmark:** KernelBench
- **SynKer: Synthesize, Kernelize, Reinforce — Teaching GPU Kernel Generation to Small Language Models** [![OpenReview](https://img.shields.io/badge/OpenReview-26.09-lightgrey)](https://openreview.net/forum?id=nZQqqpYQ0Y)
  - **Type:** Trained model · **Hardware:** NVIDIA
- **REPAIR: Learning What to Optimize for Efficient Ascend Kernels** [![OpenReview](https://img.shields.io/badge/OpenReview-26.09-lightgrey)](https://openreview.net/forum?id=hn8g8PZY5F)
  - **Type:** Trained model · **Hardware:** Ascend · **Benchmark:** MultiKernelBench
- **KernelMaster: Agentic GPU Kernel Optimization from Semantics to Execution** [![OpenReview](https://img.shields.io/badge/OpenReview-26.09-lightgrey)](https://openreview.net/forum?id=rIc8lSAsw0) [![Code](https://img.shields.io/badge/Code-Anonymous-lightgrey)](https://anonymous.4open.science/r/KernelMaster-4A2B)
  - **Type:** Trained model · **Kernel:** `CUDA` · **Hardware:** NVIDIA
- **Hardware-in-the-Loop RL for OpenCL Optimization on Mobile GPUs** [![OpenReview](https://img.shields.io/badge/OpenReview-26.09-lightgrey)](https://openreview.net/forum?id=Ktya9054vX)
  - **Type:** Trained model · **Kernel:** `OpenCL` · **Hardware:** NVIDIA, Mobile GPU
- **ForgeKernel: Self-Evolving Kernels Catching And Surpassing Experts And Agents** [![OpenReview](https://img.shields.io/badge/OpenReview-26.09-lightgrey)](https://openreview.net/forum?id=EtV3f5BPD4) [![Stars](https://img.shields.io/github/stars/OpenBMB/ForgeKernel)](https://github.com/OpenBMB/ForgeKernel)
  - **Type:** Agentic workflow · **Hardware:** NVIDIA, Ascend · **Benchmark:** CANN-Bench
- **Evoke: Structured Construction and Search for Llm-Based Native Kernel Evolution** [![OpenReview](https://img.shields.io/badge/OpenReview-26.09-lightgrey)](https://openreview.net/forum?id=iatY8aCCHw)
  - **Type:** Search & evolution · **Kernel:** `Ascend C` · **Hardware:** Ascend
- **Seeing Sparsity: Pattern-Guided Agents for Hardware-Adaptive SpMV Optimization** [![OpenReview](https://img.shields.io/badge/OpenReview-26.09-lightgrey)](https://openreview.net/forum?id=tDhF7c1KMz)
  - **Type:** Trained model · **Hardware:** NVIDIA, AMD
- **ProcessKernel: Calibrated Process Supervision for GPU Kernel Generation** [![OpenReview](https://img.shields.io/badge/OpenReview-26.09-lightgrey)](https://openreview.net/forum?id=gO1SLMPGbi) [![Code](https://img.shields.io/badge/Code-Anonymous-lightgrey)](https://anonymous.4open.science/r/ProcessKernel-733C)
  - **Type:** Search & evolution · **Hardware:** NVIDIA · **Benchmark:** KernelBench
- **ModelParts: Model-Grounded Tasks and Roofline Rewards for Training Kernel Agents on Emerging Accelerators** [![OpenReview](https://img.shields.io/badge/OpenReview-26.09-lightgrey)](https://openreview.net/forum?id=yUa4J3DuzA)
  - **Type:** Trained model · **Kernel:** `NKI` · **Hardware:** AWS Neuron
- **KernelMosaic: An Open Dataset and Agentic Framework for CUDA Kernel Generation** [![OpenReview](https://img.shields.io/badge/OpenReview-26.09-lightgrey)](https://openreview.net/forum?id=AMenxeeqRp)
  - **Type:** Trained model · **Kernel:** `CUDA` · **Hardware:** NVIDIA · **Benchmark:** KernelBench
- **EvokeAgent: A Hardware-Aware, Knowledge-Base-Co-Driven Self-Evolving Agent System for GPU Kernel Optimization** [![OpenReview](https://img.shields.io/badge/OpenReview-26.09-lightgrey)](https://openreview.net/forum?id=wu2vgmepgJ)
  - **Type:** Agentic workflow · **Kernel:** `CUDA` `Triton` · **Hardware:** NVIDIA · **Benchmark:** KernelBench
- **Evok: Evidence-Centric Multi-Agent Framework for GPU Kernel Generation** [![OpenReview](https://img.shields.io/badge/OpenReview-26.09-lightgrey)](https://openreview.net/forum?id=1iwOWSLQDb)
  - **Type:** Agentic workflow · **Hardware:** NVIDIA · **Benchmark:** KernelBench
- **BeliefOPT: Recursive Self-Evolving Agents for Autonomous Research** [![OpenReview](https://img.shields.io/badge/OpenReview-26.09-lightgrey)](https://openreview.net/forum?id=8tlQHDNJxM)
  - **Type:** Agentic workflow · **Hardware:** NVIDIA · **Benchmark:** SOL-ExecBench
- **AutoProfiler: Less Is More: Learning What to Profile for GPU Kernel Optimization** [![OpenReview](https://img.shields.io/badge/OpenReview-26.09-lightgrey)](https://openreview.net/forum?id=tE3EQdUVsO)
  - **Type:** Agentic workflow · **Hardware:** NVIDIA · **Benchmark:** KernelBench
- **AscendAgent: Evolving Context to Fit the Harness in CANN Kernel Optimization** [![OpenReview](https://img.shields.io/badge/OpenReview-26.09-lightgrey)](https://openreview.net/forum?id=gtuspdBfQo)
  - **Type:** Search & evolution · **Hardware:** NVIDIA, Ascend · **Benchmark:** CANN-Bench, KernelBench, MultiKernelBench, TritonBench
- **Glueball: Agentic Generation and Verification of Hardware-Optimized Gluon Kernels** [![OpenReview](https://img.shields.io/badge/OpenReview-26.09-lightgrey)](https://openreview.net/forum?id=4Lpg8unVZd)
  - **Type:** Agentic workflow · **Kernel:** `Gluon` · **Hardware:** NVIDIA
- **CUDACoach: Guiding CUDA Kernel Optimization with Diverse Strategies Learned from Verified Code** [![OpenReview](https://img.shields.io/badge/OpenReview-26.09-lightgrey)](https://openreview.net/forum?id=QiCosML9uw)
  - **Type:** Trained model · **Kernel:** `CUDA` · **Hardware:** NVIDIA · **Benchmark:** KernelBench
- **BIEvolve: God Does Not Play Dice: Enforcing Batch Invariance in Agentic Kernel Generation** [![OpenReview](https://img.shields.io/badge/OpenReview-26.09-lightgrey)](https://openreview.net/forum?id=hvO7ZzQiqG) [![Code](https://img.shields.io/badge/Code-Anonymous-lightgrey)](https://anonymous.4open.science/r/BIEvolve-50F0)
  - **Type:** Agentic workflow · **Hardware:** NVIDIA · **Benchmark:** FlashInfer-Bench
- **AscendEvolve: Experience Is Not Enough: Knowledge-Grounded Evolutionary Search for Ascend C Kernel Generation** [![OpenReview](https://img.shields.io/badge/OpenReview-26.09-lightgrey)](https://openreview.net/forum?id=c9fIYOvuw8)
  - **Type:** Search & evolution · **Kernel:** `Ascend C` · **Hardware:** Ascend · **Benchmark:** CANN-Bench
- **SABER: Semantic Abstraction Boundaries for Efficient Refinement of Sparse GPU Kernels** [![OpenReview](https://img.shields.io/badge/OpenReview-26.09-lightgrey)](https://openreview.net/forum?id=ayAwDugvxo)
  - **Type:** Agentic workflow · **Hardware:** NVIDIA
- **DitronGen: Compiler–LLM Coordination for Adaptive Kernel Generation and Computation–Communication Overlap** [![OpenReview](https://img.shields.io/badge/OpenReview-26.09-lightgrey)](https://openreview.net/forum?id=UHZ5QcK1kW)
  - **Type:** Agentic workflow · **Kernel:** `Triton` · **Hardware:** NVIDIA
- **FlashVector: Agent for Hierarchical Model Serving Stack Optimization** [![arXiv](https://img.shields.io/badge/arXiv-26.09-red)](https://arxiv.org/abs/2609.17391)
  - **Institution:** Stanford University, Unity Vector AI Team
  - **Type:** Agentic workflow · **Kernel:** `Triton` · **Hardware:** NVIDIA, CPU
- **Distill Before You Measure: Dual Pruning for Evaluation-Efficient GPU Kernel Optimization** [![OpenReview](https://img.shields.io/badge/OpenReview-26.09-lightgrey)](https://openreview.net/forum?id=PJTW1QziqP)
  - **Type:** Search & evolution · **Hardware:** NVIDIA · **Benchmark:** KernelBench
- **Structure Before Tuning: Decoupling Structural Search and Local Optimization for LLM-Generated GPU Kernels** [![OpenReview](https://img.shields.io/badge/OpenReview-26.09-lightgrey)](https://openreview.net/forum?id=zUPEDRs09x)
  - **Type:** Search & evolution · **Hardware:** NVIDIA · **Benchmark:** FlashInfer-Bench, SOL-ExecBench
- **RvvCoder: ISA-Grounded LLMs for High-Performance RISC-V Vector Kernel Generation** [![OpenReview](https://img.shields.io/badge/OpenReview-26.09-lightgrey)](https://openreview.net/forum?id=Xi1nczXKQL)
  - **Type:** Trained model · **Kernel:** `RVV` · **Hardware:** RISC-V
- **ARTISAN: Unlocking LLM Kernel Optimization on Unfamiliar Hardware** [![OpenReview](https://img.shields.io/badge/OpenReview-26.09-lightgrey)](https://openreview.net/forum?id=f5EFsSJVUz)
  - **Type:** Agentic workflow · **Hardware:** AWS Neuron
- **ForgeMegakernel: A General Framework for Efficient Auto-Regressive Model Decode Megakernels** [![arXiv](https://img.shields.io/badge/arXiv-26.09-red)](https://arxiv.org/abs/2609.12379)
  - **Institution:** Tsinghua University, University of Chinese Academy of Sciences, ModelBest
  - **Type:** Agentic workflow · **Kernel:** `CUDA` · **Hardware:** NVIDIA
- **Argus: Orchestrating Cross-Layer GPU Performance Measurements around Semantic Regions** [![arXiv](https://img.shields.io/badge/arXiv-26.09-red)](https://arxiv.org/abs/2609.12299)
  - **Institution:** Princeton University, UC San Diego, Meta
  - **Type:** Agentic workflow · **Hardware:** NVIDIA
- **KernelCompass: Traversing the Feasible Resource Space of the Target GPU Toward a Task-Contracted Objective** [![OpenReview](https://img.shields.io/badge/OpenReview-26.09-lightgrey)](https://openreview.net/forum?id=RkwGoFufl8)
  - **Type:** Agentic workflow · **Hardware:** NVIDIA · **Benchmark:** KernelBench
- **ServingStudio** [![Stars](https://img.shields.io/github/stars/SyFI-ServingStudio/ServingStudio)](https://github.com/SyFI-ServingStudio/ServingStudio) [![Blog](https://img.shields.io/badge/Blog-UW-blue)](https://syfi.cs.washington.edu/blog/2026-09-24-introducing-servingstudio) [![Artifacts](https://img.shields.io/badge/Artifacts-GitHub-lightgrey)](https://github.com/sgl-project/sglang/pull/38560)
  - *Agent workbench that uses serving simulation, kernel profiling and hardware validation to implement kernel and serving-stack improvements.*
  - **Institution:** University of Washington · SyFI Lab
  - **Type:** Open-source / industry system · **Hardware:** NVIDIA

### 2026-08

- **Beyond Scaling: Self-Evolving LLM Agents for Hardware Kernel Optimization via an Experience-Driven Workflow and Experience Graph Memory** [![arXiv](https://img.shields.io/badge/arXiv-26.08-red)](https://arxiv.org/abs/2608.25570)
  - **Institution:** City University of Hong Kong, Huawei
  - **Type:** Agentic workflow · **Hardware:** Ascend, RISC-V
- **FABRICA: Agentic CUDA-to-CSL Translation and Optimization for Wafer-Scale Systems** [![arXiv](https://img.shields.io/badge/arXiv-26.08-red)](https://arxiv.org/abs/2608.25124)
  - **Institution:** University of Minnesota, Argonne National Laboratory, University of Chicago
  - **Type:** Trained model · **Kernel:** `CSL` · **Hardware:** Cerebras
- **LLM4LLM: Bridging Kernel Benchmarks and Real Deployment via Closed-Loop Agentic Optimization** [![arXiv](https://img.shields.io/badge/arXiv-26.08-red)](https://arxiv.org/abs/2608.21836) [![Stars](https://img.shields.io/github/stars/hzeng2000/LLM4LLM)](https://github.com/hzeng2000/LLM4LLM)
  - **Institution:** Xidian University, Zhongguancun Academy
  - **Type:** Agentic workflow · **Kernel:** `Triton` `CUDA` `TileLang` · **Hardware:** NVIDIA · **Benchmark:** KernelBench
- **HIERA: Workload-Aware Planning Across Implementation Spaces for GPU Kernel Optimization** [![arXiv](https://img.shields.io/badge/arXiv-26.08-red)](https://arxiv.org/abs/2608.21157)
  - **Institution:** Shanghai Jiao Tong University
  - **Type:** Agentic workflow · **Kernel:** `CUDA` · **Hardware:** NVIDIA · **Benchmark:** KernelBench
- **AsmEvo: Agentic Assembly-Level Optimization of AMD GPU Kernels with Functional Equivalence Verification** [![arXiv](https://img.shields.io/badge/arXiv-26.08-red)](https://arxiv.org/abs/2608.20711)
  - **Institution:** AMD, Southern University of Science and Technology
  - **Type:** Agentic workflow · **Kernel:** `AMDGPU ISA` · **Hardware:** AMD · **Benchmark:** KernelBench
- **RLEK: Reinforcement Learning from Environment Knowledge** [![OpenReview](https://img.shields.io/badge/OpenReview-26.08-lightgrey)](https://openreview.net/forum?id=trHfIrhMk3)
  - **Type:** Trained model · **Hardware:** NVIDIA
- **KernelWeaver: A Shape-Aware Kernel Agent for GPU Kernel Optimization** [![OpenReview](https://img.shields.io/badge/OpenReview-26.08-lightgrey)](https://openreview.net/forum?id=SaboBZsQiW)
  - **Type:** Agentic workflow · **Hardware:** NVIDIA
- **PTXBench: Evaluating and Adapting LLMs for GPU Kernel Optimization with Architecture-specific PTX** [![NeurIPS Workshop 2026](https://img.shields.io/badge/NeurIPS_Workshop-26-green)](https://arxiv.org/abs/2608.17379) [![Stars](https://img.shields.io/github/stars/zhang677/PTXBench)](https://github.com/zhang677/PTXBench) [![Model](https://img.shields.io/badge/Model-HuggingFace-yellow)](https://huggingface.co/collections/Genghan/ptxbench-qwen36-27b-sft-series) [![Dataset](https://img.shields.io/badge/Dataset-HuggingFace-yellow)](https://huggingface.co/datasets/AccRL/accrl-training) [![Blog](https://img.shields.io/badge/Blog-Stanford_University-blue)](https://zhang677.github.io/blog_md/ptxbench.html)
  - **Institution:** Stanford University, Carnegie Mellon University, RadixArk
  - **Type:** Trained model · **Kernel:** `CUDA` `PTX` `Triton` · **Hardware:** NVIDIA · **Benchmark:** FlashInfer-Bench
- **KernelArc: A Multi-Agent Framework for GPU Kernel Optimization** [![arXiv](https://img.shields.io/badge/arXiv-26.08-red)](https://arxiv.org/abs/2608.17071)
  - **Institution:** AI Labs, imec
  - **Type:** Search & evolution · **Kernel:** `CUDA` `PTX` `Triton` `CUTLASS` · **Hardware:** NVIDIA · **Benchmark:** SOL-ExecBench
- **CAKE: Compiler-Agent Co-Design for Frontier Kernel Evolution** [![arXiv](https://img.shields.io/badge/arXiv-26.08-red)](https://arxiv.org/abs/2608.12629) [![Artifacts](https://img.shields.io/badge/Artifacts-GitHub-lightgrey)](https://github.com/flashinfer-ai/flashinfer/issues/4254)
  - **Institution:** NVIDIA, Carnegie Mellon University
  - **Type:** Agentic workflow · **Kernel:** `CAKE IR` `CUDA` `PTX` · **Hardware:** NVIDIA
- **SparseDitto: An Agentic Sparse Compilation Framework through Architecture-Aware Synthesis on GPUs** [![arXiv](https://img.shields.io/badge/arXiv-26.08-red)](https://arxiv.org/abs/2608.05033)
  - **Institution:** University of Minnesota, Northeastern University
  - **Type:** Agentic workflow · **Kernel:** `CUDA` · **Hardware:** NVIDIA
- **LEAP** [![arXiv](https://img.shields.io/badge/arXiv-26.08-red)](https://arxiv.org/abs/2608.01804)
  - *Multi-turn code RL prunes environment feedback adaptively instead of returning every compiler/test detail.*
  - **Institution:** Moore Threads AI
  - **Type:** Trained model · **Kernel:** `CUDA` · **Hardware:** NVIDIA · **Benchmark:** KernelBench
- **Ascend Debug Agent** [![arXiv](https://img.shields.io/badge/arXiv-26.08-red)](https://arxiv.org/abs/2608.02712)
  - *Domain-specific repair loop for near-miss operators that already compile and run.*
  - **Institution:** City University of Hong Kong, Huawei
  - **Type:** Agentic workflow · **Kernel:** `Ascend C` · **Hardware:** Ascend · **Benchmark:** NPUKernelBench
- **Zomboss: Rethinking Agentic Kernel Generation for Emerging Accelerators** [![arXiv](https://img.shields.io/badge/arXiv-26.08-red)](https://arxiv.org/abs/2608.00894)
  - **Institution:** University of Michigan, University of Texas at Austin
  - **Type:** Agentic workflow · **Kernel:** `ACT` `TAIDL` · **Hardware:** Research accelerators
- **ForgeStencil: Automating Per-Case Stencil Specialization from Kernels to 100+ Real Applications** [![arXiv](https://img.shields.io/badge/arXiv-26.09-red)](https://arxiv.org/abs/2609.06694) [![Stars](https://img.shields.io/github/stars/OpenBMB/ForgeStencil)](https://github.com/OpenBMB/ForgeStencil)
  - **Institution:** OpenBMB
  - **Type:** Agentic workflow · **Kernel:** `CUDA` · **Hardware:** NVIDIA
- **CUDA-Harness: Harnessing Agentic CUDA Kernel Generation and Optimization from Natural Language** [![arXiv](https://img.shields.io/badge/arXiv-26.09-red)](https://arxiv.org/abs/2609.00058)
  - **Institution:** Shanghai Jiao Tong University
  - **Type:** Agentic workflow · **Kernel:** `CUDA` · **Hardware:** NVIDIA

### 2026-07

- **AgenticCANN: Automated Ascend C Operator Generation via Knowledge-Augmented Agentic Evolution** [![arXiv](https://img.shields.io/badge/arXiv-26.07-red)](https://arxiv.org/abs/2607.26661)
  - **Institution:** City University of Hong Kong, Hong Kong Yuwin Technology
  - **Type:** Search & evolution · **Kernel:** `Ascend C` · **Hardware:** Ascend
- **Compiler-Grounded Hierarchical Diagnosis for LLM-Based Triton Kernel Optimization** [![arXiv](https://img.shields.io/badge/arXiv-26.07-red)](https://arxiv.org/abs/2607.23089) [![Code](https://img.shields.io/badge/Code-GitCode-blue)](https://gitcode.com/cann/cannbot-skills)
  - **Institution:** Huawei
  - **Type:** Agentic workflow · **Kernel:** `Triton` · **Hardware:** Ascend · **Benchmark:** NPUKernelBench
- **CUDAPerf: Multi-turn RL with Structural and Performance Aware Rewards for CUDA Kernel Generation** [![arXiv](https://img.shields.io/badge/arXiv-26.07-red)](https://arxiv.org/abs/2607.20908)
  - **Institution:** Iowa State University, Cisco AI Research
  - **Type:** Trained model · **Kernel:** `CUDA` · **Hardware:** NVIDIA · **Benchmark:** KernelBench
- **Harness Engineering for LLM-Driven GPU Kernel Generation** [![arXiv](https://img.shields.io/badge/arXiv-26.07-red)](https://arxiv.org/abs/2607.17979) [![Stars](https://img.shields.io/github/stars/syhya/mlsys26-flashinfer-contest)](https://github.com/syhya/mlsys26-flashinfer-contest)
  - **Institution:** Baidu
  - **Type:** Agentic workflow · **Kernel:** `CUDA` `Triton` `CUTLASS` · **Hardware:** NVIDIA · **Benchmark:** FlashInfer-Bench
- **SHADB: From Custom-Fit to Portable: Bridging the Gap Between Synthesized and Engineered GPU Query Execution** [![arXiv](https://img.shields.io/badge/arXiv-26.07-red)](https://arxiv.org/abs/2607.07632) [![Stars](https://img.shields.io/gitlab/stars/dislab%2FSHADB?gitlab_url=https%3A%2F%2Fgitlab.eurecom.fr)](https://gitlab.eurecom.fr/dislab/SHADB)
  - **Institution:** EURECOM
  - **Type:** Agentic workflow · **Kernel:** `CUDA` `HIP` · **Hardware:** NVIDIA, AMD
- **NKI-Agent / ATX Custom NKI Agent** [![arXiv](https://img.shields.io/badge/arXiv-26.07-red)](https://arxiv.org/abs/2607.04395) [![Stars](https://img.shields.io/github/stars/aws-samples/sample-ATX-custom-NKI-Agent)](https://github.com/aws-samples/sample-ATX-custom-NKI-Agent)
  - *Compile-verify-fix agent plus domain SFT for Neuron kernels.*
  - **Institution:** AWS
  - **Type:** Trained model · **Kernel:** `NKI` · **Hardware:** AWS Neuron
- **Hawk: Harnessing Hardware-Aware Knowledge for High-Performance NPU Kernel Generation** [![arXiv](https://img.shields.io/badge/arXiv-26.07-red)](https://arxiv.org/abs/2607.01590)
  - **Institution:** Sun Yat-sen University, GBA National Technology Innovation Center, Peng Cheng Laboratory
  - **Type:** Trained model · **Kernel:** `Ascend C` · **Hardware:** Ascend · **Benchmark:** CANN-Bench, MultiKernelBench
- **GEAK v4** [![Stars](https://img.shields.io/github/stars/AMD-AGI/GEAK)](https://github.com/AMD-AGI/GEAK) [![Project](https://img.shields.io/badge/Project-Page-blue)](https://rocm.docs.amd.com/projects/geak/en/latest) [![Blog](https://img.shields.io/badge/Blog-AMD-blue)](https://www.amd.com/en/developer/resources/technical-articles/2026/geak-v4.html)
  - *AMD's multi-agent kernel optimizer spans HIP, Triton, FlyDSL, TileLang and Composable Kernel.*
  - **Institution:** AMD-AGI
  - **Type:** Open-source / industry system · **Kernel:** `HIP` `Triton` `FlyDSL` `TileLang` `Composable Kernel` · **Hardware:** AMD

### 2026-06

- **Experience Graphs: The Data Foundation for Self-Improving Agents** [![arXiv](https://img.shields.io/badge/arXiv-26.06-red)](https://arxiv.org/abs/2606.29823)
  - **Institution:** Meta, University of Maryland
  - **Type:** Trained model
- **EGG: An Expert-Guided Agent Framework for Kernel Generation** [![ICML 2026](https://img.shields.io/badge/ICML-26-green)](https://arxiv.org/abs/2606.26758)
  - **Institution:** Beihang University, Shanghai Jiao Tong University, Tsinghua University, Approaching.AI
  - **Type:** Agentic workflow · **Kernel:** `Triton` · **Hardware:** NVIDIA · **Benchmark:** KernelBench, TritonBench
- **KernelPro: Optimizing CUDA like a Human: Micro-Profiling Tools as Expert Surrogates for LLM-Based GPU Kernel Optimization** [![arXiv](https://img.shields.io/badge/arXiv-26.06-red)](https://arxiv.org/abs/2606.26453) [![Artifacts](https://img.shields.io/badge/Artifacts-arXiv-lightgrey)](https://arxiv.org/abs/2606.26453)
  - **Institution:** AWS, Siemens, University of Minnesota
  - **Type:** Search & evolution · **Kernel:** `CUDA` `CUTLASS` `CuTe` · **Hardware:** NVIDIA · **Benchmark:** KernelBench
- **SpecGen: Accelerating Agentic Kernel Optimization with Speculative Generation** [![arXiv](https://img.shields.io/badge/arXiv-26.06-red)](https://arxiv.org/abs/2606.17518)
  - **Institution:** Fudan University, Shanghai Jiao Tong University, Shanghai AI Laboratory, Hong Kong University of Science and Technology, CUHK, SenseTime Research
  - **Type:** Agentic workflow · **Kernel:** `CUDA` `Triton` · **Hardware:** NVIDIA · **Benchmark:** KernelBench
- **Hawkeye: Hardware-Aware GPU Kernel Optimization with Minimal Supervision** [![ICML Workshop 2026](https://img.shields.io/badge/ICML_Workshop-26-green)](https://openreview.net/forum?id=e3pxJbBRBk)
  - **Type:** Agentic workflow · **Hardware:** NVIDIA
- **daVinci-kernel: Co-Evolving Skill Selection, Summarization, and Utilization via RL for GPU Kernel Optimization** [![arXiv](https://img.shields.io/badge/arXiv-26.06-red)](https://arxiv.org/abs/2606.16497) [![Stars](https://img.shields.io/github/stars/GAIR-NLP/daVinci-kernel)](https://github.com/GAIR-NLP/daVinci-kernel)
  - **Institution:** Shanghai Innovation Institute, Shanghai Jiao Tong University, GAIR
  - **Type:** Trained model · **Kernel:** `CUDA` `Triton` · **Hardware:** NVIDIA · **Benchmark:** KernelBench
- **AutoMegaKernel: A Statically-Checked Agent Harness for Self-Retargeting Megakernel Synthesis** [![arXiv](https://img.shields.io/badge/arXiv-26.06-red)](https://arxiv.org/abs/2606.09682) [![Stars](https://img.shields.io/github/stars/RightNow-AI/AutoMegaKernel)](https://github.com/RightNow-AI/AutoMegaKernel)
  - **Institution:** RightNow AI (YC)
  - **Type:** Agentic workflow · **Kernel:** `CUDA` · **Hardware:** NVIDIA
- **AgentCompile: An LLM-Guided Compiler for Direct CUDA Inference** [![arXiv](https://img.shields.io/badge/arXiv-26.06-red)](https://arxiv.org/abs/2606.07665) [![Stars](https://img.shields.io/github/stars/veneno1213822/AgentCompile)](https://github.com/veneno1213822/AgentCompile)
  - **Institution:** City University of Hong Kong (Dongguan), City University of Hong Kong
  - **Type:** Agentic workflow · **Kernel:** `CUDA` · **Hardware:** NVIDIA
- **MusaCoder: Native GPU Kernel Generation with Full-Stack Training on Moore Threads GPU** [![arXiv](https://img.shields.io/badge/arXiv-26.06-red)](https://arxiv.org/abs/2606.04847) [![Model](https://img.shields.io/badge/Model-HuggingFace-yellow)](https://huggingface.co/MooreThreads/MusaCoder-27B)
  - **Institution:** Moore Threads
  - **Type:** Trained model · **Kernel:** `MUSA C` `CUDA` · **Hardware:** NVIDIA, Moore Threads · **Benchmark:** KernelBench
- **MoziFlux** [![Code unavailable](https://img.shields.io/badge/Code-unavailable-lightgrey)](https://github.com/BiSheng-Compiler-Agents/MoziFlux)
  - *Apache-2.0 Hermes-driven Triton-Ascend optimizer with CANN/cannsim local and remote gates, an episode store, a 100-task KernelBench L1 corpus, and checked-in optimized kernels with per-task reports.*
  - **Institution:** BiSheng-Compiler-Agents
  - **Type:** Open-source / industry system · **Kernel:** `Triton` · **Hardware:** Ascend
- **MKEvolve: A Modular Multi-Agent Framework for Kernel Code Generation** [![ICML Workshop 2026](https://img.shields.io/badge/ICML_Workshop-26-green)](https://arxiv.org/abs/2607.20501) [![Code unavailable](https://img.shields.io/badge/Code-unavailable-lightgrey)](https://github.com/amazon-science/ModularKernelEvolution)
  - **Institution:** University of British Columbia, AWS
  - **Type:** Search & evolution · **Kernel:** `Triton` · **Hardware:** NVIDIA · **Benchmark:** FlashInfer-Bench, KernelBench
- **Kernel Forge: An Agent Harness for LLM-based Generation and Optimization of CUDA Kernels** [![arXiv](https://img.shields.io/badge/arXiv-26.07-red)](https://arxiv.org/abs/2607.24762) [![Stars](https://img.shields.io/github/stars/TheJoshBrod/KernelForge)](https://github.com/TheJoshBrod/KernelForge)
  - **Institution:** University of Michigan
  - **Type:** Search & evolution · **Kernel:** `CUDA` `Triton` · **Hardware:** NVIDIA, AMD
- **Atrex Kernel Agent (AKA): Are LLM-Generated GPU Kernels Production-Ready? A Trace-Driven Benchmark and Optimization Agent** [![arXiv](https://img.shields.io/badge/arXiv-26.07-red)](https://arxiv.org/abs/2607.14541) [![Stars](https://img.shields.io/github/stars/alibaba/atrex-kernel-agent)](https://github.com/alibaba/atrex-kernel-agent) [![Release notes](https://img.shields.io/badge/Release-Notes-blue)](https://github.com/alibaba/atrex-kernel-agent/releases/tag/v0.3.0)
  - **Institution:** ATREX Team, Alibaba Group
  - **Type:** Agentic workflow · **Kernel:** `FlyDSL` `Triton` `CUDA` `Gluon` `CUTLASS` `CuTe` `TileLang` · **Hardware:** NVIDIA, AMD, T-Head PPU

### 2026-05

- **GPU Forecasters: Language Models as Selective Surrogates for Kernel Runtime Optimization** [![arXiv](https://img.shields.io/badge/arXiv-26.05-red)](https://arxiv.org/abs/2605.31464) [![Stars](https://img.shields.io/github/stars/codezakh/gpu-forecasters)](https://github.com/codezakh/gpu-forecasters) [![Model](https://img.shields.io/badge/Model-HuggingFace-yellow)](https://huggingface.co/codezakh/gpu-forecasters-gpt-oss-20b-correctness-brier) [![Dataset](https://img.shields.io/badge/Dataset-HuggingFace-yellow)](https://huggingface.co/datasets/codezakh/gpu-forecasters-puct-search-events)
  - **Institution:** University of North Carolina at Chapel Hill, Allen Institute for AI, Johns Hopkins University, University of Texas at Austin
  - **Type:** Trained model · **Hardware:** NVIDIA
- **HTAM: Hierarchical Transition-Attended Memory for Operator Optimization** [![arXiv](https://img.shields.io/badge/arXiv-26.05-red)](https://arxiv.org/abs/2605.29734)
  - **Institution:** University of Chinese Academy of Sciences, Institute of Automation (CAS), Zhongguancun Academy, Renmin University of China, XinZhuAI
  - **Type:** Search & evolution · **Kernel:** `CUDA` · **Hardware:** NVIDIA · **Benchmark:** KernelBench
- **KLineage: Recovering the Missing When of Kernel Optimization by Deoptimizing Experts** [![arXiv](https://img.shields.io/badge/arXiv-26.05-red)](https://arxiv.org/abs/2605.28213) [![Stars](https://img.shields.io/github/stars/ict-agent/klineage)](https://github.com/ict-agent/klineage)
  - **Institution:** Institute of Computing Technology (CAS), University of Chinese Academy of Sciences, Xi'an Jiaotong University
  - **Type:** Agentic workflow · **Hardware:** NVIDIA, Ascend · **Benchmark:** KernelBench, MultiKernelBench
- **Step-TP: A Grounded, Step-Level Dataset with Chain-of-Thought Reasoning for LLM-Guided Tensor Program Optimization** [![arXiv](https://img.shields.io/badge/arXiv-26.05-red)](https://arxiv.org/abs/2605.25954) [![Stars](https://img.shields.io/github/stars/LIUMENGFAN-gif/StepTP)](https://github.com/LIUMENGFAN-gif/StepTP)
  - **Institution:** University of Hong Kong, Ant Group, University of Science and Technology of China
  - **Type:** Trained model · **Kernel:** `TVM` · **Hardware:** NVIDIA
- **CODA: Rewriting Transformer Blocks as GEMM-Epilogue Programs** [![arXiv](https://img.shields.io/badge/arXiv-26.05-red)](https://arxiv.org/abs/2605.19269) [![Stars](https://img.shields.io/github/stars/open-lm-engine/coda-kernels)](https://github.com/open-lm-engine/coda-kernels)
  - **Institution:** MIT, Princeton University, Meta, Together AI
  - **Type:** Agentic workflow · **Kernel:** `CODA` · **Hardware:** NVIDIA
- **AlphaEvolve for FHE on TPUs: Adapting AlphaEvolve to Optimize Fully Homomorphic Encryption on TPUs** [![ISCA Workshop 2026](https://img.shields.io/badge/ISCA_Workshop-26-green)](https://arxiv.org/abs/2605.14718)
  - **Institution:** Google
  - **Type:** Search & evolution · **Kernel:** `JAX` · **Hardware:** Google TPU
- **Kernel Foundry: A Diagnosis-driven Evolutionary Kernel Optimizer with Multi-Experts** [![arXiv](https://img.shields.io/badge/arXiv-26.05-red)](https://arxiv.org/abs/2605.30359)
  - **Institution:** Chinese University of Hong Kong, Huawei
  - **Type:** Search & evolution · **Hardware:** NVIDIA · **Benchmark:** KernelBench
- **KEET: Explaining Performance of GPU Kernels Using LLM Agents** [![arXiv](https://img.shields.io/badge/arXiv-26.05-red)](https://arxiv.org/abs/2605.04467)
  - **Institution:** University of Maryland, NVIDIA, Lawrence Livermore National Laboratory
  - **Type:** Single-pass / tooling · **Kernel:** `CUDA` · **Hardware:** NVIDIA
- **CuBridge: An LLM-Based Framework for Understanding and Reconstructing High-Performance Attention Kernels** [![ACL 2026](https://img.shields.io/badge/ACL-26-green)](https://arxiv.org/abs/2605.05023)
  - **Institution:** Shanghai Jiao Tong University
  - **Type:** Agentic workflow · **Kernel:** `CUDA` · **Hardware:** NVIDIA · **Benchmark:** FlashInfer-Bench
- **Qwen3.7-Max Autonomous Kernel Optimization** [![Blog](https://img.shields.io/badge/Blog-Qwen-blue)](https://qwen.ai/blog?id=qwen3.7)
  - *Qwen3.7-Max autonomously optimized SGLang's Extend Attention Kernel for a previously-unseen accelerator (T-Head Zhenwu M890 PPU, styled 'ZW-M890' in Qwen's own blog) with no hardware docs/reference ke.*
  - **Institution:** Alibaba (Qwen Team)
  - **Type:** Open-source / industry system · **Kernel:** `Triton` · **Hardware:** T-Head PPU
- **MoE-Kernel-Agent: Full-Agent Technical Write-up** [![Stars](https://img.shields.io/github/stars/Jerry2423/MoE-Kernel-Agent)](https://github.com/Jerry2423/MoE-Kernel-Agent)
  - **Type:** Open-source / industry system · **Kernel:** `Triton` · **Hardware:** NVIDIA · **Benchmark:** FlashInfer-Bench
- **KernelBrain: Coarse-to-Fine, Budget-Aware Search for Agentic GPU Kernel Optimization** [![arXiv](https://img.shields.io/badge/arXiv-26.08-red)](https://arxiv.org/abs/2608.02611)
  - **Institution:** Microsoft
  - **Type:** Search & evolution · **Kernel:** `Triton` · **Hardware:** NVIDIA
- **Kernel Design Agents (KDA): Developing GPU Kernels with Agentic Loops** [![Stars](https://img.shields.io/github/stars/NVlabs/kda)](https://github.com/NVlabs/kda)
  - **Institution:** MIT HAN Lab
  - **Type:** Open-source / industry system · **Kernel:** `CUDA` · **Hardware:** NVIDIA · **Benchmark:** FlashInfer-Bench
- **KDA-Pilot** [![Stars](https://img.shields.io/github/stars/BBuf/KDA-Pilot)](https://github.com/BBuf/KDA-Pilot)
  - *Evidence-first autonomous SGLang kernel-optimization campaigns with production baselines, strict correctness gates, NCU/KernelWiki evidence, and replayable logs.*
  - **Institution:** RadixArk
  - **Type:** Open-source / industry system · **Kernel:** `Triton` `CUDA` `CUTLASS` · **Hardware:** NVIDIA
- **FlashInfer MLSys 2026 GDN Kernel - Team Kachua** [![Report](https://img.shields.io/badge/Report-26.05-blue)](https://github.com/flashinfer-ai/mlsys26-contest/blob/2f87893/writeups/Kachua-GDN-Agent-Assisted.pdf) [![Stars](https://img.shields.io/github/stars/romitjain/kachua-mlsys)](https://github.com/romitjain/kachua-mlsys)
  - **Type:** Agentic workflow · **Hardware:** NVIDIA · **Benchmark:** FlashInfer-Bench
- **Houmao Agentic Kernel Optimization: Agentic Kernel Optimization: Generating State-of-the-Art GPU Kernels Without Hand-Written CUDA** [![arXiv](https://img.shields.io/badge/arXiv-26.08-red)](https://arxiv.org/abs/2608.14560) [![Stars](https://img.shields.io/github/stars/igamenovoer/houmao)](https://github.com/igamenovoer/houmao) [![Artifacts](https://img.shields.io/badge/Artifacts-GitHub-lightgrey)](https://github.com/CodeGandee/flashinfer-bench-starter-kit/tree/main/solution/cuda)
  - **Institution:** Intellifusion
  - **Type:** Agentic workflow · **Kernel:** `CUDA` `CUTLASS` · **Hardware:** NVIDIA · **Benchmark:** FlashInfer-Bench
- **cuda-opt-agent** [![Stars](https://img.shields.io/github/stars/KernelFlow-ops/cuda-opt-agent)](https://github.com/KernelFlow-ops/cuda-opt-agent)
  - *LangGraph-orchestrated agent for CUDA kernel optimization with an nvcc compile+correctness gate, adaptive 3-phase NCU profiling, and multi-GPU hyperparameter search.*
  - **Type:** Open-source / industry system · **Kernel:** `CUDA` · **Hardware:** NVIDIA
- **Auto GPU Kernel: Autonomous Kernel Discovery for DeepSeek Sparse Attention** [![Stars](https://img.shields.io/github/stars/Dogacel/auto-gpu-kernel)](https://github.com/Dogacel/auto-gpu-kernel)
  - **Institution:** fal
  - **Type:** Open-source / industry system · **Kernel:** `Triton` · **Hardware:** NVIDIA · **Benchmark:** FlashInfer-Bench
- **AMDKernelVault: Large-Scale Datasets and Agentic Training for AMD GPU Kernel Optimization** [![arXiv](https://img.shields.io/badge/arXiv-26.09-red)](https://arxiv.org/abs/2609.12471) [![Stars](https://img.shields.io/github/stars/AMD-AGI/AMDKernelVault)](https://github.com/AMD-AGI/AMDKernelVault) [![Dataset](https://img.shields.io/badge/Dataset-HuggingFace-yellow)](https://huggingface.co/datasets/amd/AIG-Datasets)
  - **Institution:** AMD
  - **Type:** Trained model · **Kernel:** `HIP` `Triton` · **Hardware:** AMD · **Benchmark:** KernelBench, TritonBench
- **AKO4X: AKO: Agentic Kernel Optimization** [![Stars](https://img.shields.io/github/stars/TongmingLAIC/AKO4X)](https://github.com/TongmingLAIC/AKO4X)
  - **Institution:** TLAIC
  - **Type:** Open-source / industry system · **Kernel:** `Triton` `CUDA` `TileLang` `CUTLASS` `CuTe` · **Hardware:** NVIDIA · **Benchmark:** FlashInfer-Bench

### 2026-04

- **LEGO: An LLM-Enabled Hierarchical Optimizer for Tensor Computation Graphs with Structure-Aware Search and Compositional Synthesis** [![ICML 2026](https://img.shields.io/badge/ICML-26-green)](https://openreview.net/forum?id=kYqJ5gGjHE) [![Stars](https://img.shields.io/github/stars/mmt-at/LEGO)](https://github.com/mmt-at/LEGO)
  - **Institution:** Institute of Computing Technology (CAS), University of Chinese Academy of Sciences, University of New South Wales, University of Leeds
  - **Type:** Search & evolution · **Hardware:** NVIDIA
- **FACT: Compositional Kernel Synthesis with a Three-Stage Agentic Workflow** [![arXiv](https://img.shields.io/badge/arXiv-26.04-red)](https://arxiv.org/abs/2604.26666)
  - **Institution:** Virginia Tech
  - **Type:** Agentic workflow · **Kernel:** `CUTLASS` · **Hardware:** NVIDIA · **Benchmark:** KernelBench
- **AdaExplore: Failure-Driven Adaptation and Diversity-Preserving Search for Efficient Kernel Generation** [![COLM Workshop 2026](https://img.shields.io/badge/COLM_Workshop-26-green)](https://arxiv.org/abs/2604.16625) [![Stars](https://img.shields.io/github/stars/StigLidu/AdaExplore)](https://github.com/StigLidu/AdaExplore)
  - **Institution:** Carnegie Mellon University
  - **Type:** Agentic workflow · **Kernel:** `CUDA` · **Hardware:** NVIDIA · **Benchmark:** FlashInfer-Bench, KernelBench, TritonBench
- **Ave: Guiding Agentic GPU Optimization Using Data-Flow Invariants** [![SOSP 2026](https://img.shields.io/badge/SOSP-26-green)](https://arxiv.org/abs/2604.18616)
  - **Institution:** CausalFlow, Hong Kong University of Science and Technology, University of Chinese Academy of Sciences, UC Riverside, Tsinghua University, Stanford University
  - **Type:** Agentic workflow · **Kernel:** `HIP` · **Hardware:** AMD · **Benchmark:** KernelBench
- **Record-Remix-Replay: Hierarchical GPU Kernel Optimization using Evolutionary Search** [![arXiv](https://img.shields.io/badge/arXiv-26.04-red)](https://arxiv.org/abs/2604.11109) [![Stars](https://img.shields.io/github/stars/llnl/Mneme)](https://github.com/llnl/Mneme)
  - **Institution:** Lawrence Livermore National Laboratory
  - **Type:** Search & evolution · **Hardware:** NVIDIA, AMD
- **CuTeGen: An LLM-Based Agentic Framework for Generation and Optimization of High-Performance GPU Kernels using CuTe** [![arXiv](https://img.shields.io/badge/arXiv-26.04-red)](https://arxiv.org/abs/2604.01489) [![Stars](https://img.shields.io/github/stars/taratt/cutegen)](https://github.com/taratt/cutegen)
  - **Institution:** University of Toronto, Standard Kernel
  - **Type:** Agentic workflow · **Kernel:** `CuTe` · **Hardware:** NVIDIA · **Benchmark:** KernelBench
- **TileGym** [![Stars](https://img.shields.io/github/stars/NVIDIA/TileGym)](https://github.com/NVIDIA/TileGym) [![Blog](https://img.shields.io/badge/Blog-NVIDIA-blue)](https://developer.nvidia.com/blog/automating-gpu-kernel-translation-with-ai-agents-cutile-python-to-cutile-jl)
  - *LLM agent 'skill' auto-translating cuTile Python kernels to cuTile.jl (Julia) in one validated pass (17 rules, static validator).*
  - **Institution:** NVIDIA
  - **Type:** Open-source / industry system · **Kernel:** `cuTile` · **Hardware:** NVIDIA
- **Neuron Agentic Development** [![Stars](https://img.shields.io/github/stars/aws-neuron/neuron-agentic-development)](https://github.com/aws-neuron/neuron-agentic-development) [![Blog](https://img.shields.io/badge/Blog-AWS-blue)](https://aws.amazon.com/blogs/machine-learning/stop-hand-tuning-kernels-how-neuron-agentic-development-accelerates-aws-trainium-optimizations)
  - *Open-source agent/skill toolkit for the NKI kernel lifecycle: authoring, debugging, profiling, performance optimization, and API migration on Trainium and Inferentia.*
  - **Institution:** AWS
  - **Type:** Open-source / industry system · **Kernel:** `NKI` · **Hardware:** AWS Neuron
- **Cursor Multi-Agent Kernel Optimization** [![Blog](https://img.shields.io/badge/Blog-Cursor-blue)](https://cursor.com/blog/multi-agent-kernels) [![Artifacts](https://img.shields.io/badge/Artifacts-GitHub-lightgrey)](https://github.com/anysphere/kernel-optimization-results)
  - *Planner + autonomous parallel workers optimized 235 kernels from 124+ open-source models (CUDA C w/ inline PTX and CuTe DSL) on 27x Blackwell B200 over 3 weeks using NVIDIA's SOL-ExecBench test-debug-.*
  - **Institution:** Cursor, NVIDIA
  - **Type:** Open-source / industry system · **Kernel:** `CUDA` `CUTLASS` `CuTe` `PTX` · **Hardware:** NVIDIA · **Benchmark:** SOL-ExecBench

### 2026-03

- **muCUTLASS + Speed-of-Light Guidance: Improving Efficiency of GPU Kernel Optimization Agents using a Domain-Specific Language and Speed-of-Light Guidance** [![arXiv](https://img.shields.io/badge/arXiv-26.03-red)](https://arxiv.org/abs/2603.29010)
  - **Institution:** NVIDIA, Stanford University
  - **Type:** Agentic workflow · **Kernel:** `CUTLASS` · **Hardware:** NVIDIA · **Benchmark:** KernelBench
- **Kernel-Smith: A Unified Recipe for Evolutionary Kernel Optimization** [![ICML Workshop 2026](https://img.shields.io/badge/ICML_Workshop-26-green)](https://arxiv.org/abs/2603.28342)
  - **Institution:** Shanghai AI Laboratory
  - **Type:** Trained model · **Kernel:** `Triton` · **Hardware:** NVIDIA · **Benchmark:** KernelBench
- **AVO: Agentic Variation Operators for Autonomous Evolutionary Search** [![arXiv](https://img.shields.io/badge/arXiv-26.03-red)](https://arxiv.org/abs/2603.24517) [![Project](https://img.shields.io/badge/Project-Page-blue)](https://github.com/austin1997/AVO)
  - **Institution:** NVIDIA, OctoML
  - **Type:** Search & evolution · **Kernel:** `CUDA` `PTX` · **Hardware:** NVIDIA
- **AscendOptimizer: Episodic Agent for Ascend NPU Operator Optimization** [![arXiv](https://img.shields.io/badge/arXiv-26.03-red)](https://arxiv.org/abs/2603.23566)
  - **Institution:** East China Normal University, Tongji University
  - **Type:** Agentic workflow · **Kernel:** `Ascend C` · **Hardware:** Ascend
- **DRTriton: Large-Scale Synthetic Data Driven Reinforcement Learning for Triton Kernel Generation** [![arXiv](https://img.shields.io/badge/arXiv-26.03-red)](https://arxiv.org/abs/2603.21465)
  - **Institution:** Texas A&M University
  - **Type:** Trained model · **Kernel:** `Triton` · **Hardware:** NVIDIA · **Benchmark:** KernelBench
- **AutoKernel: Autonomous GPU Kernel Optimization via Iterative Agent-Driven Search** [![arXiv](https://img.shields.io/badge/arXiv-26.03-red)](https://arxiv.org/abs/2603.21331) [![Stars](https://img.shields.io/github/stars/RightNow-AI/autokernel)](https://github.com/RightNow-AI/autokernel)
  - **Institution:** RightNow AI (YC)
  - **Type:** Agentic workflow · **Kernel:** `CUDA` `Triton` · **Hardware:** NVIDIA
- **KernelFoundry: Hardware-Aware Evolutionary GPU Kernel Optimization** [![ICML 2026](https://img.shields.io/badge/ICML-26-green)](https://arxiv.org/abs/2603.12440)
  - **Institution:** Intel
  - **Type:** Search & evolution · **Kernel:** `SYCL` `CUDA` · **Hardware:** NVIDIA, Intel · **Benchmark:** KernelBench
- **EvoKernel: Towards Cold-Start Drafting and Continual Refining: A Value-Driven Memory Approach with Application to NPU Kernel Synthesis** [![ICML 2026](https://img.shields.io/badge/ICML-26-green)](https://arxiv.org/abs/2603.10846) [![Project](https://img.shields.io/badge/Project-Page-blue)](https://evokernel.zhuo.li)
  - **Institution:** Shanghai Jiao Tong University
  - **Type:** Trained model · **Kernel:** `Ascend C` · **Hardware:** Ascend · **Benchmark:** KernelBench
- **KernelSkill: KernelClaw: A Multi-Agent Framework for GPU Kernel Optimization with Dual-Memory Mechanisms** [![arXiv](https://img.shields.io/badge/arXiv-26.03-red)](https://arxiv.org/abs/2603.10085) [![Stars](https://img.shields.io/github/stars/0satan0/KernelMem)](https://github.com/0satan0/KernelMem)
  - **Institution:** Beihang University
  - **Type:** Agentic workflow · **Kernel:** `CUDA` · **Hardware:** NVIDIA · **Benchmark:** KernelBench, TritonBench
- **CUDAMaster: Making LLMs Optimize Multi-Scenario CUDA Kernels Like Experts** [![arXiv](https://img.shields.io/badge/arXiv-26.03-red)](https://arxiv.org/abs/2603.07169) [![Project](https://img.shields.io/badge/Project-Page-blue)](https://hanyx2021.github.io/MSKernelBenchDemo)
  - **Institution:** Tsinghua University
  - **Type:** Agentic workflow · **Kernel:** `CUDA` · **Hardware:** NVIDIA
- **StitchCUDA: An Automated Multi-Agents End-to-End GPU Programing Framework with Rubric-based Agentic Reinforcement Learning** [![ICML 2026](https://img.shields.io/badge/ICML-26-green)](https://arxiv.org/abs/2603.02637)
  - **Institution:** University of Minnesota
  - **Type:** Trained model · **Kernel:** `CUDA` · **Hardware:** NVIDIA · **Benchmark:** KernelBench
- **CUCo: An Agentic Framework for Compute and Communication Co-design** [![arXiv](https://img.shields.io/badge/arXiv-26.03-red)](https://arxiv.org/abs/2603.02376) [![Stars](https://img.shields.io/github/stars/UT-InfraAI/cuco)](https://github.com/UT-InfraAI/cuco)
  - **Institution:** University of Texas at Austin
  - **Type:** Search & evolution · **Kernel:** `CUDA` · **Hardware:** NVIDIA
- **DSL-Monkeys: Self-Generated In-Context Examples for Low-Resource GPU DSL Kernels** [![ICLR Workshop 2026](https://img.shields.io/badge/ICLR_Workshop-26-green)](https://openreview.net/forum?id=2yS4j1C3zi)
  - **Type:** Trained model · **Kernel:** `TileLang` `ThunderKittens` · **Hardware:** NVIDIA · **Benchmark:** KernelBench
- **Standard Kernel** [![Blog](https://img.shields.io/badge/Blog-Standard_Kernel-blue)](https://standardkernel.com/blog/announcing-our-seed-round-is-kernel-generation-solved)
  - *Hybrid program-analysis + LLM reasoning at the PTX layer across Triton / TileLang / ThunderKittens / CUTLASS.*
  - **Institution:** Standard Kernel
  - **Type:** Open-source / industry system · **Kernel:** `PTX` · **Hardware:** NVIDIA
- **ROCm Hyperloom** [![Stars](https://img.shields.io/github/stars/AMD-AGI/Hyperloom)](https://github.com/AMD-AGI/Hyperloom) [![Project](https://img.shields.io/badge/Project-Page-blue)](https://rocm.docs.amd.com/projects/hyperloom/en/latest/index.html) [![Blog](https://img.shields.io/badge/Blog-AMD-blue)](https://rocm.blogs.amd.com/software-tools-optimization/hyperloom-optimization/README.html) [![Artifacts](https://img.shields.io/badge/Artifacts-GitHub-lightgrey)](https://github.com/AMD-AGI/Hyperloom/tree/79856335c65047ac11264132167def97047f83e5/.cursor/skills/inference-optimization/results/qwen3-14b-mi355x)
  - *Multi-agent inference optimization across serving settings, framework source, and generated GPU kernels, with independent end-to-end measurement and a reusable recipe knowledge base.*
  - **Institution:** AMD
  - **Type:** Open-source / industry system · **Kernel:** `HIP` `Triton` `FlyDSL` · **Hardware:** AMD
- **PyTorch KernelAgent** [![Stars](https://img.shields.io/github/stars/meta-pytorch/KernelAgent)](https://github.com/meta-pytorch/KernelAgent) [![Blog](https://img.shields.io/badge/Blog-PyTorch-blue)](https://pytorch.org/blog/kernelagent-hardware-guided-gpu-kernel-optimization-via-multi-agent-orchestration)
  - *5-agent system (Profiler / Judge / Analyze / Orchestrator / Benchmark) + NCU + roofline.*
  - **Institution:** Meta
  - **Type:** Open-source / industry system · **Kernel:** `Triton` · **Hardware:** NVIDIA · **Benchmark:** KernelBench
- **MaxKernel: Agentic Kernel Generation for TPUs** [![NeurIPS Workshop 2026](https://img.shields.io/badge/NeurIPS_Workshop-26-green)](https://arxiv.org/abs/2609.04523) [![Code](https://img.shields.io/badge/Code-GitHub-blue)](https://github.com/AI-Hypercomputer/accelerator-agents/tree/main/maxkernel/adk) [![Dataset](https://img.shields.io/badge/Dataset-GitHub-yellow)](https://github.com/AI-Hypercomputer/accelerator-agents/tree/main/JAXBench) [![Blog](https://img.shields.io/badge/Blog-Google-blue)](https://discuss.google.dev/t/maxkernel-automating-pallas-kernel-generation-and-optimization-via-agentic-systems/366686) [![Artifacts](https://img.shields.io/badge/Artifacts-GitHub-lightgrey)](https://github.com/AI-Hypercomputer/accelerator-agents/tree/main/maxkernel/adk/evaluation)
  - **Institution:** Google, Google DeepMind
  - **Type:** Search & evolution · **Kernel:** `Pallas` `JAX` · **Hardware:** Google TPU
- **CANNBot Skills** [![Code](https://img.shields.io/badge/Code-GitCode-blue)](https://gitcode.com/cann/cannbot-skills) [![Changelog](https://img.shields.io/badge/Changelog-GitCode-blue)](https://gitcode.com/cann/cannbot-skills/blob/master/CHANGELOG.md)
  - *Public plugin/agent/skill suite for staged NPU-operator development: architect, developer, reviewer and tester workflows cover direct and registered Ascend C kernels plus Catlass, PyPTO, TileLang and.*
  - **Institution:** Huawei CANN
  - **Type:** Open-source / industry system · **Kernel:** `Ascend C` `Catlass` `PyPTO` `TileLang` `Triton` · **Hardware:** Ascend
- **AscendOpGenAgent** [![Stars](https://img.shields.io/github/stars/Just-it/AscendOpGenAgent)](https://github.com/Just-it/AscendOpGenAgent) [![Artifacts](https://img.shields.io/badge/Artifacts-GitHub-lightgrey)](https://github.com/Just-it/AscendOpGenAgent/tree/main/archive_tasks)
  - *Claude Code agent and skill workflows generate and validate Triton-Ascend and Ascend C operators, with batch evaluation and an AutoResearch plan/edit/evaluate/keep-or-discard loop.*
  - **Type:** Open-source / industry system · **Kernel:** `Triton` `Ascend C` · **Hardware:** Ascend
- **AKO / AKO4ALL** [![Stars](https://img.shields.io/github/stars/TongmingLAIC/AKO4ALL)](https://github.com/TongmingLAIC/AKO4ALL) [![Project](https://img.shields.io/badge/Project-Page-blue)](https://tongminglaic.github.io/AKO)
  - *Generic coding-agent harness for kernel optimization.*
  - **Institution:** TLAIC
  - **Type:** Open-source / industry system · **Kernel:** `Triton` `CUDA` `TileLang` · **Hardware:** NVIDIA · **Benchmark:** SOL-ExecBench

### 2026-02

- **CUDA Agent: Large-Scale Agentic RL for High-Performance CUDA Kernel Generation** [![arXiv](https://img.shields.io/badge/arXiv-26.02-red)](https://arxiv.org/abs/2602.24286) [![Stars](https://img.shields.io/github/stars/BytedTsinghua-SIA/CUDA-Agent)](https://github.com/BytedTsinghua-SIA/CUDA-Agent) [![Dataset](https://img.shields.io/badge/Dataset-HuggingFace-yellow)](https://huggingface.co/datasets/BytedTsinghua-SIA/CUDA-Agent-Ops-6K) [![Project](https://img.shields.io/badge/Project-Page-blue)](https://cuda-agent.github.io)
  - **Institution:** ByteDance, Tsinghua University
  - **Type:** Trained model · **Kernel:** `CUDA` · **Hardware:** NVIDIA · **Benchmark:** KernelBench
- **K-Search: LLM Kernel Generation via Co-Evolving Intrinsic World Model** [![arXiv](https://img.shields.io/badge/arXiv-26.02-red)](https://arxiv.org/abs/2602.19128) [![Stars](https://img.shields.io/github/stars/caoshiyi/K-Search)](https://github.com/caoshiyi/K-Search)
  - **Institution:** UC Berkeley
  - **Type:** Search & evolution · **Kernel:** `CUDA` · **Hardware:** NVIDIA · **Benchmark:** FlashInfer-Bench
- **KernelBlaster: Continual Cross-Task CUDA Optimization via Memory-Augmented In-Context Reinforcement Learning** [![arXiv](https://img.shields.io/badge/arXiv-26.02-red)](https://arxiv.org/abs/2602.14293)
  - **Institution:** NVIDIA, UC Berkeley
  - **Type:** Trained model · **Kernel:** `CUDA` · **Hardware:** NVIDIA · **Benchmark:** KernelBench
- **OptiML: An End-to-End Framework for Program Synthesis and CUDA Kernel Optimization** [![arXiv](https://img.shields.io/badge/arXiv-26.02-red)](https://arxiv.org/abs/2602.12305)
  - **Institution:** Iowa State University
  - **Type:** Trained model · **Kernel:** `CUDA` · **Hardware:** NVIDIA
- **DICE: Diffusion Large Language Models Excel at Generating CUDA Kernels** [![arXiv](https://img.shields.io/badge/arXiv-26.02-red)](https://arxiv.org/abs/2602.11715) [![Stars](https://img.shields.io/github/stars/deadlykitten4/DICE)](https://github.com/deadlykitten4/DICE)
  - **Institution:** Westlake University
  - **Type:** Trained model · **Kernel:** `CUDA` · **Hardware:** NVIDIA · **Benchmark:** KernelBench
- **Makora: Fine-Tuning GPT-5 for GPU Kernel Generation** [![arXiv](https://img.shields.io/badge/arXiv-26.02-red)](https://arxiv.org/abs/2602.11000)
  - **Institution:** Makora
  - **Type:** Trained model · **Kernel:** `Triton` · **Hardware:** NVIDIA · **Benchmark:** KernelBench
- **Surprisal-Guided Selection: Compute-Optimal Test-Time Strategies for Execution-Grounded Code Generation** [![arXiv](https://img.shields.io/badge/arXiv-26.02-red)](https://arxiv.org/abs/2602.07670) [![Stars](https://img.shields.io/github/stars/jbarnes850/test-time-training)](https://github.com/jbarnes850/test-time-training) [![Model](https://img.shields.io/badge/Model-HuggingFace-yellow)](https://huggingface.co/Jarrodbarnes/KernelBench-RLVR-120b)
  - **Institution:** Arc Intelligence
  - **Type:** Trained model · **Benchmark:** KernelBench
- **DR. KERNEL: Reinforcement Learning Done Right for Triton Kernel Generations** [![ICML 2026](https://img.shields.io/badge/ICML-26-green)](https://arxiv.org/abs/2602.05885) [![Stars](https://img.shields.io/github/stars/hkust-nlp/KernelGYM)](https://github.com/hkust-nlp/KernelGYM)
  - **Institution:** Hong Kong University of Science and Technology
  - **Type:** Trained model · **Kernel:** `Triton` · **Hardware:** NVIDIA · **Benchmark:** KernelBench
- **Apex** [![Stars](https://img.shields.io/github/stars/AMD-AGI/Apex)](https://github.com/AMD-AGI/Apex)
  - *Agent harness (Claude Code/Codex/Cursor Agent backends) that iterates HIP/Triton kernels against a compile+correctness+speedup grader across 12 LLM-serving kernel types (flash attn, MoE, GEMM, RoPE, K.*
  - **Institution:** AMD
  - **Type:** Open-source / industry system · **Kernel:** `HIP` `Triton` · **Hardware:** AMD

### 2026-01

- **AscendCraft: Automatic Ascend NPU Kernel Generation via DSL-Guided Transcompilation** [![arXiv](https://img.shields.io/badge/arXiv-26.01-red)](https://arxiv.org/abs/2601.22760)
  - **Institution:** Nanjing University, Huawei
  - **Type:** Agentic workflow · **Kernel:** `Ascend C` · **Hardware:** Ascend · **Benchmark:** MultiKernelBench
- **SparseRL: Mastering Sparse CUDA Generation through Pretrained Models and Deep Reinforcement Learning** [![ICLR 2026](https://img.shields.io/badge/ICLR-26-green)](https://openreview.net/forum?id=VdLEaGPYWT) [![Stars](https://img.shields.io/github/stars/QiWu-NCIC/SparseRL)](https://github.com/QiWu-NCIC/SparseRL)
  - **Institution:** Institute of Computing Technology (CAS), University of Chinese Academy of Sciences, Hong Kong University of Science and Technology
  - **Type:** Trained model · **Kernel:** `CUDA` · **Hardware:** NVIDIA
- **A Two-Stage GPU Kernel Tuner Combining Semantic Refactoring and Search-Based Optimization** [![arXiv](https://img.shields.io/badge/arXiv-26.01-red)](https://arxiv.org/abs/2601.12698)
  - **Institution:** Nankai University, Beijing Institute of Computer Technology and Applications
  - **Type:** Agentic workflow · **Kernel:** `CUDA` · **Hardware:** NVIDIA
- **AscendKernelGen: LLM-Driven Kernel Generation for NPUs** [![ACL Findings 2026](https://img.shields.io/badge/ACL_Findings-26-green)](https://arxiv.org/abs/2601.07160) [![Dataset](https://img.shields.io/badge/Dataset-HuggingFace-yellow)](https://huggingface.co/datasets/AscendKernelGen/Ascend-COT-v1)
  - **Institution:** Peng Cheng Laboratory
  - **Type:** Trained model · **Kernel:** `Ascend C` · **Hardware:** Ascend · **Benchmark:** NPUKernelBench
- **Xe-Forge: Multi-Stage LLM-Powered Kernel Optimization for Intel GPU** [![Stars](https://img.shields.io/github/stars/IntelLabs/Xe-Forge)](https://github.com/IntelLabs/Xe-Forge)
  - **Institution:** Intel Labs
  - **Type:** Open-source / industry system · **Kernel:** `Triton` · **Hardware:** Intel · **Benchmark:** KernelBench
- **TT-Lang + Claude Skills** [![Stars](https://img.shields.io/github/stars/tenstorrent/tt-lang)](https://github.com/tenstorrent/tt-lang)
  - *Python-embedded DSL for Tenstorrent hardware with AI codegen in the loop.*
  - **Institution:** Tenstorrent
  - **Type:** Open-source / industry system · **Kernel:** `TT-Lang` · **Hardware:** Tenstorrent
- **GEAK-Triton v2** [![Stars](https://img.shields.io/github/stars/AMD-AGI/GEAK)](https://github.com/AMD-AGI/GEAK) [![Blog](https://img.shields.io/badge/Blog-AMD-blue)](https://rocm.blogs.amd.com/artificial-intelligence/geak-agents-family/README.html)
  - *Extension of the GEAK family for AMD GPUs.*
  - **Institution:** AMD-AGI
  - **Type:** Open-source / industry system · **Kernel:** `Triton` · **Hardware:** AMD
- **GEAK-HIP** [![Stars](https://img.shields.io/github/stars/AMD-AGI/GEAK)](https://github.com/AMD-AGI/GEAK) [![Blog](https://img.shields.io/badge/Blog-AMD-blue)](https://rocm.blogs.amd.com/software-tools-optimization/geak-hip-optimizations/README.html)
  - *GEAK extension for iterative HIP-kernel optimization on AMD GPUs.*
  - **Institution:** AMD-AGI
  - **Type:** Open-source / industry system · **Kernel:** `HIP` · **Hardware:** AMD
- **CUDAnalyst: Towards Feedback-to-Plan Decisions for Self-Evolving LLM Agents in CUDA Kernel Generation** [![ICML 2026](https://img.shields.io/badge/ICML-26-green)](https://openreview.net/forum?id=s70zO5Lvvj) [![Stars](https://img.shields.io/github/stars/yuxuan-z19/cudanalyst)](https://github.com/yuxuan-z19/cudanalyst)
  - **Institution:** Tsinghua University, Beijing National Research Center for Information Science and Technology
  - **Type:** Search & evolution · **Kernel:** `CUDA` · **Hardware:** NVIDIA · **Benchmark:** KernelBench

### 2025-12

- **KernelEvolve: Scaling Agentic Kernel Coding for Heterogeneous AI Accelerators at Meta** [![ISCA 2026](https://img.shields.io/badge/ISCA-26-green)](https://arxiv.org/abs/2512.23236) [![Blog](https://img.shields.io/badge/Blog-Meta-blue)](https://engineering.fb.com/2026/04/02/developer-tools/kernelevolve-how-metas-ranking-engineer-agent-optimizes-ai-infrastructure)
  - **Institution:** Meta
  - **Type:** Trained model · **Kernel:** `CUDA` `Triton` `TileLang` `CUTLASS` `HIP` · **Hardware:** NVIDIA, Meta MTIA · **Benchmark:** KernelBench
- **AKG-AGENT: AKG kernel Agent: A Multi-Agent Framework for Cross-Platform Kernel Synthesis** [![arXiv](https://img.shields.io/badge/arXiv-25.12-red)](https://arxiv.org/abs/2512.23424) [![Code](https://img.shields.io/badge/Code-GitHub-blue)](https://github.com/mindspore-ai/akg/tree/master/akg_agents)
  - **Institution:** Huawei, Hunan University
  - **Type:** Agentic workflow · **Kernel:** `Triton` `TileLang` `Ascend C` `CUDA` · **Hardware:** NVIDIA, Ascend, CPU · **Benchmark:** KernelBench
- **PEAK: A Performance Engineering AI-Assistant for GPU Kernels Powered by Natural Language Transformations** [![arXiv](https://img.shields.io/badge/arXiv-25.12-red)](https://arxiv.org/abs/2512.19018)
  - **Institution:** Stanford University, Microsoft Research
  - **Type:** Agentic workflow · **Kernel:** `CUDA` `HIP` · **Hardware:** NVIDIA, AMD
- **cuPilot: A Strategy-Coordinated Multi-agent Framework for CUDA Kernel Evolution** [![DAC 2026](https://img.shields.io/badge/DAC-26-green)](https://arxiv.org/abs/2512.16465) [![Artifacts](https://img.shields.io/badge/Artifacts-GitHub-lightgrey)](https://github.com/champloo2878/cuPilot-Kernels)
  - **Institution:** Southeast University, Tsinghua University, Tsing Micro
  - **Type:** Agentic workflow · **Kernel:** `CUDA` · **Hardware:** NVIDIA · **Benchmark:** KernelBench
- **GPU Kernel Optimization Beyond Full Builds: An LLM Framework with Minimal Executable Programs** [![PAKDD 2026](https://img.shields.io/badge/PAKDD-26-green)](https://arxiv.org/abs/2512.22147)
  - **Institution:** Xi'an Jiaotong University
  - **Type:** Agentic workflow · **Hardware:** NVIDIA, Hygon DCU
- **TritonForge: Profiling-Guided Framework for Automated Triton Kernel Optimization** [![ICSE Workshop 2026](https://img.shields.io/badge/ICSE_Workshop-26-green)](https://arxiv.org/abs/2512.09196) [![Stars](https://img.shields.io/github/stars/RLsys-Foundation/TritonForge)](https://github.com/RLsys-Foundation/TritonForge)
  - **Institution:** RLsys Foundation
  - **Type:** Trained model · **Kernel:** `Triton` · **Hardware:** NVIDIA, AMD · **Benchmark:** TritonBench
- **TritorX** [![arXiv](https://img.shields.io/badge/arXiv-25.12-red)](https://arxiv.org/abs/2512.10977)
  - *Generates functionally-correct Triton ATen kernels at scale for emerging accelerators.*
  - **Institution:** Meta
  - **Type:** Agentic workflow · **Kernel:** `Triton` · **Hardware:** Meta MTIA
- **CUDA-L2: Surpassing cuBLAS Performance for Matrix Multiplication through Reinforcement Learning** [![arXiv](https://img.shields.io/badge/arXiv-25.12-red)](https://arxiv.org/abs/2512.02551) [![Stars](https://img.shields.io/github/stars/ornith-ai/CUDA-L2)](https://github.com/ornith-ai/CUDA-L2)
  - **Institution:** DeepReinforce
  - **Type:** Trained model · **Kernel:** `CUDA` · **Hardware:** NVIDIA

### 2025-11

- **Automated Design Optimization via Strategic Search with Large Language Models** [![arXiv](https://img.shields.io/badge/arXiv-25.11-red)](https://arxiv.org/abs/2511.22651)
  - **Institution:** University of Michigan
  - **Type:** Agentic workflow · **Hardware:** NVIDIA · **Benchmark:** KernelBench
- **QiMeng-Kernel: Macro-Thinking Micro-Coding Paradigm for LLM-Based High-Performance GPU Kernel Generation** [![AAAI 2026](https://img.shields.io/badge/AAAI-26-green)](https://arxiv.org/abs/2511.20100) [![Stars](https://img.shields.io/github/stars/QiMeng-IPRC/QiMeng-Kernel)](https://github.com/QiMeng-IPRC/QiMeng-Kernel)
  - **Institution:** Institute of Computing Technology (CAS)
  - **Type:** Trained model · **Kernel:** `CUDA` · **Hardware:** NVIDIA · **Benchmark:** KernelBench, TritonBench
- **KernelBand: Steering LLM-based Kernel Optimization via Hardware-Aware Multi-Armed Bandits** [![ICML 2026](https://img.shields.io/badge/ICML-26-green)](https://arxiv.org/abs/2511.18868)
  - **Institution:** Peking University
  - **Type:** Search & evolution · **Kernel:** `Triton` · **Hardware:** NVIDIA · **Benchmark:** TritonBench
- **Optimizing PyTorch Inference with LLM-Based Multi-Agent Systems** [![MLSys 2026](https://img.shields.io/badge/MLSys-26-green)](https://arxiv.org/abs/2511.16964) [![Stars](https://img.shields.io/github/stars/pike-project/pike)](https://github.com/pike-project/pike) [![Dataset](https://img.shields.io/badge/Dataset-HuggingFace-yellow)](https://huggingface.co/datasets/knagaitsev/pike-data-compressed)
  - **Institution:** Northwestern University, Lawrence Berkeley National Laboratory
  - **Type:** Agentic workflow · **Hardware:** NVIDIA · **Benchmark:** KernelBench
- **AccelOpt: A Self-Improving LLM Agentic System for AI Accelerator Kernel Optimization** [![MLSys 2026](https://img.shields.io/badge/MLSys-26-green)](https://arxiv.org/abs/2511.15915) [![Stars](https://img.shields.io/github/stars/zhang677/AccelOpt)](https://github.com/zhang677/AccelOpt)
  - **Institution:** Stanford University, AWS
  - **Type:** Agentic workflow · **Kernel:** `NKI` · **Hardware:** AWS Neuron · **Benchmark:** FlashInfer-Bench
- **PRAGMA: A Profiling-Reasoned Multi-Agent Framework for Automatic Kernel Optimization** [![arXiv](https://img.shields.io/badge/arXiv-25.11-red)](https://arxiv.org/abs/2511.06345)
  - **Institution:** Beihang University
  - **Type:** Agentic workflow · **Kernel:** `Triton` · **Hardware:** NVIDIA · **Benchmark:** KernelBench
- **CudaForge: An Agent Framework with Hardware Feedback for CUDA Kernel Optimization** [![arXiv](https://img.shields.io/badge/arXiv-25.11-red)](https://arxiv.org/abs/2511.01884) [![Stars](https://img.shields.io/github/stars/OptimAI-Lab/CudaForge)](https://github.com/OptimAI-Lab/CudaForge)
  - **Institution:** University of Minnesota
  - **Type:** Agentic workflow · **Kernel:** `CUDA` · **Hardware:** NVIDIA · **Benchmark:** KernelBench
- **KForge: A Multi-Agent System for Cross-Platform Kernel Synthesis** [![ICML Workshop 2026](https://img.shields.io/badge/ICML_Workshop-26-green)](https://arxiv.org/abs/2606.02963)
  - **Institution:** Gimlet Labs
  - **Type:** Agentic workflow · **Kernel:** `Triton` `CUDA` `CUTLASS` `HIP` `SYCL` `Metal` · **Hardware:** NVIDIA, AMD, Intel, Apple · **Benchmark:** KernelBench
- **KernelFalcon** [![Blog](https://img.shields.io/badge/Blog-PyTorch-blue)](https://pytorch.org/blog/kernelfalcon-autonomous-gpu-kernel-generation-via-deep-agents)
  - *Predecessor of PyTorch KernelAgent.*
  - **Institution:** Meta
  - **Type:** Open-source / industry system · **Kernel:** `Triton` · **Hardware:** NVIDIA · **Benchmark:** KernelBench

### 2025-10

- **Integrating Performance Tools in Model Reasoning for GPU Kernel Optimization** [![arXiv](https://img.shields.io/badge/arXiv-25.10-red)](https://arxiv.org/abs/2510.17158)
  - **Institution:** Lawrence Livermore National Laboratory, University of Maryland
  - **Type:** Trained model · **Hardware:** NVIDIA
- **STARK: Strategic Team of Agents for Refining Kernels** [![ICLR 2026](https://img.shields.io/badge/ICLR-26-green)](https://arxiv.org/abs/2510.16996)
  - **Institution:** Meta
  - **Type:** Agentic workflow · **Kernel:** `CUDA` · **Hardware:** NVIDIA · **Benchmark:** KernelBench
- **TritonRL: Training LLMs to Think and Code Triton Without Cheating** [![COLM 2026](https://img.shields.io/badge/COLM-26-green)](https://arxiv.org/abs/2510.17891)
  - **Institution:** Carnegie Mellon University, Amazon
  - **Type:** Trained model · **Kernel:** `Triton` · **Hardware:** NVIDIA · **Benchmark:** KernelBench, TritonBench
- **ConCuR: Conciseness Makes State-of-the-Art Kernel Generation** [![arXiv](https://img.shields.io/badge/arXiv-25.10-red)](https://arxiv.org/abs/2510.07356) [![Model](https://img.shields.io/badge/Model-HuggingFace-yellow)](https://huggingface.co/lkongam/KernelCoder)
  - **Institution:** Hong Kong University of Science and Technology
  - **Type:** Trained model · **Kernel:** `Triton` · **Hardware:** NVIDIA · **Benchmark:** KernelBench
- **EvoEngineer: Mastering Automated CUDA Kernel Code Evolution with Large Language Models** [![arXiv](https://img.shields.io/badge/arXiv-25.10-red)](https://arxiv.org/abs/2510.03760)
  - **Institution:** City University of Hong Kong
  - **Type:** Search & evolution · **Kernel:** `CUDA` · **Hardware:** NVIDIA · **Benchmark:** KernelBench
- **Opal: A Modular Framework for Optimizing Performance using Analytics and LLMs** [![arXiv](https://img.shields.io/badge/arXiv-25.10-red)](https://arxiv.org/abs/2510.00932)
  - **Institution:** Texas State University, University of Novi Sad
  - **Type:** Single-pass / tooling · **Hardware:** NVIDIA, AMD
- **ReGraphT: From Large to Small: Transferring CUDA Optimization Expertise via Reasoning Graph** [![ICLR 2026](https://img.shields.io/badge/ICLR-26-green)](https://proceedings.iclr.cc/paper_files/paper/2026/hash/c4e40d310af1be55f2c0f32cb16a9a16-Abstract-Conference.html) [![Stars](https://img.shields.io/github/stars/blacknickwield/ReGraphT)](https://github.com/blacknickwield/ReGraphT)
  - **Institution:** Institute of Computing Technology (CAS), University of Chinese Academy of Sciences, South China University of Technology
  - **Type:** Search & evolution · **Kernel:** `CUDA` · **Hardware:** NVIDIA
- **KernelGen (Flagos)** [![Stars](https://img.shields.io/github/stars/flagos-ai/kernelgen)](https://github.com/flagos-ai/kernelgen) [![Project](https://img.shields.io/badge/Project-Page-blue)](https://kernelgen.flagos.io)
  - *Interactive kernel generation platform.*
  - **Institution:** Flagos
  - **Type:** Open-source / industry system · **Kernel:** `Triton` · **Hardware:** NVIDIA

### 2025-09

- **EoK: Evolution of Kernels: Automated RISC-V Kernel Optimization with Large Language Models** [![arXiv](https://img.shields.io/badge/arXiv-25.09-red)](https://arxiv.org/abs/2509.14265) [![Stars](https://img.shields.io/github/stars/Optima-CityU/Evolution_of_Kernels)](https://github.com/Optima-CityU/Evolution_of_Kernels)
  - **Institution:** City University of Hong Kong
  - **Type:** Search & evolution · **Hardware:** RISC-V
- **Astra: A Multi-Agent System for GPU Kernel Performance Optimization** [![NeurIPS Workshop 2025](https://img.shields.io/badge/NeurIPS_Workshop-25-green)](https://arxiv.org/abs/2509.07506) [![Stars](https://img.shields.io/github/stars/Anjiang-Wei/Astra)](https://github.com/Anjiang-Wei/Astra)
  - **Institution:** Stanford University
  - **Type:** Agentic workflow · **Kernel:** `CUDA` · **Hardware:** NVIDIA

### 2025-08

- **SwizzlePerf: Hardware-Aware LLMs for GPU Kernel Performance Optimization** [![NeurIPS Workshop 2025](https://img.shields.io/badge/NeurIPS_Workshop-25-green)](https://arxiv.org/abs/2508.20258)
  - **Institution:** Harvard University, AMD
  - **Type:** Agentic workflow · **Kernel:** `Triton` · **Hardware:** AMD

### 2025-07

- **GEAK: Introducing Triton Kernel AI Agent & Evaluation Benchmarks** [![arXiv](https://img.shields.io/badge/arXiv-25.07-red)](https://arxiv.org/abs/2507.23194) [![Stars](https://img.shields.io/github/stars/AMD-AGI/GEAK)](https://github.com/AMD-AGI/GEAK)
  - **Institution:** AMD-AGI
  - **Type:** Agentic workflow · **Kernel:** `Triton` · **Hardware:** AMD · **Benchmark:** TritonBench
- **CUDA-L1: Improving CUDA Optimization via Contrastive Reinforcement Learning** [![ICLR 2026](https://img.shields.io/badge/ICLR-26-green)](https://arxiv.org/abs/2507.14111) [![Stars](https://img.shields.io/github/stars/ornith-ai/CUDA-L1)](https://github.com/ornith-ai/CUDA-L1)
  - **Institution:** DeepReinforce
  - **Type:** Trained model · **Kernel:** `CUDA` · **Hardware:** NVIDIA · **Benchmark:** KernelBench
- **Kevin: Multi-Turn RL for Generating CUDA Kernels** [![ICLR 2026](https://img.shields.io/badge/ICLR-26-green)](https://arxiv.org/abs/2507.11948)
  - **Institution:** Cognition
  - **Type:** Trained model · **Kernel:** `CUDA` · **Hardware:** NVIDIA · **Benchmark:** KernelBench
- **AutoTriton: Automatic Triton Programming with Reinforcement Learning in LLMs** [![arXiv](https://img.shields.io/badge/arXiv-25.07-red)](https://arxiv.org/abs/2507.05687) [![Stars](https://img.shields.io/github/stars/AI9Stars/AutoTriton)](https://github.com/AI9Stars/AutoTriton)
  - **Institution:** Tsinghua University (THUNLP), AI9Stars
  - **Type:** Trained model · **Kernel:** `Triton` · **Hardware:** NVIDIA · **Benchmark:** KernelBench, TritonBench
- **QiMeng-Attention: SOTA Attention Operator is generated by SOTA Attention Algorithm** [![ACL Findings 2025](https://img.shields.io/badge/ACL_Findings-25-green)](https://aclanthology.org/2025.findings-acl.446/)
  - **Institution:** Institute of Computing Technology (CAS)
  - **Type:** Single-pass / tooling · **Kernel:** `CUDA` · **Hardware:** NVIDIA

### 2025-06

- **GPU Kernel Scientist: An LLM-Driven Framework for Iterative Kernel Optimization** [![ICML Workshop 2025](https://img.shields.io/badge/ICML_Workshop-25-green)](https://arxiv.org/abs/2506.20807)
  - **Type:** Search & evolution · **Kernel:** `CUDA` · **Hardware:** NVIDIA
- **CUDA-LLM: LLMs Can Write Efficient CUDA Kernels** [![arXiv](https://img.shields.io/badge/arXiv-25.06-red)](https://arxiv.org/abs/2506.09092)
  - **Institution:** Shanghai Jiao Tong University
  - **Type:** Search & evolution · **Kernel:** `CUDA` · **Hardware:** NVIDIA
- **QiMeng-MuPa: Mutual-Supervised Learning for Sequential-to-Parallel Code Translation** [![NeurIPS 2025](https://img.shields.io/badge/NeurIPS-25-green)](https://proceedings.neurips.cc/paper_files/paper/2025/hash/d34f0c1158c1b8c4fcbe8fb2dbf0c552-Abstract-Conference.html) [![Stars](https://img.shields.io/github/stars/QiMeng-IPRC/QiMeng-MuPa)](https://github.com/QiMeng-IPRC/QiMeng-MuPa) [![Model](https://img.shields.io/badge/Model-HuggingFace-yellow)](https://huggingface.co/collections/kcxain/qimeng-mupa) [![Dataset](https://img.shields.io/badge/Dataset-HuggingFace-yellow)](https://huggingface.co/datasets/kcxain/BabelTower)
  - **Institution:** Institute of Computing Technology (CAS), University of Chinese Academy of Sciences, Institute of Microelectronics (CAS), Institute of Software (CAS)
  - **Type:** Trained model · **Kernel:** `CUDA` · **Hardware:** NVIDIA
- **IntelliPerf** [![Stars](https://img.shields.io/github/stars/AMDResearch/intelliperf)](https://github.com/AMDResearch/intelliperf)
  - *Profiling-guided LLM framework for AMD GPUs.*
  - **Institution:** AMD Research
  - **Type:** Open-source / industry system · **Kernel:** `HIP` `Triton` · **Hardware:** AMD

### 2025-05

- **Autocomp: A Powerful and Portable Code Optimizer for Tensor Accelerators** [![NeurIPS Workshop 2025](https://img.shields.io/badge/NeurIPS_Workshop-25-green)](https://arxiv.org/abs/2505.18574) [![Stars](https://img.shields.io/github/stars/ucb-bar/autocomp)](https://github.com/ucb-bar/autocomp)
  - **Institution:** UC Berkeley
  - **Type:** Search & evolution · **Hardware:** NVIDIA, AWS Neuron, Research accelerators · **Benchmark:** KernelBench
- **QiMeng-TensorOp: One-Line Prompt is Enough for High-Performance Tensor Operator Generation with Hardware Primitives** [![IJCAI 2025](https://img.shields.io/badge/IJCAI-25-green)](https://arxiv.org/abs/2505.06302)
  - **Institution:** Institute of Computing Technology (CAS)
  - **Type:** Search & evolution · **Kernel:** `CUDA` · **Hardware:** NVIDIA, RISC-V
- **QiMeng-Xpiler: Transcompiling Tensor Programs for Deep Learning Systems with a Neural-Symbolic Approach** [![OSDI 2025](https://img.shields.io/badge/OSDI-25-green)](https://arxiv.org/abs/2505.02146)
  - **Institution:** Institute of Computing Technology (CAS), University of Science and Technology of China, Cambricon
  - **Type:** Agentic workflow · **Kernel:** `CUDA` `HIP` · **Hardware:** NVIDIA, AMD, CPU, Cambricon
- **KernelLLM** [![Model](https://img.shields.io/badge/Model-HuggingFace-yellow)](https://huggingface.co/facebook/KernelLLM)
  - *Llama 3.1 8B fine-tuned on KernelBook (~25K torch-triton pairs).*
  - **Institution:** Meta
  - **Type:** Open-source / industry system · **Kernel:** `Triton` · **Hardware:** NVIDIA

### 2025-02

- **QiMeng-GEMM: Automatically Generating High-Performance Matrix Multiplication Code by Exploiting Large Language Models** [![AAAI 2025](https://img.shields.io/badge/AAAI-25-green)](https://ojs.aaai.org/index.php/AAAI/article/view/34461)
  - **Institution:** Institute of Computing Technology (CAS)
  - **Type:** Search & evolution · **Kernel:** `CUDA` · **Hardware:** NVIDIA, RISC-V
- **AI CUDA Engineer: Towards Robust Agentic CUDA Kernel Benchmarking, Verification, and Optimization** [![arXiv](https://img.shields.io/badge/arXiv-25.09-red)](https://arxiv.org/abs/2509.14279) [![Dataset](https://img.shields.io/badge/Dataset-HuggingFace-yellow)](https://huggingface.co/datasets/SakanaAI/AI-CUDA-Engineer-Archive)
  - **Institution:** Sakana AI
  - **Type:** Agentic workflow · **Kernel:** `CUDA` · **Hardware:** NVIDIA · **Benchmark:** KernelBench

### 2023-11

- **VSCuda: LLM based CUDA extension for Visual Studio Code** [![SC Workshop 2023](https://img.shields.io/badge/SC_Workshop-23-green)](https://doi.org/10.1145/3624062.3624064)
  - **Institution:** UC Riverside
  - **Type:** Single-pass / tooling · **Kernel:** `CUDA` · **Hardware:** NVIDIA

## Benchmarks

_Benchmarks and datasets for evaluating LLM-generated kernels. The companion [awesome-kernel-benchmark](https://github.com/youyve/awesome-kernel-benchmark) catalogs 150+ benchmarks with a methodology scorecard._

### 2026-10

- **EdgeKernelBench: Unified LLM-Driven Kernel Generation for Edge Backends** [![arXiv](https://img.shields.io/badge/arXiv-26.10-red)](https://arxiv.org/abs/2610.24648) [![Stars](https://img.shields.io/github/stars/pillor9/EdgeKernelBench)](https://github.com/pillor9/EdgeKernelBench) [![Project](https://img.shields.io/badge/Project-Page-blue)](https://pillor9.github.io/EdgeKernelBench)
  - **Institution:** Westlake University, Zhejiang University
  - **Kernel:** `TVM` · **Hardware:** Mobile GPU
- **HPCAgent-Bench: A Framework for Sound Benchmarking of Code-Optimizing Agents, Harnesses, and Skills** [![arXiv](https://img.shields.io/badge/arXiv-26.10-red)](https://arxiv.org/abs/2610.20673) [![Stars](https://img.shields.io/github/stars/spcl/HPCAgent-Bench)](https://github.com/spcl/HPCAgent-Bench)
  - **Institution:** ETH Zurich, Institute of High Performance Computing (A\*STAR)
  - **Hardware:** NVIDIA, AMD
- **MetaKernelBench: Measuring GPU Kernel Knowledge Transfer Beyond Code** [![arXiv](https://img.shields.io/badge/arXiv-26.10-red)](https://arxiv.org/abs/2610.05014) [![Stars](https://img.shields.io/github/stars/YIGE24/MetaKernelBench)](https://github.com/YIGE24/MetaKernelBench) [![Project](https://img.shields.io/badge/Project-Page-blue)](https://yige24.github.io/MetaKernelBench)
  - **Institution:** Westlake University, Shanghai Jiao Tong University, Zhejiang University
  - **Kernel:** `CuTe` `TIRx` · **Hardware:** NVIDIA
- **D2K-Bench: Can LLM Agents Turn Expert Designs into Efficient GPU Kernels?** [![arXiv](https://img.shields.io/badge/arXiv-26.10-red)](https://arxiv.org/abs/2610.03226) [![Stars](https://img.shields.io/github/stars/QwenLM/D2K-Bench)](https://github.com/QwenLM/D2K-Bench)
  - **Institution:** Hong Kong University of Science and Technology, Alibaba, University of Science and Technology of China
  - **Hardware:** NVIDIA

### 2026-09

- **TileBench: A Controlled Benchmark for Performance Evaluation and Bottleneck Diagnosis of Tile-Based Programming Models** [![arXiv](https://img.shields.io/badge/arXiv-26.09-red)](https://arxiv.org/abs/2609.29067) [![Stars](https://img.shields.io/github/stars/Deep-Learning-Profiling-Tools/Tilebench)](https://github.com/Deep-Learning-Profiling-Tools/Tilebench)
  - **Institution:** George Mason University
  - **Kernel:** `Triton` `cuTile` · **Hardware:** NVIDIA
- **SparseKernelBench: A Benchmark for Sparse GPU Computation** [![OpenReview](https://img.shields.io/badge/OpenReview-26.09-lightgrey)](https://openreview.net/forum?id=7LsexQFZfO)
  - **Hardware:** NVIDIA
- **QKernelBench: Benchmarking LLMs for Quantized GPU Kernel Generation** [![OpenReview](https://img.shields.io/badge/OpenReview-26.09-lightgrey)](https://openreview.net/forum?id=TwxNTmH7Fu)
  - **Kernel:** `CUDA` · **Hardware:** NVIDIA
- **Megakernelbench: a System-Level Benchmark for Megakernel Generation and Optimization** [![OpenReview](https://img.shields.io/badge/OpenReview-26.09-lightgrey)](https://openreview.net/forum?id=PwSoG2iTIm)
  - **Hardware:** NVIDIA
- **SWE-KERNEL-BENCH: A Live Benchmark for GPU Kernel Generation** [![OpenReview](https://img.shields.io/badge/OpenReview-26.09-lightgrey)](https://openreview.net/forum?id=MQHsVFGcVK)
  - **Kernel:** `CUDA` `Triton` · **Hardware:** NVIDIA
- **KernelShift: Benchmarking Kernel Optimization Across Evolving Hardware** [![OpenReview](https://img.shields.io/badge/OpenReview-26.09-lightgrey)](https://openreview.net/forum?id=Px2KW4H05v)
  - **Hardware:** AWS Neuron, Apple
- **KernelAudit: Can LLM-Generated GPU Kernels Be Both Reliable and Competitive on Real-World Workloads?** [![OpenReview](https://img.shields.io/badge/OpenReview-26.09-lightgrey)](https://openreview.net/forum?id=yTa4gvQUGG) [![Code](https://img.shields.io/badge/Code-Anonymous-lightgrey)](https://anonymous.4open.science/r/kernelaudit-BD8D)
  - **Hardware:** NVIDIA
- **AutoTuneBench: Trustworthy Measurement for Agent Auto-Tuning of LLM Serving Engines** [![arXiv](https://img.shields.io/badge/arXiv-26.09-red)](https://arxiv.org/abs/2609.18123) [![Stars](https://img.shields.io/github/stars/li-ch/autotunebench)](https://github.com/li-ch/autotunebench)
  - **Institution:** harnets.ai
  - **Hardware:** NVIDIA, Apple

### 2026-08

- **RealisticTritonBench: A Benchmark for Triton-Kernel Generation in Real-World AI Frameworks** [![ASE 2026](https://img.shields.io/badge/ASE-26-green)](https://arxiv.org/abs/2608.12004) [![Stars](https://img.shields.io/github/stars/ZJU-CTAG/RealisticTritonBench)](https://github.com/ZJU-CTAG/RealisticTritonBench)
  - **Institution:** Zhejiang University, Nanjing University, Huawei, Chongqing University
  - **Kernel:** `Triton` · **Hardware:** NVIDIA
- **Gaming Without an Attacker: Benchmark Fingerprinting in LLM-Driven Search Under Selection Pressure** [![COLM Workshop 2026](https://img.shields.io/badge/COLM_Workshop-26-green)](https://arxiv.org/abs/2608.08722) [![Stars](https://img.shields.io/github/stars/vicgalle/kernel-fingerprinting)](https://github.com/vicgalle/kernel-fingerprinting)
  - **Institution:** Komorebi AI Technologies
  - **Kernel:** `Metal` · **Hardware:** Apple

### 2026-07

- **KernelGenBench: Can LLMs and Agents Write Efficient Kernels Across Operator Sources and Hardware Platforms?** [![arXiv](https://img.shields.io/badge/arXiv-26.07-red)](https://arxiv.org/abs/2607.27231) [![Stars](https://img.shields.io/github/stars/flagos-ai/KernelGenBench)](https://github.com/flagos-ai/KernelGenBench)
  - **Institution:** Beijing Normal University, Beijing Academy of Artificial Intelligence, Beijing Jiaotong University, Institute of Automation (CAS), Peking University
  - **Kernel:** `Triton` · **Hardware:** NVIDIA, Moore Threads, Hygon DCU, Other

### 2026-06

- **ParallelKernelBench: Can LLMs Write Fast Multi-GPU Kernels?** [![ICML Workshop 2026](https://img.shields.io/badge/ICML_Workshop-26-green)](https://openreview.net/forum?id=4IGomFc9dx) [![Stars](https://img.shields.io/github/stars/togethercomputer/ParallelKernelBench)](https://github.com/togethercomputer/ParallelKernelBench)
  - **Hardware:** NVIDIA
- **KernelBench-Verified: Do LLM-Generated Kernels Actually Beat PyTorch?** [![arXiv](https://img.shields.io/badge/arXiv-26.07-red)](https://arxiv.org/abs/2607.16241) [![Stars](https://img.shields.io/github/stars/facebookresearch/kernel_bench_verified)](https://github.com/facebookresearch/kernel_bench_verified) [![Project](https://img.shields.io/badge/Project-Page-blue)](https://scalingintelligence.stanford.edu/kernelbenchverifiedleaderboard)
  - **Institution:** Meta, Stanford University
  - **Kernel:** `CUDA` · **Hardware:** NVIDIA

### 2026-05

- **SciKernelBench: Evaluating LLM Kernels for Higher-Order Autodiff and Scientific Residuals** [![ICML Workshop 2026](https://img.shields.io/badge/ICML_Workshop-26-green)](https://openreview.net/forum?id=iywEUhqGmH) [![Code unavailable](https://img.shields.io/badge/Code-unavailable-lightgrey)](https://github.com/SciKernelBench/SciKernelBench)
  - **Institution:** Yandex School of Data Analysis, Applied AI Institute, GigaCode Research Center, ITMO University, Mohamed bin Zayed University of Artificial Intelligence
- **PassNet: Scaling Large Language Models for Graph Compiler Pass Generation** [![arXiv](https://img.shields.io/badge/arXiv-26.05-red)](https://arxiv.org/abs/2605.29357) [![Stars](https://img.shields.io/github/stars/PaddlePaddle/PassNet)](https://github.com/PaddlePaddle/PassNet) [![Dataset](https://img.shields.io/badge/Dataset-HuggingFace-yellow)](https://huggingface.co/datasets/PassNet/PassNet) [![Project](https://img.shields.io/badge/Project-Page-blue)](https://paddlepaddle.github.io/PassNet/leaderboard.html)
  - **Institution:** Baidu
  - **Hardware:** NVIDIA
- **FastKernels: Benchmarking GPU Kernel Generation in Production** [![arXiv](https://img.shields.io/badge/arXiv-26.05-red)](https://arxiv.org/abs/2605.23215) [![Stars](https://img.shields.io/github/stars/Snowflake-AI-Research/fastkernels)](https://github.com/Snowflake-AI-Research/fastkernels)
  - **Institution:** Snowflake, Carnegie Mellon University, UC San Diego, Independent researcher
  - **Hardware:** NVIDIA
- **AgentKernelArena: Generalization-Aware Benchmarking of GPU Kernel Optimization Agents** [![arXiv](https://img.shields.io/badge/arXiv-26.05-red)](https://arxiv.org/abs/2605.16819) [![Stars](https://img.shields.io/github/stars/AMD-AGI/AgentKernelArena)](https://github.com/AMD-AGI/AgentKernelArena)
  - **Institution:** AMD
  - **Kernel:** `HIP` `Triton` · **Hardware:** AMD
- **Metal-Sci: A Scientific Compute Benchmark for Evolutionary LLM Kernel Search on Apple Silicon** [![ICML Workshop 2026](https://img.shields.io/badge/ICML_Workshop-26-green)](https://arxiv.org/abs/2605.09708) [![Stars](https://img.shields.io/github/stars/vicgalle/metal-sci-kernels)](https://github.com/vicgalle/metal-sci-kernels)
  - **Institution:** Komorebi AI Technologies
  - **Kernel:** `Metal` · **Hardware:** Apple
- **CUDABeaver: Benchmarking LLM-Based Automated CUDA Debugging** [![arXiv](https://img.shields.io/badge/arXiv-26.05-red)](https://arxiv.org/abs/2605.08455) [![Stars](https://img.shields.io/github/stars/UMN-APEX-Lab/CUDABeaver)](https://github.com/UMN-APEX-Lab/CUDABeaver)
  - **Institution:** University of Minnesota
  - **Kernel:** `CUDA` · **Hardware:** NVIDIA
- **KernelBenchX: A Comprehensive Benchmark for Evaluating LLM-Generated GPU Kernels** [![arXiv](https://img.shields.io/badge/arXiv-26.05-red)](https://arxiv.org/abs/2605.04956) [![Stars](https://img.shields.io/github/stars/BonnieW05/KernelBenchX)](https://github.com/BonnieW05/KernelBenchX) [![Dataset](https://img.shields.io/badge/Dataset-HuggingFace-yellow)](https://huggingface.co/datasets/BonnieWang/KernelBenchX)
  - **Kernel:** `Triton` · **Hardware:** NVIDIA
- **JAXBench: Benchmarking Autonomous TPU Kernel Optimization** [![arXiv](https://img.shields.io/badge/arXiv-26.07-red)](https://arxiv.org/abs/2607.20466) [![Code](https://img.shields.io/badge/Code-GitHub-blue)](https://github.com/AI-Hypercomputer/accelerator-agents/tree/main/JAXBench)
  - **Institution:** Harvard University, Google, UC Berkeley, Google DeepMind
  - **Hardware:** Google TPU

### 2026-03

- **SOL-ExecBench: Speed-of-Light Benchmarking for Real-World GPU Kernels Against Hardware Limits** [![arXiv](https://img.shields.io/badge/arXiv-26.03-red)](https://arxiv.org/abs/2603.19173) [![Stars](https://img.shields.io/github/stars/NVIDIA/SOL-ExecBench)](https://github.com/NVIDIA/SOL-ExecBench) [![Dataset](https://img.shields.io/badge/Dataset-HuggingFace-yellow)](https://huggingface.co/datasets/nvidia/SOL-ExecBench) [![Project](https://img.shields.io/badge/Project-Page-blue)](https://research.nvidia.com/benchmarks/sol-execbench)
  - **Institution:** NVIDIA
  - **Kernel:** `CUDA` · **Hardware:** NVIDIA
- **MobileKernelBench: Can LLMs Write Efficient Kernels for Mobile Devices?** [![ICLR Workshop 2026](https://img.shields.io/badge/ICLR_Workshop-26-green)](https://arxiv.org/abs/2603.11935)
  - **Institution:** Zhejiang University, Westlake University, Hong Kong University of Science and Technology, Universiti Teknologi Malaysia, Alibaba
  - **Hardware:** Mobile GPU

### 2026-02

- **KernelCraft: Benchmarking for Agentic Close-to-Metal Kernel Generation on Emerging Hardware** [![ICML 2026](https://img.shields.io/badge/ICML-26-green)](https://proceedings.mlr.press/v306/nie26c.html) [![Project](https://img.shields.io/badge/Project-Page-blue)](https://kernelcraft-cam.github.io)
  - **Institution:** University of Cambridge, Imperial College London, AMD, University of Edinburgh
  - **Kernel:** `Assembly` · **Hardware:** NVIDIA, AMD, Google TPU, RISC-V, Research accelerators
- **CUDABench: Benchmarking LLMs for Text-to-CUDA Generation** [![arXiv](https://img.shields.io/badge/arXiv-26.03-red)](https://arxiv.org/abs/2603.02236) [![Stars](https://img.shields.io/github/stars/CUDA-Bench/CUDABench)](https://github.com/CUDA-Bench/CUDABench) [![Dataset](https://img.shields.io/badge/Dataset-HuggingFace-yellow)](https://huggingface.co/datasets/CUDABench/CUDABench-Set)
  - **Institution:** Shanghai Jiao Tong University
  - **Kernel:** `CUDA` · **Hardware:** NVIDIA

### 2026-01

- **FlashInfer-Bench: Building the Virtuous Cycle for AI-driven LLM Systems** [![MLSys 2026](https://img.shields.io/badge/MLSys-26-green)](https://proceedings.mlsys.org/paper_files/paper/2026/file/37e44c4b5321605735be9761f9b758fc-Paper-Conference.pdf) [![Stars](https://img.shields.io/github/stars/flashinfer-ai/flashinfer-bench)](https://github.com/flashinfer-ai/flashinfer-bench) [![Dataset](https://img.shields.io/badge/Dataset-HuggingFace-yellow)](https://huggingface.co/datasets/flashinfer-ai/flashinfer-trace) [![Project](https://img.shields.io/badge/Project-Page-blue)](https://bench.flashinfer.ai)
  - **Institution:** University of Washington, Carnegie Mellon University, NVIDIA, UC Berkeley, Independent researcher
  - **Hardware:** NVIDIA

### 2025-09

- **TritonGym: A Benchmark for Agentic LLM Workflows in Triton GPU Code Generation** [![ICML 2026](https://img.shields.io/badge/ICML-26-green)](https://openreview.net/forum?id=Htq2loTQTL)
  - **Kernel:** `Triton` · **Hardware:** NVIDIA

### 2025-07

- **MultiKernelBench: A Multi-Platform Benchmark for Kernel Generation** [![ASE 2026](https://img.shields.io/badge/ASE-26-green)](https://arxiv.org/abs/2507.17773) [![Stars](https://img.shields.io/github/stars/wzzll123/MultiKernelBench)](https://github.com/wzzll123/MultiKernelBench)
  - **Institution:** Nanjing University, Zhejiang University
  - **Hardware:** NVIDIA, Ascend, Google TPU

### 2025-06

- **HPCTransCompile: An AI Compiler Generated Dataset for High-Performance CUDA Transpilation and LLM Preliminary Exploration** [![arXiv](https://img.shields.io/badge/arXiv-25.06-red)](https://arxiv.org/abs/2506.10401) [![Stars](https://img.shields.io/github/stars/PJLAB-CHIP/HPCTransCompile)](https://github.com/PJLAB-CHIP/HPCTransCompile)
  - **Institution:** Tongji University, Shanghai Artificial Intelligence Laboratory, Tsinghua University

### 2025-02

- **TritonBench: Benchmarking Large Language Model Capabilities for Generating Triton Operators** [![ACL Findings 2025](https://img.shields.io/badge/ACL_Findings-25-green)](https://aclanthology.org/2025.findings-acl.1183/) [![Stars](https://img.shields.io/github/stars/thunlp/TritonBench)](https://github.com/thunlp/TritonBench) [![Model](https://img.shields.io/badge/Model-HuggingFace-yellow)](https://huggingface.co/collections/LiShangZ/tritonbench-67c0016bc8a8654cfd612a1a)
  - **Institution:** Tianjin University, Harbin Institute of Technology, Hong Kong University of Science and Technology (Guangzhou), Tsinghua University
  - **Kernel:** `Triton` · **Hardware:** NVIDIA
- **KernelBench: Can LLMs Write Efficient GPU Kernels?** [![ICML 2025](https://img.shields.io/badge/ICML-25-green)](https://proceedings.mlr.press/v267/ouyang25a.html) [![Stars](https://img.shields.io/github/stars/ScalingIntelligence/KernelBench)](https://github.com/ScalingIntelligence/KernelBench) [![Dataset](https://img.shields.io/badge/Dataset-HuggingFace-yellow)](https://huggingface.co/datasets/ScalingIntelligence/KernelBench)
  - **Institution:** Stanford University, Princeton University
  - **Kernel:** `CUDA` · **Hardware:** NVIDIA

## General-purpose systems with kernel results

_General agents, optimizers, or code models whose evaluations include kernel tasks._

### 2026-10

- **Organon: From Evolutionary Search to Recursive Self-Improving Agents for Scientific Discovery** [![arXiv](https://img.shields.io/badge/arXiv-26.10-red)](https://arxiv.org/abs/2610.33046)
  - **Institution:** Huawei
- **An important Bottleneck in LLM Optimizers: Principle-Level Local Optima** [![arXiv](https://img.shields.io/badge/arXiv-26.10-red)](https://arxiv.org/abs/2610.24291)
  - **Institution:** University of Manchester, University of Chinese Academy of Sciences, Zhongguancun Academy, NVIDIA, XinZhuAI, Honda Research Institute Europe
- **AReaL-RSI: Adaptive Scaling and Coordination of Recursive Self-Improvement** [![arXiv](https://img.shields.io/badge/arXiv-26.10-red)](https://arxiv.org/abs/2610.18083)
  - **Institution:** Ant Group, Zhejiang University, Hong Kong University of Science and Technology
  - **Hardware:** NVIDIA · **Benchmark:** KernelBench
- **HarnessTTT: Learn to Optimize Harness at Test-Time for Scientific Discovery** [![arXiv](https://img.shields.io/badge/arXiv-26.10-red)](https://arxiv.org/abs/2610.17370)
  - **Institution:** University of Wisconsin-Madison, NVIDIA, Johns Hopkins University, Stanford University, Meta
- **AutoEnvScaling: Automating the Data Flywheel with Terminal Agents** [![arXiv](https://img.shields.io/badge/arXiv-26.10-red)](https://arxiv.org/abs/2610.14163)
  - **Institution:** Northeastern University, Microsoft, Stanford University, University of Washington, University of North Carolina at Chapel Hill
- **UTT: Universal Textual Teaching for LLMs** [![arXiv](https://img.shields.io/badge/arXiv-26.10-red)](https://arxiv.org/abs/2610.12114)
  - **Institution:** Westlake University
- **SkillMorph: Trajectory-Guided Fault Localization for Agent Skill Evolution** [![arXiv](https://img.shields.io/badge/arXiv-26.10-red)](https://arxiv.org/abs/2610.11858)
  - **Institution:** Nanjing University, Hong Kong Polytechnic University
- **Stateless Language Agents: Scaling Long-Horizon Automated Research** [![arXiv](https://img.shields.io/badge/arXiv-26.10-red)](https://arxiv.org/abs/2610.07625) [![Project](https://img.shields.io/badge/Project-Page-blue)](https://github.com/Alex-q-z/stateless-language-agents)
  - **Institution:** Stanford University, Carnegie Mellon University, University of Washington, SambaNova Systems, UC Berkeley
  - **Kernel:** `Triton` · **Benchmark:** SOL-ExecBench
- **Guidance-TTT: Evolving in Thought Space: Training a Small Model at Test Time Unlocks Better Discoveries** [![arXiv](https://img.shields.io/badge/arXiv-26.10-red)](https://arxiv.org/abs/2610.06269)
  - **Institution:** MIT, Singapore-MIT Alliance for Research and Technology, Hong Kong Polytechnic University, ByteDance, National University of Singapore, Stanford University, University of Washington, UC Berkeley, Tsinghua University

### 2026-09

- **PCPO: Self-Evolving Algorithm-Design Agents: Escaping In-Context Evolutionary Stagnation via Population-Curated Policy Optimization** [![arXiv](https://img.shields.io/badge/arXiv-26.09-red)](https://arxiv.org/abs/2609.38757)
  - **Institution:** Nanjing University, Huawei
- **CliffCompaction: Cost-Efficient Compaction for Long-Horizon Coding Agents** [![arXiv](https://img.shields.io/badge/arXiv-26.09-red)](https://arxiv.org/abs/2609.26779)
  - **Institution:** Carnegie Mellon University, Bosch
  - **Kernel:** `CUDA`
- **Test-Time Compute Scales Better with Parallel Agent Teams** [![OpenReview](https://img.shields.io/badge/OpenReview-26.09-lightgrey)](https://openreview.net/forum?id=ZweFYN4Dy1)
- **REL: Recursive Experience Learning: As Agents Learn, Worlds Evolve** [![OpenReview](https://img.shields.io/badge/OpenReview-26.09-lightgrey)](https://openreview.net/forum?id=pR1aRoteXn)
- **AutoScaffold: AI-Guided Scaffolding for Reinforcement Learning of Language Models** [![OpenReview](https://img.shields.io/badge/OpenReview-26.09-lightgrey)](https://openreview.net/forum?id=KPRr8wWiqO)
- **LC-DFT: Allocate, Don't Just Rank: Reducing Redundancy in Test-Time Search for Scientific Discovery** [![OpenReview](https://img.shields.io/badge/OpenReview-26.09-lightgrey)](https://openreview.net/forum?id=o4wq2eZYdl)
- **DuoDiscover: Code Optimization by Discovering What to Optimize and How to Evaluate** [![OpenReview](https://img.shields.io/badge/OpenReview-26.09-lightgrey)](https://openreview.net/forum?id=8ToDSnOfqT)
- **Dream-RSI: Recursive Self-Improvement through Evolving Worlds** [![arXiv](https://img.shields.io/badge/arXiv-26.09-red)](https://arxiv.org/abs/2609.14858) [![Project](https://img.shields.io/badge/Project-Page-blue)](https://github.com/zhengkid/Dream-RSI)
  - **Institution:** Google, Google DeepMind, University of Maryland, University of Virginia
  - **Kernel:** `Triton` · **Hardware:** NVIDIA · **Benchmark:** KernelBench

### 2026-08

- **EvoMem: Memory-Augmented Evolution for Code Optimization** [![arXiv](https://img.shields.io/badge/arXiv-26.08-red)](https://arxiv.org/abs/2608.10795)
  - **Institution:** Applied AI Institute, Lomonosov Moscow State University
  - **Kernel:** `Triton` · **Hardware:** NVIDIA
- **Argus: A General-Purpose Agentic Reasoning Runtime for Long-Horizon Tasks** [![arXiv](https://img.shields.io/badge/arXiv-26.08-red)](https://arxiv.org/abs/2608.05144)
- **iCoder-27B: Recursive AI-Led Development of Frontier Industrial Coding Model** [![arXiv](https://img.shields.io/badge/arXiv-26.09-red)](https://arxiv.org/abs/2609.29626)
  - **Institution:** Shanghai Jiao Tong University, National University of Singapore, DP Technology, Endless Frontier
  - **Kernel:** `Triton`

### 2026-07

- **ResearchArena: Evaluating Sabotage and Monitoring in Automated AI R&D** [![arXiv](https://img.shields.io/badge/arXiv-26.07-red)](https://arxiv.org/abs/2607.19321)
  - **Institution:** ELLIS Institute Tübingen, Max Planck Institute for Intelligent Systems, Tübingen AI Center, ETH Zurich, University of Amsterdam
  - **Kernel:** `CUDA`

### 2026-06

- **Foundry: Host-Owned Trust and Memory for Long-Horizon Agent Swarms** [![ICML Workshop 2026](https://img.shields.io/badge/ICML_Workshop-26-green)](https://openreview.net/forum?id=MWLIRDa4DC)
  - **Institution:** UC Berkeley, Together AI, Stanford University, University of Texas at Austin
- **AutoLab: Can Frontier Models Solve Long-Horizon Auto Research and Engineering Tasks?** [![arXiv](https://img.shields.io/badge/arXiv-26.06-red)](https://arxiv.org/abs/2606.05080)
  - **Institution:** University of Washington, Bake AI, UC San Diego, University of Notre Dame, University of Waterloo, NVIDIA, Google, MIT-IBM Computing Research Lab, National University of Singapore, Stanford University, Independent researcher, Princeton University, UC Santa Barbara, MIT
  - **Kernel:** `CUDA`

### 2026-05

- **SIA: Self Improving AI with Harness & Weight Updates** [![arXiv](https://img.shields.io/badge/arXiv-26.05-red)](https://arxiv.org/abs/2605.27276)
  - **Institution:** Hexo Labs, University of Oxford
- **Prior Knowledge or Search? A Study of LLM Agents in Hardware-Aware Code Optimization** [![arXiv](https://img.shields.io/badge/arXiv-26.05-red)](https://arxiv.org/abs/2605.19782)
  - **Institution:** Applied AI Institute, ITMO University, Yandex School of Data Analysis
  - **Kernel:** `CUDA` `TVM`
- **optimize_anything: A Universal API for Optimizing any Text Parameter** [![arXiv](https://img.shields.io/badge/arXiv-26.05-red)](https://arxiv.org/abs/2605.19633)
  - **Institution:** UC Berkeley, MIT
  - **Kernel:** `CUDA`
- **SkillEvolver: Skill Learning as a Meta-Skill** [![arXiv](https://img.shields.io/badge/arXiv-26.05-red)](https://arxiv.org/abs/2605.10500)
  - **Institution:** Beijing Jiaotong University, Tsinghua University

### 2026-04

- **SimpleTES: Structured Scaling of AI Discovery Across Diverse Scientific Domains** [![arXiv](https://img.shields.io/badge/arXiv-26.04-red)](https://arxiv.org/abs/2604.19341) [![Stars](https://img.shields.io/github/stars/wq-will/SimpleTES)](https://github.com/wq-will/SimpleTES) [![Project](https://img.shields.io/badge/Project-Page-blue)](https://www.wizardquant.com/will/simpletes)
  - **Institution:** Stanford University, Peking University, Tsinghua University, Hong Kong University of Science and Technology (Guangzhou)
  - **Hardware:** NVIDIA
- **TurboEvolve: Towards Fast and Robust LLM-Driven Program Evolution** [![arXiv](https://img.shields.io/badge/arXiv-26.04-red)](https://arxiv.org/abs/2604.18607)
  - **Institution:** Hong Kong University of Science and Technology (Guangzhou), Institute of Deep Perception Technology (JITRI)

### 2026-03

- **SemRep: Generative Code Representation Learning with Code Transformations** [![arXiv](https://img.shields.io/badge/arXiv-26.03-red)](https://arxiv.org/abs/2603.13640)
  - **Institution:** University of Chicago, University of Illinois Urbana-Champaign, Columbia University, Microsoft
- **Reward Hacking in Self-Improving Code Agents** [![ICLR Workshop 2026](https://img.shields.io/badge/ICLR_Workshop-26-green)](https://openreview.net/forum?id=ikrQWGgxYg)
  - **Institution:** Weco AI
- **POLCA: Stochastic Generative Optimization with LLM** [![ICML 2026](https://img.shields.io/badge/ICML-26-green)](https://proceedings.mlr.press/v306/ren26l.html) [![Stars](https://img.shields.io/github/stars/rlx-lab/POLCA)](https://github.com/rlx-lab/POLCA)
  - **Institution:** University of Wisconsin-Madison, Google DeepMind, Google
  - **Kernel:** `CUDA` · **Hardware:** NVIDIA · **Benchmark:** KernelBench
- **InCoder-32B-Thinking: Industrial Code World Model for Thinking** [![arXiv](https://img.shields.io/badge/arXiv-26.04-red)](https://arxiv.org/abs/2604.03144) [![Stars](https://img.shields.io/github/stars/CSJianYang/Industrial-Coder)](https://github.com/CSJianYang/Industrial-Coder)
  - **Institution:** Beihang University
  - **Kernel:** `CUDA` · **Hardware:** NVIDIA · **Benchmark:** KernelBench, TritonBench
- **AlphaLab: Autonomous Multi-Agent Research Across Optimization Domains with Frontier LLMs** [![arXiv](https://img.shields.io/badge/arXiv-26.04-red)](https://arxiv.org/abs/2604.08590) [![Code](https://img.shields.io/badge/Code-GitHub-blue)](https://github.com/morganstanley/MSML/tree/ecff6184ab96102b189df8fba16f949a65356ee5/projects/alpha-lab) [![Project](https://img.shields.io/badge/Project-Page-blue)](https://brendanhogan.github.io/alphalab-paper)
  - **Institution:** Morgan Stanley
  - **Kernel:** `CUDA` · **Hardware:** NVIDIA · **Benchmark:** KernelBench

### 2026-02

- **Aster: Autonomous Scientific Discovery over 20x Faster Than Existing Methods** [![arXiv](https://img.shields.io/badge/arXiv-26.02-red)](https://arxiv.org/abs/2602.07040) [![Stars](https://img.shields.io/github/stars/aster-ai-labs/announcing-results)](https://github.com/aster-ai-labs/announcing-results) [![Project](https://img.shields.io/badge/Project-Page-blue)](https://www.asterlab.ai)
  - **Institution:** Aster AI Labs
  - **Hardware:** NVIDIA

### 2026-01

- **MaxCode: A Max-Reward Reinforcement Learning Framework for Automated Code Optimization** [![arXiv](https://img.shields.io/badge/arXiv-26.01-red)](https://arxiv.org/abs/2601.05475)
  - **Institution:** Johns Hopkins University, AWS
  - **Kernel:** `CUDA` · **Benchmark:** KernelBench
- **TTT-Discover: Learning to Discover at Test Time** [![ICML 2026](https://img.shields.io/badge/ICML-26-green)](https://proceedings.mlr.press/v306/yuksekgonul26a.html) [![Stars](https://img.shields.io/github/stars/test-time-training/discover)](https://github.com/test-time-training/discover) [![Project](https://img.shields.io/badge/Project-Page-blue)](https://test-time-training.github.io/discover)
  - **Institution:** Stanford University, UC San Diego, Together AI, Astera Institute, NVIDIA
  - **Hardware:** NVIDIA, AMD
- **PACEvolve: Enabling Long-Horizon Progress-Aware Consistent Evolution** [![ICLR Workshop 2026](https://img.shields.io/badge/ICLR_Workshop-26-green)](https://openreview.net/forum?id=7qsTTBK1vU)
  - **Institution:** University of Wisconsin-Madison, Google, Google DeepMind, UC San Diego

### 2025-10

- **The FM Agent** [![arXiv](https://img.shields.io/badge/arXiv-25.10-red)](https://arxiv.org/abs/2510.26144)
  - **Institution:** Baidu

### 2025-06

- **AlphaEvolve: A coding agent for scientific and algorithmic discovery** [![arXiv](https://img.shields.io/badge/arXiv-25.06-red)](https://arxiv.org/abs/2506.13131) [![Stars](https://img.shields.io/github/stars/google-deepmind/alphaevolve_results)](https://github.com/google-deepmind/alphaevolve_results)
  - **Institution:** Google DeepMind

### 2024-11

- **RE-Bench: Evaluating frontier AI R&D capabilities of language model agents against human experts** [![arXiv](https://img.shields.io/badge/arXiv-24.11-red)](https://arxiv.org/abs/2411.15114)
  - **Institution:** METR
  - **Kernel:** `Triton`

## Applications

_Domain systems where LLM-written kernels are part of the development or evaluation._

### 2026-10

- **FOMTools: Development and AI-Assisted Code Generation for First-Order Methods** [![arXiv](https://img.shields.io/badge/arXiv-26.10-red)](https://arxiv.org/abs/2610.26743) [![Stars](https://img.shields.io/github/stars/stellatogrp/fomtools)](https://github.com/stellatogrp/fomtools)
  - **Institution:** MIT, Princeton University
  - **Kernel:** `C` `CUDA` · **Hardware:** NVIDIA, Apple
- **Architecting for Hardware Diversity: Meta's End-to-End Co-Design for High-Performance AI Training on AMD GPUs** [![arXiv](https://img.shields.io/badge/arXiv-26.10-red)](https://arxiv.org/abs/2610.22230)
  - **Institution:** Meta, AMD

### 2026-09

- **Sol Video Inference Engine: Agent-Native Full-Stack Acceleration Framework for Efficient Video Generation** [![arXiv](https://img.shields.io/badge/arXiv-26.06-red)](https://arxiv.org/abs/2606.23743)
  - **Institution:** NVIDIA

### 2026-07

- **Per Astronomix ad Astra: High-Order Differentiable (Magneto)hydrodynamics with Energy-Conserving Self-Gravity** [![arXiv](https://img.shields.io/badge/arXiv-26.07-red)](https://arxiv.org/abs/2607.18176)
  - **Kernel:** `Pallas`

### 2026-05

- **From Human Guidance to Autonomy: Agent Skill System for End-to-End LLM Deployment on Spatial NPUs** [![arXiv](https://img.shields.io/badge/arXiv-26.06-red)](https://arxiv.org/abs/2606.07586)
  - **Institution:** Cornell University, AMD

### 2026-03

- **cuRoboV2: Dynamics-Aware Motion Generation with Depth-Fused Distance Fields for High-DoF Robots** [![arXiv](https://img.shields.io/badge/arXiv-26.03-red)](https://arxiv.org/abs/2603.05493) [![Stars](https://img.shields.io/github/stars/NVlabs/curobo)](https://github.com/NVlabs/curobo)
  - **Institution:** NVIDIA
  - **Kernel:** `CUDA` · **Hardware:** NVIDIA

## Infrastructure and tools

_Benchmarking isolation, tracing, and kernel libraries used by agents._

### 2026-09

- **KREX** [![arXiv](https://img.shields.io/badge/arXiv-26.09-red)](https://arxiv.org/abs/2609.30057)
  - *Runtime for interference-controlled kernel benchmarking on shared GPUs.*
  - **Institution:** Hong Kong University of Science and Technology, Alibaba
  - **Hardware:** NVIDIA, AMD
- **Xtrace** [![arXiv](https://img.shields.io/badge/arXiv-26.09-red)](https://arxiv.org/abs/2609.28769) [![Project](https://img.shields.io/badge/Project-Page-blue)](https://g-watch.github.io) [![Artifacts](https://img.shields.io/badge/Artifacts-g--watch.github.io-lightgrey)](https://g-watch.github.io/en/open-traces)
  - *Binary-instrumentation tracing infrastructure with GPU kernel-agent case studies.*
  - **Institution:** National University of Singapore, Meta
  - **Hardware:** NVIDIA, AMD

### 2026-01

- **TileOPs (TOPS)** [![Stars](https://img.shields.io/github/stars/tile-ai/TileOPs)](https://github.com/tile-ai/TileOPs)
  - *Spec-driven operator library: AI agents read declarative manifests (signatures, workloads, roofline formulas), generate TileLang kernels, and self-validate against Speed-of-Light bounds.*
  - **Institution:** tile-ai
  - **Kernel:** `TileLang` · **Hardware:** NVIDIA

### 2025-10

- **TileLang-Ascend** [![Stars](https://img.shields.io/github/stars/tile-ai/tilelang-ascend)](https://github.com/tile-ai/tilelang-ascend)
  - *Adapter layer connecting TileLang to the Ascend backend (not an agent).*
  - **Institution:** tile-ai
  - **Kernel:** `TileLang` · **Hardware:** Ascend

### 2025-03

- **IntelliKit** [![Stars](https://img.shields.io/github/stars/AMDResearch/intellikit)](https://github.com/AMDResearch/intellikit)
  - *LLM-ready profiling toolkit for AMD GPUs.*
  - **Institution:** AMD Research
  - **Kernel:** `HIP` · **Hardware:** AMD

## Empirical studies

_Measurement studies and analyses of how LLMs write kernels._

### 2026-10

- **What Language Should LLMs Write GPU Kernels In? Disentangling Abstraction Level from Resource Level** [![NeurIPS Workshop 2026](https://img.shields.io/badge/NeurIPS_Workshop-26-green)](https://openreview.net/forum?id=9Ppcp9PK8i)
  - **Institution:** Pusan National University, Electronics and Telecommunications Research Institute
  - **Kernel:** `CUDA` `PTX` `Triton` `TileLang` · **Hardware:** NVIDIA · **Benchmark:** KernelBench
- **RESOLVE: Language-Agnostic Validation of GPU Kernels Through Testing, Reduction, and Proof** [![arXiv](https://img.shields.io/badge/arXiv-26.10-red)](https://arxiv.org/abs/2610.05683)
  - **Institution:** UC Riverside, Math Inc., Microsoft Research
  - **Kernel:** `CUTLASS` `Triton` `Gluon` · **Hardware:** NVIDIA

### 2026-09

- **DLRM-Bench: How Much of a Real Workload Can LLM-Generated GPU Kernels Actually Reach?** [![arXiv](https://img.shields.io/badge/arXiv-26.09-red)](https://arxiv.org/abs/2609.21058) [![Stars](https://img.shields.io/github/stars/gauravapiscean/kernel-headroom)](https://github.com/gauravapiscean/kernel-headroom)
  - **Hardware:** NVIDIA · **Benchmark:** KernelBench
- **A Self-Growing Evaluation Methodology for NPU Operators with Theory-Derived Performance Upper Bounds** [![OpenReview](https://img.shields.io/badge/OpenReview-26.09-lightgrey)](https://openreview.net/forum?id=c6L1TukNbo) [![Code](https://img.shields.io/badge/Code-GitCode-blue)](https://gitcode.com/cann/cann-bench)
  - **Hardware:** Ascend

### 2026-07

- **Technical Report: AI-Assisted Gated DeltaNet Optimization on NVIDIA Blackwell** [![arXiv](https://img.shields.io/badge/arXiv-26.07-red)](https://arxiv.org/abs/2607.16831) [![Stars](https://img.shields.io/github/stars/Bammuri/mlsys26)](https://github.com/Bammuri/mlsys26)
  - **Institution:** Independent researcher
  - **Hardware:** NVIDIA · **Benchmark:** FlashInfer-Bench

### 2025-09

- **LLM-Powered Code Analysis and Optimization for Gaussian Splatting Kernels** [![arXiv](https://img.shields.io/badge/arXiv-25.09-red)](https://arxiv.org/abs/2509.25626)
  - **Institution:** North Carolina State University
  - **Hardware:** NVIDIA

### 2025-08

- **Tutoring LLM into a Better CUDA Optimizer** [![Euro-Par 2025](https://img.shields.io/badge/Euro--Par-25-green)](https://arxiv.org/abs/2510.16933) [![Stars](https://img.shields.io/github/stars/matyas-brabec/2025-europar-llm)](https://github.com/matyas-brabec/2025-europar-llm)
  - **Institution:** Charles University
  - **Kernel:** `CUDA` · **Hardware:** NVIDIA

## Evaluation integrity and reward hacking

- [robust-kbench](https://github.com/SakanaAI/robust-kbench) — hardened KernelBench after AI CUDA Engineer exploits; [paper](https://arxiv.org/abs/2509.14279)
- [METR Kernel Reward-Hacking Challenge](https://github.com/METR/RE-Bench/tree/main/ai_rd_triton_cumsum) — an evaluation task where reward hacking is explicitly audited
- [TRACE](https://arxiv.org/abs/2601.20103) — 54 exploit categories and 517 verified trajectories
- [RewardHackingAgents](https://arxiv.org/abs/2603.11337) — evaluator tampering as a first-class outcome
- [Standard Kernel Rubric](https://standardkernel.com/blog/standard-kernel-rubric/) — complexity, representation, hardware, performance, and automation rubric
- [Contract-Grade Verifier](https://arxiv.org/abs/2608.12700) — adversarial contract audit of 2,638 previously accepted generated kernels
- [KernelQuest](https://www.turing.com/blog/kernelquest-benchmark-ai-agents-triton-kernels) — 100 engineer-authored Triton tasks with compiled baselines and adversarial verification
- [D2K-Bench](https://arxiv.org/abs/2610.03226) — paired design-guided and unguided runs on 26 tasks / 85 workloads, separating design discovery from implementation

## Competitions and leaderboards

- [MLSys'26 FlashInfer Kernel-Gen Contest](https://mlsys26.flashinfer.ai/) — B200 fused MoE, sparse attention, and gated delta-net tracks
- [GPU MODE × AMD E2E Model Speedrun](https://www.amd.com/en/developer/resources/technical-articles/2026/new-gpumode-virtual-hackathon--e2e-model-speedrun.html) — MI355X end-to-end model optimization
- [GPU MODE reference kernels](https://github.com/gpu-mode/reference-kernels) — NVIDIA and AMD kernel leaderboards, including distributed kernels
- [AWS Trainium MoE Challenge](https://github.com/aws-neuron/nki-moe) — Qwen3 MoE on Trainium
- [KernelArena](https://www.kernelarena.ai/) — open accelerator-kernel evaluation and leaderboard

## Datasets

| Dataset | Content | Availability |
| --- | --- | --- |
| [AI CUDA Archive](https://huggingface.co/datasets/SakanaAI/AI-CUDA-Engineer-Archive) | CUDA, profiles, and verification records | Public dataset |
| [KernelBook](https://huggingface.co/datasets/GPUMODE/KernelBook) | PyTorch ↔ Triton pairs | Public dataset |
| [AutoTriton 14K](https://github.com/AI9Stars/AutoTriton) | Verified PyTorch-to-Triton examples | Public repository |
| [CUDA-Agent-Ops-6K](https://huggingface.co/datasets/BytedTsinghua-SIA/CUDA-Agent-Ops-6K) | Composite PyTorch operators | Public dataset |
| [kernelbot-data](https://huggingface.co/datasets/GPUMODE/kernelbot-data) | Competition submissions by hardware target | Public dataset |
| [Ascend-CoT](https://huggingface.co/datasets/AscendKernelGen/Ascend-COT-v1) | Ascend C reasoning chains | Public dataset |
| [HPC-Instruct](https://huggingface.co/datasets/hpcgroup/hpc-instruct) | HPC and parallel-programming instructions | Public dataset |

## Representations and infrastructure

**Representations:** [CUDA C/C++](https://docs.nvidia.com/cuda/cuda-c-programming-guide/) · [Triton](https://github.com/triton-lang/triton) · [CUTLASS / CuTe DSL](https://github.com/NVIDIA/cutlass) · [HIP / ROCm](https://rocm.docs.amd.com/) · [TileLang](https://github.com/tile-ai/tilelang) · [Pallas](https://docs.jax.dev/en/latest/pallas/index.html) · [cuTile Python](https://docs.nvidia.com/cuda/cutile-python/) · [Ascend C](https://www.hiascend.com/document/) · [NKI](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/general/nki/index.html) · [TT-Lang](https://github.com/tenstorrent/tt-lang).

**Agent and execution infrastructure:** [KernelGYM](https://github.com/hkust-nlp/KernelGYM) · [GPU Forecasters](https://github.com/codezakh/gpu-forecasters) · [NVIDIA CompileIQ](https://developer.nvidia.com/cuda/compileiq) · [Nsight Compute](https://docs.nvidia.com/nsight-compute/) · [Proton](https://github.com/triton-lang/triton/tree/main/third_party/proton) · [rocprof](https://rocm.docs.amd.com/projects/rocprofiler/en/latest/) · [msprof](https://www.hiascend.com/document/).

KREX (shared-GPU benchmarking isolation) and Xtrace (intra-kernel tracing) are listed under [Infrastructure and tools](#infrastructure-and-tools), not as generation agents.

**Reference and production kernel libraries:** [FlashAttention](https://github.com/Dao-AILab/flash-attention) · [FlashInfer](https://github.com/flashinfer-ai/flashinfer) · [DeepGEMM](https://github.com/deepseek-ai/DeepGEMM) · [TileKernels](https://github.com/deepseek-ai/TileKernels) · [Liger-Kernel](https://github.com/linkedin/Liger-Kernel) · [FlagGems](https://github.com/FlagOpen/FlagGems) · [AITER](https://github.com/ROCm/aiter).

## Research sources

- [Towards Automated Kernel Generation in the Era of LLMs](https://arxiv.org/abs/2601.15727) — broad survey and research index
- [awesome-LLM-driven-kernel-generation](https://github.com/flagos-ai/awesome-LLM-driven-kernel-generation) and [Awesome-LLM4Kernel](https://github.com/kcxain/Awesome-LLM4Kernel) — companion indexes

## Contributing

Add or fix an entry in [`data/entries.yaml`](data/entries.yaml), run `python3 scripts/build_readme.py`, and open a pull request. Link only a paper's own code, models, and data, not the benchmarks or tools it uses. See [CONTRIBUTING.md](CONTRIBUTING.md) for the fields and badge rules.

## Citation

```bibtex
@misc{you2026awesomekernelagent,
  author       = {Lianzhong You},
  title        = {Awesome Kernel Agent: The Living Map of LLM-Driven Kernel
                  Generation and Optimization},
  year         = {2026},
  publisher    = {GitHub},
  url          = {https://github.com/youyve/awesome-kernel-agent}
}
```

## License

List content: [CC-BY-4.0](LICENSE) · scripts: [MIT](scripts/LICENSE).

**Research cutoff:** 2026-10-19 · Maintained by [Lianzhong You](mailto:youyve@foxmail.com), HKUST (GZ)
