# Contributing to Awesome Kernel Agent

Thanks for your interest in contributing! This list aims to be the most accurate and useful index of LLM-driven kernel generation work — with **claims-annotated** entries whose evidence posture is verifiable.

## The one rule that changed

**Never edit the generated tables in README.md / README.zh.md.** The single source of truth is [`data/agents.yaml`](data/agents.yaml). Edit it, then run:

```bash
pip install pyyaml
python3 scripts/generate.py          # regenerates README.md, README.zh.md, data/agents.json
python3 scripts/generate.py --check  # validation only (what CI runs)
```

Commit the YAML **and** the regenerated files together.

## What to add

Eligible entries are LLM-driven systems that target **operator-level kernel code** (CUDA / Triton / Ascend C / HIP / TileLang / NKI / SYCL / etc.) for **GPU / NPU / ASIC accelerators**.

**Out of scope**
- General code-generation models without kernel focus (e.g., StarCoder, CodeLlama)
- Compiler-only work without an agent / LLM component (e.g., pure TVM Ansor)
- Inference-engine projects (vLLM, SGLang, TensorRT-LLM) — only their kernel-specific work qualifies
- Benchmarks — those go to [awesome-kernel-benchmark](https://github.com/youyve/awesome-kernel-benchmark)

## Entry schema (`data/agents.yaml`)

```yaml
- id: kevin                    # kebab-case, unique, stable
  name: Kevin
  org: Cognition               # use ' x ' for multiple orgs
  date: "2025-07"              # YYYY-MM, arXiv submission month
  route: C                     # A|B|C|D|E (see README Legend) | tool for non-agent tooling
  status: partial              # open|partial|wip|closed|proprietary
  dsl: CUDA                    # primary DSL — decides the README section
  dsl_also: []                 # other DSLs (rendered as `also:` + cross-listing)
  hardware: [NVIDIA]
  code: https://github.com/...   # >=1 of code/paper required
  paper: https://arxiv.org/abs/2507.11948
  blog: ...                    # optional
  desc: "One line with the key numeric result, reproduced verbatim from the source."
  note: "Honest caveats (repo empty, community reimpl, ...)."   # optional
  # ---- claims-annotation fields (objective; cite or write unknown) ----
  evaluated_on: [KernelBench]  # where the headline number comes from
  claim_baseline: "PyTorch eager (KernelBench)"   # what the speedup is measured AGAINST
  ships_kernels: unknown       # yes|partial|no|unknown — generated kernels public & re-runnable?
  budget_disclosed: yes        # yes|partial|no|unknown — attempts/iterations/compute reported?
```

### Claims-annotation rules (the part we are strict about)

1. **Primary evidence only** — paper, harness code, or repo contents. Never the project's marketing page, never inference.
2. **`unknown` is always acceptable; a guess never is.** A `?` in the rendered list is an invitation for someone to verify, not an embarrassment.
3. `claim_baseline` must name the actual denominator (eager / torch.compile / vendor library / expert reference / SOL ceiling / production incumbent). "Faster than PyTorch" without knowing the mode = `unknown`.
4. `ships_kernels: yes` requires a public artifact containing the *generated* kernels (repo dir, HF dataset, archive) — model weights alone don't count.
5. **Upgrading a `?` to a verified value (with the evidence link in the PR description) is the most valuable contribution this list accepts.**

## Pull request checklist

- [ ] Edited `data/agents.yaml`, not the READMEs
- [ ] `python3 scripts/generate.py --check` passes
- [ ] Regenerated files committed (`generate.py` without `--check`)
- [ ] All links return HTTP 200
- [ ] `status` badge matches actual repo state; `route` justified (cite the paper section)
- [ ] Claims fields follow the rules above (`unknown` over guesses)
- [ ] No marketing language; facts and numbers only

## Reporting issues

Broken link, wrong affiliation, misclassified route/DSL, or a claims field you can verify — open an issue with the entry `id` and a source URL supporting the correction.

## License

By contributing, you agree that catalog-content contributions are licensed under [CC-BY-4.0](./LICENSE) and code contributions under [MIT](./scripts/LICENSE).
