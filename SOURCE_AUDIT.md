# Source Audit

## Pinned primary source

| Artifact | SHA-256 | Scope |
| --- | --- | --- |
| evidence/source/arxiv-2602.11136.pdf | b635896b5f22a51bfe4ca59aa3c0d3b9141353a34426f0d5c00f664b22ac76af | Pinned paper PDF |
| evidence/source/arxiv-2602.11136-source.tar.gz | 48387dc382f94be29a51e2570e3f57ed05b49ee93272a1940028468e9542fff8 | Pinned arXiv source archive |

The archive contains 14 regular source members and one directory entry. Its 00README.json records TeX Live 2025 and pdflatex. No archive member is executable. The archive is paper source, styles, bibliography, and figures; it is not a copy of the authors' FormalJudge implementation.

The paper links the authors' implementation at https://github.com/htlou/FormalJudge. This audit does not treat that external repository as local evidence.

## Source members used by the ledger

| Member | SHA-256 | Relevant content |
| --- | --- | --- |
| 00README.json | 567bffe7ca323817f2d4d89689bc3503ea28c9920162939f2384203f7c2ead04 | Source manifest and pdflatex/TeX Live metadata |
| example_paper.tex | c65b1fd98a3c7fa035772aa85558fb327bb0c4b96c6d101c651d749e702da017 | Title, authors, method, toy example, benchmark protocols, and reported results |
| example_paper.bib | 92cfcff675cc5e7292990a0e13f04d13aa0e094f4c68254c432af97748dbc8b9 | Bibliography used by the paper |
| icml2026.sty | 1db15769921c973f88ef66d6a07af765934558c4b86787c1da0720e88c6d2890 | ICML style file |

Line numbers in CLAIM_EVIDENCE.md refer to example_paper.tex in this pinned archive. They are source-audit pointers, not proof that the reported experiments ran locally.

## Paper production path

The paper's headline results require these layers:

1. Benchmark trajectories and ground-truth labels for Agent-SafetyBench, VitaBench, and Deceivers.
2. Frontier/API and local Qwen models for atomic fact extraction, specification synthesis, agent generation, and judging.
3. Context-aware atomic fact extraction from each relevant trajectory segment.
4. Dafny specification generation and Dafny/Boogie/Z3 execution with the stated timeout.
5. Formal verdict aggregation against benchmark labels and baseline outputs.
6. Iterative refinement loops that feed formal violations back to agents and measure three rounds.

This repository contains only the pinned paper, a source-feasibility audit, the original truncated contract, and a deterministic symbolic composition toy. Layers 1-6 are not independently reproduced here.

## Source versus local evidence

The paper source is primary evidence for what the authors describe and report. The local toy is independent evidence only for a narrow logical-composition boundary. The two evidence classes must not be conflated.
