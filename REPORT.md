# Scoped Audit Report

## Verdict

INCONCLUSIVE_SCOPED_TO_SOURCE_AND_BOUNDED_TOY

This repository is a trustworthy record of what was pinned and checked, not a full reproduction of FormalJudge. publication_allowed is false.

## Completed checks

- The paper PDF and arXiv source archive are pinned by SHA-256.
- The source archive was inspected as paper source; it contains no executable implementation.
- The original one-claim contract is preserved, and its limitation is made explicit.
- Five paper-level claim rows are documented with source locations and production paths.
- A deterministic fixture composes three fixed atomic-fact cases and matches all three constructed labels.
- The repository has one public branch, main, with a clean descriptive name.
- The final GitHub state is checked by verify_final.py and a fresh clone.

## Claim outcomes

| Claim | Outcome |
| --- | --- |
| C1 | UNVERIFIED: no benchmark data, model calls, labels, or independent accuracy aggregation |
| C2 | UNVERIFIED: no LLM extraction, Dafny/Boogie/Z3 run, or Agent-SafetyBench output |
| C3 | UNVERIFIED: no Deceivers trajectories or weak-to-strong model matrix |
| C4 | UNVERIFIED: no refinement traces, formal feedback run, or round metrics |
| C5 | TOY_SOURCE_AUDIT: finite logical composition only |

## Interpretation

The local toy supports only the narrow statement that fixed atomic facts can be composed into a deterministic conditional verdict. It does not validate semantic extraction, formal-specification synthesis, solver execution, benchmark accuracy, or the paper's reliability claim at scale.

The repository therefore makes no benchmark score claim and no claim that the paper authors reviewed or endorsed this audit.
