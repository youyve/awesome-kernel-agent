# Kernel Agent Functional Landscape

**Research question:** Which distinct questions define this catalog's Kernel Agent data model, and what semantic role does each question play?

[README](../README.md) · [Field Map](field-map.md) · [Data](../data/agents.json)

This is a versioned catalog ontology, not a timeline, maturity ladder, causal graph, or performance ranking. Containment expresses semantic role only; screen position and group order do not imply research evolution. The facets are separate annotation questions, not a claim of statistical independence.

## Agent mechanism

Fields describing how proposals are produced, coordinated, evaluated, and retained.

Group predicate: **describes the optimization process**.

| Facet family | Question | Inclusion boundary |
| --- | --- | --- |
| **Policy adaptation** (`policy_adaptation`) | How is the proposal policy conditioned or adapted? | Prompting and model adaptation only; candidate enumeration belongs to generation/search. |
| **Generation mode** (`generation_mode`) | Is candidate production direct or revised across iterations? | Loop shape only; named search algorithms belong to search strategy. |
| **Search strategy** (`search_strategy`) | How are multiple candidate programs explored or selected? | Search/selection algorithms only; direct versus iterative execution is recorded separately. |
| **Actor composition** (`participants`) | Which agent and non-agent actors are explicitly inside the optimization loop? | Actor composition only; compiler-in-the-loop requires co-decision or transformation, not ordinary compiler feedback, and coordination topology is recorded separately. |
| **Coordination** (`coordination`) | How are participating actors organized or scheduled? | Control topology and role organization, not candidate-search algorithms. |
| **Feedback signal** (`feedback_signal`) | What outcome is observed and returned to the optimizer? | Measured outcome only; the instrument or evidence channel is recorded separately. |
| **Feedback source** (`feedback_source`) | Through which instrument or analysis channel is evidence obtained? | Compiler, execution-analysis, verification, or analytical channels; not the measured outcome itself. |
| **State retention** (`memory`) | Which state-retention or reuse mechanisms are explicitly used? | Runtime decision state, access, or persistence only; published datasets, logs, and output archives are project artifacts unless reused by the agent. |

## Optimization target and context

Fields describing what is changed and the workload or software context in scope.

Group predicate: **acts on or evaluates**.

| Facet family | Question | Inclusion boundary |
| --- | --- | --- |
| **Workload scope** (`workload_scope`) | At what workload granularity is optimization or evaluation demonstrated? | Kernel-to-system workload extent; software integration contexts are recorded separately. |
| **Integration scope** (`integration_scope`) | Which surrounding software or system context is explicitly in scope? | Library, compiler, runtime, serving, communication, or distributed integration; not a mere baseline mention. |
| **Artifact level** (`optimization_level`) | At which program or machine abstraction does the system directly edit or select artifacts? | Artifact abstraction only; algorithm and schedule decisions are recorded as optimization focus. |
| **Optimization focus** (`optimization_focus`) | Does the system explicitly optimize algorithmic structure or schedule/mapping decisions? | Decision type only; source language and IR are recorded as artifact level and representation. |
| **Representation** (`representations`) | Which concrete language, DSL, IR, or ISA represents generated or optimized artifacts? | Concrete notation only; hardware target and abstraction level remain separate. |

## Execution substrate

Fields describing the hardware on which evidence is obtained.

Group predicate: **is evaluated on**.

| Facet family | Question | Inclusion boundary |
| --- | --- | --- |
| **Hardware** (`hardware`) | On which accelerator or processor family is the system evaluated or targeted? | Execution substrate only; software representation is recorded separately. |

## Declared value relations

Values are positive and multi-label by default. The following are the only logical value relations enforced by the validator; they do not encode chronology or causality.
- Mutually exclusive within `generation_mode`: `direct`, `iterative-refinement`.
- Mutually exclusive within `participants`: `single-agent`, `multi-agent`.
- Within `policy_adaptation`, `agentic-reinforcement-learning` implies `reinforcement-learning`.
- Within `search_strategy`, `map-elites` implies `quality-diversity`, `evolutionary-search`.

## Reproducibility rules

1. Facet families, questions, boundaries, groups, and group predicates come from `schema/vocab.yaml`.
2. Every declared facet family appears exactly once; no representative system or preferred research direction is selected.
3. The Landscape contains no empirical edge, causal arrow, time ordering, or undeclared exclusivity.
4. Multi-label membership and corpus coverage belong to the Field Map, not this ontology view.
5. Empty lists mean unannotated evidence and never create a negative ontology relation.
6. Group and facet order follow the controlled vocabulary; card placement is layout only and carries no empirical meaning.
