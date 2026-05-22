# Contributing to Awesome Kernel Agent

Thanks for your interest in contributing! This list aims to be the most accurate and useful index of LLM-driven kernel generation work.

## What to add

Eligible entries are LLM-driven systems, papers, datasets, or benchmarks that target **operator-level kernel code** (CUDA / Triton / Ascend C / HIP / TileLang / NKI / SYCL / etc.) for **GPU / NPU / ASIC accelerators**.

**Out of scope**
- General code-generation models without kernel focus (e.g., StarCoder, CodeLlama)
- Compiler-only work without an agent / LLM component (e.g., pure TVM Ansor)
- Inference-engine projects (vLLM, SGLang, TensorRT-LLM) — only their kernel-specific work qualifies

## How to add an entry

### Format

Inside the appropriate `## Agents by Primary DSL > ### <DSL>` section, follow this format:

```markdown
- [Name](code-link) — Team · YYYY-MM · **[Route]** · Open-source status
  Short description (one line).
  Paper: [arXiv:XXXX.XXXXX](https://arxiv.org/abs/XXXX.XXXXX)
  Result: key numerical claim (if applicable).
```

If there is no code link, omit the inline link:

```markdown
- **Name** — Team · YYYY-MM · **[Route]** · Open-source status
  Short description.
  Paper: [arXiv:XXXX.XXXXX](https://arxiv.org/abs/XXXX.XXXXX)
```

### Required fields

| Field | Example | Notes |
|:---|:---|:---|
| Name | `Kevin` | Just the agent/system name |
| Team | `Cognition` or `Stanford × MSR Redmond` | Use `×` for multiple orgs |
| Date | `2026-03` | Year-month; use arXiv submission month |
| Route | `[A]` / `[B]` / `[C]` / `[D]` / `[E]` | See Legend in README |
| Open-source | 🟢 / 🟡 / 🟠 / ⚪ / ⚫ | See Legend in README |
| Paper | arXiv preferred | If no arXiv, use conference link |
| Code | GitHub preferred | HF / project page acceptable |

### Sorting

Within each DSL section, sort by **date (newest first)**. Special families (e.g., QiMeng-*) may be kept contiguous.

### Adding a new DSL section

If an agent's primary DSL is not yet in the README:
1. Add a new `### <DSL>` subsection under `## Agents by Primary DSL`
2. Add the DSL to the TOC
3. Add the DSL to the [DSL Languages](#dsl-languages) section
4. Update the agent count in `### <DSL> (N agents)` headings as you go

## Pull request checklist

- [ ] Entry is added in the correct DSL section
- [ ] Sorted by date (newest first) within the section
- [ ] All links return HTTP 200 (verified by clicking)
- [ ] Open-source badge matches actual repo state
- [ ] Route classification justified (mention which paper section indicates this)
- [ ] Agent counts in section headings updated
- [ ] TOC updated if new DSL section added
- [ ] No marketing language ("best", "revolutionary"); facts and numbers only

## Reporting issues

If you find a broken link, wrong team affiliation, or misclassified DSL, please open an issue with:
- The exact line(s) needing correction
- Source URL supporting the correction (paper section, repo README, official page)

## License

By contributing, you agree that your contributions will be licensed under the [Apache License 2.0](./LICENSE).
