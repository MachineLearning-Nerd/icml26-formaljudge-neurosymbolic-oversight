# FormalJudge: ICML 2026 Reproduction Audit

This repository tracks a source-pinned, claim-by-claim audit of:

> **FormalJudge: A Neuro-Symbolic Paradigm for Agentic Oversight**

The repository is intentionally evidence-first. It contains a deterministic symbolic composition toy and a source-feasibility audit; it does **not** contain the paper's LLM benchmark runs, Claude judge calls, Dafny/Z3 execution environment, or reported accuracy tables.

The repository has the standardized name `icml26-formaljudge-neurosymbolic-oversight`; its former name was `icml26-repro-tnsQ23imeD-formaljudge-neurosymbolic-oversight`. The complete audit record is in `CLAIM_EVIDENCE.md`, `SOURCE_AUDIT.md`, `REPORT.md`, and `BRANCH_AUDIT.md`.

| Resource | Link |
| --- | --- |
| Paper | [arXiv:2602.11136](https://arxiv.org/abs/2602.11136) |
| OpenReview submission | [tnsQ23imeD](https://openreview.net/forum?id=tnsQ23imeD) |
| Authors' implementation | [htlou/FormalJudge](https://github.com/htlou/FormalJudge) |
| Pinned paper PDF | [`evidence/source/arxiv-2602.11136.pdf`](evidence/source/arxiv-2602.11136.pdf) |
| Pinned source archive | [`evidence/source/arxiv-2602.11136-source.tar.gz`](evidence/source/arxiv-2602.11136-source.tar.gz) |

## Current status

**Overall result: inconclusive, scoped to a source audit and bounded toy.** The completed local work audits the method description and runs a three-case finite propositional composition toy based on the paper's trip-booking example. It does not reproduce Claude-4.5-Opus judging, LLM atomic-fact extraction, Dafny/Z3 verification, or any benchmark percentage.

The current compute policy allows local CPU and a local GTX 1050 only. It does not allow Hugging Face upgrades, remote compute, paid compute, or jobs. The machine-readable state records this as `publication_allowed: false`.

The dossier is published and verified. `publication_allowed` is false. The original one-claim contract is preserved as provenance; `claims.json` records the explicit five-claim expansion derived from the pinned paper source.

## What the paper does

FormalJudge addresses agent oversight by separating probabilistic semantic extraction from deterministic logical composition:

1. **Top-down intent decomposition:** an LLM turns natural-language requirements into small, grounded atomic yes/no facts.
2. **Context-aware extraction:** each fact receives only the relevant part of the agent trajectory; deterministic fields are parsed directly and semantic facts are extracted by an LLM.
3. **Formal proof synthesis:** the extracted facts become Dafny constants, derived predicates, and safety predicates.
4. **SMT verification:** Dafny/Boogie invokes Z3 to compute a deterministic PASS/BLOCK-style verdict from the composed predicates.

The paper evaluates this framework on Agent-SafetyBench, VitaBench, and Deceivers. It reports an average improvement of 16.6% over LLM-as-a-Judge baselines, weak-to-strong deception detection above 90% for a 7B judge against 72B agents, and improvement from 70.7% to 99.8% over three Dafny-guided refinement rounds for the stated Claude-4.5-Opus setup.

## What this repository contains

| Path | Purpose |
| --- | --- |
| `AUTONOMOUS_STATE.json` | Machine-readable phase, compute policy, next action, and bounded outcome |
| `STATUS.md` | Short human-readable audit status |
| `contract/live_claims.json` | Original anchored claim contract from the audit workflow |
| `contract/SOURCE_SNAPSHOT.json` | Source-snapshot provenance metadata |
| `evidence/source/arxiv-2602.11136.pdf` | Pinned arXiv paper PDF |
| `evidence/source/arxiv-2602.11136-source.tar.gz` | Pinned arXiv source archive |
| `evidence/source/SHA256SUMS` | Checksums for the pinned source artifacts |
| `outputs/claim1_source_audit/summary.json` | Local feasibility audit showing why the literal benchmark is unavailable |
| `outputs/claim1_symbolic_trip_toy/PROTOCOL.json` | Protocol for the bounded symbolic fixture |
| `outputs/claim1_symbolic_trip_toy/raw.json` | Three constructed trip-booking cases and formal verdicts |
| `outputs/claim1_symbolic_trip_toy/summary.json` | Toy accuracy and scope statement |
| `outputs/claim1_symbolic_trip_toy/SHA256SUMS` | Checksums for the toy artifacts |
| `src/claim1_symbolic_trip_toy.py` | Deterministic finite fact-composition toy |
| `tests/` | Minimal contract and toy checks |
| `.trackio/logbook/` | Audit log for the bounded toy attempt |
| `CLAIM_EVIDENCE.md` | Claim-to-evidence ledger and production paths |
| `SOURCE_AUDIT.md` | Pinned source hashes and source-location audit |
| `ENVIRONMENT.md` | Compute policy and paper-scale reproduction boundary |
| `REPORT.md` | Final scoped verdict and limitations |
| `CITATION.cff` | Machine-readable citation for the paper |
| `AUTHOR_THANK_YOU.md` | Thank-you note to the paper authors |
| `BRANCH_AUDIT.md` | Public/local branch and commit-attribution audit |
| `claims.json` | Machine-readable five-claim expansion |
| `EVIDENCE_MANIFEST.json` | Hash manifest for the published audit state |
| `verify_final.py` | Fail-closed local and fresh-clone verifier |

The toy composes three explicit facts—budget compliance, flying status, and hotel start date—into the conditional rule “if flying, hotel starts on or after arrival.” It checks one violation, one compliant flight, and one budget control. It does not perform natural-language extraction or invoke Dafny/Z3.

## Branch inventory

The final published branch is:

| Branch | Purpose | Current state |
| --- | --- | --- |
| `main` | Source-pinned FormalJudge reproduction audit | Contains the pinned paper artifacts, source audit, symbolic toy, and this README |

The repository originally had a stale `master` branch containing only the initial source-pinned commit. `main` already contained that history plus the later toy checkpoints; the cleanup makes `main` the default and removes the redundant published `master` branch. The obsolete local attribution backup ref was also removed; its history is not part of the public branch set.

## Claim ledger: what each claim means and how it is produced

The original machine-readable contract contains one anchored claim string that is truncated in its source snapshot. The ledger below expands the paper's method and headline results into reviewable rows; it does not turn paper-reported numbers into independent results.

| ID | Paper claim | How the paper produces the claim | Evidence currently in this repo | Status |
| --- | --- | --- | --- | --- |
| C1 | FormalJudge improves oversight accuracy by an average of 16.6% over LLM-as-a-Judge baselines across three benchmarks and seven agent models. | Run Agent-SafetyBench, VitaBench, and Deceivers; use the stated God Judge ensemble for reference labels; compare FormalJudge with vanilla, CoT, few-shot, structured, and Python baselines. | `outputs/claim1_source_audit/summary.json` records that the required frontier-model benchmark is unavailable; no benchmark data or accuracy table is present. | **Unverified** |
| C2 | FormalJudge obtains the reported main detection values, including 77.28% and 80.54% on Agent-SafetyBench for the stated agent columns. | Extract atomic facts, synthesize Dafny specifications, run the verifier, and aggregate detection accuracy against the paper's ground-truth labels for each agent/judge combination. | The pinned source contains the paper table; this repository has no LLM extraction, Dafny/Boogie/Z3 run, or independent accuracy calculation. | **Unverified** |
| C3 | A 7B judge can detect deception from 72B agents at above 90% accuracy. | Run the Deceivers benchmark across the Qwen model-size matrix, extract atomic facts, compose the deception predicates formally, and compare accuracy by judge and agent size. | No Deceivers trajectories, model calls, or weak-to-strong evaluation output is present. | **Unverified** |
| C4 | Dafny-guided iterative refinement improves safety accuracy from 70.7% to 99.8% over three rounds in the stated experiment. | Let agents receive formal verification feedback—including violated constraints and the Dafny specification—then regenerate responses for three rounds and measure safety classification accuracy. | No Agent-SafetyBench refinement run, model output, or round-by-round metric is present. | **Unverified** |
| C5 | The method's reliability comes from composing atomic semantic facts with deterministic formal predicates rather than asking an LLM for one composite verdict. | Parse or extract each atomic fact, encode logical requirements as Dafny predicates, and let the SMT verifier compute the final conjunction. | `src/claim1_symbolic_trip_toy.py` verifies this composition pattern for three fixed facts and constructed labels only; it does not validate semantic extraction or solver execution. | **Toy only; full claim unverified** |

## Reproduction boundary

It is important to distinguish three statements:

1. **Paper-reported:** a method, number, or conclusion appearing in the FormalJudge paper.
2. **Source-audited:** the paper source or a repository artifact has been pinned and inspected.
3. **Reproduced here:** this repository independently ran the relevant experiment and stored verifiable output.

This repository supports the second category and one deliberately bounded piece of the third. It does not support the paper-level benchmark claims. `REPORT.md` records the final decision and `CLAIM_EVIDENCE.md` gives the expanded claim-by-claim boundary.

```text
verdict: inconclusive
claim 1: finite symbolic composition toy only
LLM semantic extraction executed: no
Dafny/Z3 executed: no
Claude-4.5-Opus benchmark executed: no
```

## Verification commands

From the repository root:

```bash
python3 verify_final.py
python3 src/claim1_symbolic_trip_toy.py --out outputs/claim1_symbolic_trip_toy
python3 -m pytest -q tests/test_contract.py tests/test_claim1_symbolic.py  # if pytest is installed
shasum -a 256 evidence/source/arxiv-2602.11136.pdf
shasum -a 256 evidence/source/arxiv-2602.11136-source.tar.gz
```

The expected source hashes are recorded in `evidence/source/SHA256SUMS`; the toy hashes are recorded in `outputs/claim1_symbolic_trip_toy/SHA256SUMS`.

## Citation

If this audit or the paper is useful, please cite the paper:

```bibtex
@misc{zhou2026formaljudge,
  title={FormalJudge: A Neuro-Symbolic Paradigm for Agentic Oversight},
  author={Jiayi Zhou and Yang Sheng and Hantao Lou and Yaodong Yang and Jie Fu},
  year={2026},
  eprint={2602.11136},
  archivePrefix={arXiv},
  primaryClass={cs.AI},
  url={https://arxiv.org/abs/2602.11136}
}
```

## Thank you

Thank you to **Jiayi Zhou, Yang Sheng, Hantao Lou, Yaodong Yang, and Jie Fu** for making the FormalJudge paper and implementation available. The paper offers a clear separation between neural semantic extraction and formal logical verification, which makes it a useful target for careful, claim-level reproduction work.
