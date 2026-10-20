# Hardware-specific kernel agents: evidence audit, 2026-10-19

Scope: primary sources for new or previously omitted AMD/HIP, Ascend, TPU/Pallas,
Trainium/NKI, and other accelerator kernel agents. The existing v2 catalog was
checked for duplicates. Search results were discovery aids; entries below use
papers, author repositories, or first-party articles. Accepted records are
integrated into the canonical `data/agents.yaml` catalog.

## Search record

Queries included `MaxKernel kernel agent 2026`, `AMDKernelVault`, `kernel agent
Ascend NKI TPU Pallas September October 2026`, `("kernel" "agent") ("Ascend" OR
"NPU") after:2026-08-25 before:2026-10-20`, the corresponding Trainium/NKI,
AMD/HIP, and Pallas/Intel queries, `site:arxiv.org "kernel generation" "2609"`,
`site:arxiv.org "kernel generation" "2610"`, and first-party AMD blog searches
for September/October GEAK and kernel-agent work. GitHub API repository trees,
commit histories, and README files were also inspected.

## MaxKernel

Primary sources:

- [Paper and author affiliations](https://arxiv.org/abs/2609.04523), v1 2026-09-03;
  [full text](https://arxiv.org/html/2609.04523v1).
- [Current implementation](https://github.com/AI-Hypercomputer/accelerator-agents/tree/main/maxkernel/adk),
  [evaluation harness](https://github.com/AI-Hypercomputer/accelerator-agents/tree/main/maxkernel/adk/evaluation),
  [JAXBench](https://github.com/AI-Hypercomputer/accelerator-agents/tree/main/JAXBench).
- [Google Developer article](https://discuss.google.dev/t/maxkernel-automating-pallas-kernel-generation-and-optimization-via-agentic-systems/366686),
  posted 2026-05-26, independently establishes public availability before the paper.
- [March implementation/rename commit](https://github.com/AI-Hypercomputer/accelerator-agents/commit/923f118caedca6def1823d004572946cffee89a4),
  2026-03-24, migrates `tpu_kernel_gen` to `MaxKernel`.
- [February placeholder](https://github.com/AI-Hypercomputer/accelerator-agents/tree/de4f7ed55714e6d29526b90d8ece0e94b0fe02ca):
  only LICENSE, README, and contributor documentation; agents were marked coming
  soon. Do not date the system from repository creation or this placeholder.

Decision: newly index with first-public code month **2026-03**. The paper's old
`tree/main/MaxKernel` link is stale after a path reorganization; the current
implementation was confirmed through the authenticated GitHub tree/content API.
Affiliations are Google and Google DeepMind, explicitly printed in the paper.

Taxonomy evidence: sections 2.1–2.5 describe specialized planner/implementation/
test/profiling agents, optional human intervention, iterative refinement,
autotuning, local hill climbing, best-candidate rollback, beam search, and parallel
workers. A documentation RAG store excludes hand-tuned kernels; an explicit saved
search graph retains successful candidates. Compiler errors, test outcomes, and
XProf timing inform proposals. Output is JAX/Pallas on TPU, with operator/fused
workloads. Pallas needs an additive representation vocabulary value; no new facet
or architecture is required.

Claim decisions: Table 1's parallel-search result is **1.58x versus XLA-compiled
JAX**, T1, all 50 JAXBench tasks, TPU v6e; **regressions are floored at 1x**. The
budget is five concurrent trajectories with five iterations each, Gemini 3.1 Pro.
The separate 50/50 correctness claim is N/A for implementation-tier purposes.
Only 34/50 tasks beat XLA. The default numerical tolerance is 0.01, relaxed up to
0.1 on selected tasks. Do not recast the 2.32x eight-task aggregate as a speedup
against human experts: its denominator is also XLA. Table 2 and adjoining prose
disagree on which search mode produced the 6.74x Paged Attention result; it is not
promoted to a claim here.

Artifact decision: implementation and harness are public. JAXBench `optimized.py`
files are reference implementations, not demonstrated to be the paper's winning
generated kernels. Generated-kernel and exact-claim artifact availability remain
unknown; code availability does not resolve them.

## AMDKernelVault

Primary sources:

- [Paper](https://arxiv.org/abs/2609.12471), v1 2026-09-11;
  [full text](https://arxiv.org/html/2609.12471v1).
- [Current AMD implementation](https://github.com/AMD-AGI/AMDKernelVault), formerly
  `AMD-AGI/hip_kernel_llm_lab` as linked by the paper.
- [Public kernel dataset](https://huggingface.co/datasets/amd/AIG-Datasets).
- [HIP generator implementation commit](https://github.com/AMD-AGI/AMDKernelVault/commit/27092da5caddce0b5583aa4db332fe4e71e2ea75),
  2026-05-18; SFT code also appears in repository history on 2026-05-14.

Decision: newly index **2026-05** from implementation history, not the September
preprint. The paper lists AMD affiliation. This is eligible as a kernel-agent
training/generation system, not merely a dataset: HIPKernelGen/TritonKernelGen
perform generation, execution validation, and revision, and the trained model
participates in a measured agent loop.

Taxonomy evidence: sections 3–4 explicitly describe SFT, single-turn HIP GRPO,
multi-turn Triton agentic RL, reflection, compilation/correctness/runtime
feedback, and generator/reflector/optimizer roles. Source HIP and Triton DSL are
the target artifacts; operator and fused tasks are evaluated. The reported
Triton evaluator explicitly disables profiler feedback, so no profiler tag is
added merely because dataset construction includes latency profiling.

Safely structured results: Table 4 **33.2% Corr@3 on 184 TritonBench-G tasks**;
Table 5 **41.94% Corr@3 on 31 ROCmBench tasks**; Table 2 **34% Pass@1 on 200
KernelBench L1/L2 PyTorch-to-HIP tasks**. Each is correctness/pass measurement
against task references, hence N/A implementation baseline tier. Triton inference
hardware is MI355X; the precise HIP evaluation SKU is not established. Corr@3
means three feedback iterations, not three independent samples. Triton evaluation
uses OptimAgent-v2, one offspring, three iterations, identical role assignment,
and no profiler. The speed columns are not promoted because the tables do not
fully expose task-wise input/PyTorch denominator mixture and aggregation.

Artifact decision: public implementation includes HIP/Triton evaluation modules;
the dataset contains generated kernels. Exact held-out evaluation winners and
trained checkpoint availability remain unknown. The current versioned dataset
has additional records beyond the paper corpus; paper counts must not be
presented as current release counts. No exhaustive semantic overlap audit was
performed by the authors; correctness advantages do not imply universal speed
or compilation superiority.

## AscendOpGenAgent

Primary sources:

- [Author repository](https://github.com/Just-it/AscendOpGenAgent), including
  README, agent definitions, skills, batch evaluators and AutoResearch runtime.
- [Initial Ascend C agents/skills](https://github.com/Just-it/AscendOpGenAgent/commit/bdd32f7bf6a4ba0d612cc9425c13310178cdfa3b),
  2026-03-14; earliest repository creation is 2026-03-12.
- [Archived operator artifacts](https://github.com/Just-it/AscendOpGenAgent/tree/main/archive_tasks),
  including `avg_pool3_d/kernel/*.cpp`, kernel headers, and generated wrappers.
- [Benchmark report](https://github.com/Just-it/AscendOpGenAgent/blob/main/benchmarks/BASELINE_latest.md),
  dated 2026-04-30, Atlas A2, CANN 8.5.1, PyTorch 2.9.0.

Decision: newly index older omitted work, **2026-03**, author-maintained code;
organizational affiliation is not established. README explicitly supports
Triton-Ascend and Ascend C generation, multi-agent workflow coordination,
skills, correctness/performance tests, and an iterative plan/edit/evaluate/
keep-or-discard loop. Do not infer Huawei affiliation from Ascend support.

No numerical claim is promoted. Reported ratios sometimes contradict displayed
latencies: the Ascend C GELU row gives 0.086/0.186 ms but 0.13x, and several other
rows are inconsistent. No experiment-linked search budget or exact winner mapping
is established. An audit item preserves the unresolved evidence. Public archived
kernel examples support project generated-kernel status `partial` only.

## Existing entries and exclusions

- [Neuron Agentic Development](https://github.com/aws-neuron/neuron-agentic-development)
  is already cataloged as `neuron-agentic-development`; no duplicate.
- NKI-Agent / ATX Custom NKI Agent is already cataloged. The July paper and August
  AWS migration article are not separate systems.
- [ASCEND, arXiv 2609.32868](https://arxiv.org/abs/2609.32868) is an HPC job/workflow
  agent, unrelated to Huawei Ascend kernel generation; not included from name
  similarity.
- [KREX](https://arxiv.org/abs/2609.30057) is concurrent kernel-evaluation runtime
  infrastructure; forwarded for an infrastructure-section decision, not counted
  as a kernel generation agent here.
- [Xtrace](https://arxiv.org/abs/2609.28769) has agent-assisted optimization
  evidence; forwarded for the general papers/infrastructure investigation.
- KernelOPT and ForgeMegakernel were forwarded to the general-paper investigation.

## ROCm Hyperloom

Primary sources:

- [Official implementation](https://github.com/AMD-AGI/Hyperloom) and
  [AMD article, 2026-09-21](https://rocm.blogs.amd.com/software-tools-optimization/hyperloom-optimization/README.html).
- [Initial code commit](https://github.com/AMD-AGI/Hyperloom/commit/630572585f2cd737ada3e8a175670f75ca113268),
  2026-03-27, includes inference/training agent instructions, profiling,
  benchmark and optimization scripts, rather than a placeholder README.
- [March generated-kernel archive](https://github.com/AMD-AGI/Hyperloom/tree/79856335c65047ac11264132167def97047f83e5/.cursor/skills/inference-optimization/results/qwen3-14b-mi355x),
  containing two agent-written RMSNorm implementations.
- [KernelForge documentation](https://github.com/AMD-AGI/Hyperloom/blob/main/docs/kernelforge/what-is-kernelforge.md),
  an integrated backend; it is not separately counted in this update.

Identity check: GitHub repository API IDs are **1193937742** for Hyperloom and
**1167825815** for Apex. Both retain independent names, repositories and README
descriptions; Apex does not redirect to Hyperloom. Hyperloom was created March 27
with code, whereas Apex was created February 26. Index Hyperloom separately with
**2026-03**, without renaming/removing `amd-apex`.

Taxonomy evidence comes from the article and current README: orchestration,
critic and specialist roles; iterative framework/kernel optimization; independent
correctness and end-to-end performance gates; profiler/roofline feedback; and a
recipe KB read across runs. HIP, Triton and FlyDSL support is explicitly listed.
No RL annotation is added: training a policy is described as future work.

Claims: article Table 4 reports **1.73x median** across 16 serving workloads;
Table 2 reports **3.48x** for Llama-3.1-8B-Instruct on one MI355X, from 7677 to
26682 tokens/s, input/output length 1024 and concurrency 64. Baselines are stock
serving implementations, therefore Unknown rather than N/A; no T4 deployment
status is assumed. Only the single-session case explicitly has a 24-hour cap,
ending with roughly five hours unused. Precision/attention/speculation/framework
changes drive much of the gain, so neither number is presented as isolated kernel
speedup. The older generated examples establish only partial project artifacts,
not exact September winning-claim reproducibility.

The KernelForge/GEAK speedup rows in article Table 3 are not promoted: they lack a
fully specified kernel set, denominator and budget. Hyperloom's current README
links the Arbor paper for background; that is not sufficient evidence to merge
Arbor and Hyperloom identities or transfer Arbor claims.
