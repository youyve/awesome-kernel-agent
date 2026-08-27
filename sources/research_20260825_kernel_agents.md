# Kernel-agent research audit — 2026-08-25

This file records the evidence used for the 2026-08-25 catalog refresh. It is
an audit trail, not another generated catalog. `data/agents.yaml` remains the
single source of truth.

## Scope and method

- Cutoff: 2026-08-25 (Asia/Shanghai).
- Scope: LLM-driven systems that generate, repair, translate, or iteratively
  optimize operator-level accelerator kernels; compiler/agent co-design is in
  scope when an LLM makes workload-dependent kernel decisions.
- Date field: first public release; for paper-only entries, arXiv v1 month.
- Evidence order: official paper and submission history, official repository
  and artifacts, then first-party engineering posts. Search snippets and
  third-party summaries were discovery aids only.
- Claim discipline: every numerical description records its denominator and
  evaluation scope; selected-task, pass@k, end-to-end, precision-asymmetric,
  and best-case results are labeled as such. Missing artifacts are not treated
  as reproducible results.
- The preferred `parallel-cli` research backend was present but unauthenticated
  in this environment. The search was therefore repeated with the built-in web
  search/open tooling, retaining the same primary-source-only standard.

Representative queries included `kernel agent GPU arXiv 2026`, `LLM CUDA
kernel optimization agent August 2026`, `Triton kernel agent 2608`, `Ascend C
agent kernel 2026`, `NKI Agent Trainium kernel`, `AMDGPU assembly agent`, and
official GitHub searches for projects named by the papers.

## Newly cataloged: July–August 2026 evidence

| Entry | Primary evidence | Inclusion and claim-scope decision |
|---|---|---|
| LLM4LLM | [paper](https://arxiv.org/abs/2608.21836), [official repo](https://github.com/hzeng2000/LLM4LLM) | Included; end-to-end and KernelBench numbers are against PyTorch eager, and the repo omits generated results/model weights. |
| EvoMem | [paper](https://arxiv.org/abs/2608.10795) | Included as memory-augmented evolutionary search; its GPU-kernel evidence is explicitly limited to two target tasks and no artifacts are linked. |
| PTXBench / MiniPTXAgent | [paper](https://arxiv.org/abs/2608.17379), [official repo](https://github.com/zhang677/PTXBench) | Included; benchmark plus adaptation agent. The paper explicitly says no evaluated model consistently matches frontier libraries across the suite. |
| HIERA | [paper](https://arxiv.org/abs/2608.21157) | Included; result is on all 250 KernelBench tasks, but candidates may use PyTorch composites or CUDA libraries rather than custom CUDA. |
| KernelArc | [paper](https://arxiv.org/abs/2608.17071) | Included; leaderboard claim is limited to five selected SOL-ExecBench tasks and a dated snapshot. |
| SparseDitto | [paper](https://arxiv.org/abs/2608.05033) | Included; per-matrix/operator/GPU specialization and cuSPARSE out-of-resource omissions are called out. |
| LEAP | [paper](https://arxiv.org/abs/2608.01804) | Included as multi-turn code RL; headline is correctness and training throughput, not expert-kernel speedup. |
| CAKE | [paper](https://arxiv.org/abs/2608.12629), [public upstream-artifact tracker](https://github.com/flashinfer-ai/flashinfer/issues/4254) | Included as compiler-agent co-design; core system is not released, while generated production changes are traceable as upstream PRs. |
| AsmEvo | [paper](https://arxiv.org/abs/2608.20711) | Included; edits recovered AMDGPU code objects and reports a selected 30-binary study, not full KernelBench. |
| Zomboss | [paper](https://arxiv.org/abs/2608.00894) | Included; neural search chooses typed mappings inside a verified compiler boundary rather than emitting unrestricted source. |
| Ascend Debug Agent | [paper](https://arxiv.org/abs/2608.02712) | Included; repair is measured on 27 frozen near misses. The non-significant Pass@3 comparison and integrity-gate rejections are retained. |
| CUDAPerf | [paper](https://arxiv.org/abs/2607.20908) | Included; values are pass@5. The paper's `3.32` is the absolute gap between 6.41 and 3.09, not a 3.32-fold relative gain. |
| LLM-CUDA / Harness Engineering | [paper](https://arxiv.org/abs/2607.17979), [official artifact repo](https://github.com/syhya/mlsys26-flashinfer-contest) | Included; distinguishes human-guided from full-agent results and records the later randomized-validation failure. |
| AgenticCANN | [paper](https://arxiv.org/abs/2607.26661) | Included; the 54-task framing is not reported as 54 successful evaluations because Appendix C.2 says roughly 40 exhausted the API budget. |
| Hawk | [paper](https://arxiv.org/abs/2607.01590) | Included using the main eight-operator aggregate; the abstract's 2.2x is labeled as a maximum. |
| NKI-Agent / ATX Custom NKI Agent | [paper](https://arxiv.org/abs/2607.04395), [AWS sample](https://github.com/aws-samples/sample-ATX-custom-NKI-Agent) | Included; paper and sample protocols are kept separate, NKIGen-Bench is not conflated with NKIBench, and unreleased training data/adapters are noted. |
| Compiler-Grounded Hierarchical Diagnosis | [paper](https://arxiv.org/abs/2607.23089), [CANNBot Skills integration](https://gitcode.com/cann/cannbot-skills) | Included; 4.35x and 2.60x use different baselines and are not combined, and the public suite does not contain the 37 winning kernels. |
| Atrex Kernel Agent | [paper](https://arxiv.org/abs/2607.14541), [official repo](https://github.com/alibaba/atrex-kernel-agent) | Existing entry substantially updated; first public repo release is June, while optimizer evidence is a controlled three-operator case study. |
| GEAK v4 | [official AMD article](https://www.amd.com/en/developer/resources/technical-articles/2026/geak-v4.html), [official repo](https://github.com/AMD-AGI/GEAK) | Added as a distinct versioned July release without rewriting the stable GEAK-HIP ID; moving-main results are not mixed into the v4 claim. |
| ForgeStencil | [official repo](https://github.com/OpenBMB/ForgeStencil), [commit history](https://github.com/OpenBMB/ForgeStencil/commits/main/) | Included; the repo ships agents, kernels, 100 application packages, harnesses and a result registry. End-to-end gains can include application restructuring. |

## Backfills and recently revised evidence

These were missed by the previous June-cutoff catalog or received a material
July/August revision. Their catalog date still follows first public release.

| Entry | Primary evidence | Decision |
|---|---|---|
| AgentCompile | [paper](https://arxiv.org/abs/2606.07665), [official repo](https://github.com/veneno1213822/AgentCompile) | Included; August v2 was reviewed. End-to-end gains include runtime/KV/CUDA-Graph work, and the public repo is review-only and omits winning outputs. |
| SpecGen | [paper](https://arxiv.org/abs/2606.17518) | Included as a June backfill; selected-task, large-GPU-pool and unequal-token caveats are explicit. |
| Kernel Forge | [paper](https://arxiv.org/abs/2607.24762), [official repo](https://github.com/TheJoshBrod/KernelForge), [generated kernels](https://github.com/TheJoshBrod/KernelForge/tree/main/kernels/generated/individual_op_kernels) | Included with June date because the official submission/repo history predates the `2607` identifier; operator-level GB10 results only. |
| KForge | [original paper](https://arxiv.org/abs/2511.13274), [2026 evaluation update](https://arxiv.org/abs/2606.02963) | Retains the 2025-11 first-public date while linking the expanded evaluation; separates B200 end-to-end results from Intel B580 operator results. |
| Houmao | [paper](https://arxiv.org/abs/2608.14560), [official framework](https://github.com/igamenovoer/houmao), [accepted CUDA artifacts](https://github.com/CodeGandee/flashinfer-bench-starter-kit/tree/main/solution/cuda) | Included with May first-public date; reports the strong contest baseline result separately from much larger PyTorch ratios and records that the exact campaign workflow is not bundled with the general framework. |
| KernelBrain | [paper](https://arxiv.org/abs/2608.02611) | Included with May date because arXiv's official history says 2026-05-19 despite the `2608` identifier; six selected kernels, no aggregate geomean. |
| CANNBot Skills | [official repo](https://gitcode.com/cann/cannbot-skills), [Hawk paper identifying the baseline](https://arxiv.org/abs/2607.01590) | March project added because its official changelog shows material July–August expansion; capability tests are not presented as kernel performance. |

## Existing-entry corrections checked against primary sources

- AccelOpt's current arXiv v2 reports average peak-throughput efficiency rising
  from 49% to 61% on Trainium 1 and from 45% to 59% on Trainium 2; the older
  catalog shorthand "45% to 71%" was removed during the v2 migration:
  <https://arxiv.org/abs/2511.15915>.
- KDA-Pilot canonical repository and B200 artifacts:
  <https://github.com/BBuf/KDA-Pilot>.
- Kernel Design Agents and public KernelWiki:
  <https://github.com/mit-han-lab/kernel-design-agents>.
- CUCo official artifact release:
  <https://github.com/UT-InfraAI/cuco> and
  <https://arxiv.org/abs/2603.02376>.
- DICE code/checkpoints and paper:
  <https://github.com/deadlykitten4/DICE> and
  <https://arxiv.org/abs/2602.11715>.
- CUDA Agent's canonical paper, official environment repository, released
  training dataset, and denominator-specific overall/Level-3 results:
  <https://arxiv.org/abs/2602.24286>,
  <https://github.com/BytedTsinghua-SIA/CUDA-Agent>, and
  <https://huggingface.co/datasets/BytedTsinghua-SIA/CUDA-Agent-Ops-6K>.
- CuTeGen's primary CuTe representation and 1.71x average over PyTorch on
  209 KernelBench Level-1/2 tasks:
  <https://arxiv.org/abs/2604.01489> and
  <https://github.com/taratt/cutegen>.
- EGG, KernelPro and daVinci-kernel affiliations, budgets and artifact status:
  <https://arxiv.org/abs/2606.26758>,
  <https://arxiv.org/abs/2606.26453>, and
  <https://github.com/GAIR-NLP/daVinci-kernel>.
- PyTorch KernelAgent evaluation scope and artifacts:
  <https://github.com/meta-pytorch/KernelAgent> and the
  [PyTorch engineering post](https://pytorch.org/blog/kernelagent-hardware-guided-gpu-kernel-optimization-via-multi-agent-orchestration/).
- AWS Neuron agentic-development release:
  <https://github.com/aws-neuron/neuron-agentic-development>.
- Qwen3.7-Max claim corroboration:
  [Qwen technical post](https://www.alibabacloud.com/blog/qwen3-7-the-agent-frontier_603154)
  and [Alibaba corporate release](https://www.alibabagroup.com/en-US/document-1994119844504535040).

## Cataloged elsewhere or not promoted to an agent entry

- [Contract-Grade Verifier](https://arxiv.org/abs/2608.12700) is highly
  relevant but is an evaluator, not a kernel-generation agent. It was added to
  README's evaluation-integrity section instead. Its audit reports 39.5% of
  2,638 previously accepted generated kernels broken beyond tolerance choice
  and 62.1% with at least one contract violation.
- Benchmarks without an agent loop remain out of this repository and belong in
  [awesome-kernel-benchmark](https://github.com/youyve/awesome-kernel-benchmark).
- Projects with only third-party mentions, inaccessible evidence, or no
  demonstrable LLM/agent role were not added. Absence from the catalog is not a
  negative quality judgment; it means the inclusion contract was not verified
  by the cutoff.
