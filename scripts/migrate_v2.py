#!/usr/bin/env python3
"""One-time, auditable migration from the v1 catalog to schema v2.

The script is intentionally conservative: it preserves every stable ID,
turns only explicit evidence into structured claims, and records unresolved
legacy ambiguity on the affected entry.  Running it on an already-v2 file is
a validation-only no-op.

Usage:
    python3 scripts/migrate_v2.py
    python3 scripts/migrate_v2.py --input old.yaml --output migrated.yaml
"""
from __future__ import annotations

import argparse
import copy
import re
from pathlib import Path
from typing import Any

import yaml

try:
    from .lib.loader import load_yaml
    from .lib.validation import validate_catalog
except ImportError:  # Direct execution.
    from lib.loader import load_yaml
    from lib.validation import validate_catalog


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = ROOT / "data" / "agents.yaml"
ID_SNAPSHOT = ROOT / "schema" / "v1-entry-ids.txt"
RESEARCH_CUTOFF = "2026-08-25"

STATUSES = {"yes", "partial", "no", "unknown"}

def read_expected_ids() -> list[str]:
    return [
        line.strip()
        for line in ID_SNAPSHOT.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]


def status(value: Any) -> str:
    """Undo YAML 1.1's bare yes/no boolean coercion."""
    if isinstance(value, bool):
        return "yes" if value else "no"
    value = str(value)
    return value if value in STATUSES else "unknown"


def ordered_unique(values: list[str]) -> list[str]:
    result: list[str] = []
    for value in values:
        if value and value not in result:
            result.append(value)
    return result


def split_taxonomy(legacy: dict[str, list[str]]) -> dict[str, list[str]]:
    """Losslessly split the original v2 facet families by semantic question."""

    generation = {"direct", "iterative-refinement"}
    participants = {"single-agent", "multi-agent", "human-in-the-loop", "agent-compiler"}
    signals = {"correctness", "runtime", "model-level"}
    workload = {"operator", "fusion", "graph", "model", "system"}
    focus = {"schedule", "algorithm"}
    return {
        "policy_adaptation": list(legacy["learning"]),
        "generation_mode": [value for value in legacy["search"] if value in generation],
        "search_strategy": [value for value in legacy["search"] if value not in generation],
        "participants": [
            "compiler-in-the-loop" if value == "agent-compiler" else value
            for value in legacy["orchestration"]
            if value in participants
        ],
        "coordination": [
            value for value in legacy["orchestration"] if value not in participants
        ],
        "feedback_signal": [value for value in legacy["feedback"] if value in signals],
        "feedback_source": [value for value in legacy["feedback"] if value not in signals],
        "memory": list(legacy["memory"]),
        "workload_scope": [value for value in legacy["scope"] if value in workload],
        "integration_scope": [value for value in legacy["scope"] if value not in workload],
        "optimization_level": [
            value for value in legacy["optimization_level"] if value not in focus
        ],
        "optimization_focus": [
            value for value in legacy["optimization_level"] if value in focus
        ],
    }


REPRESENTATION_MAP = {
    "AMDGCN": "AMDGPU ISA",
    "CAKE-IR": "CAKE IR",
    "AscendC": "Ascend C",
    "MUSA": "MUSA C",
    "CK": "Composable Kernel",
    "JAX-TPU": "JAX",
    "Triton-FlashInfer": "Triton",
    "PPU": None,  # hardware family, not a programming representation
}

REPRESENTATION_REVIEWS = {
    "alphaevolve-fhe": (
        "representations",
        "v1 conflated JAX with the TPU backend as JAX-TPU; migrated to JAX only.",
    ),
    "auto-gpu-kernel": (
        "representations",
        "v1 used the compound label Triton-FlashInfer; migrated to Triton because FlashInfer is a library/benchmark context, not a representation.",
    ),
    "qwen3.7-max-kernel-opt": (
        "representations",
        "v1 used PPU as a DSL; PPU is hardware, so only the explicitly listed Triton representation was retained.",
    ),
}


def migrate_representations(old: dict[str, Any]) -> list[str]:
    result: list[str] = []
    for raw in [old.get("dsl"), *(old.get("dsl_also") or [])]:
        mapped = REPRESENTATION_MAP.get(raw, raw)
        if mapped:
            result.append(mapped)
    additions = {
        "ako4x": ["CuTe"],
        "kernelpro": ["CuTe"],
        "cursor-nvidia-multi-agent-kernels": ["CuTe", "PTX"],
    }
    if old["id"] == "cutegen":
        result = [value for value in result if value != "CUTLASS"]
        result.append("CuTe")
    return ordered_unique([*result, *additions.get(old["id"], [])])


def taxonomy(old: dict[str, Any], representations: list[str]) -> dict[str, list[str]]:
    """Conservative text-supported seed taxonomy; route is only a weak clue."""
    text = " ".join(
        str(old.get(key, "")) for key in ("name", "desc", "note")
    ).lower()
    result: dict[str, list[str]] = {
        "learning": [],
        "search": [],
        "orchestration": [],
        "feedback": [],
        "memory": [],
        "scope": [],
        "optimization_level": [],
    }

    def add(dimension: str, value: str, condition: bool) -> None:
        if condition and value not in result[dimension]:
            result[dimension].append(value)

    add("learning", "agentic-reinforcement-learning", "agentic rl" in text)
    add(
        "learning",
        "reinforcement-learning",
        bool(re.search(r"\b(?:rl|grpo|ppo|reinforce|rlef)\b|reinforcement", text)),
    )
    add(
        "learning",
        "supervised-fine-tuning",
        bool(re.search(r"\bsft\b|fine-tun", text)),
    )
    add("learning", "in-context-learning", "in-context" in text)
    add("learning", "self-training", "self-training" in text)
    add("learning", "distillation", "distill" in text)
    add("learning", "continual-learning", "continual learning" in text)
    add("learning", "prompting", "prompt" in text and not result["learning"])

    add("search", "mcts", "mcts" in text)
    add("search", "map-elites", "map-elites" in text)
    add("search", "quality-diversity", "quality-diversity" in text)
    add("search", "evolutionary-search", "evolution" in text)
    if "map-elites" in result["search"]:
        add("search", "quality-diversity", True)
        add("search", "evolutionary-search", True)
    add("search", "beam-search", "beam search" in text)
    add("search", "best-of-n", "best-of" in text)
    add("search", "autotuning", "auto-tun" in text or "autotun" in text)
    add("search", "portfolio-search", "portfolio" in text)
    add("search", "local-search", "local search" in text)
    add(
        "search",
        "iterative-refinement",
        old.get("route") == "B"
        or bool(re.search(r"iterative|closed.loop|refin(?:e|ement)|keep/revert", text)),
    )
    add("search", "direct", old.get("route") == "A")

    multi = bool(
        re.search(r"multi-agent|two-agent|three-agent|four-agent|5-agent|five-agent", text)
    )
    add("orchestration", "multi-agent", multi)
    add("orchestration", "hierarchical", "hierarch" in text)
    add(
        "orchestration",
        "role-specialized",
        multi and bool(re.search(r"planner|coder|judge|profiler|verifier|agent \(", text)),
    )
    add("orchestration", "planner-worker", "planner" in text and "worker" in text)
    add("orchestration", "parallel", "parallel" in text)
    add("orchestration", "human-in-the-loop", "human-orchestr" in text or "human-guided" in text)
    add("orchestration", "agent-compiler", "compiler-agent" in text or "agentic compiler" in text)
    add("orchestration", "single-agent", "single llm agent" in text)

    add("feedback", "compiler", bool(re.search(r"compiler|compile|nvcc", text)))
    add("feedback", "correctness", bool(re.search(r"correctness|verif|test|gate", text)))
    add("feedback", "runtime", bool(re.search(r"runtime|benchmark|speed|latency|throughput|timing", text)))
    add("feedback", "profiler", bool(re.search(r"profil|\bncu\b|nsys|rocprof", text)))
    add("feedback", "hardware-counters", bool(re.search(r"\bncu\b|nsys|rocprof|hardware counter", text)))
    add("feedback", "roofline", "roofline" in text or "speed-of-light" in text or "sol ceiling" in text)
    add("feedback", "ir", bool(re.search(r"\bir\b|sass", text)))
    add("feedback", "simulator", "simulat" in text or "cannsim" in text)
    add("feedback", "formal-verification", "formal" in text or "smt" in text)
    add("feedback", "differential-testing", "differential" in text)
    add("feedback", "model-level", "model-level" in text or "revalidates the model" in text)

    add("memory", "trajectory", "trajectory memory" in text)
    add("memory", "reflection", "reflect" in text)
    add("memory", "retrieval", "retriev" in text or "rag" in text)
    add("memory", "skill-library", "skill" in text)
    add("memory", "archive", "memory archive" in text or "search archive" in text)
    add("memory", "episodic", "episod" in text)
    add("memory", "cross-run", "cross-run" in text)
    add("memory", "population", "population" in text)

    add("scope", "fusion", bool(re.search(r"\b(?:fusion|fused)\b", text)))
    add("scope", "graph", "graph" in text or "megakernel" in text)
    add("scope", "model", "model" in text or "end-to-end" in text)
    add("scope", "serving", "serving" in text or "sglang" in text or "vllm" in text)
    add("scope", "runtime", "runtime" in text)
    add("scope", "library", "library" in text)
    add("scope", "compiler", "compiler" in text)
    add("scope", "communication", "communication" in text or "collective" in text)
    add("scope", "distributed", "multi-gpu" in text or "distributed" in text)
    add("scope", "system", "system-level" in text or "whole" in text)

    source_reps = {"CUDA", "HIP", "Ascend C", "MUSA C", "SYCL", "Metal"}
    dsl_reps = {
        "Triton", "CUTLASS", "CuTe", "TileLang", "NKI", "FlyDSL", "Composable Kernel", "Catlass",
        "Gluon", "PyPTO", "TAIDL", "TT-Lang", "cuTile", "JAX",
    }
    add("optimization_level", "source", bool(set(representations) & source_reps))
    add("optimization_level", "dsl", bool(set(representations) & dsl_reps))
    add("optimization_level", "custom-ir", "CAKE IR" in representations or "ACT" in representations)
    add("optimization_level", "ptx", "PTX" in representations)
    # Compiler/IR diagnosis is feedback evidence, not proof that the agent edits
    # or selects a compiler-IR artifact.
    # Assembly baselines in prose do not imply that the agent edits assembly.
    add("optimization_level", "assembly", "AMDGPU ISA" in representations)
    add("optimization_level", "binary", "machine code" in text or "code object" in text or "binar" in text)
    add("optimization_level", "schedule", "schedule" in text or "mapping decisions" in text)
    add("optimization_level", "algorithm", "algorithmic" in text or "algorithm" in text)

    # Negated prose and paper titles need explicit, evidence-backed handling;
    # these overrides prevent keyword extraction from reversing their meaning.
    if old["id"] == "kernel-design-agents":
        result["orchestration"] = ["single-agent"]
    elif old["id"] == "kernelarc":
        result["search"] = ordered_unique([*result["search"], "portfolio-search"])
        result["orchestration"] = ["multi-agent", "role-specialized", "parallel"]
    if old["id"] == "amd-apex":
        result["learning"] = []
    if old["id"] == "asmevo":
        result["search"] = ["iterative-refinement"]
        result["feedback"] = [
            value for value in result["feedback"] if value != "formal-verification"
        ]
        result["feedback"] = ordered_unique([*result["feedback"], "profiler"])
    if old["id"] == "dice":
        result["search"] = ["direct"]
    if old["id"] == "cuda-opt-agent":
        result["scope"] = ["operator"]
    if old["id"] == "agenticcann":
        result["feedback"] = [
            value for value in result["feedback"] if value != "model-level"
        ]
        result["scope"] = [value for value in result["scope"] if value != "model"]
    if old["id"] == "kernel-forge":
        result["scope"] = [value for value in result["scope"] if value != "model"]
    taxonomy_additions = {
        "k-search": {"search": ["evolutionary-search"]},
        "cudanalyst": {"search": ["evolutionary-search"]},
        "cudaforge": {
            "search": ["iterative-refinement"],
            "orchestration": ["multi-agent", "role-specialized"],
        },
        "davinci-kernel": {
            "search": ["iterative-refinement"],
            "orchestration": ["multi-agent", "role-specialized"],
        },
        "evokernel": {
            "search": ["iterative-refinement"],
            "memory": ["cross-run"],
        },
        "accelopt": {"search": ["iterative-refinement"]},
    }
    for dimension, values in taxonomy_additions.get(old["id"], {}).items():
        result[dimension] = ordered_unique([*result[dimension], *values])
    scope_overrides = {
        "tritorx": ["library"],
        "forgestencil": ["system"],
        "leap-kernel-rl": ["system"],
        "agentcompile": ["system"],
        "kernelevolve": ["serving"],
        "stitchcuda": ["system"],
        "cuco": ["system"],
        "fact": ["model"],
        "geak-v4": ["serving"],
        "amd-apex": ["communication"],
    }
    result["scope"] = ordered_unique(
        [*result["scope"], *scope_overrides.get(old["id"], [])]
    )
    false_model_scope = {
        "dr-kernel", "autotriton", "forgestencil", "ptxbench-miniptxagent",
        "specgen", "incoder-32b", "cuda-agent", "k-search",
        "cursor-nvidia-multi-agent-kernels", "stitchcuda", "davinci-kernel",
        "atrex-kernel-agent", "hawk-npu", "cake", "musacoder",
    }
    if old["id"] in false_model_scope:
        result["scope"] = [value for value in result["scope"] if value != "model"]
    if old["id"] in {"hiera", "kernelevolve"}:
        result["scope"] = [value for value in result["scope"] if value != "library"]
    if old["id"] == "leap-kernel-rl":
        result["scope"] = [
            value for value in result["scope"] if value != "compiler"
        ]
    if old["id"] == "agentcompile":
        result["scope"] = [value for value in result["scope"] if value != "runtime"]
    if old["id"] == "cutegen":
        result["optimization_level"] = [
            value for value in result["optimization_level"] if value != "schedule"
        ]
    return split_taxonomy(result)


LINK_KEYS = ("paper", "code", "article", "project", "artifact", "model", "dataset")

LINK_RECLASSIFY = {
    "concur": ("model", "Model"),
    "kernelllm": ("model", "Model"),
    "cudamaster": ("project", "Project page"),
    "cuda-agent": ("project", "Project page"),
    "ai-cuda-engineer": ("dataset", "Dataset"),
    "evokernel": ("project", "Project page"),
    "ascendkernelgen": ("dataset", "Dataset"),
    "musacoder": ("model", "Model"),
    "avo": ("project", "Community reimplementation"),
    "cake": ("artifact", "Upstream artifact tracker"),
    "cupilot": ("artifact", "Generated kernel outputs"),
    "cursor-nvidia-multi-agent-kernels": ("artifact", "Generated kernel results"),
}

BLOG_TO_PROJECT = {"ako", "kernelgen-flagos"}


def migrate_links(old: dict[str, Any]) -> dict[str, list[dict[str, str]]]:
    links = {key: [] for key in LINK_KEYS}
    if old.get("paper"):
        if old["id"] == "cuda-agent":
            links["paper"].append(
                {
                    "label": "Paper",
                    "url": "https://arxiv.org/abs/2602.24286",
                    "provenance": "author",
                }
            )
        else:
            links["paper"].append(
                {"label": "Paper", "url": old["paper"], "provenance": "author"}
            )
    if old.get("code"):
        target, label = LINK_RECLASSIFY.get(old["id"], ("code", "Code"))
        provenance = "community" if old["id"] == "avo" else "official"
        links[target].append(
            {"label": label, "url": old["code"], "provenance": provenance}
        )
    if old.get("blog"):
        target = "project" if old["id"] in BLOG_TO_PROJECT else "article"
        label = "Project page" if target == "project" else "Article"
        links[target].append(
            {"label": label, "url": old["blog"], "provenance": "official"}
        )
    if old["id"] == "cuda-agent" and old.get("paper"):
        links["project"].append(
            {
                "label": "Hugging Face paper page",
                "url": old["paper"],
                "provenance": "third-party",
            }
        )
    if old["id"] == "houmao-agentic-kernel-optimization":
        links["artifact"].append(
            {
                "label": "Accepted CUDA kernels",
                "url": "https://github.com/CodeGandee/flashinfer-bench-starter-kit/tree/main/solution/cuda",
                "provenance": "author",
            }
        )
    if old["id"] == "cuda-agent":
        links["code"].append(
            {
                "label": "Agent environment",
                "url": "https://github.com/BytedTsinghua-SIA/CUDA-Agent",
                "provenance": "official",
            }
        )
        links["dataset"].append(
            {
                "label": "CUDA-Agent-Ops-6K",
                "url": "https://huggingface.co/datasets/BytedTsinghua-SIA/CUDA-Agent-Ops-6K",
                "provenance": "official",
            }
        )
    if old["id"] == "kernelpro" and old.get("paper"):
        links["artifact"].append(
            {
                "label": "Appendix H kernel artifact",
                "url": old["paper"],
                "provenance": "author",
            }
        )
    return links


def first_url(links: dict[str, list[dict[str, str]]], *kinds: str) -> str | None:
    for kind in kinds:
        if links[kind]:
            return links[kind][0]["url"]
    return None


def migrate_artifacts(old: dict[str, Any], links: dict[str, list[dict[str, str]]]) -> dict[str, dict[str, Any]]:
    code_url = first_url(links, "code")
    generated = status(old.get("ships_kernels", "unknown"))
    generated_url = first_url(links, "artifact", "code", "dataset") if generated in {"yes", "partial"} else None
    artifacts = {
        "implementation": {"status": "yes" if code_url else "unknown", "urls": [code_url] if code_url else []},
        "generated_kernels": {"status": generated, "urls": [generated_url] if generated_url else []},
        "harness": {"status": "unknown", "urls": []},
        "model_weights": {"status": "yes" if links["model"] else "unknown", "urls": [x["url"] for x in links["model"]]},
        "trajectories": {"status": "unknown", "urls": []},
    }
    text = f"{old.get('desc', '')} {old.get('note', '')}".lower()
    if code_url and "harness" in text:
        artifacts["harness"] = {"status": "yes", "urls": [code_url]}
    if old["id"] in {"kernelpilot", "llm-cuda-harness-engineering"} and code_url:
        artifacts["trajectories"] = {"status": "yes", "urls": [code_url]}
    if old["id"] == "ptxbench-miniptxagent" and code_url:
        artifacts["trajectories"] = {"status": "partial", "urls": [code_url]}
    if old["id"] in {"dice", "davinci-kernel"} and code_url:
        artifacts["model_weights"] = {"status": "yes", "urls": [code_url]}
    if old["id"] == "tileops":
        # This is project-level library content, not a claim-linked artifact.
        artifacts["generated_kernels"] = {"status": "yes", "urls": [code_url] if code_url else []}
    if old["id"] == "cuda-agent" and code_url:
        artifacts["implementation"] = {"status": "partial", "urls": [code_url]}
        artifacts["harness"] = {"status": "partial", "urls": [code_url]}
    return artifacts


def spec(
    metric: str,
    value: float | int | dict[str, float],
    unit: str,
    aggregation: str,
    benchmark: str,
    subset: str,
    hardware: str,
    scope: str,
    tier: str,
    kind: str,
    baseline: str,
    qualifier: str = "",
    caveats: tuple[str, ...] = (),
) -> dict[str, Any]:
    return {
        "metric": metric,
        "value": value,
        "unit": unit,
        "aggregation": aggregation,
        "qualifier": qualifier,
        "workload": {"benchmark": benchmark, "subset": subset},
        "hardware": hardware,
        "scope": scope,
        "baseline": {"tier": tier, "kind": kind, "name": baseline},
        "caveats": list(caveats),
    }


# Values below come only from the existing v1 row and its evidence audit.  A
# row absent from this map intentionally receives no claim rather than a guess.
CLAIM_SPECS: dict[str, list[dict[str, Any]]] = {
    "llm4llm": [
        spec("speedup", 3.91, "x", "geometric-mean", "Language-model inference workloads", "10 workloads", "NVIDIA A100", "model", "T0", "framework-reference", "PyTorch eager"),
        spec("speedup", 6.98, "x", "geometric-mean", "Language-model inference workloads", "10 workloads", "NVIDIA H100", "model", "T0", "framework-reference", "PyTorch eager"),
        spec("speedup", 2.745, "x", "geometric-mean", "KernelBench", "Level 2", "NVIDIA A100", "operator", "T0", "framework-reference", "PyTorch eager"),
        spec("speedup", 2.628, "x", "geometric-mean", "KernelBench", "Level 2", "NVIDIA H100", "operator", "T0", "framework-reference", "PyTorch eager"),
    ],
    "compiler-grounded-hierarchical-diagnosis": [
        spec("speedup", 4.35, "x", "geometric-mean", "NPUKernelBench-derived suite", "37 successfully converted operators", "Ascend 950", "operator", "unknown", "self-baseline", "validated initial Triton kernel", caveats=("Failed AI conversions were excluded.",)),
        spec("speedup", 2.60, "x", "geometric-mean", "NPUKernelBench-derived suite", "37 successfully converted operators", "Ascend 950", "operator", "T0", "framework-reference", "Torch NPU"),
    ],
    "kernelpilot": [
        spec("speedup", 2.7499, "x", "unknown", "SGLang diffusion operator workloads", "fuse_scale_shift", "NVIDIA B200", "operator", "T4", "production-incumbent", "copied SGLang production baseline"),
        spec("speedup", 2.3118, "x", "unknown", "SGLang diffusion operator workloads", "group_norm_silu", "NVIDIA B200", "operator", "T4", "production-incumbent", "copied SGLang production baseline"),
    ],
    "drtriton": [
        spec("win-rate", 92, "percent", "unknown", "KernelBench", "Level 2; Fast_1 threshold", "NVIDIA GPU (model not specified in v1)", "operator", "T0", "framework-reference", "PyTorch eager", "Fraction of tasks exceeding the Fast_1 threshold; GPT-5.2 is reported at 23% under the same protocol."),
    ],
    "pytorch-kernelagent": [
        spec("fraction-of-ceiling", 89, "percent", "unknown", "KernelBench", "Level 1 (100 tasks)", "NVIDIA H100", "operator", "T6", "hardware-ceiling", "roofline"),
        spec("speedup", 1.56, "x", "unknown", "KernelBench", "Level 1 (100 tasks)", "NVIDIA H100", "operator", "T1", "compiler-generated", "torch.compile"),
    ],
    "ako": [
        spec("win-rate", 10, "count", "total", "SOL-ExecBench", "13 kernels", "NVIDIA GPU", "operator", "unknown", "prior-agent", "SOL-ExecBench agent-optimized NVIDIA baseline", "10 of 13 kernels beat the baseline."),
    ],
    "akg-agent": [
        spec("pass-rate", 100, "percent", "pass-at-k", "KernelBench", "Level 1, Triton-CUDA, pass@4", "NVIDIA GPU", "operator", "T0", "framework-reference", "PyTorch reference"),
        spec("speedup", 1.46, "x", "geometric-mean", "KernelBench", "Triton-Ascend", "Ascend NPU", "operator", "T0", "framework-reference", "PyTorch eager"),
    ],
    "tritorx": [
        spec("coverage", 481, "count", "total", "PyTorch OpInfo", "ATen operators", "MTIA", "library", "unknown", "none", "no comparative performance baseline", "481 generated ATen operators pass the reported test suite."),
        spec("count", 20000, "count", "total", "PyTorch OpInfo", "tests passed", "MTIA", "library", "unknown", "none", "no comparative performance baseline"),
    ],
    "kernelfalcon": [
        spec("correctness", 100, "percent", "total", "KernelBench", "all 250 Level 1/2/3 tasks", "NVIDIA GPU", "operator", "unknown", "none", "no comparative performance baseline"),
    ],
    "geak": [
        spec("speedup", 2.59, "x", "unknown", "TritonBench-revised plus ROCm kernels", "184 TritonBench-revised and 30 ROCm kernels", "AMD MI300X", "operator", "T3", "expert-implementation", "expert reference kernels"),
    ],
    "ako4x": [
        spec("speedup", 30.71, "x", "maximum", "MLSys 2026 FlashInfer contest", "DSA sparse-attention kernels", "NVIDIA B200", "operator", "T3", "expert-implementation", "FlashInfer expert kernel"),
        spec("speedup", 1.0, "x", "single", "MLSys 2026 FlashInfer contest", "GEMM", "NVIDIA B200", "operator", "T2", "vendor-library", "cuBLAS", "cuBLAS was not beaten."),
    ],
    "moe-kernel-agent": [
        spec("speedup", 25.7, "x", "median", "MLSys 2026 FlashInfer AI Kernel Generation Contest", "MoE Track", "NVIDIA B200", "operator", "T0", "framework-reference", "PyTorch reference implementation"),
    ],
    "forgestencil": [
        spec("speedup", 1.41, "x", "median", "ForgeStencil application suite", "100 A100-validated scientific/industrial applications", "NVIDIA A100", "system", "T4", "production-incumbent", "each application's production GPU path", caveats=("May include launch, fusion, and host-side restructuring.",)),
        spec("speedup", 2.05, "x", "geometric-mean", "ForgeStencil application suite", "100 A100-validated scientific/industrial applications", "NVIDIA A100", "system", "T4", "production-incumbent", "each application's production GPU path", caveats=("May include launch, fusion, and host-side restructuring.",)),
    ],
    "hiera": [
        spec("pass-rate", 92.4, "percent", "unknown", "KernelBench", "250 tasks; Fast_0; 18 candidates", "NVIDIA A100", "operator", "T0", "framework-reference", "PyTorch reference"),
        spec("pass-rate", 60.4, "percent", "unknown", "KernelBench", "250 tasks; Fast_1; 18 candidates", "NVIDIA A100", "operator", "T0", "framework-reference", "PyTorch reference"),
    ],
    "sparse-ditto": [
        spec("speedup", 2.68, "x", "geometric-mean", "SuiteSparse", "60 matrices across SpMV, SpMM and SpGEMM", "NVIDIA RTX PRO 6000", "operator", "T2", "vendor-library", "fastest applicable cuSPARSE path", caveats=("Preprocessing is excluded; seven out-of-resource SpGEMM cases are omitted.",)),
        spec("speedup", 2.79, "x", "geometric-mean", "SuiteSparse", "60 matrices across SpMV, SpMM and SpGEMM", "NVIDIA H200", "operator", "T2", "vendor-library", "fastest applicable cuSPARSE path", caveats=("Preprocessing is excluded; seven out-of-resource SpGEMM cases are omitted.",)),
    ],
    "leap-kernel-rl": [
        spec("pass-rate", 80.8, "percent", "unknown", "KernelBench", "turn 3", "NVIDIA GPU", "operator", "unknown", "ablation", "first-turn pass rate of 70.0%", "Correctness, not kernel speedup."),
        spec("throughput", 1.93, "x", "unknown", "LEAP training study", "multi-turn RL training", "NVIDIA GPU", "system", "unknown", "ablation", "unpruned multi-turn GRPO training", "Training throughput, not generated-kernel speedup."),
    ],
    "cudaperf": [
        spec("pass-rate", 93, "percent", "pass-at-k", "KernelBench", "pass@5", "NVIDIA GPU", "operator", "unknown", "none", "no comparative denominator", "CUDA Agent reports 86% under the comparison protocol."),
        spec("speedup", 6.41, "x", "geometric-mean", "KernelBench", "pass@5", "NVIDIA GPU", "operator", "T0", "framework-reference", "PyTorch reference", "CUDA Agent reports 3.09x under the comparison protocol."),
    ],
    "llm-cuda-harness-engineering": [
        spec("speedup", value, "x", "single", "MLSys 2026 FlashInfer contest", task, "NVIDIA B200", "operator", "T3", "expert-implementation", "supplied FlashInfer contest baseline")
        for task, value in zip(("task 1", "task 2", "task 3", "task 4", "task 5"), (1.62, 18.05, 29.68, 1.12, 13.70))
    ],
    "agentcompile": [
        spec("speedup", {"min": 2.23, "max": 6.98}, "x", "range", "AgentCompile model suite", "six model families; single-request inference", "NVIDIA GPU", "system", "T0", "framework-reference", "PyTorch eager", caveats=("Includes custom runtime, KV-cache design, and CUDA Graphs.",)),
        spec("speedup", {"min": 1.04, "max": 1.16}, "x", "range", "AgentCompile model suite", "six model families", "NVIDIA GPU", "system", "unknown", "production-incumbent", "vLLM", caveats=("Production-incumbent status was not independently verified in v1; tier left unknown.",)),
    ],
    "kernel-forge": [
        spec("speedup", 2.83, "x", "maximum", "Kernel Forge captured-operator suite", "14 captured operators", "NVIDIA GB10", "operator", "T0", "framework-reference", "PyTorch eager", caveats=("Operator-level, not end-to-end model performance.",)),
    ],
    "houmao-agentic-kernel-optimization": [
        spec("speedup", 1.71, "x", "single", "MLSys 2026 FlashInfer contest", "Fused MoE", "NVIDIA B200", "operator", "T3", "expert-implementation", "supplied FlashInfer contest baseline", caveats=("Human-orchestrated campaign.",)),
        spec("speedup", 92.68, "x", "single", "MLSys 2026 FlashInfer contest", "Fused MoE", "NVIDIA B200", "operator", "T0", "framework-reference", "PyTorch reference", caveats=("Weak framework denominator; not comparable to the 1.71x FlashInfer claim.",)),
        spec("speedup", 1101.02, "x", "single", "MLSys 2026 FlashInfer contest", "DSA TopK Indexer", "NVIDIA B200", "operator", "T0", "framework-reference", "PyTorch reference", caveats=("Weak framework denominator; not an expert-kernel comparison.",)),
        spec("speedup", 181.35, "x", "single", "MLSys 2026 FlashInfer contest", "DSA Sparse Attention", "NVIDIA B200", "operator", "T0", "framework-reference", "PyTorch reference", caveats=("Weak framework denominator; not an expert-kernel comparison.",)),
    ],
    "avo": [
        spec("speedup", 3.5, "percent", "single", "B200 MHA workloads", "seven-day autonomous evolution", "NVIDIA B200", "operator", "T2", "vendor-library", "cuDNN", "Reported as +3.5% over the baseline."),
        spec("speedup", 10.5, "percent", "single", "B200 MHA workloads", "seven-day autonomous evolution", "NVIDIA B200", "operator", "T3", "expert-implementation", "FlashAttention-4", "Reported as +10.5% over the baseline."),
    ],
    "autokernel": [
        spec("speedup", 5.29, "x", "single", "AutoKernel H100 suite", "RMSNorm 8192x8192", "NVIDIA H100", "operator", "T0", "framework-reference", "PyTorch eager"),
        spec("speedup", 2.83, "x", "single", "AutoKernel H100 suite", "RMSNorm 8192x8192", "NVIDIA H100", "operator", "T1", "compiler-generated", "torch.compile"),
    ],
    "kernelskill": [
        spec("speedup", value, "x", "unknown", "KernelBench", level, "NVIDIA GPU", "operator", "T0", "framework-reference", "PyTorch eager")
        for level, value in (("Level 1", 5.44), ("Level 2", 2.82), ("Level 3", 1.92))
    ],
    "cuda-agent": [
        spec("speedup", 2.11, "x", "geometric-mean", "KernelBench", "all reported tasks", "NVIDIA GPU", "operator", "T1", "compiler-generated", "torch.compile"),
        spec("speedup", 2.60, "x", "geometric-mean", "KernelBench", "all reported tasks", "NVIDIA GPU", "operator", "T0", "framework-reference", "PyTorch eager", "Overall KernelBench result."),
        spec("speedup", 1.52, "x", "geometric-mean", "KernelBench", "Level 3", "NVIDIA GPU", "operator", "T1", "compiler-generated", "torch.compile", "KernelBench Level 3 result."),
        spec("speedup", 1.80, "x", "geometric-mean", "KernelBench", "Level 3", "NVIDIA GPU", "operator", "T0", "framework-reference", "PyTorch eager", "KernelBench Level 3 result."),
    ],
    "kernelevolve": [
        spec("throughput", 60, "percent", "unknown", "Andromeda production workloads", "NVIDIA deployment", "NVIDIA GPU", "serving", "T4", "production-incumbent", "internal production kernel", "Reported as a 60% throughput gain over the baseline."),
        spec("throughput", 25, "percent", "unknown", "Andromeda production workloads", "MTIA deployment", "MTIA", "serving", "T4", "production-incumbent", "internal production kernel", "Reported as a 25% throughput gain over the baseline."),
        spec("speedup", 17, "x", "maximum", "Andromeda production workloads", "best reported case", "accelerator not specified in v1", "serving", "T4", "production-incumbent", "internal production kernel"),
        spec("correctness", 100, "percent", "unknown", "KernelBench", "reported suite", "NVIDIA GPU", "operator", "unknown", "none", "no comparative performance baseline"),
    ],
    "kforge": [
        spec("throughput", 2.12, "percent", "unknown", "gpt-oss-20b", "end-to-end", "NVIDIA B200", "model", "unknown", "production-incumbent", "TensorRT-LLM 1.3.0rc9", "Reported as a 2.12% throughput improvement over the baseline.", caveats=("Tier remains unknown because deployment status was not established in v1.",)),
        spec("speedup", 5.13, "x", "geometric-mean", "KernelBench", "37 Level-2 GEMM-tail tasks", "Intel Arc B580", "operator", "T1", "compiler-generated", "faster of PyTorch eager and torch.compile", caveats=("Operator result, not the end-to-end B200 result.",)),
    ],
    "evoengineer": [
        spec("speedup", 2.72, "x", "median", "KernelBench", "reported suite", "NVIDIA GPU", "operator", "T0", "framework-reference", "PyTorch eager"),
        spec("speedup", 36.75, "x", "maximum", "KernelBench", "best reported task", "NVIDIA GPU", "operator", "T0", "framework-reference", "PyTorch eager"),
    ],
    "astra": [
        spec("speedup", 1.32, "x", "arithmetic-mean", "SGLang kernels", "zero-shot", "NVIDIA GPU", "serving", "T4", "production-incumbent", "SGLang incumbent kernels"),
    ],
    "kevin": [
        spec("correctness", 82, "percent", "unknown", "KernelBench", "after GRPO; before value 56%", "NVIDIA GPU", "operator", "unknown", "ablation", "pre-GRPO model"),
        spec("speedup", 1.10, "x", "unknown", "KernelBench", "after GRPO; before value 0.53x", "NVIDIA GPU", "operator", "T0", "framework-reference", "PyTorch eager"),
    ],
    "cuda-l1": [
        spec("speedup", 3.12, "x", "arithmetic-mean", "KernelBench", "reported suite", "NVIDIA A100", "operator", "T0", "framework-reference", "PyTorch eager"),
        spec("speedup", 120, "x", "maximum", "KernelBench", "best reported task", "NVIDIA A100", "operator", "T0", "framework-reference", "PyTorch eager"),
    ],
    "qimeng-xpiler": [
        spec("accuracy", 95, "percent", "unknown", "QiMeng-Xpiler transpilation suite", "four backends", "multiple accelerators", "compiler", "unknown", "none", "no comparative denominator", "Approximate translation accuracy."),
        spec("speedup", 2.0, "x", "maximum", "QiMeng-Xpiler transpilation suite", "best reported case", "multiple accelerators", "operator", "T2", "vendor-library", "vendor library"),
    ],
    "qimeng-tensorop": [
        spec("throughput", 251, "percent", "single", "GEMM/tensor-op suite", "RISC-V", "RISC-V", "operator", "T2", "vendor-library", "OpenBLAS", "Preserved verbatim as 251% of OpenBLAS; not interpreted as percentage gain."),
        spec("throughput", 124, "percent", "single", "GEMM/tensor-op suite", "NVIDIA", "NVIDIA GPU", "operator", "T2", "vendor-library", "cuBLAS", "Preserved verbatim as 124% of cuBLAS; not interpreted as percentage gain."),
    ],
    "qimeng-attention": [
        spec("speedup", 2.15, "x", "single", "attention workloads", "MLA", "NVIDIA A100", "operator", "T2", "vendor-library", "cuDNN"),
    ],
    "qimeng-gemm": [
        spec("throughput", 211, "percent", "single", "GEMM suite", "RISC-V", "RISC-V", "operator", "T2", "vendor-library", "OpenBLAS", "Preserved verbatim as 211% of OpenBLAS; not interpreted as percentage gain."),
        spec("throughput", 115, "percent", "single", "GEMM suite", "NVIDIA", "NVIDIA GPU", "operator", "T2", "vendor-library", "cuBLAS", "Preserved verbatim as 115% of cuBLAS; not interpreted as percentage gain."),
    ],
    "cursor-nvidia-multi-agent-kernels": [
        spec("speedup", 38, "percent", "geometric-mean", "SOL-ExecBench", "235 problems from 124+ models", "NVIDIA B200", "operator", "unknown", "prior-agent", "PyTorch code already optimized by a single agent"),
        spec("win-rate", 149, "count", "total", "SOL-ExecBench", "235 problems", "NVIDIA B200", "operator", "unknown", "prior-agent", "PyTorch code already optimized by a single agent", "149 of 235 tasks beat the baseline."),
        spec("efficiency", 86, "percent", "unknown", "SOL-ExecBench", "GEMM", "NVIDIA B200", "operator", "T2", "vendor-library", "cuBLAS"),
        spec("speedup", 9, "percent", "maximum", "SOL-ExecBench", "small-M decode GEMM shapes", "NVIDIA B200", "operator", "T2", "vendor-library", "cuBLAS"),
    ],
    "automegakernel": [
        spec("speedup", {"min": 1.25, "max": 1.72}, "x", "range", "AutoMegaKernel autoresearch", "self-improvement", "NVIDIA GPU", "model", "unknown", "self-baseline", "pre-autoresearch AutoMegaKernel"),
        spec("speedup", 1.33, "x", "maximum", "TinyLlama-1.1B", "batch-1 decode; W8A16", "NVIDIA L4", "model", "T2", "vendor-library", "CUDA-graphed cuBLAS BF16", caveats=("Precision-asymmetric comparison.",)),
        spec("speedup", {"min": 1.25, "max": 1.27}, "x", "range", "TinyLlama-1.1B", "batch-1 decode; W8A16", "NVIDIA L40S", "model", "T2", "vendor-library", "CUDA-graphed cuBLAS BF16", caveats=("Precision-asymmetric comparison.",)),
        spec("speedup", {"min": 1.19, "max": 1.23}, "x", "range", "TinyLlama-1.1B", "batch-1 decode; W8A16", "NVIDIA RTX 5090", "model", "T2", "vendor-library", "CUDA-graphed cuBLAS BF16", caveats=("Precision-asymmetric comparison.",)),
    ],
    "stitchcuda": [
        spec("correctness", 100, "percent", "unknown", "KernelBench", "Level 3; approximate", "NVIDIA GPU", "system", "unknown", "none", "no comparative denominator"),
        spec("speedup", 1.72, "x", "unknown", "KernelBench", "Level 3", "NVIDIA GPU", "system", "unknown", "prior-agent", "CudaForge"),
        spec("speedup", 2.73, "x", "unknown", "KernelBench", "Level 3", "NVIDIA GPU", "system", "unknown", "prior-agent", "Kevin-32B"),
        spec("speedup", 1.50, "x", "arithmetic-mean", "KernelBench", "Level 3", "NVIDIA GPU", "system", "T0", "framework-reference", "PyTorch eager", "Average end-to-end result."),
    ],
    "cutegen": [
        spec("speedup", 1.71, "x", "arithmetic-mean", "KernelBench", "209 Level 1 and Level 2 tasks", "NVIDIA GPU", "operator", "T0", "framework-reference", "PyTorch", "Zero low-precision shortcuts; CudaForge's separately reported 0.89x score is not used as this claim's denominator."),
    ],
    "cuco": [
        spec("speedup", 1.57, "x", "maximum", "CUCo multi-GPU suite", "four workloads", "NVIDIA GPU", "distributed", "T0", "framework-reference", "host-driven CPU-launched collectives/streams"),
        spec("speedup", 12, "percent", "single", "DeepSeek-V3 MoE", "dispatch/compute overlap", "NVIDIA GPU", "communication", "T3", "expert-implementation", "DeepEP"),
        spec("cost", 10, "usd", "maximum", "CUCo multi-GPU suite", "LLM cost per workload", "NVIDIA GPU", "system", "unknown", "none", "no comparative denominator", "Reported as less than USD 10."),
    ],
    "dice": [
        spec("correctness", 47.0, "percent", "unknown", "KernelBench", "Level 1; 8B", "NVIDIA GPU", "operator", "unknown", "none", "no comparative denominator"),
        spec("pass-rate", 15.0, "percent", "unknown", "KernelBench", "Level 1; 8B; fast1", "NVIDIA GPU", "operator", "T0", "framework-reference", "PyTorch reference"),
        spec("pass-rate", 6.0, "percent", "unknown", "KernelBench", "Level 1; 8B; fast2", "NVIDIA GPU", "operator", "T0", "framework-reference", "PyTorch reference"),
    ],
    "egg-kernel": [
        spec("correctness", 100, "percent", "unknown", "KernelBench", "250 tasks", "NVIDIA RTX 4090", "operator", "unknown", "none", "no comparative denominator"),
        spec("speedup", 2.13, "x", "arithmetic-mean", "KernelBench", "correct kernels among 250 tasks", "NVIDIA RTX 4090", "operator", "T0", "framework-reference", "PyTorch eager"),
        *[
            spec("speedup", value, "x", "single", "TritonBench", f"representative operator {index}", "NVIDIA GPU", "operator", "T3", "expert-implementation", "hand-written Triton")
            for index, value in enumerate((1.24, 1.63, 1.08), start=1)
        ],
    ],
    "kernelpro": [
        *[
            spec("speedup", value, "x", "geometric-mean", "KernelBench", level, "NVIDIA GPU", "operator", "T0", "framework-reference", "PyTorch eager")
            for level, value in (("Level 1", 2.42), ("Level 2", 4.69), ("Level 3", 5.30))
        ],
        spec("speedup", 1.23, "x", "unknown", "VeOmni MoE", "training kernel", "NVIDIA GPU", "operator", "T3", "expert-implementation", "hand-tuned Triton"),
        spec("energy-reduction", 11.6, "percent", "unknown", "VeOmni MoE", "matched-speed preliminary result", "NVIDIA GPU", "operator", "T3", "expert-implementation", "hand-tuned Triton", caveats=("Explicitly preliminary in the paper.",)),
    ],
    "davinci-kernel": [
        spec("pass-rate", value, "percent", "unknown", "KernelBench", f"{level}; Fast_1; 14B", "NVIDIA GPU", "operator", "T0", "framework-reference", "PyTorch reference Fast_1 threshold")
        for level, value in (("Level 1", 37.2), ("Level 2", 70.6), ("Level 3", 32.2))
    ],
    "fact": [
        spec("speedup", 2.03, "x", "single", "MiniGPT", "end-to-end", "NVIDIA GPU", "model", "T0", "framework-reference", "PyTorch eager"),
        spec("speedup", 1.41, "x", "single", "Llama-3-8B", "end-to-end", "NVIDIA GPU", "model", "T0", "framework-reference", "PyTorch eager"),
    ],
    "atrex-kernel-agent": [
        spec("speedup", 1.31, "x", "maximum", "Atrex AKA case study", "three compute-bound operators", "anonymized XPU-A", "operator", "T4", "production-incumbent", "deployed production kernel (AITER where applicable)", caveats=("Controlled three-operator study, not the full 30-operator Atrex-Bench.",)),
    ],
    "ascend-debug-agent": [
        spec("pass-rate", 66.7, "percent", "pass-at-k", "NPUKernelBench-derived near-miss set", "27 frozen operators; Debug Pass@1", "Ascend NPU", "operator", "unknown", "prior-agent", "fresh CANNBot-style regeneration", "Regeneration Avg Pass@1 is 25.9%."),
        spec("pass-rate", 40.7, "percent", "pass-at-k", "NPUKernelBench-derived near-miss set", "27 frozen operators; regeneration Pass@3", "Ascend NPU", "operator", "unknown", "prior-agent", "fresh CANNBot-style regeneration", "Comparator result; difference from Debug Pass@1 was not statistically significant (p=0.1185)."),
        spec("token-reduction", 92.8, "percent", "unknown", "NPUKernelBench-derived near-miss set", "tokens per successful repair", "Ascend NPU", "operator", "unknown", "prior-agent", "three-trial regeneration"),
    ],
    "agenticcann": [
        spec("pass-rate", {"min": 90, "max": 100}, "percent", "range", "AgenticCANN deep study", "elementwise/normalization feasibility", "Ascend NPU", "operator", "unknown", "none", "no comparative denominator"),
        spec("pass-rate", 56, "percent", "unknown", "AgenticCANN deep study", "fusion feasibility", "Ascend NPU", "fusion", "unknown", "none", "no comparative denominator"),
        spec("speedup", 6.65, "x", "single", "Pangu-1B RMSNorm", "shape 1", "Ascend NPU", "operator", "T0", "framework-reference", "PyTorch reference"),
        spec("speedup", 6.19, "x", "single", "Pangu-1B RMSNorm", "shape 2", "Ascend NPU", "operator", "T0", "framework-reference", "PyTorch reference"),
    ],
    "hawk-npu": [
        spec("accuracy", 80, "percent", "unknown", "CANNBench", "Level 1; eight operators", "Ascend NPU", "operator", "unknown", "none", "no comparative denominator", "CANNBot reports 49% under the same comparison."),
        spec("speedup", 1.34, "x", "unknown", "CANNBench", "Level 1; eight operators", "Ascend NPU", "operator", "T0", "framework-reference", "PyTorch reference", "CANNBot reports 0.86x under the same comparison."),
    ],
    "ascendoptimizer": [
        spec("speedup", 1.21, "x", "geometric-mean", "cann-ops", "127 Ascend C operators", "Ascend NPU", "operator", "T3", "expert-implementation", "Ascend reference operator"),
        spec("win-rate", 49.61, "percent", "unknown", "cann-ops", "127 Ascend C operators", "Ascend NPU", "operator", "T3", "expert-implementation", "Ascend reference operator", "Fraction of operators beating the reference."),
    ],
    "geak-v4": [
        spec("speedup", 2.21, "x", "geometric-mean", "GEAK v4 kernel suite", "Triton kernels", "AMD GPU", "operator", "unknown", "self-baseline", "original per-task kernel"),
        spec("speedup", 2.72, "x", "geometric-mean", "GEAK v4 kernel suite", "HIP kernels", "AMD GPU", "operator", "unknown", "self-baseline", "original per-task kernel"),
        spec("throughput", 60, "percent", "unknown", "Qwen3.5-27B", "end-to-end serving", "AMD GPU", "serving", "unknown", "self-baseline", "pre-optimization serving stack", "Reported as a 60% end-to-end throughput gain over the baseline."),
        spec("throughput", 96, "percent", "unknown", "Qwen3-14B", "end-to-end serving", "AMD GPU", "serving", "unknown", "self-baseline", "pre-optimization serving stack", "Reported as a 96% end-to-end throughput gain over the baseline."),
        spec("throughput", 42.2, "percent", "unknown", "MiniMax M3", "end-to-end serving", "AMD GPU", "serving", "unknown", "self-baseline", "pre-optimization serving stack", "Reported as a 42.2% end-to-end throughput gain over the baseline."),
    ],
    "amd-apex": [
        spec("speedup", 36.35, "x", "maximum", "Apex registry", "all_reduce; 12 kernel types / 21 models", "AMD MI300X/MI355X", "communication", "unknown", "self-baseline", "prior kernel in the same optimization run", caveats=("Best case; most other kernels are reported near or above 1.0x.",)),
    ],
    "atx-custom-nki-agent": [
        spec("pass-rate", 77.3, "percent", "unknown", "NKIGen-Bench", "150-task evaluation split; Claude Opus 4.8", "AWS Trainium", "operator", "unknown", "ablation", "single-shot Claude without agent tools (6% pass rate)"),
    ],
    "accelopt": [
        spec("fraction-of-ceiling", 61, "percent", "arithmetic-mean", "NKIBench", "after self-improvement; before value 49%", "AWS Trainium 1", "operator", "T6", "hardware-ceiling", "peak throughput"),
        spec("fraction-of-ceiling", 59, "percent", "arithmetic-mean", "NKIBench", "after self-improvement; before value 45%", "AWS Trainium 2", "operator", "T6", "hardware-ceiling", "peak throughput"),
    ],
    "cake": [
        spec("speedup", 1.144, "x", "unknown", "Flash-KMeans", "matched implementation-hidden clean start", "NVIDIA B200", "operator", "T3", "expert-implementation", "tuned FlashML", "Direct CUDA/PTX reaches 0.928x under the same controlled study."),
    ],
    "asmevo": [
        spec("win-rate", 29, "count", "total", "KernelBench code objects", "30 selected code objects", "AMD MI308X", "operator", "unknown", "self-baseline", "original recovered AMDGPU code object", "29 of 30 selected binaries improved."),
        spec("speedup", 1.35, "x", "geometric-mean", "KernelBench code objects", "30 selected code objects", "AMD MI308X", "operator", "unknown", "self-baseline", "original recovered AMDGPU code object", caveats=("Selected already-optimized code objects; shape-, dispatch-, and CDNA-specific.",)),
        spec("speedup", 3.88, "x", "maximum", "KernelBench code objects", "30 selected code objects", "AMD MI308X", "operator", "unknown", "self-baseline", "original recovered AMDGPU code object", caveats=("Selected already-optimized code objects; shape-, dispatch-, and CDNA-specific.",)),
        spec("speedup", 1.09, "x", "geometric-mean", "production AITer binaries", "recovered production binaries", "AMD MI300X", "operator", "T4", "production-incumbent", "original AITer code object"),
        spec("speedup", 1.31, "x", "maximum", "production AITer binaries", "recovered production binaries", "AMD MI300X", "operator", "T4", "production-incumbent", "original AITer code object"),
        spec("speedup", 1.18, "x", "geometric-mean", "vLLM/SGLang Triton assembly", "recovered production binaries", "AMD MI300X", "operator", "T4", "production-incumbent", "original code object"),
        spec("speedup", 1.34, "x", "maximum", "vLLM/SGLang Triton assembly", "recovered production binaries", "AMD MI300X", "operator", "T4", "production-incumbent", "original code object"),
    ],
    "zomboss": [
        spec("correctness", 100, "percent", "total", "Zomboss Gemmini suite", "20 workload instances", "Gemmini FPGA", "compiler", "unknown", "none", "compiler-enforced correctness"),
        spec("correctness", 100, "percent", "total", "Zomboss PLENA suite", "36 workload instances", "PLENA simulator", "compiler", "unknown", "none", "compiler-enforced correctness"),
        spec("speedup", 3.34, "x", "geometric-mean", "Zomboss Gemmini suite", "20 workload instances", "Gemmini FPGA", "compiler", "T1", "compiler-default", "compiler-default mapping"),
        spec("speedup", 1.10, "x", "geometric-mean", "Zomboss PLENA suite", "36 workload instances; best of three agent runs", "PLENA simulator", "compiler", "T1", "compiler-default", "compiler-default mapping"),
    ],
    "auto-gpu-kernel": [
        spec("speedup", 34.93, "x", "arithmetic-mean", "MLSys 2026 FlashInfer contest", "DeepSeek Sparse Attention agent-only track", "NVIDIA B200", "operator", "T3", "expert-implementation", "contest reference kernel"),
    ],
    "alphaevolve-fhe": [
        spec("speedup", 2.5, "x", "single", "FHE kernel suite", "TFHE bootstrap; within 24 hours", "TPU v5e", "operator", "T3", "expert-implementation", "human state-of-the-art implementation"),
        spec("speedup", 1.31, "x", "single", "FHE kernel suite", "CKKS rotation; within 24 hours", "TPU v5e", "operator", "T3", "expert-implementation", "human state-of-the-art implementation"),
    ],
    "qwen3.7-max-kernel-opt": [
        spec("speedup", 10.0, "x", "geometric-mean", "SGLang Extend Attention Kernel", "reported evaluation shapes", "T-Head Zhenwu M890 PPU", "operator", "T4", "production-incumbent", "SGLang official Triton reference implementation", caveats=("Not independently reproduced.",)),
    ],
}


# README primary claims favor a representative performance result with an
# explicit denominator when the first source-order claim is only correctness,
# coverage, or a weaker denominator. Values are one-based claim positions.
PRIMARY_CLAIM_NUMBER = {
    "akg-agent": 2,
    "cudaperf": 2,
    "avo": 2,
    "kevin": 2,
    "qimeng-tensorop": 2,
    "qimeng-gemm": 2,
    "stitchcuda": 2,
    "egg-kernel": 2,
    "agenticcann": 3,
    "hawk-npu": 2,
    "asmevo": 2,
    "zomboss": 3,
}


MANUAL_CLAIM_REVIEW = {
    "evomem": "The 2.4941x→2.7049x combined-speedup wording does not expose a safe per-result denominator or aggregation.",
    "kernelbrain": "The 17%–48% wall-time range mixes PyTorch, supplied generated bases, and PyTorch KernelAgent across tasks.",
    "kernelarc": "The five-task leaderboard snapshot, 1.06x–143.78x task range, and separate cuBLAS case require claim-by-claim table extraction and dated T5 review.",
    "specgen": "Reported ranges pool multiple agent baselines and search settings; v1 does not map each number to one denominator.",
    "cudamaster": "The approximate 35% result lacks an explicit aggregation and the cuBLAS comparison is qualitative.",
    "incoder-32b": "The 38.0% KernelBench value is present but its exact metric/threshold is not identified in v1.",
    "cudaforge": "The paired 1.68x/2.27x values are not mapped to distinct denominators in v1.",
    "kernel-design-agents": "Contest ranks are given only as #1–#3 across unspecified tracks; no safe dated T5 claim can be constructed.",
    "optiml": "The up-to 1.64x value does not identify which listed LLM-only baseline is the denominator.",
    "mucutlass-sol": "The 0.40x→1.27x and +SOL up-to 2.07x wording mixes ablation and ceiling-relative semantics.",
    "qimeng-kernel": "Approximate Level 1/2/3 percentages do not identify the exact metric or evaluation protocol in v1.",
    "evokernel": "The 11%→83% correctness and 3.60x median lack a verified benchmark, denominator, and exact hardware in v1.",
    "ascendkernelgen": "The 0%→95.5% compilation result lacks an explicit before/after model baseline in v1.",
    "ascendcraft": "Compilation/correctness percentages lack an evaluated-on workload in v1.",
    "argus": "The 99%–104% assembly comparison and 2x–1543x prior-agent range require separate source-table extraction.",
    "standard-kernel": "The proprietary 80%–4x end-to-end range has no public workload-to-value mapping.",
}

SUMMARY_OVERRIDES = {
    "accelopt": (
        "Self-improving agentic system for accelerator kernels; the latest paper reports mean peak-throughput efficiency improving from 49% to 61% on Trainium 1 and from 45% to 59% on Trainium 2. Ships the NKIBench suite. MLSys'26."
    ),
}

CLAIM_LINKED_YES = {
    "kernelpilot",
    "ako4x",
    "moe-kernel-agent",
    "forgestencil",
    "kernel-forge",
    "houmao-agentic-kernel-optimization",
    "cursor-nvidia-multi-agent-kernels",
    "auto-gpu-kernel",
}

NON_TIER_BASELINE_KINDS = {
    "none",
    "ablation",
    "evaluation-reference",
}
RELATIONAL_BASELINE_KINDS = {"prior-agent", "self-baseline"}
IMPLEMENTATION_PERFORMANCE_METRICS = {
    "speedup",
    "latency",
    "throughput",
    "efficiency",
    "fraction-of-ceiling",
    "energy-reduction",
    "time-reduction",
}
EVALUATION_REFERENCE_CLAIMS = {
    "akg-agent-claim-1",
    "hiera-claim-1",
}
BASELINE_REVIEWS = {
    "agentcompile": [(
        "claims.agentcompile-claim-2.baseline.tier",
        "vLLM is an implementation denominator, but the primary evidence available during migration did not establish whether this instance was a deployed production incumbent; tier remains Unknown.",
    )],
    "kforge": [(
        "claims.kforge-claim-1.baseline.tier",
        "TensorRT-LLM 1.3.0rc9 is an implementation denominator, but deployment/incumbency status was not established; tier remains Unknown.",
    )],
    "compiler-grounded-hierarchical-diagnosis": [(
        "claims.compiler-grounded-hierarchical-diagnosis-claim-1.baseline.tier",
        "The validated initial Triton kernel is a real implementation denominator, but its T0-T6 provenance is unresolved; tier remains Unknown.",
    )],
    "cursor-nvidia-multi-agent-kernels": [(
        "claims.cursor-nvidia-multi-agent-kernels-claim-1.baseline.tier",
        "The single-agent-optimized kernel is a real implementation denominator, but it does not map safely to T0-T6; tier remains Unknown.",
    )],
    "automegakernel": [(
        "claims.automegakernel-claim-1.baseline.tier",
        "The pre-autoresearch implementation is a real implementation denominator, but it does not map safely to T0-T6; tier remains Unknown.",
    )],
    "stitchcuda": [
        (
            "claims.stitchcuda-claim-2.baseline.tier",
            "CudaForge output is a real generated implementation denominator, but its T0-T6 provenance is unresolved; tier remains Unknown.",
        ),
        (
            "claims.stitchcuda-claim-3.baseline.tier",
            "Kevin-32B output is a real generated implementation denominator, but its T0-T6 provenance is unresolved; tier remains Unknown.",
        ),
    ],
    "geak-v4": [
        (
            f"claims.geak-v4-claim-{index}.baseline.tier",
            "The original or pre-optimization implementation is a real denominator, but it does not map safely to T0-T6; tier remains Unknown.",
        )
        for index in range(1, 6)
    ],
    "amd-apex": [(
        "claims.amd-apex-claim-1.baseline.tier",
        "The prior kernel from the same optimization run is a real implementation denominator, but it does not map safely to T0-T6; tier remains Unknown.",
    )],
    "asmevo": [
        (
            "claims.asmevo-claim-2.baseline.tier",
            "The original recovered AMDGPU code object is a real implementation denominator, but it does not map safely to T0-T6; tier remains Unknown.",
        ),
        (
            "claims.asmevo-claim-3.baseline.tier",
            "The original recovered AMDGPU code object is a real implementation denominator, but it does not map safely to T0-T6; tier remains Unknown.",
        ),
    ],
}


def source_for_claim(links: dict[str, list[dict[str, str]]]) -> tuple[str, str]:
    for kind, locator in (
        ("paper", "unknown"),
        ("article", "page"),
        ("code", "README"),
        ("project", "page"),
        ("artifact", "artifact"),
        ("model", "model card"),
        ("dataset", "dataset card"),
    ):
        if links[kind]:
            return links[kind][0]["url"], locator
    raise ValueError("entry has no typed source link")


def claim_reproducibility(
    old: dict[str, Any], links: dict[str, list[dict[str, str]]]
) -> dict[str, Any]:
    project_state = status(old.get("ships_kernels", "unknown"))
    if project_state in {"no", "unknown"}:
        return {"claim_linked_artifact": project_state, "artifact_url": None}
    artifact_url = first_url(links, "artifact", "code")
    if not artifact_url:
        return {"claim_linked_artifact": "unknown", "artifact_url": None}
    claim_state = "yes" if old["id"] in CLAIM_LINKED_YES else "partial"
    return {"claim_linked_artifact": claim_state, "artifact_url": artifact_url}


def build_claims(
    old: dict[str, Any], links: dict[str, list[dict[str, str]]]
) -> list[dict[str, Any]]:
    source_url, locator = source_for_claim(links)
    budget_state = status(old.get("budget_disclosed", "unknown"))
    if budget_state == "yes":
        budget_details = "Optimization/search budget is reported in the primary source; v1 did not normalize the details."
    elif budget_state == "partial":
        budget_details = "The primary source reports only part of the optimization/search budget."
    else:
        budget_details = ""
    budget_detail_overrides = {
        "cuda-agent": "Evaluation permits up to 200 agent turns per task.",
        "kernel-forge": "50 optimization iterations per kernel.",
        "houmao-agentic-kernel-optimization": "Approximately 1.9 billion agent tokens across the three-task campaign.",
        "cursor-nvidia-multi-agent-kernels": "Three-week campaign on 27 NVIDIA B200 GPUs; per-task token and iteration budgets are not reported.",
        "stitchcuda": "Training used approximately 20 hours on four NVIDIA H200 GPUs; per-task inference budget was not normalized in v1.",
        "cake": "80 million tokens per matched clean-start campaign; other resource accounting is partial.",
        "qwen3.7-max-kernel-opt": "Approximately 35 autonomous hours, 432 kernel evaluations, and 1,158 tool calls.",
    }
    budget_details = budget_detail_overrides.get(old["id"], budget_details)
    repro = claim_reproducibility(old, links)
    result: list[dict[str, Any]] = []
    for index, raw in enumerate(CLAIM_SPECS.get(old["id"], []), start=1):
        item = copy.deepcopy(raw)
        item["id"] = f"{old['id']}-claim-{index}"
        if item["id"] in EVALUATION_REFERENCE_CLAIMS:
            item["baseline"]["tier"] = "not-applicable"
            item["baseline"]["kind"] = "evaluation-reference"
        elif (
            item["baseline"]["kind"] in RELATIONAL_BASELINE_KINDS
            and item["baseline"]["tier"] == "unknown"
        ):
            item["baseline"]["tier"] = (
                "unknown"
                if item["metric"] in IMPLEMENTATION_PERFORMANCE_METRICS
                else "not-applicable"
            )
        elif item["baseline"]["kind"] in NON_TIER_BASELINE_KINDS:
            item["baseline"]["tier"] = "not-applicable"
        elif item["baseline"]["tier"] == "unknown":
            item["baseline"]["kind"] = "unresolved-implementation"
        item["baseline"]["evidence"] = None
        item["budget"] = {"status": budget_state, "details": budget_details}
        item["reproducibility"] = copy.deepcopy(repro)
        item["primary_source"] = {"url": source_url, "locator": locator}
        # Keep the stable field order readable in YAML.
        ordered = {
            "id": item["id"],
            "metric": item["metric"],
            "value": item["value"],
            "unit": item["unit"],
            "aggregation": item["aggregation"],
            "qualifier": item["qualifier"],
            "workload": item["workload"],
            "hardware": item["hardware"],
            "scope": item["scope"],
            "baseline": item["baseline"],
            "budget": item["budget"],
            "reproducibility": item["reproducibility"],
            "primary_source": item["primary_source"],
            "caveats": ordered_unique(item["caveats"]),
        }
        result.append(ordered)
    return result


def migrate_entry(old: dict[str, Any]) -> dict[str, Any]:
    links = migrate_links(old)
    representations = migrate_representations(old)
    claims = build_claims(old, links)
    reviews: list[dict[str, str]] = []
    if old["id"] in MANUAL_CLAIM_REVIEW:
        reviews.append({"field": "claims", "issue": MANUAL_CLAIM_REVIEW[old["id"]]})
    elif old.get("route") != "tool" and not claims:
        reviews.append(
            {
                "field": "claims",
                "issue": "No numerical headline claim could be safely structured from the v1 row; verify the primary evidence before adding one.",
            }
        )
    if old["id"] in REPRESENTATION_REVIEWS:
        field, issue = REPRESENTATION_REVIEWS[old["id"]]
        reviews.append({"field": field, "issue": issue})
    for field, issue in BASELINE_REVIEWS.get(old["id"], []):
        reviews.append({"field": field, "issue": issue})

    primary_number = PRIMARY_CLAIM_NUMBER.get(old["id"], 1)
    primary_claim = (
        f"{old['id']}-claim-{primary_number}"
        if len(claims) >= primary_number
        else (claims[0]["id"] if claims else None)
    )
    caveats = [old["note"]] if old.get("note") else []
    if old["id"] == "dice":
        caveats = [
            caveat.replace(
                "Route A follows the paper's one-shot evaluation protocol",
                "The system follows the paper's one-shot evaluation protocol",
            )
            for caveat in caveats
        ]
    entry_taxonomy = taxonomy(old, representations)
    evidenced_workload_scopes = {
        claim["scope"]
        for claim in claims
        if claim["scope"] in {"operator", "fusion", "graph", "model", "system"}
    }
    recorded_workload_scopes = {
        *entry_taxonomy["workload_scope"],
        *evidenced_workload_scopes,
    }
    entry_taxonomy["workload_scope"] = [
        scope
        for scope in ("operator", "fusion", "graph", "model", "system")
        if scope in recorded_workload_scopes
    ]
    entry = {
        "id": old["id"],
        "name": old["name"],
        "organization": old["org"],
        "date": str(old["date"]),
        "entry_type": "tool" if old.get("route") == "tool" else "agent",
        "status": old["status"],
        "summary": SUMMARY_OVERRIDES.get(old["id"], old["desc"]),
        "caveats": caveats,
        "taxonomy": entry_taxonomy,
        "representations": representations,
        "hardware": old.get("hardware") or [],
        "links": links,
        "artifacts": migrate_artifacts(old, links),
        "claims": claims,
        "primary_claim": primary_claim,
    }
    if reviews:
        entry["migration_review"] = reviews
    return entry


def migrate_document(document: dict[str, Any]) -> dict[str, Any]:
    expected = read_expected_ids()
    if document.get("schema_version") == 2:
        actual = [entry["id"] for entry in document.get("agents", [])]
        if len(actual) != len(set(actual)):
            raise ValueError("v2 file contains duplicate IDs")
        missing = sorted(set(expected) - set(actual))
        if missing:
            raise ValueError(f"v2 file lost v1 IDs: {', '.join(missing)}")
        validation_errors = validate_catalog(document)
        if validation_errors:
            raise ValueError(
                "v2 validation failed:\n" + "\n".join(validation_errors)
            )
        return document

    old_entries = document.get("agents")
    if not isinstance(old_entries, list):
        raise ValueError("input is neither a v1 nor a v2 agents catalog")
    old_ids = [entry.get("id") for entry in old_entries]
    if len(old_ids) != len(set(old_ids)):
        raise ValueError("v1 file contains duplicate IDs")
    if old_ids != expected:
        missing = sorted(set(expected) - set(old_ids))
        added = sorted(set(old_ids) - set(expected))
        raise ValueError(
            "v1 ID snapshot mismatch; "
            f"missing={missing or 'none'}, added={added or 'none'}, order_changed={set(old_ids) == set(expected)}"
        )

    migrated = [migrate_entry(entry) for entry in old_entries]
    migrated_ids = [entry["id"] for entry in migrated]
    if migrated_ids != expected:
        raise AssertionError("migration did not preserve the full ordered ID snapshot")
    result = {
        "schema_version": 2,
        "research_cutoff": RESEARCH_CUTOFF,
        "agents": migrated,
    }
    validation_errors = validate_catalog(result)
    if validation_errors:
        raise ValueError(
            "migrated v2 validation failed:\n" + "\n".join(validation_errors)
        )
    return result


def dump_yaml(document: dict[str, Any]) -> str:
    return yaml.safe_dump(
        document,
        allow_unicode=True,
        sort_keys=False,
        width=110,
        default_flow_style=False,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    output = args.output or args.input
    document = load_yaml(args.input)
    if not isinstance(document, dict):
        raise ValueError("input catalog root must be a mapping")
    already_v2 = document.get("schema_version") == 2
    migrated = migrate_document(document)
    if already_v2 and output == args.input:
        print(f"{args.input}: already schema v2; ID preservation verified; no changes")
        return 0
    output.write_text(dump_yaml(migrated), encoding="utf-8")
    claim_count = sum(len(entry["claims"]) for entry in migrated["agents"])
    review_count = sum(len(entry.get("migration_review", [])) for entry in migrated["agents"])
    print(
        f"migrated {len(migrated['agents'])} entries / {claim_count} claims / "
        f"{review_count} review items -> {output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
