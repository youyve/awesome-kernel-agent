# Kernel Agent research refresh — 2026-10-19

This refresh preserves the approved v2 architecture. The research window is
2026-08-26 through 2026-10-19, with older omissions backfilled at their evidenced
first-public month. The starting catalog contained 112 agents, 3 tools and 145
structured claims. All starting IDs are retained. Canonical records are in
[`data/agents.yaml`](../data/agents.yaml); generated views are not independently
edited.

Final coverage: **127 agents (+15), 5 tools (+2), 176 claims (+31)**. Six existing
records received source-backed release/artifact updates. The nine baseline states
contain T0=47, T1=13, T2=15, T3=24, T4=17, T5=0, T6=4, Unknown=22 and N/A=34.

New agent IDs: `areal-rsi`, `tilecas`, `stateless-language-agents`, `dream-rsi`,
`flashvector`, `forgemegakernel`, `kernelopt`, `servingstudio`,
`triton-ai-compiler`, `cuda-harness`, `amdkernelvault`, `maxkernel`,
`ascendopgenagent`, `hyperloom`, `maxcode`. Tools: `krex`, `xtrace`.

## Search and verification

Three parallel searches covered new papers, hardware-specific projects, and
updates to existing systems. Queries combined kernel generation/optimization,
agent, CUDA, Triton, PTX/IR, profiling, memory, RL, AMD/HIP, Ascend, TPU/Pallas,
Trainium/NKI, and September/October dates. Companion indexes and search snippets
were discovery aids only. Papers, author repositories, dated commits and
first-party articles establish the retained facts. Inspect the lane notes for
per-work source locators and inclusion decisions:

- [New papers](research_20261019_new_papers.md)
- [Hardware-specific systems](research_20261019_hardware_projects.md)
- [Existing-entry updates](research_20261019_existing_updates.md)

The `research-lookup` workflow was used with built-in search because its optional
`parallel-cli` backend was unavailable. Raw search/retrieval records are retained
in [`20261019/`](20261019/). The arXiv bulk endpoint returned HTTP 429, so direct
paper pages and focused searches were used instead. This is a broad primary-source
refresh, not a guarantee that every unpublished or unindexed project was found.
Failure to retrieve a link does not prove that its artifact is absent.

## Additional retained systems

### KernelOPT

[September paper](https://arxiv.org/abs/2609.30059), revised
[October 6, v2](https://arxiv.org/html/2609.30059v2). Red Hat's system preserves
vendor dispatch while optimizing Inductor-produced Triton/Helion kernels.
Table 1's all-task geometric means are 1.23× overall, 1.40× L1, 1.15× L2 and
1.07× L3, each against `torch.compile(max_autotune)` (T1); fallbacks are included.
The much larger optimized-only results are not substituted for those populations.
§5 specifies the plan/retry budget and H200 hardware. Appendix G contains examples.

The [author-linked repository](https://github.com/TorchedHat/KernelOPT) was not
retrievable during this audit. The Code link is retained with its provenance,
but implementation and winning-bundle availability stay unknown. A separate
`giveen/KernelOPT` implementation is not substituted as official code. IR input
and NCU feedback are not evidence that the agent edits compiler IR.

### ServingStudio

The [UW SyFI introduction](https://syfi.cs.washington.edu/blog/2026-09-24-introducing-servingstudio/)
is dated September 24 and links the [implementation](https://github.com/SyFI-ServingStudio/ServingStudio).
Its three cases report +5.6%, +10.8% and +25.6% **serving throughput**, with
different workloads and explicit SGLang/vLLM implementation denominators. These
are three claims, not one kernel-speedup aggregate. Baseline tiers remain Unknown:
the article does not establish production-incumbent status or an unambiguous
kernel-baseline tier. Case 1 links a [concrete tuning PR](https://github.com/sgl-project/sglang/pull/38560),
so K is partial, not complete. Source-level edits are evidenced; a concrete
generated-kernel representation is not inferred from CUDA Graph terminology.

### Dream-RSI

[Paper](https://arxiv.org/abs/2609.14858), first September 14, revised October 6.
[§4.1 and Appendix B](https://arxiv.org/html/2609.14858v2) separate runtime gains
on ConvDiv/ConvMax from reduced discovery-call counts on other tasks. The retained
2.09×/1.44× claims compare kernels found by Recursive Fixed Exploration; these
have real implementation denominators with unresolved tiers, not N/A.
The experiments use L40S; Appendix E.2 provides a Triton ConvDiv program. The
[official release plan](https://github.com/zhengkid/Dream-RSI) still marks the full
code and reproduction scripts as forthcoming, so that repository is a Project
link. Replay is a simulator of discovery decisions, not hardware simulation;
the analogy to RL does not establish parameter-training RL.

### AReaL-RSI

[October 13 paper](https://arxiv.org/abs/2610.18083),
[§5](https://arxiv.org/html/2610.18083v1): seven explicit KernelBench tasks establish
inclusion. The reference implementation, GPU model and generated language are
not precisely identified. Table 1's speedups therefore remain outside structured
claims rather than being guessed as T0, or reinterpreted as runtime ratios against
Codex-Goal. Failed tasks score zero, and one hour per researcher does not mean
equal whole-system compute. The paper explicitly leaves model weights unchanged.

## Benchmarks and tools, kept separate from agents

- [KernelQuest, September 7](https://www.turing.com/blog/kernelquest-benchmark-ai-agents-triton-kernels):
  100 Triton tasks, compiled baselines and adversarial verification. Added to the
  README's evaluation-integrity pointers, not counted as a generation system.
- [D2K-Bench, October 2](https://arxiv.org/abs/2610.03226): 26 tasks / 85 workloads
  contrasting runs with and without expert design guidance. Benchmark pointer only.
- [KREX](https://arxiv.org/abs/2609.30057): shared-GPU kernel measurement isolation.
  Added as a tool; benchmark throughput is not generated-kernel speedup.
- [Xtrace](https://arxiv.org/abs/2609.28769): binary-instrumentation tracing with
  agent case studies. Added as a tool; tracer instrumentation does not imply
  binary-level optimization by the agent. Public-use claims are not treated as
  an open-source agent or a complete winning artifact.

Linux scheduler work, general coding models without kernel-specific mechanisms,
benchmark-only papers, community reimplementations presented as author code, and
duplicate project names are not added as new generation agents.

## Integrity and maintenance decisions

- Dates follow actual first public code/paper evidence, not arXiv identifier month,
  last revision, repository creation, or later renamed paths.
- Pallas and Helion are additive representation values for explicitly evidenced
  outputs. No taxonomy dimension, architecture, baseline semantics or chart concept
  changes. Empty annotations continue to mean unannotated, never absent.
- KernelOPT/AReaL-RSI and source-inconsistent or incompletely released projects keep
  explicit caveats/review items. Public framework code does not certify K.
- Coverage assertions now derive totals from the catalog instead of hard-coding
  112 systems. The original migration baseline regression remains scoped to the
  preserved v1 ID manifest; new claims do not invalidate that historical check.
- All four SVGs and both READMEs are regenerated. The Timeline remains complete,
  month-grouped and deterministic, without milestone selection.
- Independent review caught ForgeMegakernel's excluded Llama-3.2-1B cell:
  speedup aggregates cover 13 of 14 evaluated cells. This exclusion is retained
  in both structured claims, rather than silently assuming full-suite coverage.
- The renderer preserves iterative `Corr@3` separately from independent
  `pass@k`; it also reads a supplied Pass@k value from the claim qualifier.
- Updated positive coverage is artifact level 126/127, representation 125/127,
  hardware 124/127. New unannotated entries are not populated from names or
  tool brands merely to preserve the previous full-coverage appearance.

## Final verification

- `scripts/validate.py`: 132 entries / 176 claims; all 115 pre-refresh IDs retained.
- `python -m unittest discover -s tests -p 'test_*.py' -v`: 80 tests pass.
- `scripts/generate.py` and `scripts/generate.py --check`: 14 outputs consistent;
  consecutive regeneration produces identical SHA-256 hashes for every output.
- Timeline XML membership equals all 127 Agent IDs; both README catalogs and the
  linked timeline report retain every system.
- `rsvg-convert` previews were inspected at 900px width for Landscape, Field Map
  and Baseline Distribution; the 1200px Timeline was inspected in full-height
  consecutive strips. No text overlap or clipping was observed. No layout or
  structural changes were necessary.
- `git diff --check` passes. Remaining review items total 80 across 70 entries,
  including inherited migration uncertainty; they are not silently resolved by
  this refresh. AlphaCu and KernelOwl remain discovery leads pending adequate
  primary evidence, not catalog facts.
