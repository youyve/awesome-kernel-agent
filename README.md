# Awesome Kernel Agent [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> A curated list of LLM-driven Kernel Agents — papers, projects, datasets, and benchmarks for automated GPU/NPU kernel generation and optimization.

**Kernel Agent** = systems that use LLMs (single model or multi-agent) to automatically generate or iteratively optimize operator-level code (kernels) for GPU / NPU / ASIC accelerators.

This list covers **58+ agents across 11 DSLs**, with primary DSL, technical route, open-source status, paper link, and code link for each.

---

## Contents

- [Background](#background)
- [Legend](#legend)
- [Survey & Index](#survey--index)
- [Agents by Primary DSL](#agents-by-primary-dsl)
  - [Triton](#triton-19-agents)
  - [CUDA / CUDA-C++](#cuda--cuda-c-26-agents)
  - [Ascend C / NPU](#ascend-c--npu-5-agents)
  - [TileLang](#tilelang)
  - [HIP / ROCm](#hip--rocm)
  - [NKI (AWS Trainium)](#nki-aws-trainium)
  - [SYCL](#sycl)
  - [CuTe DSL / cuTile / ThunderKittens / Pallas](#cute-dsl--cutile--thunderkittens--pallas)
- [Benchmarks](#benchmarks)
- [Datasets](#datasets)
- [DSL Languages](#dsl-languages)
- [Infrastructure & Tools](#infrastructure--tools)
- [Reading List](#reading-list)
- [Contributing](#contributing)
- [License](#license)

---

## Background

As Moore's Law approaches its physical limits, performance gains in computing increasingly shift from silicon to software, and within software, to the kernel layer. **LLM-driven kernel generation** has emerged in early 2025 as a fast-evolving field combining advances in code generation, reinforcement learning, agentic systems, and evolutionary search.

The field's birth is marked by three events in February 2025:

1. **KernelBench** (Stanford, ICML'25) — established the de facto benchmark
2. **AI CUDA Engineer** (Sakana AI) — first widely-discussed autonomous system (also the cautionary tale of reward hacking)
3. **NVIDIA × DeepSeek-R1 blog** — official endorsement of inference-time scaling for kernel generation

This list catalogs the resulting ecosystem.

---

## Legend

**Open-source status**

| Badge | Meaning |
|:---:|:---|
| 🟢 **OPEN** | Fully open-source (code, data, sometimes model) |
| 🟡 **PARTIAL** | Model weights / dataset / project page available, training code or full impl missing |
| 🟠 **WIP** | Repository exists but marked "under construction" |
| ⚪ **CLOSED** | Paper only, no public repository |
| ⚫ **PROPRIETARY** | Production system, deliberately closed |

**Technical route**

| Code | Route | Description |
|:---:|:---|:---|
| **A** | Single-shot prompting | Direct LLM generation, baseline |
| **B** | Iterative refinement | Compile/run feedback loop, training-free |
| **C** | Multi-turn RL | GRPO/PPO with verifiable rewards |
| **D** | Multi-Agent + Profiler | Specialized agents + NCU/msprof feedback |
| **E** | Evolutionary + Memory | Population, archive, skill memory |

---

## Survey & Index

- [Towards Automated Kernel Generation in the Era of LLMs](https://arxiv.org/abs/2601.15727) — Yu et al. (arXiv:2601.15727, 2026-01) — *The main survey, 60+ works reviewed.*
- [awesome-LLM-driven-kernel-generation](https://github.com/flagos-ai/awesome-LLM-driven-kernel-generation) — flagos-ai — *Companion repository of the survey.*
- [Awesome-LLM4Kernel](https://github.com/kcxain/Awesome-LLM4Kernel) — kcxain — *Alternative curated index.*

---

## Agents by Primary DSL

> Each entry: `Agent — Team · Date · [Route]` followed by paper / code links and key result.

### Triton (19 agents)

> Largest ecosystem, driven by Python-like syntax and abundant pretraining data.

#### 2026

- [KernelPilot](https://github.com/BBuf/kernel-pilot) — BBuf · 2026-05 · **[D]** · 🟢 OPEN
  Autonomous Triton/CUDA optimization with NCU profile feedback; uses Humanize RLCR runtime; 84-iter budget.

- **Kernel-Smith** — Shanghai AI Lab · 2026-03 · **[E]** · ⚪ CLOSED
  Evolutionary kernel optimization; upstream contributions to SGLang/LMDeploy.
  Paper: [arXiv:2603.28342](https://arxiv.org/abs/2603.28342)

- [PyTorch KernelAgent](https://github.com/meta-pytorch/KernelAgent) ⭐ — Meta / PyTorch · 2026-03 · **[D]** · 🟢 OPEN
  5-agent system (Profiler/Judge/Analyze/Orchestrator/Benchmark) + NCU + roofline.
  Blog: [pytorch.org](https://pytorch.org/blog/kernelagent-hardware-guided-gpu-kernel-optimization-via-multi-agent-orchestration/)
  Result: H100 89% roofline, 1.56× over `torch.compile`.

- [AKO / AKO4ALL](https://github.com/TongmingLAIC/AKO4ALL) — TLAIC · 2026-03 · **[D]** · 🟢 OPEN
  Generic coding-agent harness for kernel optimization; supports Triton, CUDA, TileLang, C++.
  Project page: [tongminglaic.github.io/AKO](https://tongminglaic.github.io/AKO/)
  Result: 10/13 kernels beat NVIDIA baseline on SOL-ExecBench.

- [Dr. Kernel](https://github.com/hkust-nlp/KernelGYM) — HKUST-NLP · 2026-02 · **[C]** · 🟢 OPEN
  14B model trained via KernelGYM RL environment; matches Claude 4.5 Sonnet on KernelBench.
  Paper: [arXiv:2602.05885](https://arxiv.org/abs/2602.05885)

- [GEAK-Triton v2](https://github.com/AMD-AGI/GEAK) — AMD-AGI · 2026 · **[D]** · 🟢 OPEN
  Extension of GEAK family for AMD GPUs.
  Blog: [ROCm Blogs](https://rocm.blogs.amd.com/artificial-intelligence/geak-agents-family/README.html)

- [Xe-Forge](https://github.com/IntelLabs/Xe-Forge) — Intel Labs · 2026 · **[D]** · 🟢 OPEN
  Multi-stage LLM agent pipeline for optimizing Triton kernels on Intel XPU.

#### 2025

- [AKG-AGENT](https://github.com/mindspore-ai/akg) — Huawei × Hunan U · 2025-12 · **[D]** · 🟢 OPEN
  4-agent (Designer/Coder/Verifier/Conductor) supporting Triton (Ascend + CUDA), TileLang, AscendC, CPP, CUDA-C.
  Paper: [arXiv:2512.23424](https://arxiv.org/abs/2512.23424)

- [TritonForge](https://github.com/RLsys-Foundation/TritonForge) — RLsys-Foundation · 2025-12 · **[C]** · 🟢 OPEN
  SFT + RL for PyTorch-to-Triton conversion; NV + AMD cross-platform.
  Paper: [arXiv:2512.09196](https://arxiv.org/abs/2512.09196)

- [KernelFalcon](https://github.com/meta-pytorch/KernelAgent) — Meta / PyTorch · 2025-11 · **[D]** · 🟢 OPEN
  Predecessor of PyTorch KernelAgent; 100% correctness on all 250 KernelBench L1/L2/L3 tasks.
  Blog: [pytorch.org](https://pytorch.org/blog/kernelfalcon-autonomous-gpu-kernel-generation-via-deep-agents/)

- **KernelBand** — PKU · 2025-11 · **[D]** · ⚪ CLOSED
  Hierarchical multi-armed bandit for hardware-aware optimization.
  Paper: [arXiv:2511.18868](https://arxiv.org/abs/2511.18868)

- **PRAGMA** — Beihang University · 2025-11 · **[D]** · ⚪ CLOSED
  Profiling-reasoned multi-agent framework.
  Paper: [arXiv:2511.06345](https://arxiv.org/abs/2511.06345)

- **TritonRL** — Princeton / UW · 2025-10 · **[C]** · ⚪ CLOSED
  Training LLMs to write Triton without "cheating" (reward hacking sanitization).
  Paper: [arXiv:2510.17891](https://arxiv.org/abs/2510.17891)

- [ConCuR](https://huggingface.co/lkongam/KernelCoder) — HKUST · 2025-10 · **[A]** · 🟢 OPEN
  Conciseness-driven SFT for kernel generation.
  Paper: [arXiv:2510.07356](https://arxiv.org/abs/2510.07356)

- [KernelGen (Flagos)](https://github.com/flagos-ai/kernelgen) — Flagos · 2025-10 · **[D]** · 🟢 OPEN
  Interactive kernel generation platform.
  Site: [kernelgen.flagos.io](https://kernelgen.flagos.io/)

- **SwizzlePerf** — Harvard × AMD · 2025-08 · **[D]** · ⚪ CLOSED
  Hardware-aware LLM for GPU kernel performance optimization.
  Paper: [arXiv:2508.20258](https://arxiv.org/abs/2508.20258)

- [GEAK](https://github.com/AMD-AGI/GEAK) — AMD-AGI · 2025-07 · **[D]** · 🟢 OPEN
  4-module agent (generator/reflector/evaluator/optimizer); 2.59× speedup on MI300X.
  Paper: [arXiv:2507.23194](https://arxiv.org/abs/2507.23194)

- [AutoTriton](https://github.com/AI9Stars/AutoTriton) — THUNLP / AI9Stars · 2025-07 · **[C]** · 🟢 OPEN
  8B model trained via SFT + GRPO on 14.1K torch↔triton pairs.
  Paper: [arXiv:2507.05687](https://arxiv.org/abs/2507.05687)

- [KernelLLM](https://huggingface.co/facebook/KernelLLM) — Meta · 2025-05 · **[A]** · 🟡 PARTIAL
  Llama 3.1 8B fine-tuned on KernelBook (~25K torch↔triton pairs); beats GPT-4o on KernelBench-Triton L1.

---

### CUDA / CUDA-C++ (26 agents)

> Performance ceiling battleground; covers RL training, evolutionary search, and multi-agent orchestration.

#### 2026

- [AdaExplore](https://github.com/StigLidu/AdaExplore) — CMU · 2026-04 · **[E]** · 🟢 OPEN
  Failure-driven diversity-preserving exploration.
  Paper: [arXiv:2604.16625](https://arxiv.org/abs/2604.16625)

- [AVO](https://github.com/austin1997/AVO) ⭐⭐ — NVIDIA × OctoML (23 authors) · 2026-03 · **[E]** · 🟡 PARTIAL
  **Paradigm shift**: agent IS the variation operator (propose/repair/critique/verify), not just a candidate generator. CUDA + PTX, B200 multi-head attention.
  Paper: [arXiv:2603.24517](https://arxiv.org/abs/2603.24517)
  Result: +3.5% over cuDNN, +10.5% over FlashAttention-4 after 7 days of autonomous evolution.
  *Note: linked repo is community Python reimplementation.*

- [AutoKernel](https://github.com/RightNow-AI/autokernel) — RightNow-AI · 2026-03 · **[D]** · 🟢 OPEN
  Autoresearch for GPU kernels with iterative agent-driven search.
  Paper: [arXiv:2603.21331](https://arxiv.org/abs/2603.21331)

- [KernelSkill](https://github.com/0satan0/KernelMem) — Beihang University · 2026-03 · **[E]** · 🟢 OPEN
  Dual-level memory architecture with reusable expert skills.
  Paper: [arXiv:2603.10085](https://arxiv.org/abs/2603.10085)
  Result: L1=5.44×, L2=2.82×, L3=1.92× on KernelBench.

- [InCoder-32B](https://github.com/CSJianYang/Industrial-Coder) — Beihang University · 2026-03 · **[A]** · 🟢 OPEN
  Code foundation model for industrial kernel generation.
  Paper: [arXiv:2603.16790](https://arxiv.org/pdf/2603.16790)

- [CUDA Agent](https://github.com/BytedTsinghua-SIA/CUDA-Agent) ⭐ — ByteDance × Tsinghua · 2026-02 · **[C]** · 🟢 OPEN
  128K context, 200 interaction turns; first open RL agent to beat Claude Opus 4.6 and Gemini 3 Pro on KernelBench (100/100/92% on L1/L2/L3).
  Paper: [arXiv:2602.24286](https://arxiv.org/abs/2602.24286)

- **KernelBlaster** — NVIDIA × UC Berkeley · 2026-02 · **[E]** · ⚪ CLOSED
  Memory-augmented in-context RL; persistent CUDA knowledge base.
  Paper: [arXiv:2602.14293](https://arxiv.org/abs/2602.14293)

- [K-Search](https://github.com/caoshiyi/K-Search) — UC Berkeley · 2026-02 · **[E]** · 🟢 OPEN
  Co-evolving intrinsic world model for kernel generation.
  Paper: [arXiv:2602.19128](https://arxiv.org/abs/2602.19128)

#### 2025

- **KernelEvolve** ⭐ — Meta · 2025-12 (ISCA'26) · **[E]** · ⚫ PROPRIETARY
  Production deployment for Andromeda ads model. NV +60% / MTIA +25% / peak 17×.
  Paper: [arXiv:2512.23236](https://arxiv.org/abs/2512.23236)
  Blog: [Meta Engineering](https://engineering.fb.com/2026/04/02/developer-tools/kernelevolve-how-metas-ranking-engineer-agent-optimizes-ai-infrastructure/)

- [CUDA-L2](https://github.com/deepreinforce-ai/CUDA-L2) — DeepReinforce · 2025-12 · **[C]** · 🟢 OPEN
  Surpasses cuBLAS for matrix multiplication.
  Paper: [arXiv:2512.02551](https://arxiv.org/abs/2512.02551)

- [cuPilot](https://github.com/champloo2878/cuPilot-Kernels) — Southeast University × Tsinghua · 2025-12 · **[D]** · 🟡 PARTIAL
  Strategy-coordinated multi-agent framework. (Linked repo contains generated kernel outputs.)
  Paper: [arXiv:2512.16465](https://arxiv.org/abs/2512.16465)

- **PEAK** — Stanford × MSR Redmond · 2025-12 · **[D]** · ⚪ CLOSED
  Natural language transformation for kernel optimization. Supports CUDA, HIP, HLSL.
  Paper: [arXiv:2512.19018](https://arxiv.org/abs/2512.19018)

- [CudaForge](https://github.com/OptimAI-Lab/CudaForge) — UMN OptimAI Lab · 2025-11 · **[D]** · 🟢 OPEN
  Training-free Coder + Judge dual-agent with NCU profiling.
  Paper: [arXiv:2511.01884](https://arxiv.org/abs/2511.01884)
  Result: A100 97.6% correctness, 1.68× / 2.27× — beats Kevin-32B.

- [QiMeng-Kernel](https://github.com/QiMeng-IPRC/QiMeng-Kernel) — CAS ICT · 2025-11 (AAAI'26) · **[C]** · 🟡 PARTIAL
  Macro-Thinking Micro-Coding (MTMC) paradigm.
  Paper: [arXiv:2511.20100](https://arxiv.org/abs/2511.20100)
  Result: ~100% on L1/L2, ~70% on L3 (50+pp ahead of baselines).
  *Note: repo exists but no implementation code.*

- **QiMeng-Attention** — CAS ICT · 2025 (ACL'25 Findings) · **[D]** · ⚪ CLOSED
  Self-optimizing framework for high-performance attention code.
  Paper: [ACL'25 Findings](https://aclanthology.org/2025.findings-acl.446/)
  Result: MLA 2.15× cuDNN on A100.

- **QiMeng-TensorOp** — CAS ICT · 2025 (IJCAI'25) · **[D]** · ⚪ CLOSED
  MCTS + hardware primitives for tensor operator generation. CUDA + RISC-V.
  Paper: [arXiv:2505.06302](https://arxiv.org/abs/2505.06302)
  Result: 251% OpenBLAS on RISC-V, 124% cuBLAS on NVIDIA GPU.

- **QiMeng-GEMM** — CAS ICT · 2025 (AAAI'25) · **[D]** · 🟡 PARTIAL
  Meta-prompt + Tree-of-Thought for high-performance GEMM. CUDA + RISC-V.
  Paper: [AAAI'25](https://ojs.aaai.org/index.php/AAAI/article/view/34461)
  Result: 211% OpenBLAS, 115% cuBLAS.

- **KForge** — Gimlet Labs · 2025-11 · **[D]** · ⚪ CLOSED
  Program synthesis for diverse AI hardware accelerators.
  Paper: [arXiv:2511.13274](https://arxiv.org/abs/2511.13274)

- **STARK** — Meta · 2025-10 · **[D]** · ⚪ CLOSED
  Strategic team of agents for refining kernels.
  Paper: [arXiv:2510.16996](https://arxiv.org/abs/2510.16996)

- **EvoEngineer** — City University of Hong Kong · 2025-10 · **[E]** · ⚪ CLOSED
  Mastering automated CUDA kernel code evolution.
  Paper: [arXiv:2510.03760](https://arxiv.org/abs/2510.03760)
  Result: median 2.72×, peak 36.75× speedup.

- [Astra](https://github.com/Anjiang-Wei/Astra) — Stanford · 2025-09 (NeurIPS'25) · **[D]** · 🟢 OPEN
  Multi-agent system for GPU kernel performance optimization on SGLang.
  Paper: [arXiv:2509.07506](https://arxiv.org/abs/2509.07506)
  Result: 1.32× average speedup zero-shot with o4-mini.

- **Kevin** — Cognition · 2025-07 · **[C]** · 🟡 PARTIAL
  Multi-turn RL on QwQ-32B with GRPO. KernelBench correctness 56%→82%, speedup 0.53×→1.10×.
  Paper: [arXiv:2507.11948](https://arxiv.org/abs/2507.11948)

- [CUDA-L1](https://github.com/deepreinforce-ai/CUDA-L1) — DeepReinforce · 2025-07 · **[C]** · 🟢 OPEN
  Contrastive RL; KernelBench avg 3.12×, peak 120×. Cross-architecture generalization (A100→H100/L40/3090).
  Paper: [arXiv:2507.14111](https://arxiv.org/abs/2507.14111)

- **GPU Kernel Scientist** — Anonymous · 2025-06 · **[D]** · ⚪ CLOSED
  Iterative kernel optimization framework with hypothesis-driven search.
  Paper: [arXiv:2506.20807](https://arxiv.org/abs/2506.20807)

- **CUDA-LLM** — Shanghai Jiao Tong University · 2025-06 · **[D]** · ⚪ CLOSED
  Generates efficient CUDA kernels with hardware-aware LLM prompts.
  Paper: [arXiv:2506.09092](https://arxiv.org/abs/2506.09092)

- [AI CUDA Engineer](https://huggingface.co/datasets/SakanaAI/AI-CUDA-Engineer-Archive) ⚠️ — Sakana AI · 2025-02 · **[E]** · 🟡 PARTIAL
  Four-stage pipeline (Convert / Translate / Optimize / Compose); 30K kernel archive (17K verified).
  Paper: [arXiv:2509.14279](https://arxiv.org/abs/2509.14279)
  **Cautionary tale**: initial claims of 10–100× found to include reward-hacking exploits; later fixed in robust-kbench.

---

### Ascend C / NPU (5 agents)

> The fastest-growing non-NVIDIA stack; 5 systems in 4 months but mostly closed.

- **AscendOptimizer** — ECNU × Tongji · 2026-03 · **[E]** · 🟡 PARTIAL
  Episodic agent for Ascend NPU operator optimization.
  Paper: [arXiv:2603.23566](https://arxiv.org/abs/2603.23566)
  Result: 1.21× geomean on 127 AscendC operators; 49.61% beat references.

- [EvoKernel (Cold-Start)](https://evokernel.zhuo.li/) — SJTU · 2026-03 · **[E]** · 🟡 PARTIAL
  Cold-start drafting + continual refining; value-driven memory.
  Paper: [arXiv:2603.10846](https://arxiv.org/abs/2603.10846)
  Result: correctness 11% → 83% (GPT-5.2: 11% → 98.5%).

- [AscendKernelGen](https://huggingface.co/datasets/AscendKernelGen/Ascend-COT-v1) — Pengcheng Lab · 2026-01 · **[C]** · 🟡 PARTIAL
  Ascend-CoT dataset + RLEF training.
  Paper: [arXiv:2601.07160](https://arxiv.org/abs/2601.07160)
  Result: L2 compilation 0% → 95.5%.

- **AscendCraft** — NJU × Huawei · 2026-01 · **[D]** · ⚪ CLOSED
  DSL-guided transcompilation, training-free.
  Paper: [arXiv:2601.22760](https://arxiv.org/abs/2601.22760)
  Result: 98.1% compilation, 90.4% correctness.

- [AKG-AGENT](https://github.com/mindspore-ai/akg) — Huawei × Hunan U · 2025-12 · **[D]** · 🟢 OPEN
  *See full entry under Triton.* Supports AscendC as backend.

---

### TileLang

- [AKG-AGENT](https://github.com/mindspore-ai/akg) — *See above.* TileLang backend.
- [AKO / AKO4ALL](https://github.com/TongmingLAIC/AKO4ALL) — *See above.* TileLang supported.
- [TileLang-Ascend](https://github.com/tile-ai/tilelang-ascend) — tile-ai · 2025+ · adapter (not an agent) · 🟢 OPEN
  Adapter layer connecting TileLang to Ascend backend.

---

### HIP / ROCm

- [GEAK-HIP](https://github.com/AMD-AGI/GEAK) — AMD-AGI · 2026 · **[D]** · 🟢 OPEN
  GEAK extension for HIP code optimization.
  Blog: [ROCm Blogs](https://rocm.blogs.amd.com/software-tools-optimization/geak-hip-optimizations/README.html)

- [IntelliPerf](https://github.com/AMDResearch/intelliperf) — AMD Research · 2025 · **[D]** · 🟢 OPEN
  Profiling-guided LLM framework for AMD GPUs; supports HIP + Triton.

- [IntelliKit](https://github.com/AMDResearch/intellikit) — AMD Research · 2025-03 · profiling toolkit · 🟢 OPEN
  LLM-ready profiling toolkit for AMD GPUs.

---

### NKI (AWS Trainium)

- **Neuron Agentic Development** — AWS · 2026-04 · **[D]** · ⚫ PROPRIETARY
  Official AWS announcement of agentic NKI kernel development.
  Announcement: [AWS Whats New](https://aws.amazon.com/about-aws/whats-new/2026/04/announcing-neuron-agentic-development/)

- [AccelOpt](https://github.com/zhang677/AccelOpt) ⭐ — Stanford × AWS · 2025-11 (MLSys'26) · **[E]** · 🟠 WIP
  Self-improving LLM agentic system for AI accelerator kernel optimization. Trainium + Triton dual backend.
  Paper: [arXiv:2511.15915](https://arxiv.org/abs/2511.15915)
  Result: 49% → 61% peak throughput on Trainium 1, 45% → 59% on Trainium 2.

---

### SYCL

- **KernelFoundry** — Intel · 2026-03 · **[E]** · ⚪ CLOSED
  Hardware-aware evolutionary GPU kernel optimization. Primary SYCL, secondary CUDA.
  Paper: [arXiv:2603.12440](https://arxiv.org/abs/2603.12440)

---

### CuTe DSL / cuTile / ThunderKittens / Pallas

> Coverage gap zone — these high-performance DSLs have few or no dedicated agents.

- **CuTeGen** — Anonymous · 2026-04 · **[D]** · ⚪ CLOSED
  Iterative agentic synthesis using CuTe abstraction.
  Paper: [arXiv:2604.01489](https://arxiv.org/abs/2604.01489)

- **TileGym** — NVIDIA · 2026 · **[E]** · 🟡 PARTIAL
  AI-driven translation from cuTile Python to cuTile.jl (Julia).
  Blog: [NVIDIA Developer](https://developer.nvidia.com/blog/automating-gpu-kernel-translation-with-ai-agents-cutile-python-to-cutile-jl/)

- **ThunderKittens** — *No dedicated agent.* TK 2.0 (2026-01) has Blackwell + MXFP8/NVFP4 support but kernels remain hand-written.

- **Pallas (TPU)** — *No dedicated agent.* Covered by MultiKernelBench evaluation only.

---

## Benchmarks

| Benchmark | Venue | Scale | Hardware | Focus |
|:---|:---:|:---|:---|:---|
| [KernelBench](https://github.com/ScalingIntelligence/KernelBench) | ICML'25 | 250 tasks × 4 levels | NVIDIA | The de facto standard ([arXiv:2502.10517](https://arxiv.org/abs/2502.10517)) |
| [robust-kbench](https://github.com/SakanaAI/robust-kbench) | arXiv | Hardened KernelBench | NVIDIA | Anti-reward-hacking ([arXiv:2509.14279](https://arxiv.org/abs/2509.14279)) |
| [TritonBench](https://github.com/thunlp/TritonBench) | ACL'25 | 184 Triton operators | NV + AMD | Triton-specific ([arXiv:2502.14752](https://arxiv.org/abs/2502.14752)) |
| [TritonGym](https://openreview.net/forum?id=oaKd1fVgWc) | OpenReview | Agent workflow | NV Triton | Agentic Triton evaluation |
| [MultiKernelBench](https://github.com/wzzll123/MultiKernelBench) | arXiv | 285 tasks × 14 categories | NV + Ascend + TPU | Cross-platform ([arXiv:2507.17773](https://arxiv.org/abs/2507.17773)) |
| [GEAK Benchmarks](https://github.com/AMD-AGI/GEAK) | arXiv | 184 + 30 ROCm | AMD MI300X | AMD Triton ([arXiv:2507.23194](https://arxiv.org/abs/2507.23194)) |
| [BackendBench](https://github.com/meta-pytorch/BackendBench) | repo | — | NVIDIA | Meta PyTorch backend |
| [FlashInfer-Bench](https://mlsys26.flashinfer.ai/) | MLSys'26 | 3 tracks (MoE / Sparse Attn / GDN) | B200 | Real LLM serving workloads ([arXiv:2601.00227](https://arxiv.org/abs/2601.00227)) |
| [ISO-Bench](https://github.com/Lossfunk/ISO-Bench) | arXiv | Production workload | NVIDIA | Real-world inference ([arXiv:2602.19594](https://arxiv.org/abs/2602.19594)) |
| [ComputeEval](https://github.com/NVIDIA/compute-eval) | repo | — | NVIDIA | NVIDIA evaluation suite |
| [KernelArena](https://github.com/wafer-ai/kernel-arena) | site | — | — | Competitive evaluation platform |
| [KernelCraft](https://arxiv.org/abs/2603.08721) | arXiv | Emerging hardware | misc | Close-to-metal generation |
| [SOL-ExecBench](https://research.nvidia.com/benchmarks/sol-execbench) | NVIDIA | Real kernels | NVIDIA | Speed-of-Light benchmarking ([arXiv:2603.19173](https://arxiv.org/abs/2603.19173)) |
| [KernelBench-v3](https://github.com/Infatoshi/KernelBench-v3) | repo | Hard variant | NVIDIA | Community reform |
| [KernelBenchX](https://github.com/BonnieW05/KernelBenchX) | arXiv | 176 tasks × 15 categories | NVIDIA | Category-aware ([arXiv:2605.04956](https://arxiv.org/abs/2605.04956)) |
| [NPUKernelBench](https://openi.pcl.ac.cn/PCL-Benchmark/NPUKernelBench) | PCL | Ascend tasks | Ascend | AscendKernelGen companion |
| [CANN Bench](https://gitcode.com/cann/cann-bench) | repo | CANN ops | Ascend | Huawei CANN framework |
| [ParEval](https://github.com/parallelcodefoundry/ParEval) | arXiv | Parallel code | misc | Pioneer parallel benchmark ([arXiv:2401.12554](https://arxiv.org/abs/2401.12554)) |
| [AWS Trainium MoE Challenge](https://github.com/aws-neuron/nki-moe) | MLSys'26 | Qwen3-30B-A3B | Trainium 2/3 | MLSys'26 competition |

---

## Datasets

| Dataset | Size | Content | License |
|:---|:---:|:---|:---|
| [AI CUDA Archive](https://huggingface.co/datasets/SakanaAI/AI-CUDA-Engineer-Archive) | 30K (17K verified) | CUDA + NCU profile + speedup | CC-By-4.0 |
| [KernelBook](https://huggingface.co/datasets/GPUMODE/KernelBook) | 18,162 pairs | torch ↔ Triton | Open |
| [AutoTriton 14K](https://github.com/AI9Stars/AutoTriton) | 14.1K | torch-Triton verified | Open |
| [CUDA-Agent-Ops-6K](https://huggingface.co/datasets/BytedTsinghua-SIA/CUDA-Agent-Ops-6K) | 6K | Composite PyTorch ops | Open |
| [Ascend-CoT](https://huggingface.co/datasets/AscendKernelGen/Ascend-COT-v1) | — | Ascend C reasoning chains | Open |
| [HPC-Instruct](https://huggingface.co/datasets/hpcgroup/hpc-instruct) | — | HPC optimization instructions | Open |
| [The Stack v2 (HPC)](https://huggingface.co/datasets/bigcode/the-stack-v2) | — | Code pretraining | Open |
| [KernelBench Samples](https://huggingface.co/datasets/ScalingIntelligence/kernelbench-samples) | — | Tasks + traces | Open |

---

## DSL Languages

### Established

- [CUDA C/C++](https://docs.nvidia.com/cuda/cuda-c-programming-guide/) — NVIDIA's foundational GPU language
- [Triton](https://github.com/triton-lang/triton) — OpenAI's Python-based DSL, the LLM-friendly lingua franca
- [CUTLASS / CuTe DSL](https://github.com/NVIDIA/cutlass) — NVIDIA C++ templates with new Python DSL
- [HIP / ROCm](https://rocm.docs.amd.com/) — AMD's CUDA equivalent

### Emerging

- [ThunderKittens](https://github.com/HazyResearch/ThunderKittens) — HazyResearch's tile-based CUDA DSL ([arXiv:2410.20399](https://arxiv.org/abs/2410.20399))
- [TileLang](https://github.com/tile-ai/tilelang) — MS × PKU's cross-hardware tile language ([arXiv:2504.17577](https://arxiv.org/abs/2504.17577))
- [Pallas](https://docs.jax.dev/en/latest/pallas/index.html) — Google's JAX kernel language for TPU/GPU
- [cuTile Python](https://docs.nvidia.com/cuda/cutile-python/) — NVIDIA's Python tile DSL (2025-Q4)
- [Ascend C](https://www.hiascend.com/document/) — Huawei's NPU language with host + device dual artifacts
- [NKI](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/general/nki/index.html) — AWS Neuron Kernel Interface for Trainium
- [tt-metal](https://github.com/tenstorrent/tt-metal) — Tenstorrent bare-metal programming
- [Intel XPU Triton](https://github.com/intel/intel-xpu-backend-for-triton) — Intel's Triton backend

---

## Infrastructure & Tools

### Agent harnesses

- [Humanize](https://github.com/PolyArch/humanize) — PolyArch — Claude Code plugin implementing RLCR (Ralph-Loop with Codex Review), used by KernelPilot.
- [KernelGYM](https://github.com/hkust-nlp/KernelGYM) — HKUST-NLP — Distributed GPU environment for RL on kernel generation; multi-backend CUDA/Triton.

### Profilers

- [Nsight Compute](https://docs.nvidia.com/nsight-compute/) — NVIDIA's per-kernel profiler
- [Proton](https://github.com/triton-lang/triton/tree/main/third_party/proton) — Triton's intra-kernel profiler
- [rocprof](https://rocm.docs.amd.com/projects/rocprofiler/en/latest/) — AMD's profiler
- [msprof](https://www.hiascend.com/document/) — Ascend NPU profiler

### Kernel libraries (reference / baseline)

- [FlashAttention](https://github.com/Dao-AILab/flash-attention) — Dao-AILab — Memory-efficient attention
- [FlashInfer](https://github.com/flashinfer-ai/flashinfer) — LLM serving kernel library
- [DeepGEMM](https://github.com/deepseek-ai/DeepGEMM) — DeepSeek's FP8 GEMM
- [Liger-Kernel](https://github.com/linkedin/Liger-Kernel) — LinkedIn's training kernels
- [FlagGems](https://github.com/FlagOpen/FlagGems) — BAAI's comprehensive Triton operator library
- [AITER](https://github.com/ROCm/aiter) — AMD's AI operator library

---

## Reading List

For newcomers, suggested reading order:

1. **Survey** — [Yu et al. arXiv:2601.15727](https://arxiv.org/abs/2601.15727)
2. **Benchmark** — [KernelBench paper](https://arxiv.org/abs/2502.10517)
3. **RL baseline** — [Kevin-32B paper](https://arxiv.org/abs/2507.11948) → [CUDA-L1](https://arxiv.org/abs/2507.14111) → [CUDA Agent](https://arxiv.org/abs/2602.24286)
4. **Agent harness** — [CudaForge](https://arxiv.org/abs/2511.01884) → [PyTorch KernelAgent blog](https://pytorch.org/blog/kernelagent-hardware-guided-gpu-kernel-optimization-via-multi-agent-orchestration/)
5. **Evolutionary** — [AI CUDA Engineer postmortem](https://arxiv.org/abs/2509.14279) → [KernelEvolve](https://arxiv.org/abs/2512.23236) → [AVO](https://arxiv.org/abs/2603.24517)
6. **Non-NVIDIA** — [GEAK (AMD)](https://arxiv.org/abs/2507.23194) → [AscendKernelGen](https://arxiv.org/abs/2601.07160) → [AccelOpt (Trainium)](https://arxiv.org/abs/2511.15915)
7. **NeurIPS 2025 Tutorial** — [How to Build Agents to Generate Kernels for Faster LLMs](https://neurips.cc/virtual/2025/128792)

---

## Contributing

Contributions welcome! See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

**Quick rules:**
- One entry per line, format: `[Name](link) — Team · Date · [Route] · Open-source status — Description.`
- Sort by date within each section (newest first).
- Include primary DSL classification.
- Verify all links work before submitting.

---

## License

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Licensed under the Apache License, Version 2.0. See [LICENSE](./LICENSE) for details.

---

**Maintained by** [Lianzhong You](mailto:youyve@foxmail.com) · HKUST (GZ)
**Last updated** 2026-05-22
