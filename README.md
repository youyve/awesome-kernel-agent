# Awesome Kernel Agent [![Awesome](https://awesome.re/badge.svg)](https://awesome.re) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md) [![Last Commit](https://img.shields.io/github/last-commit/youyve/awesome-kernel-agent)](https://github.com/youyve/awesome-kernel-agent/commits/main)

> A high-density, evidence-driven research index of LLM systems that generate and optimize accelerator kernels.

[中文](README.zh.md) · [Benchmarks](BENCHMARKS.md) · [Data](data/agents.json) · [Contributing](CONTRIBUTING.md)

**112 agent systems** · **145 structured claims** · **45 claims with linked artifacts** · **17 hardware targets** · **3 tooling entries** · research cutoff **2026-08-25**

## Research Landscape

**Research Landscape question:** Which distinct questions define the catalog's Kernel Agent data model, and what semantic role does each question play?

[![Functional ontology of the Kernel Agent catalog; no timeline, ranking, or representative-system selection](assets/landscape.svg)](assets/landscape.svg)
_The Landscape is a containment-only ontology generated from [explicit facet definitions](reports/landscape.md); it encodes no chronology, causality, maturity, or system selection._

## Latest

[Ascend Debug Agent](catalog/2026.md#ascend-debug-agent) · [AsmEvo](catalog/2026.md#asmevo) · [CAKE](catalog/2026.md#cake) · [EvoMem](catalog/2026.md#evomem) · [ForgeStencil](catalog/2026.md#forgestencil)

## How to Read the Catalog

- **Profile:** a deterministic, presentation-only summary of evidenced taxonomy. The second line lists concrete representations; full facets remain in the yearly catalog. `—` means unannotated, not absent.
- **Baseline tiers:** T0 Reference/framework · T1 General compiler-generated · T2 Optimized generic/vendor library · T3 Specialized expert implementation · T4 Production incumbent · T5 Externally verified best-known implementation · T6 Hardware ceiling. Tiers classify provenance, specialization, and deployment status—not guaranteed runtime ordering. **10× @ T0 may be less meaningful than 1.1× @ T4.** `Unknown` is an unresolved implementation tier; `N/A` means this tier model does not apply.
- **Evidence:** `K` is availability of the displayed claim's exact winning artifact; `B` is disclosure of its optimization/search budget. ✓ yes · ◐ partial · — no/not applicable · ? unknown.

## Agent Catalog

Each row is generated from the v2 taxonomy and one explicitly selected primary claim. Full taxonomy, all claims, denominators, artifacts, budgets, caveats, and sources remain in the linked yearly catalog.

### 2026-08

| System | Profile | Headline claim | Evidence |
| --- | --- | --- | :---: |
| **[Ascend Debug Agent](catalog/2026.md#ascend-debug-agent)**<br><sub>City University of Hong Kong x Huawei · closed · [Paper](https://arxiv.org/abs/2608.02712)</sub> | Iterative refinement · Compiler feedback<br><sub>Ascend C</sub> | 66.7% pass@1 · Ascend NPU<br><sub>N/A · fresh CANNBot-style regeneration</sub> | K — · B ✓ |
| **[AsmEvo](catalog/2026.md#asmevo)**<br><sub>AMD x Southern University of Science and Technology · closed · [Paper](https://arxiv.org/abs/2608.20711)</sub> | Iterative refinement · Profiler<br><sub>AMDGPU ISA</sub> | 1.35× · AMD MI308X<br><sub>Unknown · original recovered AMDGPU code object</sub> | K — · B ✓ |
| **[CAKE](catalog/2026.md#cake)**<br><sub>NVIDIA x Carnegie Mellon University · partial · [Paper](https://arxiv.org/abs/2608.12629) · [Artifact: Upstream artifact tracker](https://github.com/flashinfer-ai/flashinfer/issues/4254)</sub> | Compiler in loop · IR feedback<br><sub>CAKE IR · CUDA · PTX</sub> | 1.144× · NVIDIA B200<br><sub>T3 · tuned FlashML</sub> | K ◐ · B ◐ |
| **[EvoMem](catalog/2026.md#evomem)**<br><sub>Anonymous organization (Moscow) x Applied AI Institute x Lomonosov Moscow State University · closed · [Paper](https://arxiv.org/abs/2608.10795)</sub> | Evolution · Runtime feedback<br><sub>Triton</sub> | — | — |
| **[ForgeStencil](catalog/2026.md#forgestencil)**<br><sub>OpenBMB · open · [Code](https://github.com/OpenBMB/ForgeStencil)</sub> | Multi-agent · Profiler<br><sub>CUDA</sub> | 1.41× · NVIDIA A100<br><sub>T4 · each application's production GPU path</sub> | K ✓ · B — |
| **[HIERA](catalog/2026.md#hiera)**<br><sub>Shanghai Jiao Tong University · closed · [Paper](https://arxiv.org/abs/2608.21157)</sub> | Iterative refinement · Profiler<br><sub>CUDA</sub> | 92.4% pass rate · NVIDIA A100<br><sub>N/A · PyTorch reference</sub> | K — · B ✓ |
| **[KernelArc](catalog/2026.md#kernelarc)**<br><sub>AI Labs x imec · closed · [Paper](https://arxiv.org/abs/2608.17071)</sub> | Portfolio search · Runtime feedback<br><sub>CUDA · PTX · Triton · +1</sub> | — | — |
| **[LEAP](catalog/2026.md#leap-kernel-rl)**<br><sub>Moore Threads AI · closed · [Paper](https://arxiv.org/abs/2608.01804)</sub> | Reinforcement learning · Compiler feedback<br><sub>CUDA</sub> | 80.8% pass rate · NVIDIA GPU<br><sub>N/A · first-turn pass rate of 70.0%</sub> | K — · B ✓ |
| **[LLM4LLM](catalog/2026.md#llm4llm)**<br><sub>Xidian University x Zhongguancun Academy · partial · [Paper](https://arxiv.org/abs/2608.21836) · [Code](https://github.com/hzeng2000/LLM4LLM)</sub> | Iterative refinement · Profiler<br><sub>Triton · CUDA · TileLang</sub> | 3.91× · NVIDIA A100<br><sub>T0 · PyTorch eager</sub> | K — · B ✓ |
| **[PTXBench / MiniPTXAgent](catalog/2026.md#ptxbench-miniptxagent)**<br><sub>Stanford x Carnegie Mellon University x RadixArk · open · [Paper](https://arxiv.org/abs/2608.17379) · [Code](https://github.com/zhang677/PTXBench)</sub> | IR feedback<br><sub>CUDA · PTX · Triton</sub> | — | — |
| **[SparseDitto](catalog/2026.md#sparse-ditto)**<br><sub>University of Minnesota x Northeastern University · closed · [Paper](https://arxiv.org/abs/2608.05033)</sub> | Correctness feedback<br><sub>CUDA</sub> | 2.68× · NVIDIA RTX PRO 6000<br><sub>T2 · fastest applicable cuSPARSE path</sub> | K — · B ✓ |
| **[Zomboss](catalog/2026.md#zomboss)**<br><sub>University of Michigan x University of Texas at Austin · closed · [Paper](https://arxiv.org/abs/2608.00894)</sub> | Best-of-N · Compiler feedback<br><sub>ACT · TAIDL</sub> | 3.34× · Gemmini FPGA<br><sub>T1 · compiler-default mapping</sub> | K — · B ✓ |

### 2026-07

| System | Profile | Headline claim | Evidence |
| --- | --- | --- | :---: |
| **[AgenticCANN](catalog/2026.md#agenticcann)**<br><sub>City University of Hong Kong x Hong Kong Yuwin Technology · closed · [Paper](https://arxiv.org/abs/2607.26661)</sub> | Evolution · Runtime feedback<br><sub>Ascend C</sub> | 6.65× · Ascend NPU<br><sub>T0 · PyTorch reference</sub> | K — · B ✓ |
| **[Compiler-Grounded Hierarchical Diagnosis](catalog/2026.md#compiler-grounded-hierarchical-diagnosis)**<br><sub>Huawei Technologies · open · [Paper](https://arxiv.org/abs/2607.23089) · [Code](https://gitcode.com/cann/cannbot-skills)</sub> | Iterative refinement · Compiler feedback<br><sub>Triton</sub> | 4.35× · Ascend 950<br><sub>Unknown · validated initial Triton kernel</sub> | K — · B ✓ |
| **[CUDAPerf](catalog/2026.md#cudaperf)**<br><sub>Iowa State University x Cisco AI Research · closed · [Paper](https://arxiv.org/abs/2607.20908)</sub> | Reinforcement learning · Correctness feedback<br><sub>CUDA</sub> | 6.41× · NVIDIA GPU<br><sub>T0 · PyTorch reference</sub> | K — · B ✓ |
| **[GEAK v4](catalog/2026.md#geak-v4)**<br><sub>AMD-AGI · open · [Code](https://github.com/AMD-AGI/GEAK) · [Article](https://www.amd.com/en/developer/resources/technical-articles/2026/geak-v4.html)</sub> | Multi-agent · Runtime feedback<br><sub>HIP · Triton · FlyDSL · +2</sub> | 2.21× · AMD GPU<br><sub>Unknown · original per-task kernel</sub> | K ◐ · B ✓ |
| **[Hawk](catalog/2026.md#hawk-npu)**<br><sub>Sun Yat-sen University x GBA National Technology Innovation Center x Peng Cheng Laboratory · closed · [Paper](https://arxiv.org/abs/2607.01590)</sub> | Distillation · Correctness feedback<br><sub>Ascend C</sub> | 1.34× · Ascend NPU<br><sub>T0 · PyTorch reference</sub> | K — · B ✓ |
| **[LLM-CUDA / Harness Engineering](catalog/2026.md#llm-cuda-harness-engineering)**<br><sub>Baidu · open · [Paper](https://arxiv.org/abs/2607.17979) · [Code](https://github.com/syhya/mlsys26-flashinfer-contest)</sub> | Iterative refinement · Correctness feedback<br><sub>CUDA · Triton · CUTLASS</sub> | 1.62× · NVIDIA B200<br><sub>T3 · supplied FlashInfer contest baseline</sub> | K ◐ · B ✓ |
| **[NKI-Agent / ATX Custom NKI Agent](catalog/2026.md#atx-custom-nki-agent)**<br><sub>Amazon Web Services · open · [Paper](https://arxiv.org/abs/2607.04395) · [Code](https://github.com/aws-samples/sample-ATX-custom-NKI-Agent)</sub> | SFT · Compiler feedback<br><sub>NKI</sub> | 77.3% pass rate · AWS Trainium<br><sub>N/A · single-shot Claude without agent tools (6% pass rate)</sub> | K ◐ · B ✓ |

### 2026-06

| System | Profile | Headline claim | Evidence |
| --- | --- | --- | :---: |
| **[AgentCompile](catalog/2026.md#agentcompile)**<br><sub>City University of Hong Kong (Dongguan) x City University of Hong Kong · partial · [Paper](https://arxiv.org/abs/2606.07665) · [Code](https://github.com/veneno1213822/AgentCompile)</sub> | Iterative refinement · Compiler feedback<br><sub>CUDA</sub> | 2.23–6.98× · NVIDIA GPU<br><sub>T0 · PyTorch eager</sub> | K — · B ◐ |
| **[Atrex Kernel Agent (AKA)](catalog/2026.md#atrex-kernel-agent)**<br><sub>ATREX Team, Alibaba Group · open · [Paper](https://arxiv.org/abs/2607.14541) · [Code](https://github.com/alibaba/atrex-kernel-agent)</sub> | Profiler<br><sub>FlyDSL · Triton · CUDA · +2</sub> | up to 1.31× · anonymized XPU-A<br><sub>T4 · deployed production kernel (AITER where applicable)</sub> | K — · B ◐ |
| **[AutoMegaKernel](catalog/2026.md#automegakernel)**<br><sub>RightNow AI (YC) · open · [Paper](https://arxiv.org/abs/2606.09682) · [Code](https://github.com/RightNow-AI/AutoMegaKernel)</sub> | Iterative refinement · Compiler feedback<br><sub>CUDA</sub> | 1.25–1.72× · NVIDIA GPU<br><sub>Unknown · pre-autoresearch AutoMegaKernel</sub> | K ◐ · B ◐ |
| **[daVinci-kernel](catalog/2026.md#davinci-kernel)**<br><sub>Shanghai Innovation Institute x Shanghai Jiao Tong University x GAIR · open · [Paper](https://arxiv.org/abs/2606.16497) · [Code](https://github.com/GAIR-NLP/daVinci-kernel)</sub> | SFT · Skill library<br><sub>CUDA · Triton</sub> | 37.2% pass rate · NVIDIA GPU<br><sub>T0 · PyTorch reference Fast_1 threshold</sub> | K — · B ✓ |
| **[EGG](catalog/2026.md#egg-kernel)**<br><sub>Beihang University x Shanghai Jiao Tong University x Tsinghua University x Approaching.AI · closed · [Paper](https://arxiv.org/abs/2606.26758)</sub> | Multi-agent · Profiler<br><sub>Triton</sub> | 2.13× · NVIDIA RTX 4090<br><sub>T0 · PyTorch eager</sub> | K — · B ✓ |
| **[Kernel Forge](catalog/2026.md#kernel-forge)**<br><sub>University of Michigan · open · [Paper](https://arxiv.org/abs/2607.24762) · [Code](https://github.com/TheJoshBrod/KernelForge)</sub> | MCTS · Correctness feedback<br><sub>CUDA · Triton</sub> | up to 2.83× · NVIDIA GB10<br><sub>T0 · PyTorch eager</sub> | K ✓ · B ✓ |
| **[KernelPro](catalog/2026.md#kernelpro)**<br><sub>Amazon Web Services x Siemens x University of Minnesota · closed · [Paper](https://arxiv.org/abs/2606.26453) · [Artifact: Appendix H kernel artifact](https://arxiv.org/abs/2606.26453)</sub> | MCTS · Profiler<br><sub>CUDA · CUTLASS · CuTe</sub> | 2.42× · NVIDIA GPU<br><sub>T0 · PyTorch eager</sub> | K ◐ · B ✓ |
| **[MoziFlux](catalog/2026.md#moziflux)**<br><sub>BiSheng-Compiler-Agents · open · [Code](https://github.com/BiSheng-Compiler-Agents/MoziFlux)</sub> | Iterative refinement · Simulator<br><sub>Triton</sub> | — | — |
| **[MusaCoder](catalog/2026.md#musacoder)**<br><sub>Moore Threads · partial · [Paper](https://arxiv.org/abs/2606.04847) · [Model](https://huggingface.co/MooreThreads/MusaCoder-27B)</sub> | Reinforcement learning<br><sub>MUSA C · CUDA</sub> | — | — |
| **[SpecGen](catalog/2026.md#specgen)**<br><sub>Fudan University x Shanghai Jiao Tong University x Shanghai AI Laboratory x HKUST x CUHK x SenseTime Research · closed · [Paper](https://arxiv.org/abs/2606.17518)</sub> | Parallel · Profiler<br><sub>CUDA · Triton</sub> | — | — |

### 2026-05

| System | Profile | Headline claim | Evidence |
| --- | --- | --- | :---: |
| **[AKO4X](catalog/2026.md#ako4x)**<br><sub>TLAIC · open · [Code](https://github.com/TongmingLAIC/AKO4X)</sub> | Iterative refinement · Correctness feedback<br><sub>Triton · CUDA · TileLang · +2</sub> | up to 30.71× · NVIDIA B200<br><sub>T3 · FlashInfer expert kernel</sub> | K ✓ · B ? |
| **[AlphaEvolve for FHE on TPUs](catalog/2026.md#alphaevolve-fhe)**<br><sub>Google · closed · [Paper](https://arxiv.org/abs/2605.14718)</sub> | Evolution<br><sub>JAX</sub> | 2.5× · TPU v5e<br><sub>T3 · human state-of-the-art implementation</sub> | K — · B ✓ |
| **[auto-gpu-kernel](catalog/2026.md#auto-gpu-kernel)**<br><sub>Dogacel · open · [Code](https://github.com/Dogacel/auto-gpu-kernel)</sub> | Iterative refinement · Correctness feedback<br><sub>Triton</sub> | 34.93× · NVIDIA B200<br><sub>T3 · contest reference kernel</sub> | K ✓ · B ◐ |
| **[CuBridge](catalog/2026.md#cubridge)**<br><sub>Shanghai Jiao Tong University · closed · [Paper](https://arxiv.org/abs/2605.05023)</sub> | Iterative refinement · Compiler feedback<br><sub>CUDA</sub> | — | — |
| **[cuda-opt-agent](catalog/2026.md#cuda-opt-agent)**<br><sub>KernelFlow-ops · open · [Code](https://github.com/KernelFlow-ops/cuda-opt-agent)</sub> | Iterative refinement · Compiler feedback<br><sub>CUDA</sub> | — | — |
| **[Houmao Agentic Kernel Optimization](catalog/2026.md#houmao-agentic-kernel-optimization)**<br><sub>Intellifusion · partial · [Paper](https://arxiv.org/abs/2608.14560) · [Code](https://github.com/igamenovoer/houmao) · [Artifact: Accepted CUDA kernels](https://github.com/CodeGandee/flashinfer-bench-starter-kit/tree/main/solution/cuda)</sub> | Multi-agent · Correctness feedback<br><sub>CUDA · CUTLASS</sub> | 1.71× · NVIDIA B200<br><sub>T3 · supplied FlashInfer contest baseline</sub> | K ✓ · B ✓ |
| **[KDA-Pilot](catalog/2026.md#kernelpilot)**<br><sub>BBuf · open · [Code](https://github.com/BBuf/KDA-Pilot)</sub> | Profiler<br><sub>Triton · CUDA · CUTLASS</sub> | 2.7499× · NVIDIA B200<br><sub>T4 · copied SGLang production baseline</sub> | K ✓ · B ◐ |
| **[Kernel Design Agents (KDA)](catalog/2026.md#kernel-design-agents)**<br><sub>MIT HAN Lab · wip · [Code](https://github.com/mit-han-lab/kernel-design-agents)</sub> | Iterative refinement · Correctness feedback<br><sub>CUDA</sub> | — | — |
| **[KernelBrain](catalog/2026.md#kernelbrain)**<br><sub>Microsoft · closed · [Paper](https://arxiv.org/abs/2608.02611)</sub> | Iterative refinement · Profiler<br><sub>Triton</sub> | — | — |
| **[MoE-Kernel-Agent](catalog/2026.md#moe-kernel-agent)**<br><sub>Jerry2423 · open · [Code](https://github.com/Jerry2423/MoE-Kernel-Agent)</sub> | Iterative refinement · Correctness feedback<br><sub>Triton</sub> | 25.7× · NVIDIA B200<br><sub>T0 · PyTorch reference implementation</sub> | K ✓ · B ◐ |
| **[Qwen3.7-Max Autonomous Kernel Optimization](catalog/2026.md#qwen3.7-max-kernel-opt)**<br><sub>Alibaba / Qwen Team · proprietary · [Article](https://qwen.ai/blog?id=qwen3.7)</sub> | Runtime feedback<br><sub>Triton</sub> | 10× · T-Head Zhenwu M890 PPU<br><sub>T4 · SGLang official Triton reference implementation</sub> | K — · B ✓ |

### 2026-04

| System | Profile | Headline claim | Evidence |
| --- | --- | --- | :---: |
| **[AdaExplore](catalog/2026.md#adaexplore)**<br><sub>CMU · open · [Paper](https://arxiv.org/abs/2604.16625) · [Code](https://github.com/StigLidu/AdaExplore)</sub> | —<br><sub>CUDA</sub> | — | — |
| **[ARGUS](catalog/2026.md#argus)**<br><sub>Mai, Kozyrakis, Yuan et al. · wip · [Paper](https://arxiv.org/abs/2604.18616)</sub> | In-context learning · Compiler feedback<br><sub>HIP</sub> | — | — |
| **[Cursor Multi-Agent Kernel Optimization](catalog/2026.md#cursor-nvidia-multi-agent-kernels)**<br><sub>Cursor / NVIDIA · open · [Article](https://cursor.com/blog/multi-agent-kernels) · [Artifact: Generated kernel results](https://github.com/anysphere/kernel-optimization-results)</sub> | Planner Worker · Correctness feedback<br><sub>CUDA · CUTLASS · CuTe · +1</sub> | +38% speedup · NVIDIA B200<br><sub>Unknown · PyTorch code already optimized by a single agent</sub> | K ✓ · B ◐ |
| **[CuTeGen](catalog/2026.md#cutegen)**<br><sub>U Toronto x Standard Kernel · open · [Paper](https://arxiv.org/abs/2604.01489) · [Code](https://github.com/taratt/cutegen)</sub> | Iterative refinement · Profiler<br><sub>CuTe</sub> | 1.71× · NVIDIA GPU<br><sub>T0 · PyTorch</sub> | K ? · B ? |
| **[FACT](catalog/2026.md#fact)**<br><sub>Heidari &amp; Nikolopoulos · closed · [Paper](https://arxiv.org/abs/2604.26666)</sub> | Autotuning<br><sub>CUTLASS</sub> | 2.03× · NVIDIA GPU<br><sub>T0 · PyTorch eager</sub> | K — · B ? |
| **[Neuron Agentic Development](catalog/2026.md#neuron-agentic-development)**<br><sub>AWS · open · [Code](https://github.com/aws-neuron/neuron-agentic-development) · [Article](https://aws.amazon.com/blogs/machine-learning/stop-hand-tuning-kernels-how-neuron-agentic-development-accelerates-aws-trainium-optimizations/)</sub> | Profiler<br><sub>NKI</sub> | — | — |
| **[TileGym](catalog/2026.md#tilegym)**<br><sub>NVIDIA · open · [Code](https://github.com/NVIDIA/TileGym) · [Article](https://developer.nvidia.com/blog/automating-gpu-kernel-translation-with-ai-agents-cutile-python-to-cutile-jl/)</sub> | Direct generation · Skill library<br><sub>cuTile</sub> | — | — |

### 2026-03

| System | Profile | Headline claim | Evidence |
| --- | --- | --- | :---: |
| **[AKO / AKO4ALL](catalog/2026.md#ako)**<br><sub>TLAIC · open · [Code](https://github.com/TongmingLAIC/AKO4ALL) · [Project](https://tongminglaic.github.io/AKO/)</sub> | —<br><sub>Triton · CUDA · TileLang</sub> | 10 wins · NVIDIA GPU<br><sub>N/A · SOL-ExecBench agent-optimized NVIDIA baseline</sub> | K ? · B ? |
| **[AscendOptimizer](catalog/2026.md#ascendoptimizer)**<br><sub>ECNU x Tongji · partial · [Paper](https://arxiv.org/abs/2603.23566)</sub> | Episodic memory<br><sub>Ascend C</sub> | 1.21× · Ascend NPU<br><sub>T3 · Ascend reference operator</sub> | K ? · B ? |
| **[AutoKernel](catalog/2026.md#autokernel)**<br><sub>RightNow AI (YC) · open · [Paper](https://arxiv.org/abs/2603.21331) · [Code](https://github.com/RightNow-AI/autokernel)</sub> | Iterative refinement · Compiler feedback<br><sub>CUDA · Triton</sub> | 5.29× · NVIDIA H100<br><sub>T0 · PyTorch eager</sub> | K ? · B ✓ |
| **[AVO](catalog/2026.md#avo)**<br><sub>NVIDIA x OctoML (23 authors) · partial · [Paper](https://arxiv.org/abs/2603.24517) · [Project: Community reimplementation (community)](https://github.com/austin1997/AVO)</sub> | Evolution · Correctness feedback<br><sub>CUDA · PTX</sub> | +10.5% speedup · NVIDIA B200<br><sub>T3 · FlashAttention-4</sub> | K — · B ✓ |
| **[CANNBot Skills](catalog/2026.md#cannbot-skills)**<br><sub>Huawei CANN · open · [Code](https://gitcode.com/cann/cannbot-skills)</sub> | Profiler<br><sub>Ascend C · Catlass · PyPTO · +2</sub> | — | — |
| **[CUCo](catalog/2026.md#cuco)**<br><sub>UT Austin · open · [Paper](https://arxiv.org/abs/2603.02376) · [Code](https://github.com/UT-InfraAI/cuco)</sub> | Evolution · Correctness feedback<br><sub>CUDA</sub> | up to 1.57× · NVIDIA GPU<br><sub>T0 · host-driven CPU-launched collectives/streams</sub> | K ◐ · B ✓ |
| **[CUDAMaster](catalog/2026.md#cudamaster)**<br><sub>Tsinghua · partial · [Paper](https://arxiv.org/abs/2603.07169) · [Project](https://hanyx2021.github.io/MSKernelBenchDemo/)</sub> | Multi-agent · Profiler<br><sub>CUDA</sub> | — | — |
| **[DRTriton](catalog/2026.md#drtriton)**<br><sub>Texas A&amp;M · wip · [Paper](https://arxiv.org/abs/2603.21465)</sub> | Reinforcement learning · Correctness feedback<br><sub>Triton</sub> | 92% win rate · NVIDIA GPU (model not specified in v1)<br><sub>T0 · PyTorch eager</sub> | K ? · B ◐ |
| **[EvoKernel](catalog/2026.md#evokernel)**<br><sub>SJTU · partial · [Paper](https://arxiv.org/abs/2603.10846) · [Project](https://evokernel.zhuo.li/)</sub> | SFT · Correctness feedback<br><sub>Ascend C</sub> | — | — |
| **[InCoder-32B](catalog/2026.md#incoder-32b)**<br><sub>Beihang University · open · [Paper](https://arxiv.org/abs/2604.03144) · [Code](https://github.com/CSJianYang/Industrial-Coder)</sub> | Direct generation · Correctness feedback<br><sub>CUDA</sub> | — | — |
| **[Kernel-Smith](catalog/2026.md#kernel-smith)**<br><sub>Shanghai AI Lab · closed · [Paper](https://arxiv.org/abs/2603.28342)</sub> | Evolution<br><sub>Triton</sub> | — | — |
| **[KernelFoundry](catalog/2026.md#kernelfoundry)**<br><sub>Intel · wip · [Paper](https://arxiv.org/abs/2603.12440)</sub> | MAP-Elites<br><sub>SYCL · CUDA</sub> | — | — |
| **[KernelSkill](catalog/2026.md#kernelskill)**<br><sub>Beihang University · open · [Paper](https://arxiv.org/abs/2603.10085) · [Code](https://github.com/0satan0/KernelMem)</sub> | Skill library<br><sub>CUDA</sub> | 5.44× · NVIDIA GPU<br><sub>T0 · PyTorch eager</sub> | K ? · B ? |
| **[muCUTLASS + Speed-of-Light Guidance](catalog/2026.md#mucutlass-sol)**<br><sub>NVIDIA x Stanford · wip · [Paper](https://arxiv.org/abs/2603.29010)</sub> | In-context learning · Roofline<br><sub>CUTLASS</sub> | — | — |
| **[PyTorch KernelAgent](catalog/2026.md#pytorch-kernelagent)**<br><sub>Meta / PyTorch · open · [Code](https://github.com/meta-pytorch/KernelAgent) · [Article](https://pytorch.org/blog/kernelagent-hardware-guided-gpu-kernel-optimization-via-multi-agent-orchestration/)</sub> | Role Specialized · Compiler feedback<br><sub>Triton</sub> | 89% of hardware ceiling · NVIDIA H100<br><sub>T6 · roofline</sub> | K ◐ · B ✓ |
| **[Standard Kernel](catalog/2026.md#standard-kernel)**<br><sub>Standard Kernel (startup) · closed · [Article](https://standardkernel.com/blog/announcing-our-seed-round-is-kernel-generation-solved/)</sub> | —<br><sub>PTX</sub> | — | — |
| **[StitchCUDA](catalog/2026.md#stitchcuda)**<br><sub>University of Minnesota Twin Cities · closed · [Paper](https://arxiv.org/abs/2603.02637)</sub> | Agentic RL · Correctness feedback<br><sub>CUDA</sub> | 1.72× · NVIDIA GPU<br><sub>Unknown · CudaForge</sub> | K ? · B ✓ |

### 2026-02

| System | Profile | Headline claim | Evidence |
| --- | --- | --- | :---: |
| **[Apex](catalog/2026.md#amd-apex)**<br><sub>AMD · open · [Code](https://github.com/AMD-AGI/Apex)</sub> | Iterative refinement · Compiler feedback<br><sub>HIP · Triton</sub> | up to 36.35× · AMD MI300X/MI355X<br><sub>Unknown · prior kernel in the same optimization run</sub> | K — · B ✓ |
| **[CUDA Agent](catalog/2026.md#cuda-agent)**<br><sub>ByteDance x Tsinghua · partial · [Paper](https://arxiv.org/abs/2602.24286) · [Code: Agent environment](https://github.com/BytedTsinghua-SIA/CUDA-Agent) · [Project](https://cuda-agent.github.io/) · [Project: Hugging Face paper page (third-party)](https://huggingface.co/papers/2602.24286) · [Dataset: CUDA-Agent-Ops-6K](https://huggingface.co/datasets/BytedTsinghua-SIA/CUDA-Agent-Ops-6K)</sub> | Agentic RL · Compiler feedback<br><sub>CUDA</sub> | 2.11× · NVIDIA GPU<br><sub>T1 · torch.compile</sub> | K ? · B ✓ |
| **[DICE](catalog/2026.md#dice)**<br><sub>Westlake University · open · [Paper](https://arxiv.org/abs/2602.11715) · [Code](https://github.com/deadlykitten4/DICE)</sub> | Reinforcement learning · Correctness feedback<br><sub>CUDA</sub> | 47% correctness · NVIDIA GPU<br><sub>N/A · no comparative denominator</sub> | K — · B ◐ |
| **[Dr. Kernel](catalog/2026.md#dr-kernel)**<br><sub>HKUST-NLP · open · [Paper](https://arxiv.org/abs/2602.05885) · [Code](https://github.com/hkust-nlp/KernelGYM)</sub> | Reinforcement learning<br><sub>Triton</sub> | — | — |
| **[K-Search](catalog/2026.md#k-search)**<br><sub>UC Berkeley · open · [Paper](https://arxiv.org/abs/2602.19128) · [Code](https://github.com/caoshiyi/K-Search)</sub> | Evolution<br><sub>CUDA</sub> | — | — |
| **[KernelBlaster](catalog/2026.md#kernelblaster)**<br><sub>NVIDIA x UC Berkeley · closed · [Paper](https://arxiv.org/abs/2602.14293)</sub> | In-context learning<br><sub>CUDA</sub> | — | — |
| **[OptiML](catalog/2026.md#optiml)**<br><sub>Iowa State University · closed · [Paper](https://arxiv.org/abs/2602.12305)</sub> | MCTS · Profiler<br><sub>CUDA</sub> | — | — |

### 2026-01

| System | Profile | Headline claim | Evidence |
| --- | --- | --- | :---: |
| **[AscendCraft](catalog/2026.md#ascendcraft)**<br><sub>NJU x Huawei · closed · [Paper](https://arxiv.org/abs/2601.22760)</sub> | Direct generation · Correctness feedback<br><sub>Ascend C</sub> | — | — |
| **[AscendKernelGen](catalog/2026.md#ascendkernelgen)**<br><sub>Pengcheng Lab · partial · [Paper](https://arxiv.org/abs/2601.07160) · [Dataset](https://huggingface.co/datasets/AscendKernelGen/Ascend-COT-v1)</sub> | Reinforcement learning<br><sub>Ascend C</sub> | — | — |
| **[CUDAnalyst](catalog/2026.md#cudanalyst)**<br><sub>Yee Hin Chong et al. · open · [Paper](https://openreview.net/forum?id=s70zO5Lvvj) · [Code](https://github.com/yuxuan-z19/cudanalyst)</sub> | Evolution · Profiler<br><sub>CUDA</sub> | — | — |
| **[GEAK-HIP](catalog/2026.md#geak-hip)**<br><sub>AMD-AGI · open · [Code](https://github.com/AMD-AGI/GEAK) · [Article](https://rocm.blogs.amd.com/software-tools-optimization/geak-hip-optimizations/README.html)</sub> | Iterative refinement<br><sub>HIP</sub> | — | — |
| **[GEAK-Triton v2](catalog/2026.md#geak-triton-v2)**<br><sub>AMD-AGI · open · [Code](https://github.com/AMD-AGI/GEAK) · [Article](https://rocm.blogs.amd.com/artificial-intelligence/geak-agents-family/README.html)</sub> | —<br><sub>Triton</sub> | — | — |
| **[TT-Lang + Claude Skills](catalog/2026.md#tt-lang-claude-skills)**<br><sub>Tenstorrent · open · [Code](https://github.com/tenstorrent/tt-lang)</sub> | Direct generation · Simulator<br><sub>TT-Lang</sub> | — | — |
| **[Xe-Forge](catalog/2026.md#xe-forge)**<br><sub>Intel Labs · open · [Code](https://github.com/IntelLabs/Xe-Forge)</sub> | —<br><sub>Triton</sub> | — | — |

### 2025-12

| System | Profile | Headline claim | Evidence |
| --- | --- | --- | :---: |
| **[AKG-AGENT](catalog/2025.md#akg-agent)**<br><sub>Huawei x Hunan U · open · [Paper](https://arxiv.org/abs/2512.23424) · [Code](https://github.com/mindspore-ai/akg/tree/master/akg_agents)</sub> | Role Specialized · Correctness feedback<br><sub>Triton · TileLang · Ascend C · +1</sub> | 1.46× · Ascend NPU<br><sub>T0 · PyTorch eager</sub> | K ? · B ✓ |
| **[CUDA-L2](catalog/2025.md#cuda-l2)**<br><sub>DeepReinforce · open · [Paper](https://arxiv.org/abs/2512.02551) · [Code](https://github.com/ornith-ai/CUDA-L2)</sub> | —<br><sub>CUDA</sub> | — | — |
| **[cuPilot](catalog/2025.md#cupilot)**<br><sub>Southeast U x Tsinghua x Tsing Micro · partial · [Paper](https://arxiv.org/abs/2512.16465) · [Artifact: Generated kernel outputs](https://github.com/champloo2878/cuPilot-Kernels)</sub> | Multi-agent<br><sub>CUDA</sub> | — | — |
| **[KernelEvolve](catalog/2025.md#kernelevolve)**<br><sub>Meta · proprietary · [Paper](https://arxiv.org/abs/2512.23236) · [Article](https://engineering.fb.com/2026/04/02/developer-tools/kernelevolve-how-metas-ranking-engineer-agent-optimizes-ai-infrastructure/)</sub> | Agentic RL · Retrieval memory<br><sub>CUDA · Triton · TileLang · +2</sub> | +60% throughput · NVIDIA GPU<br><sub>T4 · internal production kernel</sub> | K — · B ? |
| **[PEAK](catalog/2025.md#peak)**<br><sub>Stanford x MSR Redmond · closed · [Paper](https://arxiv.org/abs/2512.19018)</sub> | —<br><sub>CUDA · HIP</sub> | — | — |
| **[TritonForge](catalog/2025.md#tritonforge)**<br><sub>RLsys-Foundation · open · [Paper](https://arxiv.org/abs/2512.09196) · [Code](https://github.com/RLsys-Foundation/TritonForge)</sub> | SFT<br><sub>Triton</sub> | — | — |
| **[TritorX](catalog/2025.md#tritorx)**<br><sub>Meta · closed · [Paper](https://arxiv.org/abs/2512.10977)</sub> | Correctness feedback<br><sub>Triton</sub> | 481 ATen operators covered · MTIA<br><sub>N/A · no comparative performance baseline</sub> | K — · B ? |

### 2025-11

| System | Profile | Headline claim | Evidence |
| --- | --- | --- | :---: |
| **[AccelOpt](catalog/2025.md#accelopt)**<br><sub>Stanford x AWS · wip · [Paper](https://arxiv.org/abs/2511.15915) · [Code](https://github.com/zhang677/AccelOpt)</sub> | Iterative refinement · Runtime feedback<br><sub>NKI</sub> | 61% of hardware ceiling · AWS Trainium 1<br><sub>T6 · peak throughput</sub> | K ? · B ? |
| **[CudaForge](catalog/2025.md#cudaforge)**<br><sub>UMN OptimAI Lab · open · [Paper](https://arxiv.org/abs/2511.01884) · [Code](https://github.com/OptimAI-Lab/CudaForge)</sub> | Iterative refinement · Profiler<br><sub>CUDA</sub> | — | — |
| **[KernelBand](catalog/2025.md#kernelband)**<br><sub>PKU · closed · [Paper](https://arxiv.org/abs/2511.18868)</sub> | Hierarchical<br><sub>Triton</sub> | — | — |
| **[KernelFalcon](catalog/2025.md#kernelfalcon)**<br><sub>Meta / PyTorch · open · [Code](https://github.com/meta-pytorch/KernelAgent) · [Article](https://pytorch.org/blog/kernelfalcon-autonomous-gpu-kernel-generation-via-deep-agents/)</sub> | Correctness feedback<br><sub>Triton</sub> | 100% correctness · NVIDIA GPU<br><sub>N/A · no comparative performance baseline</sub> | K ? · B ? |
| **[KForge](catalog/2025.md#kforge)**<br><sub>Gimlet Labs · closed · [Paper](https://arxiv.org/abs/2606.02963)</sub> | Prompting · Compiler feedback<br><sub>Triton · CUDA · CUTLASS · +3</sub> | +2.12% throughput · NVIDIA B200<br><sub>Unknown · TensorRT-LLM 1.3.0rc9</sub> | K — · B ◐ |
| **[PRAGMA](catalog/2025.md#pragma)**<br><sub>Beihang University · closed · [Paper](https://arxiv.org/abs/2511.06345)</sub> | Multi-agent · Profiler<br><sub>Triton</sub> | — | — |
| **[QiMeng-Kernel](catalog/2025.md#qimeng-kernel)**<br><sub>CAS ICT · partial · [Paper](https://arxiv.org/abs/2511.20100) · [Code](https://github.com/QiMeng-IPRC/QiMeng-Kernel)</sub> | —<br><sub>CUDA</sub> | — | — |

### 2025-10

| System | Profile | Headline claim | Evidence |
| --- | --- | --- | :---: |
| **[ConCuR](catalog/2025.md#concur)**<br><sub>HKUST · open · [Paper](https://arxiv.org/abs/2510.07356) · [Model](https://huggingface.co/lkongam/KernelCoder)</sub> | SFT<br><sub>Triton</sub> | — | — |
| **[EvoEngineer](catalog/2025.md#evoengineer)**<br><sub>City University of Hong Kong · closed · [Paper](https://arxiv.org/abs/2510.03760)</sub> | Evolution · Runtime feedback<br><sub>CUDA</sub> | 2.72× · NVIDIA GPU<br><sub>T0 · PyTorch eager</sub> | K — · B ? |
| **[KernelGen (Flagos)](catalog/2025.md#kernelgen-flagos)**<br><sub>Flagos · open · [Code](https://github.com/flagos-ai/kernelgen) · [Project](https://kernelgen.flagos.io/)</sub> | —<br><sub>Triton</sub> | — | — |
| **[STARK](catalog/2025.md#stark)**<br><sub>Meta · closed · [Paper](https://arxiv.org/abs/2510.16996)</sub> | —<br><sub>CUDA</sub> | — | — |
| **[TritonRL](catalog/2025.md#tritonrl)**<br><sub>CMU x Amazon · closed · [Paper](https://arxiv.org/abs/2510.17891)</sub> | —<br><sub>Triton</sub> | — | — |

### 2025-09

| System | Profile | Headline claim | Evidence |
| --- | --- | --- | :---: |
| **[Astra](catalog/2025.md#astra)**<br><sub>Stanford · open · [Paper](https://arxiv.org/abs/2509.07506) · [Code](https://github.com/Anjiang-Wei/Astra)</sub> | Multi-agent · Retrieval memory<br><sub>CUDA</sub> | 1.32× · NVIDIA GPU<br><sub>T4 · SGLang incumbent kernels</sub> | K ? · B ✓ |

### 2025-08

| System | Profile | Headline claim | Evidence |
| --- | --- | --- | :---: |
| **[SwizzlePerf](catalog/2025.md#swizzleperf)**<br><sub>Harvard x AMD · closed · [Paper](https://arxiv.org/abs/2508.20258)</sub> | —<br><sub>Triton</sub> | — | — |

### 2025-07

| System | Profile | Headline claim | Evidence |
| --- | --- | --- | :---: |
| **[AutoTriton](catalog/2025.md#autotriton)**<br><sub>THUNLP / AI9Stars · open · [Paper](https://arxiv.org/abs/2507.05687) · [Code](https://github.com/AI9Stars/AutoTriton)</sub> | SFT<br><sub>Triton</sub> | — | — |
| **[CUDA-L1](catalog/2025.md#cuda-l1)**<br><sub>DeepReinforce · open · [Paper](https://arxiv.org/abs/2507.14111) · [Code](https://github.com/ornith-ai/CUDA-L1)</sub> | Reinforcement learning<br><sub>CUDA</sub> | 3.12× · NVIDIA A100<br><sub>T0 · PyTorch eager</sub> | K ◐ · B ? |
| **[GEAK](catalog/2025.md#geak)**<br><sub>AMD-AGI · open · [Paper](https://arxiv.org/abs/2507.23194) · [Code](https://github.com/AMD-AGI/GEAK)</sub> | Parallel · Runtime feedback<br><sub>Triton</sub> | 2.59× · AMD MI300X<br><sub>T3 · expert reference kernels</sub> | K ? · B ✓ |
| **[Kevin](catalog/2025.md#kevin)**<br><sub>Cognition · partial · [Paper](https://arxiv.org/abs/2507.11948)</sub> | Reinforcement learning · Correctness feedback<br><sub>CUDA</sub> | 1.1× · NVIDIA GPU<br><sub>T0 · PyTorch eager</sub> | K ? · B ✓ |
| **[QiMeng-Attention](catalog/2025.md#qimeng-attention)**<br><sub>CAS ICT · closed · [Paper](https://aclanthology.org/2025.findings-acl.446/)</sub> | —<br><sub>CUDA</sub> | 2.15× · NVIDIA A100<br><sub>T2 · cuDNN</sub> | K — · B ? |

### 2025-06

| System | Profile | Headline claim | Evidence |
| --- | --- | --- | :---: |
| **[CUDA-LLM](catalog/2025.md#cuda-llm)**<br><sub>Shanghai Jiao Tong University · closed · [Paper](https://arxiv.org/abs/2506.09092)</sub> | Prompting<br><sub>CUDA</sub> | — | — |
| **[GPU Kernel Scientist](catalog/2025.md#gpu-kernel-scientist)**<br><sub>Anonymous · closed · [Paper](https://arxiv.org/abs/2506.20807)</sub> | Iterative refinement<br><sub>CUDA</sub> | — | — |
| **[IntelliPerf](catalog/2025.md#intelliperf)**<br><sub>AMD Research · open · [Code](https://github.com/AMDResearch/intelliperf)</sub> | Profiler<br><sub>HIP · Triton</sub> | — | — |

### 2025-05

| System | Profile | Headline claim | Evidence |
| --- | --- | --- | :---: |
| **[KernelLLM](catalog/2025.md#kernelllm)**<br><sub>Meta · partial · [Model](https://huggingface.co/facebook/KernelLLM)</sub> | SFT<br><sub>Triton</sub> | — | — |
| **[QiMeng-TensorOp](catalog/2025.md#qimeng-tensorop)**<br><sub>CAS ICT · closed · [Paper](https://arxiv.org/abs/2505.06302)</sub> | MCTS<br><sub>CUDA</sub> | 124% of baseline throughput · NVIDIA GPU<br><sub>T2 · cuBLAS</sub> | K — · B ? |
| **[QiMeng-Xpiler](catalog/2025.md#qimeng-xpiler)**<br><sub>CAS ICT x USTC x Cambricon · wip · [Paper](https://arxiv.org/abs/2505.02146)</sub> | Autotuning · Compiler feedback<br><sub>CUDA · HIP</sub> | 95% accuracy · multiple accelerators<br><sub>N/A · no comparative denominator</sub> | K ? · B ? |

### 2025-02

| System | Profile | Headline claim | Evidence |
| --- | --- | --- | :---: |
| **[AI CUDA Engineer](catalog/2025.md#ai-cuda-engineer)**<br><sub>Sakana AI · partial · [Paper](https://arxiv.org/abs/2509.14279) · [Dataset](https://huggingface.co/datasets/SakanaAI/AI-CUDA-Engineer-Archive)</sub> | Correctness feedback<br><sub>CUDA</sub> | — | — |
| **[QiMeng-GEMM](catalog/2025.md#qimeng-gemm)**<br><sub>CAS ICT · partial · [Paper](https://ojs.aaai.org/index.php/AAAI/article/view/34461)</sub> | Prompting<br><sub>CUDA</sub> | 115% of baseline throughput · NVIDIA GPU<br><sub>T2 · cuBLAS</sub> | K ? · B ? |

## Field Map

**Question:** Along which major dimensions can Kernel Agent systems be understood and compared, and where does the catalog contain positive evidence?

[![Nine-dimension presentation projection of Kernel Agent evidence coverage](assets/field-map.svg)](assets/field-map.svg)
_This is a data-derived reading projection, not the detailed schema and not an exclusive Route. Its nine groups partition every facet family exactly once; generation mode/search strategy, signal/source, workload/integration scope, artifact level/focus, and representation remain distinct in the [complete reverse index and coverage audit](reports/field-map.md). Empty means unannotated—not absent._

## Baseline Distribution

Every numerical comparison keeps its own denominator. The chart separates T0–T6 implementation baselines, unresolved implementation tiers (`Unknown`), and comparisons where implementation tiers do not apply (`N/A`); see the [complete distribution table](reports/baseline-distribution.md).

![Distribution of claim baseline tiers T0 through T6, Unknown, and N/A](assets/baseline-distribution.svg)
_Baseline tier is claim-specific. A larger tier number does not assert a universally faster baseline._

## Timeline

[![Complete chronological Timeline containing every cataloged Kernel Agent system](assets/timeline.svg)](assets/timeline.svg)
_The SVG and [complete linked Timeline](reports/timeline.md) both contain all Agent systems; no milestone or representative-system selection is used._

## Benchmarks

The full benchmark catalog lives in [awesome-kernel-benchmark](https://github.com/youyve/awesome-kernel-benchmark), with 151 benchmark records, two evidence layers, and a methodology scorecard. The local [benchmark pointer](BENCHMARKS.md) preserves the integration boundary between systems and evaluation substrates.

### Evaluation integrity and reward hacking

- [robust-kbench](https://github.com/SakanaAI/robust-kbench) — hardened KernelBench after AI CUDA Engineer exploits; [paper](https://arxiv.org/abs/2509.14279)
- [METR Kernel Reward-Hacking Challenge](https://github.com/METR/RE-Bench/tree/main/ai_rd_triton_cumsum) — an evaluation task where reward hacking is explicitly audited
- [TRACE](https://arxiv.org/abs/2601.20103) — 54 exploit categories and 517 verified trajectories
- [RewardHackingAgents](https://arxiv.org/abs/2603.11337) — evaluator tampering as a first-class outcome
- [Standard Kernel Rubric](https://standardkernel.com/blog/standard-kernel-rubric/) — complexity, representation, hardware, performance, and automation rubric
- [Contract-Grade Verifier](https://arxiv.org/abs/2608.12700) — adversarial contract audit of 2,638 previously accepted generated kernels

### Competitions and leaderboards

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

**Reference and production kernel libraries:** [FlashAttention](https://github.com/Dao-AILab/flash-attention) · [FlashInfer](https://github.com/flashinfer-ai/flashinfer) · [DeepGEMM](https://github.com/deepseek-ai/DeepGEMM) · [TileKernels](https://github.com/deepseek-ai/TileKernels) · [Liger-Kernel](https://github.com/linkedin/Liger-Kernel) · [FlagGems](https://github.com/FlagOpen/FlagGems) · [AITER](https://github.com/ROCm/aiter).

## Research sources

- [Towards Automated Kernel Generation in the Era of LLMs](https://arxiv.org/abs/2601.15727) — broad survey and research index
- [awesome-LLM-driven-kernel-generation](https://github.com/flagos-ai/awesome-LLM-driven-kernel-generation) and [Awesome-LLM4Kernel](https://github.com/kcxain/Awesome-LLM4Kernel) — companion indexes
- [2026-08-25 primary-source audit](sources/research_20260825_kernel_agents.md) — search protocol, inclusion decisions, corrections, and exclusions for the latest refresh
- [v2 migration review](reports/migration-review.md) — facts intentionally left unresolved instead of inferred

## Contributing

Edit [`data/agents.yaml`](data/agents.yaml), validate it, and regenerate every derived artifact. Claims require one explicit denominator and primary source; `unknown` is always preferable to inference. See [CONTRIBUTING.md](CONTRIBUTING.md) for the v2 schema and review checklist.

## Citation

```bibtex
@misc{you2026awesomekernelagent,
  author       = {Lianzhong You},
  title        = {Awesome Kernel Agent: An Evidence-Driven Research Index of
                  LLM Systems for Accelerator Kernel Generation},
  year         = {2026},
  publisher    = {GitHub},
  url          = {https://github.com/youyve/awesome-kernel-agent}
}
```

## License

Catalog content: [CC-BY-4.0](LICENSE) · generator code: [MIT](scripts/LICENSE).

**Research cutoff:** 2026-08-25 · Maintained by [Lianzhong You](mailto:youyve@foxmail.com), HKUST (GZ)
