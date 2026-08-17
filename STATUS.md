# Status

- OpenReview ID: `tnsQ23imeD`
- Original contract: `contract/live_claims.json` preserves one truncated anchored claim / 2 points.
- Current phase: standardized dossier **published and verified**.
- Overall verdict: `INCONCLUSIVE_SCOPED_TO_SOURCE_AND_BOUNDED_TOY`.
- Source: arXiv:2602.11136v1, archive/PDF pinned in `evidence/source/`.
- Compute policy: local CPU/local GTX 1050 only; no HF cpu-upgrade, Jobs, paid, or remote compute.
- Claims C1-C4: unverified because models, benchmark data, labels, formal runtime, and refinement traces are absent.
- Claim C5: deterministic symbolic toy only; no semantic extraction, Dafny, or Z3.
- Publication: `publication_allowed: false`.
- Branch state: public and local `main` only; repository name is `icml26-formaljudge-neurosymbolic-oversight`.
- Final evidence: `CLAIM_EVIDENCE.md`, `SOURCE_AUDIT.md`, `REPORT.md`, `BRANCH_AUDIT.md`, `claims.json`, `EVIDENCE_MANIFEST.json`, and `verify_final.py`.
