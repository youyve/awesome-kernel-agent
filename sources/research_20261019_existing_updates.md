# Existing-entry update audit — 2026-10-19

Audit window: after the 2026-08-25 evidence sweep through 2026-10-19. This note records six updates applied to existing stable IDs; a later paper or software release does not reset the first-public-release month. Primary sources below were inspected directly. The search backend was the available web tool because `parallel-cli` is not installed. Raw query/open results are retained under `sources/20261019/existing-*.json`. Subsequent backfill checks and an independent review of six new entries are recorded below.

## Confirmed existing-entry updates

### ForgeStencil — `forgestencil`

- Add `links.paper: [{label: Paper, url: https://arxiv.org/abs/2609.06694, provenance: author}]`.
- Paper v1: 2026-09-06; v2: 2026-09-18. Keep `date: 2026-08`, because the repository preceded the paper.
- Existing application claims 1.41× median and 2.05× geomean remain supported. Their `primary_source` is now `https://arxiv.org/abs/2609.06694`, locator `v2, Section 7.3.1; Appendix D, Table 8 (E1)`; the existing repository artifact URL is preserved.
- Add caveat: `The September paper reports 100 integrated applications from 116 candidates; application gains include bespoke stencil kernels, non-stencil kernels and host/structural rewrites. Operator microbenchmarks do not validate application-level claims.`
- Do not add an undifferentiated 37-case operator speedup: the paper separates fp16/fp32 and uses per-case Halide/Devito/EBISU denominators. Its operator matrix also differs from the older repository README. No T5 inference is justified merely by the authors' “public-SOTA” wording.

Evidence: [paper metadata](https://arxiv.org/abs/2609.06694), [paper §7.3.1–7.3.2 and Appendices D–E](https://arxiv.org/html/2609.06694v2), [official repository Results](https://github.com/OpenBMB/ForgeStencil).

### Atrex Kernel Agent — `atrex-kernel-agent`

- v0.3.0 was released 2026-09-23; keep first-public month 2026-06.
- Add article/release link: `{label: "v0.3.0 release", url: https://github.com/alibaba/atrex-kernel-agent/releases/tag/v0.3.0, provenance: official}`.
- Suggested summary: `Profile-driven optimizer grounded in GPU Wiki and structured measurement history; v0.3.0 adds resumable isolated episodes, supervisor-owned correctness/performance promotion and native Atrex-Bench production campaigns. The paper's controlled three-operator FlyDSL study reports up to 1.31x over deployed kernels.`
- Suggested caveat: `The paper's 1.31x claim remains a three-operator, two-model study on anonymized XPU-A hardware. The September software release supports broader targets and workflows, but that does not extend the paper's measured result or release its exact winning kernels.`
- `representations` may add `CuTe` and `TileLang`: both are explicitly listed as supported campaigns in the versioned README. Preserve existing representations because historical support was already evidenced. Do not infer a new result for any target.
- Hardware support now explicitly includes T-Head PPU/zwm890p, added using the existing `T-Head-Zhenwu-M890-PPU` vocabulary value.

Evidence: [release date](https://github.com/alibaba/atrex-kernel-agent/releases/tag/v0.3.0), [versioned README Overview/News](https://github.com/alibaba/atrex-kernel-agent/blob/v0.3.0/README.md), [current quickstart](https://github.com/alibaba/atrex-kernel-agent/blob/main/docs/quickstart.md).

### PTXBench / MiniPTXAgent — `ptxbench-miniptxagent`

- Paper v3 is dated 2026-09-28. Keep 2026-08 first-public date and stable ID.
- Replace stale release caveat with: `The September v3 paper studies repair-conditioned SFT and reports uneven transfer; no model consistently matches frontier libraries across the suite. The current repository supplies profiling, agent-loop and training/evaluation code plus runnable examples, but explicitly excludes paper outputs, plots and the full prepared experiment matrix.`
- Set `artifacts.harness` to `{status: yes, urls: [https://github.com/zhang677/PTXBench]}`: `fib-profile`, `multiturn` evaluators and `ptxbench-eval` are visible.
- Set `artifacts.trajectories` to `unknown` with empty URLs: AccRL publishes workload/reference records, not verified optimization histories. A run-export feature does not establish a published historical trajectory artifact.
- Retain `generated_kernels: partial`, but point to the author SFT dataset rather than a generic repository. Its public viewer exposes generated CUDA-code previews and the file tree lists data payloads. The dataset card also describes the release as private; complete downloads and full optimization histories were not verified. This supersedes the preliminary proposal to set generated kernels to unknown.
- Add typed author Article, Model and Dataset links. The model collection and SFT dataset have access-unverified labels; no model-weight availability upgrade. Add supervised fine-tuning to policy adaptation, which v3 explicitly studies. No numerical headline or claim-linked artifact was added.
- Add a migration-review note for the inconsistent access signals. Model-card visibility, file listings and code previews do not prove complete reproducibility or weight download access.

Evidence: [arXiv submission history](https://arxiv.org/abs/2608.17379), [v3 §3/§5](https://arxiv.org/html/2608.17379v3), [official repository opening paragraph and directory map](https://github.com/zhang677/PTXBench), [author article](https://zhang677.github.io/blog_md/ptxbench.html), [SFT dataset viewer and card](https://huggingface.co/datasets/Genghan/PTXBench-Qwen3.6-27B-SFT), [adapter collection](https://huggingface.co/collections/Genghan/ptxbench-qwen36-27b-sft-series), [AccRL dataset](https://huggingface.co/datasets/AccRL/accrl-training). Some repository pages were cached at different revisions; the audit does not assign a new release date to older model/dataset links.

### CANNBot Skills — `cannbot-skills`

- Update the July–August-only caveat to cover the inspected September–October changes: `Licensed under CANN Open Software License v2.0. September–October updates add NPU profiling, runtime memory/synchronization checking, simulator and disassembly diagnosis, and theoretical-performance estimation; parts of plugin orchestration and optimization knowledge moved to companion repositories. These capabilities are not aggregate kernel-generation performance results.`
- Useful exact locators: 2026-09-20 `tool-npu-compute`; 2026-09-22 `npu-check`/`npu-objdump-toolkit`; 2026-10-12 plugin and knowledge migration; 2026-10-13 `ops-theoretical-performance-estimation`.
- No new performance claim or winning-artifact assertion. Disassembly inspection is feedback; it does not establish assembly-level optimization.

Evidence: [official dated changelog](https://gitcode.com/cann/cannbot-skills/blob/master/CHANGELOG.md).

### GEAK v4 — `geak-v4`

- Current README still identifies the project as v4. Do not create a separate v5 entry from generic search hits.
- Add/update a caveat: `The current repository additionally documents whole-model serving optimization, deterministic single-kernel and end-to-end workflows, and a Codex CLI backend. These software capabilities do not extend the earlier five-kernel numerical claims; machine-produced warm-start patches are described as gitignored.`
- Optional project documentation link: `{label: Documentation, url: https://rocm.docs.amd.com/projects/geak/en/latest/, provenance: official}`.
- Current README reports 3.68× versus 1.90× for a 12-HIP-kernel experiment, but its short table does not identify the implementation denominator completely. Do not silently add 3.68× as a structured speedup or divide the two numbers into a new claim.

Evidence: [official README Overview, e2e_workflow, Results and Repository layout](https://github.com/AMD-AGI/GEAK), [raw README](https://raw.githubusercontent.com/AMD-AGI/GEAK/main/README.md).

### CAKE — `cake`

- The upstream tracker now links categorized kernel work and standalone packages, with category sub-issues added 2026-10-16. This supports continued project-level partial generated-kernel availability.
- Do not upgrade core implementation or the Flash-KMeans headline artifact: the inspected tracker does not identify the exact 1.144× clean-start winner. Existing `partial` claim status must not be interpreted as complete reproducibility.
- Suggested caveat addition: `The upstream tracker expanded through October 2026, but these upstream kernels do not by themselves identify the exact Flash-KMeans clean-start winning candidate.`
- The October 10 Gang Liao explainer is not a CAKE-author primary source; do not label it an official CAKE article.

Evidence: [official tracker, description and October 16 activity](https://github.com/flashinfer-ai/flashinfer/issues/4254), [paper history, still v1](https://arxiv.org/abs/2608.12629), [explainer author's disclosure](https://gangliao.me/blog/2026/cake-deep-dive/).

## Checked without a supported release change

| Existing ID | Primary check | Outcome |
|---|---|---|
| `asmevo` | [arXiv](https://arxiv.org/abs/2608.20711) | Still v1 dated 2026-08-21; targeted official-code search found no verified release. |
| `kernelarc` | [arXiv](https://arxiv.org/abs/2608.17071) | Latest history remains v2 dated 2026-08-20; no author implementation verified. |
| `kernelbrain` | [arXiv](https://arxiv.org/abs/2608.02611) | Still v1 with the unusual official 2026-05-19 timestamp; do not infer August from the identifier. |
| `leap-kernel-rl` | [arXiv](https://arxiv.org/abs/2608.01804) | Latest history remains v2 dated 2026-08-04; no official code/model artifact verified. |
| `specgen` | [arXiv](https://arxiv.org/abs/2606.17518) | Still v1 dated 2026-06-16; generic SpecGen repositories are unrelated. |
| `llm4llm` | [official repository Benchmarks](https://github.com/hzeng2000/LLM4LLM) | Explicitly still excludes generated results and model weights. No artifact upgrade. |
| `hiera` | [paper](https://arxiv.org/abs/2608.21157) plus targeted code search | No verified author code release surfaced. |
| `sparse-ditto` | [paper](https://arxiv.org/abs/2608.05033) plus targeted code search | No verified author code release surfaced. |
| `evomem` | [paper](https://arxiv.org/abs/2608.10795) plus targeted code search | No verified release change surfaced. |
| `zomboss` | [paper](https://arxiv.org/abs/2608.00894) plus targeted code search | No verified release change surfaced; game repositories are unrelated. |

An unsuccessful search is not proof that no artifact exists. These rows retain current uncertainty rather than adding categorical negative claims.

## Evaluation-integrity pointers

- PTXBench v3 separates correctness, dynamic target-instruction execution and runtime performance. Static PTX/SASS presence is insufficient. [Paper §2.2 and Appendix A.2](https://arxiv.org/html/2608.17379v3).
- ForgeStencil §7.4 reports its own measurement retractions, while Appendix E explicitly separates operator and application evidence. A short integrity pointer is justified; no new benchmark catalog is needed. [Paper](https://arxiv.org/html/2609.06694v2).
- FlashInfer's official 2026-09-22 autotuner article explains that eager execution and CUDA Graph replay require different timing objectives, and that timing only GPU device work may mis-rank deployed alternatives. This is an evaluation-methodology reference, not a Kernel Agent system. [Official article](https://flashinfer.ai/2026/09/22/autotuner-v2.html).

## Search log and exclusions

Queries included exact system names with `code github`, `SpecGen kernel code github`, `LEAP 2608.01804 github`, `CANNBot September October 2026`, official AMD-domain GEAK September/October queries, `GEAK v5`, `cannbot-skills 2026-10`, `GPU kernel September 2026 benchmark`, `GPU kernel October 2026 evaluation`, and HIERA/SparseDitto/EvoMem/Zomboss code-release searches. Exact existing primary URLs and new release/version URLs were then opened directly.

Unrelated hits excluded: Swiss building-certification GEAK releases; formal-Java, ontology, web-application and chemistry SpecGen repositories; vision-model Hiera; Plants-vs-Zombies Zomboss. A CANNBench team-ranking statement on a participant's personal page was not promoted to T5 without independent dated leaderboard evidence. Third-party PTXBench/CAKE explainers were discovery leads only.

This is a targeted audit of update-prone existing systems and search results, not a claim that every repository commit or every version of all 112 agents was exhaustively inspected.

## Backfill candidates checked

### MaxCode — verified candidate

The accepted record is `maxcode` in `data/agents.yaml`. [arXiv](https://arxiv.org/abs/2601.05475) dates the paper to 2026-01-09; [full text](https://arxiv.org/html/2601.05475v1) identifies Johns Hopkins University and AWS.

- §2 freezes the proposal policy. The separate trained value model is not evidence of policy RL, despite the title. The candidate therefore does not annotate policy reinforcement learning or policy SFT.
- §2.2–2.4 supports iterative beam search, generator/critic roles, execution feedback and retained critiques/trajectory context. §3.1 explicitly names generated CUDA source, KernelBench L1/L2 and default PyTorch denominators.
- Table 1 gives 3.17× / 1.61×, each a median of per-task maximum observed speedup across 100 tasks; the candidate uses two T0 claims, not the abstract's mixed-dataset percentage. Budget is depth 8 and K=8, using Claude-3.7-Sonnet.
- Hardware stays unannotated. No author implementation was verified. Google's accelerator-agents MaxCode is a different project and was not linked.

### Held or excluded candidates

| Candidate | Primary evidence / discovery | Decision |
|---|---|---|
| AlphaCu | [First author's page](https://iquitap.github.io/) announces ASE 2026 acceptance in July; [coauthor page](https://wangqing.io/) and [official ASE list](https://conf.researchr.org/track/ase-2026/ase-2026-research-track) agree on the title. | Hold for full method evidence. No accessible paper or artifact establishing concrete mechanism/representation was verified. Do not infer CUDA from the name, nor treat acceptance month as a verified paper-release date. |
| KernelOwl | Exact-name searches surfaced [a third-party index](https://github.com/qhy991/Awesome-LLM-Kernel-Agent), where it appears in diagrams but not a primary-linked paper row. | Hold: no primary paper/project located; do not create an entry from an unattributed diagram label. |
| DiffAgent / DiffBench | [Paper](https://arxiv.org/html/2601.03178v1), Methods: planning/coding/debugging plus evolutionary selection over diffusion pipeline acceleration techniques. | Exclude from the core kernel-agent catalog for now: inspected tasks combine sampling, caching, token merging and framework APIs; no custom kernel-generation mechanism was established. Distinct from the unrelated CVPR 2024 image-generation DiffAgent. |

Additional queries: exact AlphaCu/KernelOwl names with GPU/kernel/GitHub/DOI; MaxCode paper/code queries; DiffAgent diffusion acceleration. An unavailable source is a review boundary, not proof the work lacks a release.

## Independent review of six newly added records

The six entries below were checked against their primary sources after the main agent drafted them. No main-data edits were made during this second review. Raw retrievals are in `sources/20261019/independent-root-review-*.json`.

| ID | Checks | Conclusion |
|---|---|---|
| `kernelopt` | [v2](https://arxiv.org/html/2609.30059v2), Table 1, §§4–6, Appendix A | 1.23/1.40/1.15/1.07 all-task geomeans and torch.compile denominator agree; fixed per-iteration plan budget is not multiplied by beam width. Cross-run tracker is explicitly described but post-hoc guidelines did not affect Table 1. No unsupported code-availability upgrade found. |
| `servingstudio` | [official introduction](https://syfi.cs.washington.edu/blog/2026-09-24-introducing-servingstudio/), Cases 1–3; [repository](https://github.com/SyFI-ServingStudio/ServingStudio) | Throughput changes 5.6%, 10.8%, 25.6% and separate denominators/hardware agree. Unknown implementation tiers are conservative. Repository exposes pinned Agent/Sim/UI components; project code is not treated as exact winning kernels. Representation remains unknown. |
| `dream-rsi` | [v2](https://arxiv.org/html/2609.14858v2), §3, Figure 3, Appendices B and E; [release plan](https://github.com/zhengkid/Dream-RSI) | 2.09× and 1.44× compare runtime performance of discovered implementations, so Unknown rather than N/A is correct. L40S, round/call limits, retained replay state and differentiated policy-development/discovery roles are supported. Repository still says code and reproduction scripts are being prepared. |
| `areal-rsi` | [paper](https://arxiv.org/html/2610.18083v1), §§2–5 | §3 explicitly supports retrieval; §§2/4 support role/harness coordination and reusable skills. KernelBench reference is not sufficiently identified, so omitting a numerical primary claim is warranted. No GPU vendor or generated language was inferred from CUDA-event timing. |
| `krex` | [paper](https://arxiv.org/html/2609.30057v1), §§5–6 | Infrastructure/tool classification is correct; NVIDIA and AMD support are explicit. Throughput is benchmarking-system capacity, not generated-kernel speedup; no such claim is promoted. |
| `xtrace` | [paper](https://arxiv.org/html/2609.28769v1), §§3–5 and Appendix A.2; [open traces](https://g-watch.github.io/en/open-traces/) | Binary splicing is the tracer's operation, not evidence that the agent optimizes binaries. AMD/NVIDIA support is explicit. Open profiling traces are not optimization trajectories or winning generated kernels. No artifact-availability upgrade recommended. |

Validation after the six existing-record edits passed (`115 entries and 145 claims` at that point); `git diff --check -- data/agents.yaml` passed. The isolated MaxCode candidate also passed `validate_json_schema` and `validate_catalog(..., require_legacy_ids=False)`. Final integrated regeneration/testing is owned by the main update pass.
