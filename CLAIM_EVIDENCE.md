# Claim-to-Evidence Ledger

This ledger separates paper-reported results, source-audited production paths, and the bounded local evidence in this repository.

Paper: FormalJudge: A Neuro-Symbolic Paradigm for Agentic Oversight
Authors: Jiayi Zhou, Yang Sheng, Hantao Lou, Yaodong Yang, and Jie Fu
OpenReview: tnsQ23imeD
arXiv: 2602.11136v1
Pinned source: evidence/source/arxiv-2602.11136-source.tar.gz

Important provenance note: contract/live_claims.json is the original audit contract and contains one truncated anchored claim string with max_points 2. The five rows below are an explicit expansion of the paper's claims from the pinned source; they do not silently replace the original contract.

Status vocabulary:

- PAPER_REPORTED: stated in the paper or its tables.
- SOURCE_AUDITED: located in the pinned primary source, but not independently rerun here.
- TOY_SOURCE_AUDIT: checked by a bounded deterministic fixture that does not reproduce the paper-scale experiment.
- UNVERIFIED: the repository lacks the model, data, runtime, or result artifacts needed to test the claim.

| ID | Paper claim | How the paper produces the claim | Evidence in this repository | Status |
| --- | --- | --- | --- | --- |
| C1 | FormalJudge improves oversight accuracy by an average of 16.6% over LLM-as-a-Judge baselines across three benchmarks and seven agent models. | Run Agent-SafetyBench, VitaBench, and Deceivers; establish reference labels with the stated God Judge process; run FormalJudge and six baselines; aggregate safe/unsafe classification accuracy. | The source audit pins example_paper.tex:437-534. outputs/claim1_source_audit/summary.json records that the literal frontier-model benchmark is unavailable. No benchmark data or accuracy table is present locally. | UNVERIFIED |
| C2 | The main benchmark table reports FormalJudge values including 77.28% and 80.54% on Agent-SafetyBench and 73.26% on a further agent column. | Extract atomic facts from trajectories, generate Dafny specifications, run Dafny/Boogie/Z3 verification, and aggregate verdict accuracy for each benchmark and agent model. | The paper table is source-audited at example_paper.tex:437-536. No LLM extraction, Dafny/Boogie/Z3 run, ground-truth labels, or independent accuracy calculation is present. | UNVERIFIED |
| C3 | A 7B judge detects deception from 72B agents at above 90% accuracy. | Run the Deceivers benchmark over the Qwen 7B/14B/32B/72B judge-agent matrix, extract the 15 atomic deception facts, compose the formal predicates, and score 200 deceptive plus 200 non-deceptive trajectories for each configuration. | The production path and reported outcome are source-audited at example_paper.tex:746-816 and 569-577. No Deceivers trajectories, model calls, or weak-to-strong evaluation output is present. | UNVERIFIED |
| C4 | Dafny-guided iterative refinement improves safety accuracy from 70.7% to 99.8% over three rounds for the stated Claude-4.5-Opus experiment. | Run Agent-SafetyBench responses, feed back the Dafny specification and concrete violations, regenerate responses for three rounds, and compare Dafny, Python, natural-language, and baseline refinement. | The protocol and reported result are source-audited at example_paper.tex:1358-1390 and 588-594. No model output, refinement trace, Dafny run, or round-by-round metric is present. | UNVERIFIED |
| C5 | Separating probabilistic atomic extraction from deterministic logical composition is the source of the framework's reliability. | Decompose intent into binary grounded facts, extract each fact from relevant trajectory context, synthesize Dafny predicates, and let the SMT verifier compute the conjunction or disjunction of violations. | The formal path is source-audited at example_paper.tex:273-355 and 364-410. The local toy composes three fixed propositional facts across one violation, one compliant case, and one budget control. | TOY_SOURCE_AUDIT; semantic extraction and Dafny/Z3 execution remain unverified. |

## What the local fixture actually establishes

The finite toy checks three constructed cases:

1. A flight with a hotel starting before arrival is blocked by the conditional date rule.
2. A compliant flight passes.
3. A non-flying trip over budget is blocked by the budget rule.

It reaches exact agreement with all three constructed labels and records the atomic facts, verdicts, violations, protocol, and checksums. It does not call an LLM, extract facts from natural language, synthesize Dafny, invoke Z3, or evaluate a benchmark.

## Overall decision

~~~text
overall_verdict: INCONCLUSIVE_SCOPED_TO_SOURCE_AND_BOUNDED_TOY
publication_allowed: false
C1-C4: unverified
C5: toy/source audit only
~~~

No benchmark score, full-paper reproduction, or author endorsement is claimed.
