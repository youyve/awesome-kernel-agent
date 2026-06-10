# Awesome Kernel Agent [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> A curated list of LLM-driven **Kernel Agents** — papers, projects, datasets, and benchmarks for automated GPU / NPU / ASIC kernel generation and optimization.

A **Kernel Agent** uses an LLM (a single model or a multi-agent system) to automatically write or iteratively optimize operator-level code (kernels) for accelerators. This list tracks the systems, the benchmarks they compete on, the datasets they train on, and the tooling around them.

| | |
|:---|:---|
| **Systems & agents** | 75+ |
| **DSLs / backends covered** | 13 — Triton · CUDA · CUTLASS/CuTe · Ascend C · HIP/ROCm · NKI · SYCL · TileLang · cuTile · MUSA · TT-Lang · MTIA · TPU |
| **Benchmarks** | 151 in the companion list → [awesome-kernel-benchmark](https://github.com/youyve/awesome-kernel-benchmark) |
| **Competitions** | 4 active leaderboards |
| **Last updated** | 2026-06-05 |

---

## Contents

- [Background](#background)
- [Legend](#legend)
- [Survey & Index](#survey--index)
- [Agents by Primary DSL](#agents-by-primary-dsl)
  - [Triton](#triton)
  - [CUDA / CUDA-C++](#cuda--cuda-c)
  - [CUTLASS / CuTe DSL](#cutlass--cute-dsl)
  - [Ascend C / NPU](#ascend-c--npu)
  - [HIP / ROCm (AMD)](#hip--rocm-amd)
  - [NKI (AWS Trainium)](#nki-aws-trainium)
  - [SYCL (Intel)](#sycl-intel)
  - [TileLang](#tilelang)
  - [Emerging DSLs & other accelerators](#emerging-dsls--other-accelerators)
- [Benchmarks](#benchmarks) → full catalog: [**awesome-kernel-benchmark**](https://github.com/youyve/awesome-kernel-benchmark)
  - [Evaluation integrity & reward-hacking](#evaluation-integrity--reward-hacking)
  - [Competitions & leaderboards](#competitions--leaderboards)
- [Datasets](#datasets)
- [DSL Languages](#dsl-languages)
- [Infrastructure & Tools](#infrastructure--tools)
- [Reading List](#reading-list)
- [Contributing](#contributing)
- [License](#license)

---

## Background

As Moore's Law slows, performance increasingly comes from software, and within software from the kernel layer. **LLM-driven kernel generation** emerged in early 2025 and now spans code generation, reinforcement learning, agentic systems, and evolutionary search.

The field's birth is marked by three events in **February 2025**:

1. **KernelBench** (Stanford, ICML'25) — established the de facto benchmark.
2. **AI CUDA Engineer** (Sakana AI) — first widely-discussed autonomous system, and the cautionary tale of reward hacking.
3. **NVIDIA × DeepSeek-R1 blog** — official endorsement of inference-time scaling for kernel generation.

By mid-2026 the field has shifted from single-shot prompting toward **trained RL agents**, **evolutionary search with skill memory**, **profiler-in-the-loop multi-agent systems**, and **first-principles (Speed-of-Light) reward shaping** to fight benchmark gaming. Coverage is broadening beyond NVIDIA to AMD, Ascend, Trainium, Intel, and emerging domestic accelerators (Moore Threads MUSA, Cambricon, Tenstorrent).

---

## Legend

**Open-source status**

| Badge | Meaning |
|:---:|:---|
| 🟢 **OPEN** | Code (and often data / weights) publicly available |
| 🟡 **PARTIAL** | Weights / dataset / project page out, but training code or full impl missing |
| 🟠 **WIP** | Repo exists, marked "under construction" |
| ⚪ **CLOSED** | Paper only, no public repo |
| ⚫ **PROPRIETARY** | Production system, deliberately closed |

**Technical route**

| Code | Route | Description |
|:---:|:---|:---|
| **A** | Single-shot / translation | Direct generation or one-pass transpilation |
| **B** | Iterative refinement | Compile/run feedback loop, training-free |
| **C** | Multi-turn RL | GRPO / PPO with verifiable rewards |
| **D** | Multi-agent + profiler | Specialized agents + NCU / msprof feedback |
| **E** | Evolutionary + memory | Population, archive, skill memory |

Entry shape: `Name — Team · Date · [Route] · Status` then a one-line description with the key result and links.

---

## Survey & Index

- [Towards Automated Kernel Generation in the Era of LLMs](https://arxiv.org/abs/2601.15727) — Yu et al. · arXiv:2601.15727 · 2026-01 — the main survey, 60+ works reviewed.
- [awesome-LLM-driven-kernel-generation](https://github.com/flagos-ai/awesome-LLM-driven-kernel-generation) — flagos-ai — companion repo of the survey.
- [Awesome-LLM4Kernel](https://github.com/kcxain/Awesome-LLM4Kernel) — kcxain — alternative curated index.

---

## Agents by Primary DSL

> Sorted newest-first within each section. Multi-DSL systems are listed once under their primary DSL, with a `· also:` tag.

### Triton

> Largest ecosystem — Python-like syntax and abundant pretraining data make it the LLM lingua franca.

- [KernelPilot](https://github.com/BBuf/kernel-pilot) — BBuf · 2026-05 · **[D]** · 🟢 OPEN
  Autonomous Triton/CUDA optimization with NCU feedback over a Humanize RLCR runtime; 84-iteration budget.
- [DRTriton](https://arxiv.org/abs/2603.21465) — Texas A&M · 2026-03 · **[C]** · 🟠 WIP
  Scalable RL (CSP-DAG synthetic data + curriculum RL + test-time search); DRTriton-7B speeds up 92% of KernelBench L2 vs 23% for GPT-5.2.
- **Kernel-Smith** — Shanghai AI Lab · 2026-03 · **[E]** · ⚪ CLOSED
  Evolutionary kernel optimization; upstream contributions to SGLang/LMDeploy. [Paper](https://arxiv.org/abs/2603.28342)
- [PyTorch KernelAgent](https://github.com/meta-pytorch/KernelAgent) — Meta / PyTorch · 2026-03 · **[D]** · 🟢 OPEN
  5-agent system (Profiler / Judge / Analyze / Orchestrator / Benchmark) + NCU + roofline. H100 89% of roofline, 1.56× over `torch.compile`. [Blog](https://pytorch.org/blog/kernelagent-hardware-guided-gpu-kernel-optimization-via-multi-agent-orchestration/)
- [AKO / AKO4ALL](https://github.com/TongmingLAIC/AKO4ALL) — TLAIC · 2026-03 · **[D]** · 🟢 OPEN · also: CUDA, TileLang, C++
  Generic coding-agent harness for kernel optimization; 10/13 kernels beat the NVIDIA baseline on SOL-ExecBench. [Project](https://tongminglaic.github.io/AKO/)
- [Dr. Kernel](https://github.com/hkust-nlp/KernelGYM) — HKUST-NLP · 2026-02 · **[C]** · 🟢 OPEN
  14B model trained in the KernelGYM RL environment; matches Claude 4.5 Sonnet on KernelBench. [Paper](https://arxiv.org/abs/2602.05885)
- [GEAK-Triton v2](https://github.com/AMD-AGI/GEAK) — AMD-AGI · 2026 · **[D]** · 🟢 OPEN
  Extension of the GEAK family for AMD GPUs. [Blog](https://rocm.blogs.amd.com/artificial-intelligence/geak-agents-family/README.html)
- [Xe-Forge](https://github.com/IntelLabs/Xe-Forge) — Intel Labs · 2026 · **[D]** · 🟢 OPEN
  Multi-stage LLM agent pipeline optimizing Triton kernels on Intel XPU.
- [AKG-AGENT](https://github.com/mindspore-ai/akg/tree/master/akg_agents) — Huawei × Hunan U · 2025-12 · **[A]** · 🟢 OPEN · also: TileLang, AscendC, CUDA-C, C++
  Multi-agent (Designer / Coder / Verifier / Conductor) builds a DSL-agnostic "Unified Sketch" then lowers to 5 backends across NVIDIA GPU + Ascend NPU + CPU; 100% on KernelBench L1 (Triton-CUDA pass@4). [Paper](https://arxiv.org/abs/2512.23424)
- [TritonForge](https://github.com/RLsys-Foundation/TritonForge) — RLsys-Foundation · 2025-12 · **[C]** · 🟢 OPEN
  SFT + RL for PyTorch→Triton conversion; NVIDIA + AMD cross-platform. [Paper](https://arxiv.org/abs/2512.09196)
- **TritorX** — Meta · 2025-12 · **[D]** · ⚪ CLOSED · targets MTIA
  Generates functionally-correct Triton ATen kernels at scale for emerging accelerators; 481 ATen operators passing 20,000+ PyTorch OpInfo tests. [Paper](https://arxiv.org/abs/2512.10977)
- [KernelFalcon](https://github.com/meta-pytorch/KernelAgent) — Meta / PyTorch · 2025-11 · **[D]** · 🟢 OPEN
  Predecessor of PyTorch KernelAgent; 100% correctness on all 250 KernelBench L1/L2/L3 tasks. [Blog](https://pytorch.org/blog/kernelfalcon-autonomous-gpu-kernel-generation-via-deep-agents/)
- **KernelBand** — PKU · 2025-11 · **[D]** · ⚪ CLOSED
  Hierarchical multi-armed bandit for hardware-aware optimization. [Paper](https://arxiv.org/abs/2511.18868)
- **PRAGMA** — Beihang University · 2025-11 · **[D]** · ⚪ CLOSED
  Profiling-reasoned multi-agent framework. [Paper](https://arxiv.org/abs/2511.06345)
- **TritonRL** — Princeton / UW · 2025-10 · **[C]** · ⚪ CLOSED
  Trains LLMs to write Triton without "cheating" (reward-hacking sanitization). [Paper](https://arxiv.org/abs/2510.17891)
- [ConCuR](https://huggingface.co/lkongam/KernelCoder) — HKUST · 2025-10 · **[A]** · 🟢 OPEN
  Conciseness-driven SFT for kernel generation. [Paper](https://arxiv.org/abs/2510.07356)
- [KernelGen (Flagos)](https://github.com/flagos-ai/kernelgen) — Flagos · 2025-10 · **[D]** · 🟢 OPEN
  Interactive kernel generation platform. [Site](https://kernelgen.flagos.io/)
- **SwizzlePerf** — Harvard × AMD · 2025-08 · **[D]** · ⚪ CLOSED
  Hardware-aware LLM for GPU kernel performance optimization. [Paper](https://arxiv.org/abs/2508.20258)
- [GEAK](https://github.com/AMD-AGI/GEAK) — AMD-AGI · 2025-07 · **[D]** · 🟢 OPEN
  4-module agent (generator / reflector / evaluator / optimizer); 2.59× speedup on MI300X. [Paper](https://arxiv.org/abs/2507.23194)
- [AutoTriton](https://github.com/AI9Stars/AutoTriton) — THUNLP / AI9Stars · 2025-07 · **[C]** · 🟢 OPEN
  8B model trained via SFT + GRPO on 14.1K torch↔triton pairs. [Paper](https://arxiv.org/abs/2507.05687)
- [KernelLLM](https://huggingface.co/facebook/KernelLLM) — Meta · 2025-05 · **[A]** · 🟡 PARTIAL
  Llama 3.1 8B fine-tuned on KernelBook (~25K torch↔triton pairs); beats GPT-4o on KernelBench-Triton L1.

### CUDA / CUDA-C++

> The performance-ceiling battleground — RL training, evolutionary search, and multi-agent orchestration.

- [AdaExplore](https://github.com/StigLidu/AdaExplore) — CMU · 2026-04 · **[E]** · 🟢 OPEN
  Failure-driven, diversity-preserving exploration. [Paper](https://arxiv.org/abs/2604.16625)
- [AVO](https://github.com/austin1997/AVO) — NVIDIA × OctoML (23 authors) · 2026-03 · **[E]** · 🟡 PARTIAL · also: PTX
  **Paradigm shift**: the agent *is* the variation operator (propose / repair / critique / verify), not just a candidate generator. After 7 days of autonomous evolution on B200 MHA: +3.5% over cuDNN, +10.5% over FlashAttention-4. [Paper](https://arxiv.org/abs/2603.24517) · *linked repo is a community reimplementation.*
- [AutoKernel](https://github.com/RightNow-AI/autokernel) — RightNow AI (YC) · 2026-03 · **[B]** · 🟢 OPEN · also: Triton
  Keep/revert agent loop with Amdahl-law profiling and a 5-stage correctness harness (~40 experiments/hr); H100 RMSNorm 5.29× over eager / 2.83× over `torch.compile`. [Paper](https://arxiv.org/abs/2603.21331)
- [KernelSkill](https://github.com/0satan0/KernelMem) — Beihang University · 2026-03 · **[E]** · 🟢 OPEN
  Dual-level memory with reusable expert skills; KernelBench L1=5.44×, L2=2.82×, L3=1.92×. [Paper](https://arxiv.org/abs/2603.10085)
- [CUDAMaster](https://hanyx2021.github.io/MSKernelBenchDemo/) — Tsinghua · 2026-03 · **[D]** · 🟡 PARTIAL
  Bottleneck-aware filtered-profiling multi-agent + full toolchain generation across algebra / LLM / sparse / scientific kernels; ~35% over Astra, occasionally matches cuBLAS. Introduces [MSKernelBench](https://github.com/youyve/awesome-kernel-benchmark#layer-1--purpose-built-agent-benchmarks). [Paper](https://arxiv.org/abs/2603.07169)
- [InCoder-32B](https://github.com/CSJianYang/Industrial-Coder) — Beihang University · 2026-03 · **[A]** · 🟢 OPEN
  Industrial code foundation model; the 2026-04 **InCoder-32B-Thinking** variant adds an industrial code world model (ICWM) for pre-compilation self-verification, 38.0% on KernelBench, runs on RTX 4090. [Paper](https://arxiv.org/abs/2604.03144)
- [CUDA Agent](https://cuda-agent.github.io/) — ByteDance × Tsinghua · 2026-02 · **[B]** · 🟡 PARTIAL
  Large-scale agentic RL on Seed-1.6 MoE (OpenHands ReAct loop, 200 turns, 131K ctx); first open agent to beat Claude Opus and Gemini 3 Pro on KernelBench (2.11× geomean over `torch.compile`). Companion model repo [ByteDance-Seed/cudaLLM](https://github.com/ByteDance-Seed/cudaLLM). [Paper](https://huggingface.co/papers/2602.24286)
- **KernelBlaster** — NVIDIA × UC Berkeley · 2026-02 · **[E]** · ⚪ CLOSED
  Memory-augmented in-context RL; persistent CUDA knowledge base. [Paper](https://arxiv.org/abs/2602.14293)
- [K-Search](https://github.com/caoshiyi/K-Search) — UC Berkeley · 2026-02 · **[E]** · 🟢 OPEN
  Co-evolving intrinsic world model for kernel generation. [Paper](https://arxiv.org/abs/2602.19128)
- [CUDAnalyst](https://github.com/yuxuan-z19/cudanalyst) — Yee Hin Chong et al. · 2026-01 (ICML'26) · **[E]** · 🟢 OPEN
  Self-evolving agent (OpenEvolve + LLM4AD/EoH) that decouples *feedback acquisition* (Debugger / Analyzer / Profiler) from *plan generation*, doing causal generation-level attribution of which feedback signal drives the next plan. Ships generated `sol.cu` kernels and evaluates on PolyBench-ACC / NPB / XSBench. [OpenReview](https://openreview.net/forum?id=s70zO5Lvvj)
- **KernelEvolve** — Meta · 2025-12 (ISCA'26) · **[E]** · ⚫ PROPRIETARY · also: Triton, TLX, CuTe, HIP, MTIA C++
  Six-component agent (synthesizer + MCTS/evolutionary tree search + self-evolving RAG skill library + agentic RL) deployed on Andromeda ads: NVIDIA +60% / MTIA +25% / peak 17×; 100% on KernelBench. [Paper](https://arxiv.org/abs/2512.23236) · [Blog](https://engineering.fb.com/2026/04/02/developer-tools/kernelevolve-how-metas-ranking-engineer-agent-optimizes-ai-infrastructure/)
- [CUDA-L2](https://github.com/deepreinforce-ai/CUDA-L2) — DeepReinforce · 2025-12 · **[C]** · 🟢 OPEN
  Surpasses cuBLAS for matrix multiplication. [Paper](https://arxiv.org/abs/2512.02551)
- [cuPilot](https://github.com/champloo2878/cuPilot-Kernels) — Southeast U × Tsinghua · 2025-12 · **[D]** · 🟡 PARTIAL
  Strategy-coordinated multi-agent framework (linked repo holds generated kernel outputs). [Paper](https://arxiv.org/abs/2512.16465)
- **PEAK** — Stanford × MSR Redmond · 2025-12 · **[D]** · ⚪ CLOSED · also: HIP, HLSL
  Natural-language transformation for kernel optimization. [Paper](https://arxiv.org/abs/2512.19018)
- [CudaForge](https://github.com/OptimAI-Lab/CudaForge) — UMN OptimAI Lab · 2025-11 · **[D]** · 🟢 OPEN
  Training-free Coder + Judge dual-agent with NCU profiling; A100 97.6% correctness, 1.68× / 2.27× — beats Kevin-32B. [Paper](https://arxiv.org/abs/2511.01884)
- **KForge** — Gimlet Labs · 2025-11 · **[D]** · ⚪ CLOSED
  Program synthesis for diverse AI hardware accelerators. [Paper](https://arxiv.org/abs/2511.13274)
- **STARK** — Meta · 2025-10 · **[D]** · ⚪ CLOSED
  Strategic team of agents for refining kernels. [Paper](https://arxiv.org/abs/2510.16996)
- **EvoEngineer** — City University of Hong Kong · 2025-10 · **[E]** · ⚪ CLOSED
  Automated CUDA kernel code evolution; median 2.72×, peak 36.75× speedup. [Paper](https://arxiv.org/abs/2510.03760)
- [Astra](https://github.com/Anjiang-Wei/Astra) — Stanford · 2025-09 (NeurIPS'25) · **[D]** · 🟢 OPEN
  Multi-agent GPU kernel optimization on SGLang; 1.32× average zero-shot with o4-mini. [Paper](https://arxiv.org/abs/2509.07506)
- **Kevin** — Cognition · 2025-07 · **[C]** · 🟡 PARTIAL
  Multi-turn RL on QwQ-32B with GRPO; KernelBench correctness 56%→82%, speedup 0.53×→1.10×. [Paper](https://arxiv.org/abs/2507.11948)
- [CUDA-L1](https://github.com/deepreinforce-ai/CUDA-L1) — DeepReinforce · 2025-07 · **[C]** · 🟢 OPEN
  Contrastive RL; KernelBench avg 3.12×, peak 120×; A100→H100/L40/3090 generalization. [Paper](https://arxiv.org/abs/2507.14111)
- **GPU Kernel Scientist** — Anonymous · 2025-06 · **[D]** · ⚪ CLOSED
  Hypothesis-driven iterative kernel optimization. [Paper](https://arxiv.org/abs/2506.20807)
- **CUDA-LLM** — Shanghai Jiao Tong University · 2025-06 · **[D]** · ⚪ CLOSED
  Hardware-aware prompts for efficient CUDA generation. [Paper](https://arxiv.org/abs/2506.09092)
- [AI CUDA Engineer](https://huggingface.co/datasets/SakanaAI/AI-CUDA-Engineer-Archive) ⚠️ — Sakana AI · 2025-02 (paper 2025-09) · **[E]** · 🟡 PARTIAL
  Four-stage pipeline (Convert / Translate / Optimize / Compose); 30K-kernel archive (17K verified). **Cautionary tale**: initial 10–100× claims included reward-hacking exploits, later hardened in robust-kbench. Paper *"Towards Robust Agentic CUDA Kernel Benchmarking…"* [arXiv:2509.14279](https://arxiv.org/abs/2509.14279)

**QiMeng family** (CAS ICT — full-stack processor auto-design):

- [QiMeng-Kernel](https://github.com/QiMeng-IPRC/QiMeng-Kernel) — CAS ICT · 2025-11 (AAAI'26) · **[C]** · 🟡 PARTIAL
  Macro-Thinking Micro-Coding (MTMC); ~100% on L1/L2, ~70% on L3. [Paper](https://arxiv.org/abs/2511.20100) · *repo has no impl code yet.*
- [QiMeng-Xpiler](https://arxiv.org/abs/2505.02146) — CAS ICT × USTC × Cambricon · 2025-05 (OSDI'25) · **[D]** · 🟠 WIP · also: HIP, BANG, VNNI
  Neural-symbolic tensor-program transcompiler (LLM transform + SMT repair + hierarchical auto-tuning); ~95% translation accuracy across 4 backends, up to 2.0× over vendor libraries.
- **QiMeng-TensorOp** — CAS ICT · 2025 (IJCAI'25) · **[D]** · ⚪ CLOSED · also: RISC-V
  MCTS + hardware primitives; 251% OpenBLAS on RISC-V, 124% cuBLAS on NVIDIA. [Paper](https://arxiv.org/abs/2505.06302)
- **QiMeng-Attention** — CAS ICT · 2025 (ACL'25 Findings) · **[D]** · ⚪ CLOSED
  Self-optimizing attention code; MLA 2.15× cuDNN on A100. [Paper](https://aclanthology.org/2025.findings-acl.446/)
- **QiMeng-GEMM** — CAS ICT · 2025 (AAAI'25) · **[D]** · 🟡 PARTIAL · also: RISC-V
  Meta-prompt + Tree-of-Thought for GEMM; 211% OpenBLAS, 115% cuBLAS. [Paper](https://ojs.aaai.org/index.php/AAAI/article/view/34461)

### CUTLASS / CuTe DSL

> Template-level performance with a steep learning curve — agents must reason about tiles, layouts, and warp specialization.

- [CuTeGen](https://github.com/taratt/cutegen) — U Toronto × Standard Kernel · 2026-04 · **[D]** · 🟢 OPEN
  Generate-test-refine loop with a "delayed profiling" schedule (withholds low-level NCU feedback until structure stabilizes); 1.71× avg over PyTorch on 209 KernelBench L1/L2 tasks vs CudaForge 0.89×, zero low-precision shortcuts. [Paper](https://arxiv.org/abs/2604.01489)
- **FACT** — Heidari & Nikolopoulos · 2026-04 · **[B]** · ⚪ CLOSED
  Three-stage agentic workflow (pattern discovery / realization / composition) transpiling PyTorch modules into auto-tuned CUTLASS; 2.03× on MiniGPT, 1.41× on Llama-3-8B over PyTorch eager. [Paper](https://arxiv.org/abs/2604.26666)
- **μCUTLASS + Speed-of-Light Guidance** — NVIDIA × Stanford · 2026-03 · **[D]** · 🟠 WIP
  Two design principles for kernel-opt agents: a compact in-context-learnable DSL (μCUTLASS over CUTLASS) + first-principles Speed-of-Light bounds to budget trials and flag benchmark gaming; GPT-5-mini 0.40×→1.27×, +SOL up to 2.07×, saving 19–43% tokens. [Paper](https://arxiv.org/abs/2603.29010)

### Ascend C / NPU

> The fastest-growing non-NVIDIA stack — 5 systems in months, but mostly closed.

- **AscendOptimizer** — ECNU × Tongji · 2026-03 · **[E]** · 🟡 PARTIAL
  Episodic agent for Ascend NPU operator optimization; 1.21× geomean on 127 AscendC operators, 49.61% beat references. [Paper](https://arxiv.org/abs/2603.23566)
- [EvoKernel](https://evokernel.zhuo.li/) — SJTU · 2026-03 · **[E]** · 🟡 PARTIAL
  Cold-start drafting + continual refining with value-driven memory (stage-specific Q-values, cross-task sharing, no fine-tuning); correctness 11%→83%, median 3.60×. [Paper](https://arxiv.org/abs/2603.10846) · *paper frames the target as generic NPU/DSA; Ascend inferred.*
- [AscendKernelGen](https://huggingface.co/datasets/AscendKernelGen/Ascend-COT-v1) — Pengcheng Lab · 2026-01 · **[C]** · 🟡 PARTIAL
  Ascend-CoT dataset + RLEF training; L2 compilation 0%→95.5%. [Paper](https://arxiv.org/abs/2601.07160)
- **AscendCraft** — NJU × Huawei · 2026-01 · **[A]** · ⚪ CLOSED
  DSL-guided, training-free transcompilation; 98.1% compilation, 90.4% correctness. [Paper](https://arxiv.org/abs/2601.22760)
- [AKG-AGENT](https://github.com/mindspore-ai/akg/tree/master/akg_agents) — Huawei × Hunan U · 2025-12 — *see [Triton](#triton)*; AscendC is one of its five lowering backends (1.46× geomean over PyTorch Eager on Triton-Ascend).

### HIP / ROCm (AMD)

- **ARGUS** — Mai, Kozyrakis, Yuan et al. · 2026-04 · **[D]** · 🟠 WIP
  Agentic optimization guided by compile-time data-flow invariants (abstract interpretation + SMT with counterexamples) + in-context RL planner; on MI300X reaches **99–104% of hand-tuned assembly**, 2–1543× faster than prior agentic systems, 100% KernelBench L1 / 90% L2. [Paper](https://arxiv.org/abs/2604.18616)
- [GEAK-HIP](https://github.com/AMD-AGI/GEAK) — AMD-AGI · 2026 · **[D]** · 🟢 OPEN
  GEAK extension for HIP optimization. [Blog](https://rocm.blogs.amd.com/software-tools-optimization/geak-hip-optimizations/README.html)
- [IntelliPerf](https://github.com/AMDResearch/intelliperf) — AMD Research · 2025 · **[D]** · 🟢 OPEN · also: Triton
  Profiling-guided LLM framework for AMD GPUs.
- [IntelliKit](https://github.com/AMDResearch/intellikit) — AMD Research · 2025-03 · *profiling toolkit* · 🟢 OPEN
  LLM-ready profiling toolkit for AMD GPUs.

### NKI (AWS Trainium)

- **Neuron Agentic Development** — AWS · 2026-04 · **[D]** · ⚫ PROPRIETARY
  Official AWS announcement of agentic NKI kernel development. [Announcement](https://aws.amazon.com/about-aws/whats-new/2026/04/announcing-neuron-agentic-development/)
- [AccelOpt](https://github.com/zhang677/AccelOpt) — Stanford × AWS · 2025-11 (MLSys'26) · **[E]** · 🟠 WIP
  Self-improving agentic system for accelerator kernels; 45%→71% peak throughput on Trainium 1/2. Ships the [NKIBench](https://github.com/youyve/awesome-kernel-benchmark#layer-1--purpose-built-agent-benchmarks) suite. [Paper](https://arxiv.org/abs/2511.15915)

### SYCL (Intel)

- **KernelFoundry** — Intel · 2026-03 · **[E]** · 🟠 WIP · also: CUDA
  Hardware-aware evolutionary optimization (MAP-Elites quality-diversity + meta-prompting) generating CUDA *and* SYCL; demonstrated on Intel Arc B580 (Xe2). [Paper](https://arxiv.org/abs/2603.12440)

### TileLang

- [TileOPs (TOPS)](https://github.com/tile-ai/TileOPs) — tile-ai · 2026-01 · *agent-oriented op library* · 🟢 OPEN
  Spec-driven operator library: AI agents read declarative manifests (signatures, workloads, roofline formulas), generate TileLang kernels, and self-validate against Speed-of-Light bounds.
- [AKG-AGENT](https://github.com/mindspore-ai/akg/tree/master/akg_agents) — Huawei × Hunan U · 2025-12 — *see [Triton](#triton)*; TileLang is a lowering backend.
- [AKO / AKO4ALL](https://github.com/TongmingLAIC/AKO4ALL) — TLAIC · 2026-03 — *see [Triton](#triton)*; TileLang supported.
- [TileLang-Ascend](https://github.com/tile-ai/tilelang-ascend) — tile-ai · 2025+ · *adapter (not an agent)* · 🟢 OPEN
  Adapter layer connecting TileLang to the Ascend backend.

### Emerging DSLs & other accelerators

> New backends where AI codegen is in the loop from day one — and DSLs still waiting for a dedicated agent.

- [MusaCoder](https://arxiv.org/abs/2606.04847) — Moore Threads · 2026-06 · **[C]** · 🟠 WIP · CUDA + MUSA
  Full-stack training (progressive data synthesis + diversity-preserving rejection FT + execution-feedback RL via MooreEval) for native kernels on the domestic **Moore Threads MUSA** backend; 9B matches frontier closed models, 27B sets SOTA on a MUSA-ported KernelBench.
- [auto-gpu-kernel](https://github.com/Dogacel/auto-gpu-kernel) — Dogacel · 2026-05 · **[B]** · 🟢 OPEN · Triton (FlashInfer fmt)
  Claude-Code-driven autonomous optimizer that won **#1 (agent-only)** in the MLSys'26 FlashInfer contest, DeepSeek Sparse Attention track, avg **34.93×** speedup; runs `/optimize` every 15 min indefinitely on Modal cloud.
- [TileGym](https://github.com/NVIDIA/TileGym) — NVIDIA · 2026-04 · **[A]** · 🟢 OPEN · cuTile
  LLM agent "skill" auto-translating cuTile Python kernels to cuTile.jl (Julia) in one validated pass (17 rules, static validator); GEMM port ~4 min / ~78K tokens, no manual intervention. [Blog](https://developer.nvidia.com/blog/automating-gpu-kernel-translation-with-ai-agents-cutile-python-to-cutile-jl/)
- [TT-Lang + Claude Skills](https://github.com/tenstorrent/tt-lang) — Tenstorrent · 2026-01 · **[A]** · 🟢 OPEN · TT-Lang
  Python-embedded DSL for Tenstorrent hardware with AI codegen in the loop; ships Claude Skills that convert CUDA/Triton/cuTile/TileLang kernels "in seconds" + a functional simulator for hardware-free iteration.
- **AlphaEvolve for FHE on TPUs** — Google · 2026-05 · **[E]** · ⚪ CLOSED · JAX/TPU
  Applies AlphaEvolve evolutionary codegen to fully-homomorphic-encryption kernels on TPU v5e; within 24h: 2.5× TFHE bootstrap, 1.31× CKKS rotation vs human SOTA. [Paper](https://arxiv.org/abs/2605.14718)
- **Standard Kernel** — Standard Kernel (startup) · 2026-03 · **[D]** · ⚪ CLOSED · PTX layer
  Hybrid program-analysis + LLM reasoning at the PTX layer across Triton / TileLang / ThunderKittens / CUTLASS; reports 80%–4× end-to-end gains on H100. Raised $20M seed (Mar 2026; angels incl. Jeff Dean, Jonathan Frankle). [Announcement](https://standardkernel.com/blog/announcing-our-seed-round-is-kernel-generation-solved/)
- **ThunderKittens** — *no dedicated agent.* TK 2.0 (2026-01) adds Blackwell + MXFP8/NVFP4 support, but kernels remain hand-written.
- **Pallas (TPU)** — *no dedicated generation agent.* Evaluated only via [MultiKernelBench](https://github.com/youyve/awesome-kernel-benchmark#layer-1--purpose-built-agent-benchmarks).
- **Triton Gluon** — *no dedicated agent yet.* The lower-level Gluon dialect is an open coverage gap.

---

## Benchmarks

> 📊 **The full benchmark catalog has moved to its own repo: [awesome-kernel-benchmark](https://github.com/youyve/awesome-kernel-benchmark)** — **151 benchmarks** across two layers and 13 families, with a faceted (Berkeley-motif × abstraction) schema, a [motif × family coverage matrix](https://github.com/youyve/awesome-kernel-benchmark#motif--family-coverage-matrix), an [agent ↔ substrate map](https://github.com/youyve/awesome-kernel-benchmark#agent--substrate-map), and a machine-readable [`benchmarks.yaml`](https://github.com/youyve/awesome-kernel-benchmark/blob/main/data/benchmarks.yaml).

Kernel agents are evaluated in **two layers**: *purpose-built agent benchmarks* — [KernelBench](https://github.com/ScalingIntelligence/KernelBench), [TritonBench](https://github.com/thunlp/TritonBench), [CUDABench](https://github.com/CUDA-Bench/CUDABench), [SOL-ExecBench](https://research.nvidia.com/benchmarks/sol-execbench), [FlashInfer-Bench](https://github.com/flashinfer-ai/flashinfer-bench), … — that score LLM kernel generation directly, and *foundational substrate suites* — PolyBench, NPB, XSBench, Rodinia, HeCBench, … — that agents are evaluated *on* or asked to *optimize / translate*. An agent reporting "we optimize PolyBench-ACC / NPB / XSBench" (e.g. [CUDAnalyst](#cuda--cuda-c)) is using a substrate, not a purpose-built benchmark. **The four comparability anchors are PolyBench · NPB · XSBench · HeCBench.** Full tables, per-agent usage, and verification/auditability flags live in the [dedicated repo](https://github.com/youyve/awesome-kernel-benchmark).

The two evaluation sub-topics most tightly coupled to *agents* are tracked here:

### Evaluation integrity & reward-hacking

> Kernel agents are unusually prone to gaming timers and leaking reference outputs — a dedicated evaluation sub-field has formed.

- [robust-kbench](https://github.com/SakanaAI/robust-kbench) — Sakana AI · 2025-09 — hardened KernelBench after the AI CUDA Engineer exploits. [Paper](https://arxiv.org/abs/2509.14279)
- [METR Kernel Reward-Hacking Challenge](https://github.com/METR/RE-Bench/tree/main/ai_rd_triton_cumsum) — METR · 2026-01 — prefix-sum task where reward hacking is *allowed* and a model-judge reviews for cheating; documents `torch.cuda.synchronize` monkey-patching and stack-scavenging.
- [TRACE](https://arxiv.org/abs/2601.20103) — 2026-01 — reward-hack detection benchmark: 54 exploit categories, 517 verified trajectories; GPT-5.2 max-reasoning hits 63% detection.
- [RewardHackingAgents](https://arxiv.org/abs/2603.11337) — 2026-03 — treats evaluation integrity as a first-class outcome; evaluator-tampering in ~50% of natural episodes, eliminated by evaluator locking.
- [Standard Kernel Rubric](https://standardkernel.com/blog/standard-kernel-rubric/) — Standard Kernel · 2026-03 — 5-axis grading rubric (Complexity / Representation / Hardware / Performance / Automation) for "what counts as a win."

### Competitions & leaderboards

- [MLSys'26 FlashInfer Kernel-Gen Contest](https://mlsys26.flashinfer.ai/) — FlashInfer · 2026 — 3 tracks (fused MoE / sparse attention / gated delta net) on B200, biweekly bare-metal evals, human vs agent.
- [GPU MODE × AMD — $1.1M E2E Model Speedrun](https://www.amd.com/en/developer/resources/technical-articles/2026/new-gpumode-virtual-hackathon--e2e-model-speedrun.html) — 2026 — MXFP4 MoE / MLA / GEMM qualifiers → end-to-end DeepSeek-R1 & Kimi K2.5 on MI355X. Largest LLM-kernel competition to date.
- [GPU MODE — NVFP4 on Blackwell](https://github.com/gpu-mode/reference-kernels) — 2025-12 — fastest NVFP4 kernels (mxfp4-mm / moe-mxfp4 / mixed-mla), live Discord leaderboard.
- [GPU MODE × AMD — $100K Distributed Kernels](https://github.com/gpu-mode/reference-kernels) — 2025 — multi-GPU All-to-All / GEMM+ReduceScatter / AllGather+GEMM on 8× MI300X.
- [AWS Trainium MoE Challenge](https://github.com/aws-neuron/nki-moe) — MLSys'26 — Qwen3-30B-A3B on Trainium 2/3.
- [KernelArena](https://github.com/wafer-ai/kernel-arena) — wafer-ai — competitive evaluation platform.

---

## Datasets

| Dataset | Size | Content | License |
|:---|:---:|:---|:---|
| [AI CUDA Archive](https://huggingface.co/datasets/SakanaAI/AI-CUDA-Engineer-Archive) | 30K (17K verified) | CUDA + NCU profile + speedup | CC-BY-4.0 |
| [KernelBook](https://huggingface.co/datasets/GPUMODE/KernelBook) | 18,162 pairs | torch ↔ Triton | Open |
| [AutoTriton 14K](https://github.com/AI9Stars/AutoTriton) | 14.1K | torch-Triton verified | Open |
| [CUDA-Agent-Ops-6K](https://huggingface.co/datasets/BytedTsinghua-SIA/CUDA-Agent-Ops-6K) | 6K | composite PyTorch ops | Open |
| [GPUMODE/kernelbot-data](https://huggingface.co/datasets/GPUMODE/kernelbot-data) | competition corpus | KernelBot submissions by HW target (fp8-gemm, moe, mla, all2all…) | Open |
| [Ascend-CoT](https://huggingface.co/datasets/AscendKernelGen/Ascend-COT-v1) | — | Ascend C reasoning chains | Open |
| [HPC-Instruct](https://huggingface.co/datasets/hpcgroup/hpc-instruct) | ~122K | HPC/parallel instruction-answer pairs | Open |
| [The Stack v2 (HPC)](https://huggingface.co/datasets/bigcode/the-stack-v2) | — | code pretraining | Open |
| [KernelBench Samples](https://huggingface.co/datasets/ScalingIntelligence/kernelbench-samples) | — | tasks + traces | Open |

---

## DSL Languages

### Established

- [CUDA C/C++](https://docs.nvidia.com/cuda/cuda-c-programming-guide/) — NVIDIA's foundational GPU language.
- [Triton](https://github.com/triton-lang/triton) — Python-based DSL, the LLM-friendly lingua franca (lower-level **Gluon** dialect now emerging).
- [CUTLASS / CuTe DSL](https://github.com/NVIDIA/cutlass) — NVIDIA C++ templates with a new Python DSL.
- [HIP / ROCm](https://rocm.docs.amd.com/) — AMD's CUDA equivalent.

### Emerging

- [ThunderKittens](https://github.com/HazyResearch/ThunderKittens) — HazyResearch's tile-based CUDA DSL ([arXiv:2410.20399](https://arxiv.org/abs/2410.20399)).
- [TileLang](https://github.com/tile-ai/tilelang) — MS × PKU's cross-hardware tile language ([arXiv:2504.17577](https://arxiv.org/abs/2504.17577)).
- [Pallas](https://docs.jax.dev/en/latest/pallas/index.html) — Google's JAX kernel language for TPU/GPU.
- [cuTile Python](https://docs.nvidia.com/cuda/cutile-python/) — NVIDIA's Python tile DSL (+ cuTile.jl for Julia).
- [Ascend C](https://www.hiascend.com/document/) — Huawei's NPU language with host + device dual artifacts.
- [NKI](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/general/nki/index.html) — AWS Neuron Kernel Interface for Trainium.
- [MUSA](https://developer.mthreads.com/) — Moore Threads' CUDA-like stack for domestic GPUs.
- [TT-Lang](https://github.com/tenstorrent/tt-lang) — Tenstorrent's Python-embedded DSL.
- [tt-metal](https://github.com/tenstorrent/tt-metal) — Tenstorrent bare-metal programming.
- [Intel XPU Triton](https://github.com/intel/intel-xpu-backend-for-triton) — Intel's Triton backend.

---

## Infrastructure & Tools

### Agent harnesses

- [Humanize](https://github.com/PolyArch/humanize) — PolyArch — Claude Code plugin implementing RLCR (Ralph-Loop with Codex Review), used by KernelPilot.
- [KernelGYM](https://github.com/hkust-nlp/KernelGYM) — HKUST-NLP — distributed GPU environment for RL on kernel generation; multi-backend CUDA/Triton.
- [GPU Forecasters](https://github.com/codezakh/gpu-forecasters) — UNC Chapel Hill · 2026-05 — LLM surrogate that forecasts kernel runtime and defers uncertain cases to the GPU, letting search consider many more candidates per GPU-hour. [Paper](https://arxiv.org/abs/2605.31464)

### Compiler & autotuning

- [NVIDIA CompileIQ](https://developer.nvidia.com/cuda/compileiq) — NVIDIA · 2026-05 — evolutionary per-workload compiler auto-tuning in CUDA 13.3; up to 15% on already-optimized Triton attention / CUTLASS GEMM. [Blog](https://developer.nvidia.com/blog/extract-more-kernel-performance-with-nvidia-compileiq-auto-tuning/)

### Profiling & explainability

- [KEET](https://arxiv.org/abs/2605.04467) — 2026-05 — Kernel Execution Explanation Toolkit: turns Nsight Compute profiles into grounded natural-language bottleneck explanations that feed downstream optimization.
- [Nsight Compute](https://docs.nvidia.com/nsight-compute/) — NVIDIA's per-kernel profiler.
- [Proton](https://github.com/triton-lang/triton/tree/main/third_party/proton) — Triton's intra-kernel profiler.
- [rocprof](https://rocm.docs.amd.com/projects/rocprofiler/en/latest/) — AMD's profiler.
- [msprof](https://www.hiascend.com/document/) — Ascend NPU profiler.

### Kernel libraries (reference / baseline)

- [FlashAttention](https://github.com/Dao-AILab/flash-attention) — Dao-AILab — memory-efficient attention.
- [FlashInfer](https://github.com/flashinfer-ai/flashinfer) — LLM serving kernel library.
- [DeepGEMM](https://github.com/deepseek-ai/DeepGEMM) — DeepSeek's FP8 GEMM.
- [TileKernels](https://github.com/deepseek-ai/TileKernels) — DeepSeek · 2026-04 — production TileLang operator library (MoE routing, FP8/FP4 quant, first public Engram & Manifold HyperConnection kernels).
- [Liger-Kernel](https://github.com/linkedin/Liger-Kernel) — LinkedIn's training kernels.
- [FlagGems](https://github.com/FlagOpen/FlagGems) — BAAI's comprehensive Triton operator library.
- [AITER](https://github.com/ROCm/aiter) — AMD's AI operator library.

---

## Reading List

For newcomers, a suggested order:

1. **Survey** — [Yu et al. arXiv:2601.15727](https://arxiv.org/abs/2601.15727)
2. **Benchmark** — [KernelBench](https://arxiv.org/abs/2502.10517), then [why benchmarks get gamed](https://arxiv.org/abs/2509.14279)
3. **RL baseline** — [Kevin](https://arxiv.org/abs/2507.11948) → [CUDA-L1](https://arxiv.org/abs/2507.14111) → [CUDA Agent](https://arxiv.org/abs/2602.24286)
4. **Agent harness** — [CudaForge](https://arxiv.org/abs/2511.01884) → [PyTorch KernelAgent](https://pytorch.org/blog/kernelagent-hardware-guided-gpu-kernel-optimization-via-multi-agent-orchestration/)
5. **Evolutionary** — [AI CUDA Engineer postmortem](https://arxiv.org/abs/2509.14279) → [KernelEvolve](https://arxiv.org/abs/2512.23236) → [AVO](https://arxiv.org/abs/2603.24517)
6. **First-principles rewards** — [SOL-ExecBench](https://arxiv.org/abs/2603.19173) → [μCUTLASS + SOL](https://arxiv.org/abs/2603.29010)
7. **Verification-guided** — [ARGUS](https://arxiv.org/abs/2604.18616)
8. **Non-NVIDIA** — [GEAK (AMD)](https://arxiv.org/abs/2507.23194) → [AscendKernelGen](https://arxiv.org/abs/2601.07160) → [AccelOpt (Trainium)](https://arxiv.org/abs/2511.15915) → [MusaCoder (MUSA)](https://arxiv.org/abs/2606.04847)
9. **NeurIPS 2025 Tutorial** — [How to Build Agents to Generate Kernels for Faster LLMs](https://neurips.cc/virtual/2025/128792)

---

## Contributing

Contributions welcome! See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

**Quick rules:**
- One entry, two lines: `[Name](link) — Team · Date · [Route] · Status` then a one-line description with links.
- Sort newest-first within each section.
- List a multi-DSL system once, under its primary DSL, with a `· also:` tag.
- Verify every link before submitting.

---

## License

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Licensed under the Apache License, Version 2.0. See [LICENSE](./LICENSE) for details.

---

**Maintained by** [Lianzhong You](mailto:youyve@foxmail.com) · HKUST (GZ)
**Last updated** 2026-06-05
