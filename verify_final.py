import hashlib
import json
import subprocess
import tarfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPOSITORY = "MachineLearning-Nerd/icml26-formaljudge-neurosymbolic-oversight"
FORMER_REPOSITORY = "MachineLearning-Nerd/icml26-repro-tnsQ23imeD-formaljudge-neurosymbolic-oversight"
ALLOWED_EMAILS = {
    "MachineLearning-Nerd@users.noreply.github.com",
    "37579156+MachineLearning-Nerd@users.noreply.github.com",
}
REQUIRED_FILES = {
    "README.md",
    "STATUS.md",
    "AUTONOMOUS_STATE.json",
    "contract/live_claims.json",
    "contract/SOURCE_SNAPSHOT.json",
    "CLAIM_EVIDENCE.md",
    "SOURCE_AUDIT.md",
    "ENVIRONMENT.md",
    "REPORT.md",
    "AUTHOR_THANK_YOU.md",
    "CITATION.cff",
    "BRANCH_AUDIT.md",
    "branch-audit.md",
    "claims.json",
    "EVIDENCE_MANIFEST.json",
    "verify_final.py",
}


def fail(message):
    raise SystemExit("FINAL_AUDIT=FAILED " + message)


def git(*args):
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if result.returncode:
        fail("git_" + args[0] + "=" + result.stderr.strip().replace("\n", " "))
    return result.stdout.strip()


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_sha(path, expected):
    if not path.is_file():
        fail("missing=" + str(path.relative_to(ROOT)))
    actual = sha256(path)
    if actual != expected:
        fail("sha256=" + str(path.relative_to(ROOT)) + ":" + actual)


def read_json(relative):
    path = ROOT / relative
    try:
        return json.loads(path.read_text())
    except Exception as exc:
        fail("invalid_json=" + relative + ":" + str(exc))


def check_checksum_file(relative):
    checksum_path = ROOT / relative
    for line in checksum_path.read_text().splitlines():
        if not line.strip():
            continue
        expected, name = line.split("  ", 1)
        check_sha(checksum_path.parent / name, expected)


if git("status", "--porcelain", "--untracked-files=all"):
    fail("working_tree_not_clean")
if git("branch", "--show-current") != "main":
    fail("current_branch_not_main")

local_branches = set(
    filter(
        None,
        git("for-each-ref", "--format=%(refname:short)", "refs/heads").splitlines(),
    )
)
if local_branches != {"main"}:
    fail("local_branches=" + repr(sorted(local_branches)))

stale_refs = git(
    "for-each-ref", "--format=%(refname)", "refs/original"
).splitlines()
if stale_refs:
    fail("stale_refs=" + repr(stale_refs))

remote_url = git("remote", "get-url", "origin").removesuffix(".git")
if remote_url not in {
    "https://github.com/" + REPOSITORY,
    "git@github.com:" + REPOSITORY,
}:
    fail("remote=" + remote_url)

remote_heads = git("ls-remote", "--heads", "origin").splitlines()
if len(remote_heads) != 1 or not remote_heads[0].endswith("\trefs/heads/main"):
    fail("remote_heads=" + repr(remote_heads))

head = git("rev-parse", "HEAD")
commits = git(
    "log",
    "main",
    "--format=%an%x09%ae%x09%cn%x09%ce%x09%s",
).splitlines()
if len(commits) < 6:
    fail("commit_count=" + str(len(commits)))
for record in commits:
    fields = record.split("\t", 4)
    if len(fields) != 5:
        fail("malformed_commit_record")
    author_name, author_email, committer_name, committer_email, subject = fields
    if author_name != "MachineLearning-Nerd" or committer_name != "MachineLearning-Nerd":
        fail("commit_identity=" + record)
    if author_email not in ALLOWED_EMAILS or committer_email not in ALLOWED_EMAILS:
        fail("commit_email=" + record)
    if "co-authored-by:" in subject.lower():
        fail("coauthor_trailer=" + subject)

state = read_json("AUTONOMOUS_STATE.json")
if state.get("phase") != "published_and_verified":
    fail("state_phase=" + repr(state.get("phase")))
if state.get("next_action") != "select_next_icml_repository":
    fail("state_next_action=" + repr(state.get("next_action")))
if state.get("publication_allowed") is not False:
    fail("publication_allowed")
if state.get("github_repository") != "https://github.com/" + REPOSITORY:
    fail("state_repository")
if state.get("former_github_repository") != "https://github.com/" + FORMER_REPOSITORY:
    fail("state_former_repository")
if state.get("branch_set") != ["main"]:
    fail("state_branches")
if state.get("overall_verdict") != "INCONCLUSIVE_SCOPED_TO_SOURCE_AND_BOUNDED_TOY":
    fail("state_verdict")
if state.get("claim_statuses") != {
    "C1": "unverified",
    "C2": "unverified",
    "C3": "unverified",
    "C4": "unverified",
    "C5": "toy_source_audit",
}:
    fail("state_claim_statuses")
checkpoint = state.get("last_known_git_commit")
if not isinstance(checkpoint, str) or subprocess.run(
    ["git", "merge-base", "--is-ancestor", checkpoint, head],
    cwd=ROOT,
).returncode:
    fail("state_checkpoint_not_ancestor")

claims = read_json("claims.json")
if claims.get("repository") != REPOSITORY:
    fail("claims_repository")
if claims.get("former_repository") != FORMER_REPOSITORY:
    fail("claims_former_repository")
if claims.get("overall_verdict") != state.get("overall_verdict"):
    fail("claims_verdict")
if claims.get("publication_allowed") is not False:
    fail("claims_publication")
if claims.get("original_contract", {}).get("claim_count") != 1:
    fail("original_contract")
if [claim.get("id") for claim in claims.get("claims", [])] != [
    "C1",
    "C2",
    "C3",
    "C4",
    "C5",
]:
    fail("claim_ids")

contract = read_json("contract/live_claims.json")
if contract.get("orid") != "tnsQ23imeD":
    fail("claim_contract_id")
if contract.get("claim_count") != 1 or len(contract.get("claims", [])) != 1:
    fail("claim_contract_count")
if "Claude-4.5-Opus" not in contract["claims"][0].get("text", ""):
    fail("claim_contract_text")

required_missing = [
    name for name in REQUIRED_FILES if not (ROOT / name).is_file()
]
if required_missing:
    fail("missing_required=" + repr(sorted(required_missing)))

check_checksum_file("evidence/source/SHA256SUMS")
check_checksum_file("outputs/claim1_source_audit/SHA256SUMS")
check_checksum_file("outputs/claim1_symbolic_trip_toy/SHA256SUMS")
check_sha(
    ROOT / "evidence/source/arxiv-2602.11136-source.tar.gz",
    "48387dc382f94be29a51e2570e3f57ed05b49ee93272a1940028468e9542fff8",
)
check_sha(
    ROOT / "evidence/source/arxiv-2602.11136.pdf",
    "b635896b5f22a51bfe4ca59aa3c0d3b9141353a34426f0d5c00f664b22ac76af",
)

with tarfile.open(ROOT / "evidence/source/arxiv-2602.11136-source.tar.gz") as archive:
    members = archive.getmembers()
regular_members = [member for member in members if member.isfile()]
directory_members = [member for member in members if member.isdir()]
if len(regular_members) != 14 or len(directory_members) != 1:
    fail(
        "source_members=regular:"
        + str(len(regular_members))
        + ",directories:"
        + str(len(directory_members))
    )
if any(member.mode & 0o111 for member in regular_members):
    fail("executable_source_member")

toy = read_json("outputs/claim1_symbolic_trip_toy/summary.json")
if toy.get("n_cases") != 3:
    fail("toy_case_count")
if toy.get("accuracy_against_constructed_labels") != 1.0:
    fail("toy_accuracy")
if toy.get("source_case_detected") is not True:
    fail("toy_source_case")
if toy.get("verdict") != "toy":
    fail("toy_verdict")

source_audit = read_json("outputs/claim1_source_audit/summary.json")
if source_audit.get("verdict") != "inconclusive":
    fail("source_audit_verdict")

readme = (ROOT / "README.md").read_text()
for phrase in (
    "FormalJudge",
    "tnsQ23imeD",
    "CITATION",
    "Thank you",
    "publication_allowed",
    "claims.json",
    "main",
):
    if phrase not in readme:
        fail("readme_phrase=" + phrase)

manifest = read_json("EVIDENCE_MANIFEST.json")
entries = manifest.get("files")
if not isinstance(entries, list):
    fail("manifest_files")
manifest_paths = [entry.get("path") for entry in entries]
if len(manifest_paths) != len(set(manifest_paths)):
    fail("manifest_duplicate")
tracked = set(filter(None, git("ls-files", "-z").split("\0")))
expected_manifest = tracked - {"AUTONOMOUS_STATE.json", "EVIDENCE_MANIFEST.json"}
if set(manifest_paths) != expected_manifest:
    fail(
        "manifest_paths_missing="
        + repr(sorted(expected_manifest - set(manifest_paths)))
        + ",extra="
        + repr(sorted(set(manifest_paths) - expected_manifest))
    )
for entry in entries:
    path = entry.get("path")
    digest = entry.get("sha256")
    if not isinstance(path, str) or not isinstance(digest, str):
        fail("manifest_entry")
    check_sha(ROOT / path, digest)

print(
    "FINAL_AUDIT=VERIFIED "
    + "branches="
    + str(len(local_branches))
    + " commits="
    + str(len(commits))
    + " claims=C1:unverified,C2:unverified,C3:unverified,C4:unverified,C5:toy_source_audit "
    + "publication_allowed=false"
)
