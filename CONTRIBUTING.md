# Contributing to Awesome Kernel Agent

_How to add evidence without weakening the catalog's machine-readable contract._

The v2 catalog treats each system as a multidimensional object and each numerical result as a separate claim. Edit only the source data and templates; never hand-edit generated catalogs, reports, JSON, or SVG files.

## Development workflow

Install the pinned validation dependencies, validate, test, and regenerate:

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate.py
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/generate.py
python3 scripts/generate.py --check
```

Commit the source change and every regenerated output together:

- `README.md` and `README.zh.md`
- `data/agents.json`
- `catalog/*.md`
- `reports/*.md`
- `assets/*.svg`

`--check` is read-only and compares every expected output byte-for-byte. Pull-request CI also regenerates the repository and rejects any resulting diff or untracked output.

## Inclusion boundary

Eligible entries use an LLM or agent to generate, translate, repair, select, or optimize operator-level accelerator kernels. Compiler/agent co-design is in scope when the model makes workload-dependent kernel decisions.

Out of scope:

- General code-generation models without kernel-specific evidence
- Compiler-only work without an LLM or agent decision loop
- Inference engines without kernel-specific agent work
- Standalone benchmarks, which belong in [awesome-kernel-benchmark](https://github.com/youyve/awesome-kernel-benchmark)

## v2 entry schema

The portable schema is [`schema/agents.schema.json`](schema/agents.schema.json); exact controlled values are in [`schema/vocab.yaml`](schema/vocab.yaml). The following example shows the complete shape of an agent entry:

```yaml
- id: example-agent
  name: Example Agent
  organization: Example Lab
  date: "2026-08"
  entry_type: agent
  status: partial
  summary: "Compiler-guided evolutionary optimization for a public CUDA workload."
  caveats:
    - "The numerical result covers selected tasks, not the full benchmark."
  taxonomy:
    policy_adaptation: [prompting]
    generation_mode: [iterative-refinement]
    search_strategy: [evolutionary-search]
    participants: [multi-agent]
    coordination: [role-specialized]
    feedback_signal: [correctness, runtime]
    feedback_source: [compiler, profiler]
    memory: [archive]
    workload_scope: [operator]
    integration_scope: []
    optimization_level: [source]
    optimization_focus: []
  representations: [CUDA]
  hardware: [NVIDIA]
  links:
    paper:
      - label: Paper
        url: https://arxiv.org/abs/0000.00000
        provenance: official
    code:
      - label: Implementation
        url: https://github.com/example/example-agent
        provenance: official
    article: []
    project: []
    artifact:
      - label: Winning kernels
        url: https://github.com/example/example-agent/tree/main/results
        provenance: official
    model: []
    dataset: []
  artifacts:
    implementation:
      status: "yes"
      urls: [https://github.com/example/example-agent]
    generated_kernels:
      status: partial
      urls: [https://github.com/example/example-agent/tree/main/results]
    harness:
      status: unknown
      urls: []
    model_weights:
      status: "no"
      urls: []
    trajectories:
      status: "no"
      urls: []
  claims:
    - id: selected-kernel-speedup
      metric: speedup
      value: 1.14
      unit: x
      aggregation: geometric-mean
      qualifier: selected tasks
      workload:
        benchmark: ExampleBench
        subset: 12 selected operators
      hardware: NVIDIA H100
      scope: operator
      baseline:
        tier: T3
        kind: expert-implementation
        name: Hand-tuned expert kernels
        evidence: null
      budget:
        status: "yes"
        details: 50 candidates per task
      reproducibility:
        claim_linked_artifact: partial
        artifact_url: https://github.com/example/example-agent/tree/main/results
      primary_source:
        url: https://arxiv.org/abs/0000.00000
        locator: Table 3
      caveats:
        - "Geometric mean excludes three unsupported tasks."
  primary_claim: selected-kernel-speedup
  migration_review: []
```

Every taxonomy dimension and typed-link array is required, even when it is empty. Taxonomy lists record positive evidence only: an empty list means unannotated/unknown, not a verified negative. `entry_type: tool` preserves infrastructure entries without presenting them as research agents.

`date` is the first-public-release month. For a paper-only system, use the first public preprint version month; later revisions do not move the system on the Timeline.

## Taxonomy and Representation

Do not add `route`, `dsl`, or `dsl_also`. These are forbidden legacy fields.

- `taxonomy` separates policy adaptation, generation mode, search strategy, participants, coordination, feedback signal, feedback source, retained state, workload scope, integration scope, artifact level, and optimization focus
- `representations` records source or intermediate languages such as CUDA, Triton, CuTe, CAKE IR, PTX, or AMDGPU ISA
- `optimization_level` records the artifact abstraction directly edited or selected, such as source, DSL, custom IR, compiler IR, PTX, assembly, or binary
- `optimization_focus` separately records algorithmic or schedule/mapping decisions
- `feedback_signal` records what outcome is observed; `feedback_source` records the instrument or analysis channel that produced it
- `workload_scope` records kernel-to-system granularity; `integration_scope` records surrounding library/compiler/runtime/serving/communication contexts
- Exact questions, boundaries, group roles, and hierarchy constraints live in `schema/vocab.yaml`; do not infer a tag from a keyword or baseline mention

Representation and optimization level are different facts. For example, an agent may consume Triton while optimizing compiler IR, or emit CUDA containing inline PTX.

README Profile text is automatically compressed from taxonomy; it is not a schema field and must not be added to YAML. The deterministic rule lives in `schema/vocab.yaml#profile_derivation`: for each of the two presentation slots, scan configured dimensions and controlled-vocabulary values after removing implied parents; generic fallback values (`prompting`, `direct`, `single-agent`) are used only when no non-fallback candidate exists, and configured suppressions prevent the second slot from restating the first. Empty evidence renders as `—` and is never filled by inference.

The README Field Map is likewise a presentation layer, not a second taxonomy. `presentation_taxonomy` partitions every detailed facet family exactly once into nine reading dimensions. Validation rejects a missing or duplicated facet; value-level distinctions and reverse links remain in `reports/field-map.md`.

## Claim discipline

One numerical result means one claim and one denominator. Never combine `5.2× vs PyTorch`, `1.8× vs torch.compile`, and `1.13× vs FlashInfer` into one claim.

Preserve qualifiers exactly:

- Use `aggregation` for geometric mean, median, maximum, range, Pass@k, or best-of-N semantics
- Use `qualifier` for facts such as `up to`, `selected tasks`, or protocol-specific restrictions
- Use `workload.subset` for exclusions, task levels, shapes, and evaluation slices
- Use claim `caveats` when the headline needs context that cannot fit those fields
- Use `value: unknown` instead of extracting a number from ambiguous prose

`primary_claim` selects the one claim displayed in README. It must reference a claim ID, and entries with no safely structured numerical result use `claims: []` and `primary_claim: null`.

## Baseline tiers

Tier belongs to the claim, not to a software brand. It captures provenance, specialization, and status; it is not a strict speed ordering.

| Tier | Baseline provenance |
| --- | --- |
| T0 | Reference or framework implementation |
| T1 | General compiler-generated implementation |
| T2 | Optimized generic or vendor library |
| T3 | Specialized expert implementation |
| T4 | Production incumbent |
| T5 | Externally verified, time-specific best-known implementation |
| T6 | Roofline, SOL, or analytical hardware ceiling |
| `unknown` | An implementation baseline exists, but its tier is unresolved |
| `not-applicable` | The implementation-baseline tier model does not apply |

T0–T6 apply only to implementation/performance comparison baselines. Use `unknown` when an implementation denominator exists but its provenance/status cannot be resolved. Use `not-applicable` for no comparison and for non-implementation results such as correctness/pass/compile rates, coverage or win counts, and method ablations. A `prior-agent` or `self-baseline` relationship is not automatically N/A: speed or throughput against an earlier/generated implementation is `unknown` unless T0–T6 can be evidenced. Do not use Unknown to mean “this concept does not apply.” T5 requires `baseline.evidence.url` and an `as_of` date. T6 normally uses `efficiency` or `fraction-of-ceiling`, not an ordinary speedup. A `10×` T0 result is not automatically stronger evidence than a `1.1×` T4 result.

## Artifacts and reproducibility

Project artifacts and claim reproducibility are separate layers:

- `artifacts.generated_kernels` answers whether the project publishes any generated kernels
- `claims[].reproducibility.claim_linked_artifact` answers whether that claim's winning kernel is public

README's `K` badge always uses the second field. A project can publish example kernels while withholding the kernel behind its headline result.

Statuses are `"yes"`, `partial`, `"no"`, or `unknown`. Quote bare `yes` and `no`: PyYAML otherwise interprets them as booleans. A `yes` or `partial` artifact status requires a URL; a claim-linked artifact URL must also appear in the entry's typed links. Use `links.artifact` for a dedicated result/kernel location; a repository URL may remain `links.code` when the same repository is both implementation and artifact.

## Typed links and source quality

Use the correct link type:

- `paper` — archival paper or official preprint
- `code` — implementation source, not a model card or dataset
- `article` — first-party technical article or blog
- `project` — project landing page
- `artifact` — generated kernels, traces, result archive, or claim evidence
- `model` — weights or model card
- `dataset` — training or evaluation data

Set provenance to `official`, `author`, `community`, or `third-party`. Community reimplementations stay visible but are never rendered as official Code. A claim's `primary_source.url` must also appear in that entry's typed links.

## Evidence policy

Use primary evidence in this order: paper and appendices, official repository and artifacts, then first-party engineering articles. Search snippets and third-party summaries are discovery aids, not claim evidence.

Use `unknown` whenever a required fact is genuinely unresolved, and `not-applicable` where that state is explicitly supported by the schema. Do not infer:

- Baseline tier from a product or library name alone
- Hardware from an affiliation or neighboring experiment
- Claim-linked reproducibility from project-level code availability
- Search budget from a default configuration not tied to the reported result
- T5 status without dated external evidence

Record unresolved migration facts in `migration_review` with a precise field path and issue. The generated [migration report](reports/migration-review.md) makes this work queue visible.

## Pull-request checklist

- [ ] Preserved every stable entry ID; no rename for cosmetic reasons
- [ ] Used only values from `schema/vocab.yaml`
- [ ] Added direct Paper, Code, Article, Project, Artifact, Model, and Dataset links under the correct types
- [ ] Split every numerical result by denominator
- [ ] Selected a valid `primary_claim`, or used `null` when no safe numerical claim exists
- [ ] Kept project artifacts separate from claim-linked artifacts
- [ ] Added T5 dated evidence, used `unknown` for an unresolved implementation tier, or used `not-applicable` when tiers do not apply
- [ ] Preserved `up to`, selected-task, Pass@k, and exclusion semantics
- [ ] Ran validation, tests, generation, and `--check`
- [ ] Did not hand-edit generated output

External-link availability is checked by a separate weekly workflow. A temporary website failure never blocks deterministic pull-request validation.

## License

Catalog contributions are licensed under [CC-BY-4.0](LICENSE); code contributions under [MIT](scripts/LICENSE).
