# Contributing to Awesome Kernel Agent

Thanks for helping keep the map current. Every entry lives in one file, [`data/entries.yaml`](data/entries.yaml). `README.md` and `browse/` are generated from it, so do not edit them by hand.

## Workflow

```bash
python3 -m pip install -r requirements-dev.txt
# edit data/entries.yaml
python3 scripts/build_readme.py          # validates the data, then rewrites README.md and browse/
python3 -m unittest discover -s tests -p 'test_*.py'
```

Commit `data/entries.yaml` together with the regenerated `README.md` and `browse/`. CI runs `python3 scripts/build_readme.py --check` and fails if they are out of date.

## What belongs here

In scope: systems that use an LLM or agent to generate, translate, repair, select, or optimize accelerator kernels, plus the benchmarks, studies, and tools built around them. Compiler/agent co-design counts when the model makes workload-dependent kernel decisions. General-purpose agents and code models count when their published evaluation includes kernel tasks.

Out of scope: general code generation without kernel results, compiler-only work without an LLM decision loop, and inference engines without kernel-specific agent work.

## Entry fields

```yaml
- id: example-agent                  # unique; lowercase letters, digits, '.', '-'
  name: ExampleAgent                 # short system name
  title: 'ExampleAgent: Agentic CUDA Kernel Optimization'   # paper title; omit for repositories without a paper
  type: agentic                      # see the type list below
  date: '2026-10-16'                 # first public release: arXiv v1, OpenReview submission, blog post, or repo (YYYY-MM or YYYY-MM-DD)
  venue: ICML 2026                   # only after acceptance; workshops as 'ICML Workshop 2026'
  paper: https://arxiv.org/abs/2610.00000
  code: https://github.com/example/example-agent     # the paper's own code only
  model: https://huggingface.co/example/model        # optional
  dataset: https://huggingface.co/datasets/example/data  # optional
  project: https://example.github.io/agent           # optional
  blog: https://example.com/blog/agent               # optional
  artifacts: https://github.com/example/results      # optional: released kernels, logs, or results
  institution: [Example University, Example Corp]    # as printed on the paper's first page, in author order
  kernel: [CUDA, Triton]             # languages the system writes kernels in; leave out if the paper does not say
  hardware: [NVIDIA, AMD]            # evaluated hardware
  benchmarks: [KernelBench]          # evaluation benchmarks
  summary: One sentence.             # only for entries without a paper title
```

Types: `agentic`, `search`, `trained`, `single-pass`, `industry` (systems without a paper) appear under **Kernel agents**. `benchmark`, `general`, `application`, `tool`, and `study` each have their own section.

Hardware values: NVIDIA, AMD, Ascend, Intel, Google TPU, AWS Neuron, Apple, CPU, RISC-V, Mobile GPU, Meta MTIA, Moore Threads, Cambricon, Tenstorrent, T-Head PPU, Hygon DCU, Cerebras, Research accelerators, Other.

## Rules that keep the list trustworthy

- **Own artifacts only.** Papers often list the benchmark, evaluator, or dataset they used (KernelBench, KernelBook, ...) next to their own code. Link only what the authors released. A test fails when one entry's code link is another entry's repository.
- **Repository root for stars.** A GitHub `code` link to the repository root shows a live star count. Link a sub-directory (`/tree/<branch>/<path>`) when the project lives inside a larger repository; it then shows a plain Code badge, so the parent's stars are not credited to it.
- **Dead repositories.** If a published repository disappears, keep its URL and add `code_status: unavailable`. The entry then shows a grey `Code-unavailable` badge that still links to the published URL.
- **Venue only after acceptance.** Preprints show an arXiv badge, and OpenReview submissions show a grey badge until accepted.
- **Institutions from the paper.** Use institution-level names (no departments), with no commas inside a name. For repositories without a paper, use the affiliation stated on the maintainer's GitHub profile, or leave it out.
- **Kernel languages must be stated.** Do not infer CUDA from "GPU kernels", and do not tag languages that appear only as baselines or background.

## Pull requests

Describe what you added or fixed and link the primary source. One PR per batch of related entries is fine.
