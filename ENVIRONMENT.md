# Environment and Reproduction Boundary

## Allowed compute

The audit policy is local CPU and the local GTX 1050 only. It excludes Hugging Face upgrades, Hugging Face Jobs, paid compute, and remote jobs.

## Available local evidence

| Requirement for a paper-scale reproduction | Present here |
| --- | --- |
| Python interpreter for deterministic toy | Yes |
| Pinned paper PDF and source archive | Yes |
| Agent-SafetyBench, VitaBench, and Deceivers data | No |
| Claude-4.5-Opus, GPT-5, Gemini-3-Pro, or Qwen checkpoints/API calls | No |
| Authors' FormalJudge implementation cloned and executed | No |
| Dafny, Boogie, and Z3 runtime | No |
| LLM atomic-fact extraction outputs | No |
| Ground-truth labels and baseline results | No |
| Iterative refinement traces and round metrics | No |

The missing model, dataset, and formal-runtime layers are why C1-C4 remain UNVERIFIED and why C5 is limited to a symbolic toy.

## Lightweight commands

From the repository root:

~~~bash
python3 verify_final.py
python3 src/claim1_symbolic_trip_toy.py --out outputs/claim1_symbolic_trip_toy
python3 -m pytest -q tests/test_contract.py tests/test_claim1_symbolic.py
~~~

The pytest command is optional and depends on pytest being installed. The fail-closed repository verifier uses only the Python standard library and does not launch model calls, Dafny, Z3, or benchmark jobs.

## Artifact policy

The source archive, PDF, contract, source snapshot, toy raw data, toy summary, protocol, and checksums are evidence artifacts. A future full reproduction must add separately identified model, dataset, formal-runtime, trajectory, and aggregation artifacts rather than relabeling this toy as a benchmark result.
