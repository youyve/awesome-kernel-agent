# Kernel-Agent Benchmark Inventory

> Companion to the main list's [Benchmarks](README.md#benchmarks) section.
> A kernel agent is evaluated in one of two ways, and the two are routinely confused:
>
> 1. **Purpose-built agent benchmarks** — harnesses *designed* to score LLM kernel generation (correctness + speedup vs a reference). KernelBench, TritonBench, CUDABench, SOL-ExecBench, … These are the headline numbers.
> 2. **Foundational / substrate suites** — pre-LLM HPC / GPU / DL benchmark suites that agents are evaluated *on*, fine-tuned *against*, or asked to *optimize / translate*. PolyBench, NPB, Rodinia, XSBench, HeCBench, DeepBench, … An agent paper that says "we optimize PolyBench-ACC / NPB / XSBench kernels" (e.g. [CUDAnalyst](https://github.com/yuxuan-z19/cudanalyst)) is using a Layer-2 substrate, not a Layer-1 benchmark.
>
> The original list only catalogued Layer 1. This document adds Layer 2 — the substrate suites — plus an **[agent ↔ substrate map](#agent--substrate-map)** showing which agents run on which classic suite. That map is the part that matters for future benchmark-centric work: it tells you, for any suite, which agents already touch it (so results are comparable) and which ship re-runnable solution kernels (so they are auditable).

**Layer-2 count:** ~70 distinct suites / ports across 6 families (deduplicated from a 106-entry raw survey). License and exact kernel counts vary by port; where a family has many ports (PolyBench, NPB, DeepBench) the canonical row links the rest.

## Contents

- [How the columns work](#how-the-columns-work)
- [Layer 1 — purpose-built agent benchmarks](#layer-1--purpose-built-agent-benchmarks)
- [Layer 2 — foundational / substrate suites](#layer-2--foundational--substrate-suites)
  - [Polyhedral & loop-nest suites (PolyBench lineage)](#polyhedral--loop-nest-suites-polybench-lineage)
  - [HPC proxy & mini-apps](#hpc-proxy--mini-apps)
  - [Classic GPU / heterogeneous suites](#classic-gpu--heterogeneous-suites)
  - [Graph-analytics suites](#graph-analytics-suites)
  - [DL operator micro-benchmarks & vendor baselines](#dl-operator-micro-benchmarks--vendor-baselines)
  - [Tensor-compiler & autotuning substrates](#tensor-compiler--autotuning-substrates)
- [Agent ↔ substrate map](#agent--substrate-map)
- [Lineage notes](#lineage-notes)
- [Contributing](#contributing)

---

## How the columns work

- **Verify** — does the suite ship a built-in correctness oracle (reference output, checksum, residual)? This is what makes a suite *anti-gaming*: a "fast but wrong" kernel fails the check rather than scoring a fake speedup.
- **Ships kernels** — does it ship re-runnable reference/solution kernels (✅), only a harness/driver around vendor libs or generated code (◐), or neither (—)? ✅ suites double as a human baseline *and* an audit target.
- **Used by (agents)** — LLM kernel-agent / GPU-code-LLM works that use the suite as an evaluation substrate. Empty = no agent use found yet (a coverage opportunity). Names link to the [agent ↔ substrate map](#agent--substrate-map).

---

## Layer 1 — purpose-built agent benchmarks

These are tabulated in the main list under [Benchmarks › Correctness & performance](README.md#purpose-built-agent-benchmarks). In scope, for cross-reference:

KernelBench (+ KernelBench-v3 / KernelBenchX / robust-kbench) · TritonBench · TritonGym · MultiKernelBench · GEAK Benchmarks · MSKernelBench · CUDABench · AgentKernelArena · NPUEval · NKIBench · NPUKernelBench · CANN Bench · FlashInfer-Bench · SOL-ExecBench · ISO-Bench · ComputeEval · BackendBench · KernelCraft · ParEval.

> **ParEval is a hinge case:** it was *built* as an agent benchmark ("Can LLMs Write Parallel Code?", HPDC'24) but is now also *reused as a substrate* by later agents (RLPF, HPC-Coder, OMPar). It appears in both layers.

---

## Layer 2 — foundational / substrate suites

### Polyhedral & loop-nest suites (PolyBench lineage)

The polyhedral suite kernel agents most often optimize. Affine loop nests with clean reference outputs ⇒ easy correctness checks and legal-transformation reasoning.

| Suite | Kernels | Languages | Verify | Ships kernels | Used by (agents) |
|:---|:---|:---|:---:|:---:|:---|
| [PolyBench/C 4.2.1](https://github.com/MatthiasJReisinger/PolyBenchC-4.2.1) | 30 | C | ✅ array dump | ✅ | [Performance-Aligned LLMs](#agent--substrate-map), [ComPilot](#agent--substrate-map), [ACCeLLiuM](#agent--substrate-map) |
| [PolyBench-ACC](https://github.com/cavazos-lab/PolyBench-ACC) | ~29 | CUDA · OpenCL · OpenACC · OpenMP · HMPP | ✅ host-vs-device | ✅ | **[CUDAnalyst](#agent--substrate-map)**, [MEP](#agent--substrate-map) |
| [PolyBench/GPU](https://github.com/sgrauerg/polybenchGpu) | 15 | CUDA · OpenCL · HMPP · OpenACC | ✅ CPU-vs-GPU | ✅ | [MIREncoder](#agent--substrate-map) |
| [PolyBench/Python](https://github.com/UDC-GAC/polybench-python) | 30 | Python · NumPy | ✅ vs PolyBench/C | ✅ | — |
| [PolyBench/Fortran](https://www.cs.colostate.edu/~pouchet/software/polybench/) | 30 | Fortran | ✅ | ✅ | — |
| [PolyBench-NN](https://github.com/IITH-Compilers/PolyBench-NN) | 8 (conv/pool/RNN/LSTM, fwd+bwd) | C (affine) | ✅ | ✅ | — |
| [PolyBench-RAJA](https://github.com/willkill07/PolyBench-RAJA) | 30 | C++ (RAJA → CUDA/OpenMP) | ✅ | ✅ | — |

*Upstream:* the canonical release is [L.-N. Pouchet's PolyBench/C](https://www.cs.colostate.edu/~pouchet/software/polybench/) (OSU/CSU); the [Meinersbur mirror](https://github.com/Meinersbur/polybench) is the copy bundled in the LLVM test-suite for Polly. Baselines are typically Pluto and LLVM `-O3`.

### HPC proxy & mini-apps

DOE/NASA mini-apps: small, science-representative, almost all ship a verification FOM. The substrate for HPC-translation and source-optimization agents.

| Suite | Domain / pattern | Languages | Verify | Ships kernels | Used by (agents) |
|:---|:---|:---|:---:|:---:|:---|
| [NPB](https://www.nas.nasa.gov/software/npb.html) (NAS Parallel Benchmarks) | 8 kernels/pseudo-apps (BT CG EP FT IS LU MG SP) +UA/DC/DT | Fortran · C → ports below | ✅ per-class checksum | ✅ | **[CUDAnalyst](#agent--substrate-map)**, [AutoParLLM](#agent--substrate-map) |
| [XSBench](https://github.com/ANL-CESAR/XSBench) | Monte-Carlo neutron cross-section lookup (memory-bound) | C · CUDA · OpenCL · SYCL · OpenMP-target | ✅ hash | ✅ | **[CUDAnalyst](#agent--substrate-map)**, [LLMPerf-Opt](#agent--substrate-map), [LASSI](#agent--substrate-map), [OMPar](#agent--substrate-map), [ParEval-Repo](#agent--substrate-map) |
| [RSBench](https://github.com/ANL-CESAR/RSBench) | MC multipole cross-section (compute-bound companion to XSBench) | C · CUDA · OpenCL · SYCL · OpenMP-target | ✅ | ✅ | [LLMPerf-Opt](#agent--substrate-map) |
| [miniFE](https://github.com/Mantevo/miniFE) | implicit FE assembly + CG solve (SpMV-bound) | C++ · CUDA · Kokkos · OpenMP | ✅ CG residual | ✅ | [LLMPerf-Opt](#agent--substrate-map) |
| [LULESH](https://github.com/LLNL/LULESH) | unstructured Lagrangian shock hydro | C++ · CUDA · RAJA · OpenMP | ✅ energy check | ✅ | — |
| [HPGMG](https://bitbucket.org/hpgmg/hpgmg) | geometric multigrid (FV/FE) | C · CUDA (hpgmg-cuda) | ✅ convergence | ✅ | — |
| [CoMD](https://github.com/ECP-copa/CoMD) | classical MD (LJ/EAM, cell lists) | C · CUDA · OpenCL · OpenMP | ✅ energy | ✅ | — |
| [miniMD](https://github.com/Mantevo/miniMD) | MD (neighbor lists, LAMMPS proxy) | C++ · Kokkos · OpenMP | ✅ thermo | ✅ | — |
| [Quicksilver](https://github.com/LLNL/Quicksilver) | MC particle transport (divergent) | C++ · CUDA · OpenMP | ✅ tallies | ✅ | — |
| [Nekbone](https://github.com/Nek5000/Nekbone) | spectral-element CFD (Ax mat-vec) | Fortran · CUDA-Fortran · OpenACC | ✅ CG residual | ✅ | — |
| [SU3_Bench](https://gitlab.com/NERSC/nersc-proxies/su3_bench) | lattice-QCD SU(3) mat-mul (bandwidth) | C · CUDA · HIP · SYCL · OpenMP | ✅ | ✅ | via [HeCBench](#agent--substrate-map) |
| [BabelStream](https://github.com/UoB-HPC/BabelStream) | sustained memory bandwidth | 15+ models (CUDA/HIP/SYCL/Kokkos/RAJA/…) | ✅ | ✅ | — |
| [PENNANT](https://github.com/lanl/PENNANT) | 2D unstructured Lagrangian hydro | C++ · CUDA · MPI | ✅ energy | ✅ | — |
| [miniAMR](https://github.com/Mantevo/miniAMR) | AMR octree + stencil | C · MPI · OpenMP | ✅ | ◐ (no in-repo CUDA) | — |
| [SimpleMOC](https://github.com/ANL-CESAR/SimpleMOC) | deterministic (MOC) neutron transport | C · CUDA · OpenCL · OpenMP-target | ✅ flux | ◐ | [ParEval-Repo](#agent--substrate-map) |

*NPB ports* (all retain per-class verification): [SNU-NPB](http://aces.snu.ac.kr/software/snu-npb/) (C/OpenMP-C) · [SNU-NPB 2019](http://opencl.snu.ac.kr/software/snu-npb-2019/) (OpenCL+CUDA, GPU-optimized) · [NPB-CPP](https://github.com/GMAP/NPB-CPP) (C++/OpenMP/TBB/FastFlow) · [NPB-GPU](https://github.com/GMAP/NPB-GPU) (CUDA+HIP, GMAP — the maintained GPU port) · [openacc-npb](https://github.com/uhhpctools/openacc-npb) (OpenACC, 7 apps) · [NPB-Rust](https://github.com/GMAP/NPB-Rust) · [LLNL/NPB](https://github.com/LLNL/NPB) (git mirror of the NASA source).

### Classic GPU / heterogeneous suites

The pre-DL GPU canon (Berkeley-dwarf coverage) plus the multi-language superset HeCBench, which subsumes many of the others.

| Suite | Apps | Languages | Verify | Ships kernels | Used by (agents) |
|:---|:---|:---|:---:|:---:|:---|
| [HeCBench](https://github.com/zjin-lcf/HeCBench) | **700+** programs (~350 distinct) | CUDA · HIP · SYCL · OpenMP-target | ✅ per-bench | ✅ | **[LASSI](#agent--substrate-map)**, [OMPar](#agent--substrate-map), [LLMPerf-Opt](#agent--substrate-map), [Bolet et al.](#agent--substrate-map) |
| [Rodinia](https://github.com/yuhc/gpu-rodinia) | ~23 (backprop, bfs, hotspot, srad, lud, nw, particlefilter, …) | C · CUDA · OpenCL · OpenMP | ✅ ref output | ✅ | [AutoParLLM](#agent--substrate-map), [MIREncoder](#agent--substrate-map) |
| [Parboil](https://github.com/yuhc/gpu-parboil) | 11 (sgemm, spmv, stencil, mri-q, lbm, …) | C · CUDA · OpenCL · OpenMP | ✅ ref output | ✅ | [MIREncoder](#agent--substrate-map) |
| [SHOC](https://github.com/vetter/shoc) | 20+ across 3 levels (+ stress tests) | CUDA · OpenCL · MPI | ✅ stress+verify | ✅ | [MIREncoder](#agent--substrate-map) |
| [Altis](https://github.com/utcs-scea/altis) | SHOC successor + DNN kernels | CUDA | ✅ | ✅ | — |
| [Mirovia](https://github.com/sarahgrace/mirovia) | SHOC/Rodinia + DNN (Altis predecessor) | CUDA | ✅ | ✅ | — |
| [Hetero-Mark](https://github.com/NUCAR-DEV/Hetero-Mark) | ~11 CPU-GPU collaborative | CUDA · HIP · HC · OpenCL | ✅ | ✅ | — |
| [Chai](https://github.com/chai-benchmarks/chai) | 14 (SVM + system-wide atomics) | CUDA · OpenCL | ✅ | ✅ | — |
| [OpenDwarfs](https://github.com/vtsynergy/OpenDwarfs) | 13 Berkeley dwarfs | OpenCL | ✅ | ✅ | — |
| [cuda-samples](https://github.com/NVIDIA/cuda-samples) | 180+ reference samples | CUDA | ◐ run_tests | ✅ | seed/idiom source |
| [GPGPU-Sim ISPASS-2009](https://github.com/gpgpu-sim/ispass2009-benchmarks) | 11 (AES, BFS, MUM, RAY, …) | CUDA | ✅ | ✅ | — |
| [Tango](https://www.mocalab.org/downloads) | 7 DNN (5 CNN + 2 RNN), library-free | CUDA · OpenCL | ✅ vs trained model | ✅ | — |
| [Tartan](https://github.com/uuudown/Tartan) | multi-GPU interconnect micro+apps | CUDA · MPI | — | ◐ | — |
| [Mars](https://cse.hkust.edu.hk/gpuqp/Mars.html) | 6 GPU-MapReduce apps | CUDA | ✅ | ◐ | — |

### Graph-analytics suites

Irregular / amorphous-data-parallel kernels — a distinct substrate from dense linear algebra, with strong optimized baselines.

| Suite | Kernels | Languages | Verify | Ships kernels | Notes |
|:---|:---|:---|:---:|:---:|:---|
| [GAP Benchmark Suite](https://github.com/sbeamer/gapbs) | 6 (BFS SSSP PR CC BC TC) | C++ · OpenMP (+ many GPU ports) | ✅ per-kernel verifier | ✅ | the standardized graph-kernel vocabulary |
| [LonestarGPU / Lonestar](https://github.com/IntelligentSoftwareSystems/GaloisGPU) | ~12 irregular (sssp, bfs, mst, dmr, …) | CUDA / C++ (Galois) | ✅ | ✅ | origin of the irregular-kernel task set |
| [Pannotia](https://github.com/pannotia/pannotia) | 6 (bc, color, fw, mis, prk, sssp) | OpenCL · HIP · CUDA | ✅ | ✅ | most-reported AMD/OpenCL graph suite |
| [Gunrock](https://github.com/gunrock/gunrock) | many primitives | CUDA · HIP | ✅ `--validate` vs Boost | ✅ | leading high-perf GPU graph library |
| [GraphBIG](https://github.com/graphbig/graphBIG) | broad CPU+GPU set | C++ · CUDA | ✅ shared core | ✅ | industry-derived; HW-counter profiling |
| [GARDENIA](https://github.com/chenxuhao/gardenia) | ~10 graph + sparse-LA + ML | CUDA · OpenCL · OpenMP | ✅ | ✅ | heavily-optimized baselines |
| [GBBS](https://github.com/ParAlg/gbbs) | 20+ (Ligra-based, provably-efficient) | C++ | ✅ | ✅ | largest CPU graph-kernel reference |
| [Indigo3](https://github.com/burtscher/Indigo3Suite) | 7 algos × 13 styles × 15 bug types = **41,790 labeled** | C · OpenMP · CUDA · HIP | ✅ bug-labeled | ✅ | race/deadlock-labeled — **anti-reward-hacking substrate** |

### DL operator micro-benchmarks & vendor baselines

The "reference kernel you must beat." For most agent papers the real baseline is `torch` → cuDNN/cuBLAS, even when unstated.

| Suite | Ops | Languages | Verify | Ships kernels | Used by (agents) |
|:---|:---|:---|:---:|:---:|:---|
| [cuDNN / cuBLAS](https://developer.nvidia.com/cudnn) | all DL ops (GEMM, conv, attn, norm, RNN) | CUDA (closed) | n/a | ✅ (vendor, closed) | the implicit bar for KernelBench, AI CUDA Engineer, TritonBench (via torch) |
| [DeepBench](https://github.com/baidu-research/DeepBench) (+ [ROCm fork](https://github.com/ROCm/DeepBench)) | GEMM · conv · RNN · all-reduce | CUDA · HIP · ARM | ◐ timing | ◐ vendor-backed | — |
| [Triton tutorial kernels](https://github.com/triton-lang/triton/tree/main/python/tutorials) | 10 (matmul, fused-softmax, flash-attn, layernorm, …) | Triton | ✅ vs torch | ✅ | [TritonBench](README.md#purpose-built-agent-benchmarks), GEAK, KernelLLM, AutoTriton |
| [Liger-Kernel](https://github.com/linkedin/Liger-Kernel/tree/main/benchmark) | 20+ LLM-training kernels (RMSNorm, RoPE, SwiGLU, FLCE, …) | Triton | ✅ vs HF | ✅ | [TritonBench](README.md#purpose-built-agent-benchmarks) (production-Triton source) |
| [FlashAttention bench](https://github.com/Dao-AILab/flash-attention) | attention fwd/bwd sweeps (FA1–FA4) | CUDA · CuTeDSL | ✅ vs torch | ✅ | attention-task reference baseline |
| [xFormers bench](https://github.com/facebookresearch/xformers) | memory-efficient attention + blocks | CUDA · CUTLASS · Triton | ✅ | ✅ | — |
| [operator_benchmark](https://github.com/pytorch/pytorch/tree/main/benchmarks/operator_benchmark) / [TorchBench](https://github.com/pytorch/benchmark) | 100s of ATen ops / ~100 models | Python · CUDA | ◐ | ◐ ATen-backed | — |
| [DNNMark](https://github.com/doody1986/DNNMark) | per-layer (conv, pool, BN, softmax, FC, RNN) | CUDA · HIP | ◐ | ◐ vendor-backed | — |
| [nvbench](https://github.com/NVIDIA/nvbench) | timing harness (axis sweeps) | CUDA · C++17 | — | — (harness) | substrate for other op suites vs cuBLAS/CUTLASS |
| [Fathom](https://github.com/rdadolf/fathom) | 8 archetypal DL workloads | Python (TF) | — | — (model-level) | — |
| [MLPerf](https://github.com/mlcommons/training) | ~8–10 training + inference models | Python (PyTorch/TF) | ✅ closed-division | — (model-level) | end-to-end target, not op-level |

### Tensor-compiler & autotuning substrates

Search/learned-cost-model substrates — the "ML-for-systems" data and the autoscheduled baselines kernel agents are compared against.

| Substrate | What it provides | Languages | Ships kernels | Notes |
|:---|:---|:---|:---:|:---|
| [TenSet](https://github.com/tlc-pack/tenset) | 52M measured tensor-program records, 6 platforms | TVM schedules (JSON) | ◐ records | canonical learned-cost-model training/eval set |
| [TVM/Ansor](https://github.com/apache/tvm) (AutoTVM + auto-scheduler) | op/subgraph tuning tasks + tuned schedules | TVM TE/TIR → CUDA/LLVM/OpenCL | ✅ | the standard search-based compiler baseline |
| [Roller](https://github.com/microsoft/nnfusion/tree/osdi22_artifact/artifacts/roller) | construction-based op kernels | TVM TE → CUDA/ROCm (NNFusion) | ✅ | fast-compilation autotuning baseline |
| [Welder](https://github.com/nox-410/Welder) | tile-graph fused kernels + perf/acc tests | TVM + CUTLASS → CUDA | ✅ | operator-fusion baseline |
| [Hidet](https://github.com/hidet-org/hidet) | task-mapping op/model kernels + bench scripts | Python DSL → CUDA | ✅ | modern tensor-core reference |
| [AKG / AKG-AGENT](https://github.com/mindspore-ai/akg) | Ascend polyhedral op suite + LLM op-gen platform (AscendKernelBench) | DSL · polyhedral · Triton-Ascend | ✅ | Huawei Ascend-NPU substrate ([AKG kernel Agent](https://arxiv.org/abs/2512.23424)) |
| [CUTLASS Profiler](https://github.com/NVIDIA/cutlass) | GEMM/conv config sweeps + verification | CUDA · CuTe · Python DSL | ✅ | the high-perf GEMM autotuning baseline |
| [IREE benchmarks](https://github.com/iree-org/iree) | end-to-end model benchmarks + comparative suite | MLIR (Linalg) | ◐ codegen | MLIR-codegen baseline |
| [MLIR microkernels](https://github.com/llvm/llvm-project/tree/main/mlir) | linalg/affine codegen integration tests | MLIR | ◐ | infra beneath IREE / AKG-MLIR |

---

## Agent ↔ substrate map

The cross-reference: which kernel-agent / GPU-code-LLM works evaluate on a **classic** substrate (Layer 2) rather than (or in addition to) a purpose-built benchmark. This is the comparability table — two agents are only directly comparable if they share a substrate *and* a verification method.

| Agent / work | Year | Classic substrate(s) used | Ships re-runnable kernels? |
|:---|:---:|:---|:---:|
| **[CUDAnalyst](https://github.com/yuxuan-z19/cudanalyst)** (ICML'26) | 2026 | PolyBench-ACC · NPB (BT/CG/EP/FT/IS/LU/MG/SP) · XSBench | ✅ `sol.cu` per task |
| [AI CUDA Engineer](https://huggingface.co/datasets/SakanaAI/AI-CUDA-Engineer-Archive) (Sakana) | 2025 | KernelBench *(L1)* — canonical reward-hacking case | ✅ 17K–30K archive |
| [Performance-Aligned LLMs / RLPF](https://arxiv.org/abs/2404.18864) (Nichols et al.) | 2024 | PolyBench (30 kernels) · ParEval · CodeContests | ◐ 20 variants/kernel |
| [ParEval](https://github.com/parallelcodefoundry/ParEval) — "Can LLMs Write Parallel Code?" | 2024 | *(origin; reused as substrate downstream)* | ◐ drivers+tests |
| [HPC-Coder](https://github.com/parallelcodefoundry/HPC-Coder) / [HPC-Coder-V2](https://arxiv.org/abs/2412.15178) | 2023–25 | ParEval (7 execution models) · Rodinia *(comparative)* | — |
| [AutoParLLM](https://github.com/quazirafi/AutoParLLM) (NAACL'25) | 2023–25 | NPB · Rodinia (12 apps, 454 loops) | — |
| [LASSI](https://arxiv.org/abs/2407.01638) / LASSI-EE (ANL) | 2024 | HeCBench (CUDA↔OpenMP) | — (uses HeCBench refs) |
| [OMPar](https://github.com/Scientific-Computing-Lab/OMPar) | 2024 | HeCBench (770 loops / 175 benches) · ParEval | — |
| LLMPerf-Opt — "Do LLMs Understand Performance Optimization?" | 2025 | XSBench · RSBench · miniFE | ◐ |
| [Astra](https://github.com/Anjiang-Wei/Astra) (Stanford) | 2025 | SGLang **production** kernels (deliberately not KernelBench) | ✅ vs SGLang |
| MEP framework (arXiv:2512.22147) | 2025 | PolyBench · AMD APP SDK · supercomputing hotspots | ◐ minimal-exec programs |
| [Tutoring LLM into a Better CUDA Optimizer](https://github.com/matyas-brabec/2025-europar-llm) | 2025 | custom classic CUDA tasks (histogram, kNN) | ✅ replication pkg |
| [ACCeLLiuM](https://arxiv.org/abs/2509.20380) | 2025 | GitHub-mined OpenACC set · PolyBench/C *(follow-up)* | ◐ dataset |
| [OMPGPT / MonoCoder](https://arxiv.org/abs/2401.16445) | 2024 | HPCorpus (mined OpenMP) | — |
| [Integrating Perf Tools in Model Reasoning](https://arxiv.org/abs/2510.17158) (Nichols et al.) | 2025 | HeCBench | ◐ |
| Can LLMs Predict Parallel Code Performance (Bolet et al.) | 2025 | HeCBench | — |
| ComPilot / Agentic Auto-Scheduling (Merouani et al., arXiv:2511.00592) | 2025 | PolyBench | ◐ schedules |
| MIREncoder | 2024 | Rodinia · Parboil · SHOC · PolyBench-GPU | — |
| [AKG kernel Agent](https://arxiv.org/abs/2512.23424) (Huawei) | 2025 | AKG op suite / AscendKernelBench (~198 ops) | ✅ op KB |

**Reading the map for future work:**
- **PolyBench / NPB / XSBench / HeCBench are the four most-used classic substrates** — any new agent targeting HPC kernels should report on at least one for comparability.
- Agents marked ✅ ship re-runnable kernels and are therefore **auditable for reward-hacking** (cf. the audit angle in [Evaluation integrity](README.md#evaluation-integrity--reward-hacking)). CUDAnalyst, AI CUDA Engineer, Astra and the EuroPar tutoring work are the high-value audit targets.
- HeCBench's contamination risk (it ships *both*-language reference implementations) was flagged by ParEval-Repo for translation tasks — worth controlling for when an agent "translates" between two models HeCBench already provides.

---

## Lineage notes

- **Berkeley 13 Dwarfs / Motifs** ([TR EECS-2006-183](https://www2.eecs.berkeley.edu/Pubs/TechRpts/2006/EECS-2006-183.pdf)) is the taxonomy behind Rodinia / Parboil / OpenDwarfs / PolyBench app selection — a framework, not a runnable suite.
- **SHOC → Mirovia → Altis** is one modernization lineage (same UT-Austin/VMware authors); **SHOC → HeCBench** is the multi-language-superset lineage.
- **PolyBench/GPU → PolyBench-ACC** is the GPU-port lineage that produced the suite CUDAnalyst now uses.
- **Valar** (NUCAR, GPGPU'13) is the conceptual precursor to Hetero-Mark but has no maintained public repo, so it is not a re-testable substrate.

---

## Contributing

Add a substrate suite only if a kernel agent could plausibly be *evaluated on* or *fine-tuned against* it. For each entry, fill the **Verify** and **Ships kernels** columns (they determine auditability) and — most importantly — populate **Used by (agents)** with a citation, or leave it empty to mark a coverage gap. New agent↔substrate pairs go in the [map](#agent--substrate-map). See [CONTRIBUTING.md](CONTRIBUTING.md) for entry format.
