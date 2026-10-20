# v2 Migration Review

_Facts that could not be safely inferred during the v1 → v2 migration. `unknown` is intentional until primary evidence resolves an item._

**80 review items** across **70 entries**.

| System | Field | Review item |
| --- | --- | --- |
| [AReaL-RSI](../catalog/2026.md#areal-rsi) | `taxonomy.optimization_level` | The paper establishes GPU kernel optimization but does not identify a concrete editable artifact level or representation. Hardware is also unannotated. |
| [AReaL-RSI](../catalog/2026.md#areal-rsi) | `claims` | Table 1 reports 2.30x/8.59x mean speedup and relative gains over Codex-Goal, but the implementation reference is unspecified. Do not reinterpret these as speedup directly against Codex-Goal kernels. |
| [ServingStudio](../catalog/2026.md#servingstudio) | `representations` | Introduction and linked tuning change establish source-level optimization but do not identify a generated-kernel representation; left unannotated. |
| [KernelOPT](../catalog/2026.md#kernelopt) | `artifacts.implementation` | Author-linked KernelOPT repository was not retrievable at the audit cutoff; public availability and exact winning artifacts require rechecking. |
| [PTXBench / MiniPTXAgent](../catalog/2026.md#ptxbench-miniptxagent) | `claims` | No numerical headline claim could be safely structured from the v1 row; verify the primary evidence before adding one. |
| [PTXBench / MiniPTXAgent](../catalog/2026.md#ptxbench-miniptxagent) | `artifacts.model_weights` | The official SFT dataset and model cards expose previews/file metadata but describe the repositories as private; full download access and complete historical trajectories remain unverified as of 2026-10-19. |
| [KernelArc](../catalog/2026.md#kernelarc) | `claims` | The five-task leaderboard snapshot, 1.06x–143.78x task range, and separate cuBLAS case require claim-by-claim table extraction and dated T5 review. |
| [EvoMem](../catalog/2026.md#evomem) | `claims` | The 2.4941x→2.7049x combined-speedup wording does not expose a safe per-result denominator or aggregation. |
| [AsmEvo](../catalog/2026.md#asmevo) | `claims.asmevo-claim-3.baseline.tier` | The original recovered AMDGPU code object is a real implementation denominator, but it does not map safely to T0-T6; tier remains Unknown. |
| [AsmEvo](../catalog/2026.md#asmevo) | `claims.asmevo-claim-2.baseline.tier` | The original recovered AMDGPU code object is a real implementation denominator, but it does not map safely to T0-T6; tier remains Unknown. |
| [GEAK v4](../catalog/2026.md#geak-v4) | `claims.geak-v4-claim-5.baseline.tier` | The original or pre-optimization implementation is a real denominator, but it does not map safely to T0-T6; tier remains Unknown. |
| [GEAK v4](../catalog/2026.md#geak-v4) | `claims.geak-v4-claim-4.baseline.tier` | The original or pre-optimization implementation is a real denominator, but it does not map safely to T0-T6; tier remains Unknown. |
| [GEAK v4](../catalog/2026.md#geak-v4) | `claims.geak-v4-claim-3.baseline.tier` | The original or pre-optimization implementation is a real denominator, but it does not map safely to T0-T6; tier remains Unknown. |
| [GEAK v4](../catalog/2026.md#geak-v4) | `claims.geak-v4-claim-2.baseline.tier` | The original or pre-optimization implementation is a real denominator, but it does not map safely to T0-T6; tier remains Unknown. |
| [GEAK v4](../catalog/2026.md#geak-v4) | `claims.geak-v4-claim-1.baseline.tier` | The original or pre-optimization implementation is a real denominator, but it does not map safely to T0-T6; tier remains Unknown. |
| [Compiler-Grounded Hierarchical Diagnosis](../catalog/2026.md#compiler-grounded-hierarchical-diagnosis) | `claims.compiler-grounded-hierarchical-diagnosis-claim-1.baseline.tier` | The validated initial Triton kernel is a real implementation denominator, but its T0-T6 provenance is unresolved; tier remains Unknown. |
| [SpecGen](../catalog/2026.md#specgen) | `claims` | Reported ranges pool multiple agent baselines and search settings; v1 does not map each number to one denominator. |
| [MusaCoder](../catalog/2026.md#musacoder) | `claims` | No numerical headline claim could be safely structured from the v1 row; verify the primary evidence before adding one. |
| [MoziFlux](../catalog/2026.md#moziflux) | `claims` | No numerical headline claim could be safely structured from the v1 row; verify the primary evidence before adding one. |
| [AutoMegaKernel](../catalog/2026.md#automegakernel) | `claims.automegakernel-claim-1.baseline.tier` | The pre-autoresearch implementation is a real implementation denominator, but it does not map safely to T0-T6; tier remains Unknown. |
| [AgentCompile](../catalog/2026.md#agentcompile) | `claims.agentcompile-claim-2.baseline.tier` | vLLM is an implementation denominator, but the primary evidence available during migration did not establish whether this instance was a deployed production incumbent; tier remains Unknown. |
| [Qwen3.7-Max Autonomous Kernel Optimization](../catalog/2026.md#qwen3.7-max-kernel-opt) | `representations` | v1 used PPU as a DSL; PPU is hardware, so only the explicitly listed Triton representation was retained. |
| [KernelBrain](../catalog/2026.md#kernelbrain) | `claims` | The 17%–48% wall-time range mixes PyTorch, supplied generated bases, and PyTorch KernelAgent across tasks. |
| [Kernel Design Agents (KDA)](../catalog/2026.md#kernel-design-agents) | `claims` | Contest ranks are given only as #1–#3 across unspecified tracks; no safe dated T5 claim can be constructed. |
| [cuda-opt-agent](../catalog/2026.md#cuda-opt-agent) | `claims` | No numerical headline claim could be safely structured from the v1 row; verify the primary evidence before adding one. |
| [CuBridge](../catalog/2026.md#cubridge) | `claims` | No numerical headline claim could be safely structured from the v1 row; verify the primary evidence before adding one. |
| [auto-gpu-kernel](../catalog/2026.md#auto-gpu-kernel) | `representations` | v1 used the compound label Triton-FlashInfer; migrated to Triton because FlashInfer is a library/benchmark context, not a representation. |
| [AlphaEvolve for FHE on TPUs](../catalog/2026.md#alphaevolve-fhe) | `representations` | v1 conflated JAX with the TPU backend as JAX-TPU; migrated to JAX only. |
| [TileGym](../catalog/2026.md#tilegym) | `claims` | No numerical headline claim could be safely structured from the v1 row; verify the primary evidence before adding one. |
| [Neuron Agentic Development](../catalog/2026.md#neuron-agentic-development) | `claims` | No numerical headline claim could be safely structured from the v1 row; verify the primary evidence before adding one. |
| [Cursor Multi-Agent Kernel Optimization](../catalog/2026.md#cursor-nvidia-multi-agent-kernels) | `claims.cursor-nvidia-multi-agent-kernels-claim-1.baseline.tier` | The single-agent-optimized kernel is a real implementation denominator, but it does not map safely to T0-T6; tier remains Unknown. |
| [ARGUS](../catalog/2026.md#argus) | `claims` | The 99%–104% assembly comparison and 2x–1543x prior-agent range require separate source-table extraction. |
| [AdaExplore](../catalog/2026.md#adaexplore) | `claims` | No numerical headline claim could be safely structured from the v1 row; verify the primary evidence before adding one. |
| [StitchCUDA](../catalog/2026.md#stitchcuda) | `claims.stitchcuda-claim-3.baseline.tier` | Kevin-32B output is a real generated implementation denominator, but its T0-T6 provenance is unresolved; tier remains Unknown. |
| [StitchCUDA](../catalog/2026.md#stitchcuda) | `claims.stitchcuda-claim-2.baseline.tier` | CudaForge output is a real generated implementation denominator, but its T0-T6 provenance is unresolved; tier remains Unknown. |
| [Standard Kernel](../catalog/2026.md#standard-kernel) | `claims` | The proprietary 80%–4x end-to-end range has no public workload-to-value mapping. |
| [muCUTLASS + Speed-of-Light Guidance](../catalog/2026.md#mucutlass-sol) | `claims` | The 0.40x→1.27x and +SOL up-to 2.07x wording mixes ablation and ceiling-relative semantics. |
| [KernelFoundry](../catalog/2026.md#kernelfoundry) | `claims` | No numerical headline claim could be safely structured from the v1 row; verify the primary evidence before adding one. |
| [Kernel-Smith](../catalog/2026.md#kernel-smith) | `claims` | No numerical headline claim could be safely structured from the v1 row; verify the primary evidence before adding one. |
| [InCoder-32B](../catalog/2026.md#incoder-32b) | `claims` | The 38.0% KernelBench value is present but its exact metric/threshold is not identified in v1. |
| [ROCm Hyperloom](../catalog/2026.md#hyperloom) | `claims.hyperloom-llama-mi355x.baseline.tier` | The initial stock vLLM implementation is specified, but no evidence establishes its specialization/deployment status within T0-T6; retain Unknown. |
| [ROCm Hyperloom](../catalog/2026.md#hyperloom) | `claims.hyperloom-fleet-median.baseline.tier` | Stock full-stack serving configurations are real implementation denominators, but the article does not establish one T0-T6 provenance/status classification for this heterogeneous set. |
| [EvoKernel](../catalog/2026.md#evokernel) | `claims` | The 11%→83% correctness and 3.60x median lack a verified benchmark, denominator, and exact hardware in v1. |
| [CUDAMaster](../catalog/2026.md#cudamaster) | `claims` | The approximate 35% result lacks an explicit aggregation and the cuBLAS comparison is qualitative. |
| [CANNBot Skills](../catalog/2026.md#cannbot-skills) | `claims` | No numerical headline claim could be safely structured from the v1 row; verify the primary evidence before adding one. |
| [AscendOpGenAgent](../catalog/2026.md#ascendopgenagent) | `claims` | April 30 benchmark report has inconsistent latency/speedup rows (e.g. Ascend C GELU 0.086/0.186 ms versus reported 0.13x); search budget and exact result-to-artifact correspondence require clarification. |
| [OptiML](../catalog/2026.md#optiml) | `claims` | The up-to 1.64x value does not identify which listed LLM-only baseline is the denominator. |
| [KernelBlaster](../catalog/2026.md#kernelblaster) | `claims` | No numerical headline claim could be safely structured from the v1 row; verify the primary evidence before adding one. |
| [K-Search](../catalog/2026.md#k-search) | `claims` | No numerical headline claim could be safely structured from the v1 row; verify the primary evidence before adding one. |
| [Dr. Kernel](../catalog/2026.md#dr-kernel) | `claims` | No numerical headline claim could be safely structured from the v1 row; verify the primary evidence before adding one. |
| [Apex](../catalog/2026.md#amd-apex) | `claims.amd-apex-claim-1.baseline.tier` | The prior kernel from the same optimization run is a real implementation denominator, but it does not map safely to T0-T6; tier remains Unknown. |
| [Xe-Forge](../catalog/2026.md#xe-forge) | `claims` | No numerical headline claim could be safely structured from the v1 row; verify the primary evidence before adding one. |
| [TT-Lang + Claude Skills](../catalog/2026.md#tt-lang-claude-skills) | `claims` | No numerical headline claim could be safely structured from the v1 row; verify the primary evidence before adding one. |
| [MaxCode](../catalog/2026.md#maxcode) | `hardware` | The inspected paper does not specify a GPU model or vendor for the KernelBench results; no hardware was inferred from CUDA. |
| [MaxCode](../catalog/2026.md#maxcode) | `artifacts.implementation` | No author code repository was verified at the 2026-10-19 cutoff; generic Google accelerator-agents MaxCode refers to another system. |
| [GEAK-Triton v2](../catalog/2026.md#geak-triton-v2) | `claims` | No numerical headline claim could be safely structured from the v1 row; verify the primary evidence before adding one. |
| [GEAK-HIP](../catalog/2026.md#geak-hip) | `claims` | No numerical headline claim could be safely structured from the v1 row; verify the primary evidence before adding one. |
| [CUDAnalyst](../catalog/2026.md#cudanalyst) | `claims` | No numerical headline claim could be safely structured from the v1 row; verify the primary evidence before adding one. |
| [AscendKernelGen](../catalog/2026.md#ascendkernelgen) | `claims` | The 0%→95.5% compilation result lacks an explicit before/after model baseline in v1. |
| [AscendCraft](../catalog/2026.md#ascendcraft) | `claims` | Compilation/correctness percentages lack an evaluated-on workload in v1. |
| [TritonForge](../catalog/2025.md#tritonforge) | `claims` | No numerical headline claim could be safely structured from the v1 row; verify the primary evidence before adding one. |
| [PEAK](../catalog/2025.md#peak) | `claims` | No numerical headline claim could be safely structured from the v1 row; verify the primary evidence before adding one. |
| [cuPilot](../catalog/2025.md#cupilot) | `claims` | No numerical headline claim could be safely structured from the v1 row; verify the primary evidence before adding one. |
| [CUDA-L2](../catalog/2025.md#cuda-l2) | `claims` | No numerical headline claim could be safely structured from the v1 row; verify the primary evidence before adding one. |
| [QiMeng-Kernel](../catalog/2025.md#qimeng-kernel) | `claims` | Approximate Level 1/2/3 percentages do not identify the exact metric or evaluation protocol in v1. |
| [PRAGMA](../catalog/2025.md#pragma) | `claims` | No numerical headline claim could be safely structured from the v1 row; verify the primary evidence before adding one. |
| [KForge](../catalog/2025.md#kforge) | `claims.kforge-claim-1.baseline.tier` | TensorRT-LLM 1.3.0rc9 is an implementation denominator, but deployment/incumbency status was not established; tier remains Unknown. |
| [KernelBand](../catalog/2025.md#kernelband) | `claims` | No numerical headline claim could be safely structured from the v1 row; verify the primary evidence before adding one. |
| [CudaForge](../catalog/2025.md#cudaforge) | `claims` | The paired 1.68x/2.27x values are not mapped to distinct denominators in v1. |
| [TritonRL](../catalog/2025.md#tritonrl) | `claims` | No numerical headline claim could be safely structured from the v1 row; verify the primary evidence before adding one. |
| [STARK](../catalog/2025.md#stark) | `claims` | No numerical headline claim could be safely structured from the v1 row; verify the primary evidence before adding one. |
| [KernelGen (Flagos)](../catalog/2025.md#kernelgen-flagos) | `claims` | No numerical headline claim could be safely structured from the v1 row; verify the primary evidence before adding one. |
| [ConCuR](../catalog/2025.md#concur) | `claims` | No numerical headline claim could be safely structured from the v1 row; verify the primary evidence before adding one. |
| [SwizzlePerf](../catalog/2025.md#swizzleperf) | `claims` | No numerical headline claim could be safely structured from the v1 row; verify the primary evidence before adding one. |
| [AutoTriton](../catalog/2025.md#autotriton) | `claims` | No numerical headline claim could be safely structured from the v1 row; verify the primary evidence before adding one. |
| [IntelliPerf](../catalog/2025.md#intelliperf) | `claims` | No numerical headline claim could be safely structured from the v1 row; verify the primary evidence before adding one. |
| [GPU Kernel Scientist](../catalog/2025.md#gpu-kernel-scientist) | `claims` | No numerical headline claim could be safely structured from the v1 row; verify the primary evidence before adding one. |
| [CUDA-LLM](../catalog/2025.md#cuda-llm) | `claims` | No numerical headline claim could be safely structured from the v1 row; verify the primary evidence before adding one. |
| [KernelLLM](../catalog/2025.md#kernelllm) | `claims` | No numerical headline claim could be safely structured from the v1 row; verify the primary evidence before adding one. |
| [AI CUDA Engineer](../catalog/2025.md#ai-cuda-engineer) | `claims` | No numerical headline claim could be safely structured from the v1 row; verify the primary evidence before adding one. |
