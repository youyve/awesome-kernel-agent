# Kernel-agent paper evidence audit — 2026-10-19

Scope: public material through 2026-10-19, prioritizing papers first public after
the catalog's 2026-08-25 cutoff. Existing IDs were checked before proposing
entries. This file records primary-source findings; search snippets and external
awesome lists were used only for discovery. Accepted records are integrated into
`data/agents.yaml`, the canonical catalog source.

The research-lookup workflow was used. Its optional parallel-cli backend was not
installed; built-in web search and direct primary-source retrieval supplied the
evidence instead. No paper's absence from a search is treated as proof that code
or artifacts do not exist.

## Search log

Queries included:

- `site:arxiv.org kernel agent September 2026 CUDA Triton`
- `site:arxiv.org kernel generation October 2026 reinforcement learning`
- `"kernel" "2026" "September" "agent" Triton`
- `site:arxiv.org/abs/2609 "kernel" "LLM"`
- `site:arxiv.org/abs/2610 "kernel" "agent"`
- `site:arxiv.org/abs/2609 "Triton"`
- `site:arxiv.org/abs/2610 "CUDA" "kernel"`
- `GPU kernel generation agent "October" "2026" arxiv`
- `GPU kernel generation agent "September" "2026" arxiv`
- `"kernel" "reinforcement learning" "September 2026"`
- `"Triton" "agent" "October 2026"`
- Exact-name searches for ForgeMegakernel, CUDA-Harness, Triton AI Compiler,
  FlashVector, AlphaCu, KernelMem, Model2Kernel, and KernelOwl.

Discovery indexes inspected:

- https://github.com/flagos-ai/awesome-LLM-driven-kernel-generation
- https://github.com/qhy991/Awesome-LLM-Kernel-Agent

Cross-lane discoveries: KernelOPT (arXiv:2609.30059) is researched by the main
agent; its author repository is TorchedHat/KernelOPT, not the unrelated giveen
repository. AMDKernelVault and MaxKernel go to the hardware lane. KernelQuest,
D2K-Bench (2610.03226), and KREX (2609.30057) belong in benchmark/infrastructure
sections rather than becoming additional generation-agent entries. KernelMem is
the implementation of the already cataloged KernelSkill, not a new system.
Model2Kernel (2603.24595) performs symbolic verification, not LLM kernel generation.
AlphaCu is assigned to the existing-work audit. Dream-RSI (2609.14858) and
AReaL-RSI (2610.18083) are assigned to the main agent. Stateless Language Agents
(2610.07625) is retained in this lane for follow-up.

## Include: CUDA-Harness

- First-public paper date: **2026-08-30**, from the arXiv submission history;
  the `2609` identifier must not be used to move it to September.
- Authors: Qi Fan, An Zou, Yehan Ma; Shanghai Jiao Tong University (paper header).
- Paper: https://arxiv.org/abs/2609.00058
- Full text: https://arxiv.org/html/2609.00058v1
- No author implementation/model/artifact link was located. Availability remains
  unknown; no community repository is relabeled as official code.
- Method evidence: Sections 4.1–4.3 describe a structured CUDA scaffold, separate
  test-synthesis context, compiler/correctness/profiling feedback, best-of-three
  iterative optimization, and retained optimization insights. Section 4.3.2
  explicitly says there are **no updatable parameters**. Its use of the name
  RLVR is not evidence of parameter-training RL; candidates use prompting,
  in-context learning, iterative refinement, best-of-N, and reflection memory.
- Claims: Table 1 overall functional correctness **80.5%**, compilation **99.7%**;
  CUDABench three prompt levels, NVIDIA A40, Seed2.0 Lite without thinking.
  These have an evaluation reference and **N/A** implementation tier, not T0.
  Section 5.1.1 gives three rounds and three candidates per round after initial
  generation. Each metric is an independent claim.
- Caveat: **110.7 RScore is not 110.7% or 1.107x**. Section 5.1.2 defines mean
  inverse milliseconds with failures scored zero. It is not added as a claim
  because the controlled units do not represent inverse milliseconds. Table 2
  reports 8.7% of cases passing synthesized checks but failing benchmark checks.
- Final source consistency check: Table 3 prints a GLM-5.1 functional rate of
  101.8, which is not a valid percentage, and Section 5.1 describes A40 as
  `sm_80`. Neither detail is propagated into structured claims. The retained
  Seed2.0 Lite figures are directly stated in Table 1.

## Include: ForgeMegakernel

- First-public paper date **2026-09-11**, arXiv history.
- Authors/organizations: Leshan Li, Zhui Zhu, Xianglong Deng, Yaojian Chen,
  Qingfeng He, Yuxuan Li, Rong Zhao, Xu Han, Zhiyuan Liu; Tsinghua University,
  University of Chinese Academy of Sciences, ModelBest (paper header).
- Paper: https://arxiv.org/abs/2609.12379
- Full text: https://arxiv.org/html/2609.12379v1
- Method: Section 4.3 explicitly separates coding and review agents, restarts
  agent contexts, and carries measured evidence in a ledger. Sections 4.1–4.2
  establish source-level CUDA generation, structural milestones, profiler and
  bandwidth-roofline checks, and an independent numerical oracle.
- Claims: abstract, Section 5.1–5.2 and Figure 3 report **1.21x geometric mean vs
  SGLang 0.5.18**, and separately **1.54x vs Mirage Persistent Kernel (MPK)**;
  the study evaluates fourteen selected decode model/configuration cells across
  eight model families, **but Section 5.2.1 excludes Llama-3.2-1B b1 x 96 from
  aggregate comparisons**. Hardware is NVIDIA H100 80GB HBM3, bf16 weights/KV.
  SGLang uses CUDA graphs and torch.compile;
  MPK uses its demo path. SGLang is treated as a tuned specialized implementation
  (**T3**), not assigned T4 merely because it is a production-capable product.
  MPK's compiler-produced implementation is **T1**.
- A separate **50.5%–85.9% model bandwidth utilization** range uses the explicit
  **3350 GB/s peak HBM bandwidth denominator (T6)**, Section 2.2 Equation 3.
- Budget: Section 6 Table 3 provides per-cell costs; median 47 rounds, 14.7
  agent-hours, approximately 178M tokens, USD177. These are measured campaign
  costs, not fixed caps.
- Limits: one GPU architecture; selected cells; independent tests are not formal
  correctness proofs. No official full-code or winning-kernel release was found.

## Include: FlashVector

- First-public paper date **2026-09-15**, arXiv history. The manuscript header
  says August, but that is not itself evidence of an August public release.
- Qi Wu et al.; Stanford University and Unity Vector AI Team (paper header).
- Paper: https://arxiv.org/abs/2609.17391
- Full text: https://arxiv.org/html/2609.17391v1
- Sections 4.1–4.3: layer-specific profile/diagnose/optimize/verify agents,
  retrieved cookbook/skills, post-run knowledge refinement and cross-run reuse.
  Hardware profiling and runtime/correctness/model checks are explicit. The
  word hierarchical describes the serving stack; no extra hierarchical-agent
  topology is inferred from the title.
- Section 5.2.1–5.2.2 / Figure 5: **3.56x** attention-module latency improvement
  (996.5 to 279.8 microseconds), FP16 multi-task recommendation model, batch 2000,
  NVIDIA RTX PRO 6000 Blackwell. Denominator is the actual incumbent production
  model's AOTInductor implementation (**T4**, despite compiler provenance).
- Section 5 Table 1: ranking model 2 separately reports **1.98x latency speedup**
  and **2.00x relative throughput** against its incumbent production stack.
  No hardware model is unambiguously attached to this table row, so these claim
  hardware fields stay unknown rather than borrowing Case 2's hardware.
- Representation evidence: Section 5.2 describes PyTorch rewrites compiled to a
  fused **Triton kernel**. The NVIDIA Triton Inference Server is a different
  product and does not establish a kernel language. Directly edited Python/C++
  source establishes `source` level without inventing new vocabulary values.
- Claims have undisclosed numerical search budgets and unknown exact public
  artifacts. A server optimization was contributed upstream, but that is not
  proof the attention kernel or full agent system is public.

## Include: Triton AI Compiler (TAIC)

- First-public paper date **2026-09-29**; François Costa and Azalia Mirhoseini
  (Stanford), Charly Castes and Thomas Bourgeat (EPFL).
- Paper: https://arxiv.org/abs/2609.36800
- Full text: https://arxiv.org/html/2609.36800v1
- Author agent implementation: https://github.com/francois141/triton_ai_compiler
- Author evaluator: https://github.com/francois141/ptx_gym
- Section 3.3: planner/subagents propose and revise PTX; feedback includes
  assembly, sanitizer, numerical correctness, performance and Nsight Compute.
  Three skills cover NCU interpretation, PTX documentation and optimization.
  Generated representation/level is **PTX**; Triton input alone does not mean the
  agent edits Triton DSL or compiler IR.
- Section 4.4 / Figure 5: best accepted **3.34x BitDelta** and separately
  **1.37x FlashAttention** kernels on NVIDIA B200, against each paper authors'
  official, target-autotuned Triton implementation (**T3**), with unnecessary
  masks removed. Each result has its own implementation denominator. API budget
  is USD15/run; request-completion overshoot is allowed because gates run before
  each request. These are selected results, not means.
- Verification caveat: Figure 5 kernels pass numerical checks; original-Volta
  proof-constrained search has lower speed. Extended Volta still cannot verify
  all kernels, notably bit-level manipulations used by BitDelta. Formal support
  is an evidenced optional feedback channel, not universal proof of the claims.
- Reproduction caveat: current author README defaults to compiler-generated PTX
  as the seed; the paper describes direct synthesis from Triton. Public agent and
  harness availability do not certify a claim-linked winning PTX artifact.

## Include: TileCas

- First-public paper date **2026-10-10**; Xinyu Xiao, Zihe Song, Dezhi Ran,
  Wei Yang, Tao Xie. Affiliations: Fudan, UT Dallas, Peking University, Beijing
  Tongming Lake Information Technology Application Innovation Center.
- Paper: https://arxiv.org/abs/2610.14740
- Full text: https://arxiv.org/html/2610.14740v1
- Author code: https://github.com/Alex4210987/tilecas
- Author project: https://alex4210987.github.io/tilecas/
- Sections 3.2–3.4 and repository README support iterative cross-level diagnosis,
  candidate restoration and retained versioned histories. One conversation owns
  decisions across levels; do not infer multi-agent from integration with AKO/KDA.
  The heterogeneous search tree is not automatically MCTS or beam search.
- Editable levels are TileLang DSL and native HIP/Ascend C source, not compiler
  IR. Evaluations use Ascend 910B3 and AMD Radeon AI PRO R9700; repository CUDA
  utilities do not establish NVIDIA evaluation.
- Section 4.1 / Table 1: **4.836x AKO+TileCas** and separately **4.425x
  KDA+TileCas**, arithmetic means vs workload-specific KernelBench references
  (**T0**). Fifty Level-3 workloads, two accelerators and two models (GPT-6 Astra,
  DeepSeek-V4.1-Flash), five seeds. Failed runs count zero; averages first cover
  seeds/workloads and then equally weight the four hardware/model configurations.
- Budget: 120 minutes per run, including failed attempts, diagnosis, conversions
  and evaluation. Current repository supplies framework/evaluation code; exact
  winning-kernel availability for the reported aggregates is left unknown.

## Include: Stateless Language Agents (SLA)

- First-public paper date **2026-10-06**; Qizheng Zhang and 17 coauthors.
  Affiliations include Stanford, Carnegie Mellon, University of Washington,
  SambaNova Systems and UC Berkeley (paper author block).
- Paper: https://arxiv.org/abs/2610.07625
- Full text: https://arxiv.org/html/2610.07625v1
- Author project: https://github.com/Alex-q-z/stateless-language-agents
  At audit time this repository contains only `assets/` and one commit, not an
  implementation. It is therefore a **Project placeholder**, not a Code link.
- Sections 3.1–3.3: one fresh Advisor invocation assigns concrete experiments to
  parallel, isolated Workers. The harness retains candidate snapshots, measured
  outcomes and chronological traces, while reconstructing role-specific context.
  This supports prompting, iterative refinement, multi-agent/planner-worker/
  parallel coordination, trajectory/archive memory. Models remain frozen; this
  is not RL training (Appendix A).
- Section 4.1: actual GPU evidence consists of SOL-ExecBench tasks #1, #58 and
  #210, selected by submission count on 2026-08-01. Section 4.2 explicitly says
  the best #210 kernels use Triton. This supports DSL-level optimization and
  Triton representation; permitted CUDA in a prompt is not proof of its use.
- **95.9% token reduction**, Table 3, is specifically SLA versus **EvoX** on
  SOL-ExecBench #58 (MoE token sorting/prefix sums), reaching the common final
  baseline score of 0.804 at 14.5M rather than 354.1M tokens. This is a search-cost
  comparison (**N/A**, prior-agent), not an implementation runtime speedup.
- Budget: 500M cumulative input/output tokens per GPU task/method, Codex
  v0.152.1 with GPT-5.5/high reasoning; default three Workers and three local
  trials per Advisor epoch. These GPU results use **one run per method**.
- The prominent 93.1% token saving is from a separate **simulated VLIW SIMD**
  problem; do not advertise it as a GPU result. Exact GPU model is not specified
  in the inspected primary paper, so claim hardware stays unknown and the
  hardware facet is unannotated. Do not copy B200 from generic SOL benchmark
  documentation into a paper-specific claim.
- Appendix E defines SOL score as the mean of
  `1 / (1 + (T_kernel - T_SOL) / (T_baseline - T_SOL))`, not a direct
  fraction-of-hardware-ceiling. The 0.862 final #58 score is consequently not
  mislabeled as 86.2% hardware efficiency.

## Boundary review: Scaling Discovery Requires Forgetting — not added

- Primary paper: https://arxiv.org/abs/2610.20563, first public **2026-10-14**.
  Full PDF: https://arxiv.org/pdf/2610.20563. Authors Shangyin Tan and ten
  coauthors; UC Berkeley, Stanford and Bespoke Labs (page 1 author block).
- PDF-only primary source was inspected, including Section 4 / Table 1,
  Section 4.2 and Appendix A Table 4. A four-agent team drops old sessions and
  candidate histories three times, retaining the best program between rounds.
- The only kernel experiment is **Anthropic's simulated VLIW SIMD machine**.
  The edited Python program emits instruction bundles for tree traversal and
  batch hashing. Table 1 reports 1097 +/- 18 mean best simulated cycles versus
  1426 +/- 197 for one agent and 1220 +/- 44 for four independent agents, three
  runs each, USD40 model-token budget per replicate. These are real simulated
  implementation denominators, not N/A method-only runtime comparisons.
- Its physical H100 experiment edits a **nanochat training script** and measures
  validation bits per byte; it does not demonstrate GPU kernel generation.
- Decision: record as adjacent search/memory research, **exclude from this
  accelerator-kernel update** rather than expanding the inclusion boundary or
  vocabulary. No candidate for this paper remains in the staging YAML.
- Additional closing queries were `"Stateless Language Agents" "B200"`,
  `"Stateless Language Agents" site:github.com` and `"2610.20563"`. Discovery
  indexes were not used as performance evidence. No further general research
  harnesses were expanded into catalog entries in this pass.

## Unresolved facts / deliberately omitted numbers

- No guessed official code or winning artifact for CUDA-Harness, ForgeMegakernel
  or FlashVector.
- No inferred hardware model for FlashVector Table 1.
- No RL tag for CUDA-Harness's parameter-free insight updates.
- No custom/compiler IR tag for TileCas's high-to-native-source interface.
- No suite-wide or geometric-mean reinterpretation of TileCas arithmetic means.
- No claim that TAIC's BitDelta result is formally verified, or that the current
  repository default exactly reproduces the paper's synthesis initialization.
- No claimed SLA implementation release based on its placeholder repository,
  no guessed GPU model, and no conversion of nonlinear SOL score into hardware
  efficiency.
- Six new entries and thirteen independent numerical claims are integrated into
  the canonical `data/agents.yaml` catalog;
  baseline states retain the approved T0–T6/Unknown/N/A semantics.
