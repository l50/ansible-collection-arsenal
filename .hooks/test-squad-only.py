#!/usr/bin/env python3
"""Test the squad-only rule in every forbidden_content hook that ships it.

Commits and pull request titles and bodies come only from squad_commit and
squad_pr. The hook must deny every command an agent would actually reach for to
write that text itself - a raw commit, an amend, gh or gh-axi pr create/edit,
gh api writes to a pulls endpoint - while allowing squad_commit, squad_pr, and
read-only git and gh commands, plus the attribution guard it already carried.

The one exemption is `git commit --no-edit` while a merge is in progress: it is
how the no-mistakes pipeline's agent concludes a merge-strategy conflict, and it
carries git's own message rather than hand-written text. It is exercised in a
real repository with and without MERGE_HEAD.

KNOWN_GAPS records what is deliberately not caught. Each has to be constructed
on purpose; they are asserted to pass so the boundary stays explicit.

The claude_code and antigravity roles ship the same detector behind different
wire contracts. Each body is extracted from its shipped YAML and executed
through `sh` exactly as its harness runs it, so block-scalar embedding and shell
escaping are covered too, and every case must get the same verdict from both.
"""

from __future__ import annotations

import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile

REPO = pathlib.Path(__file__).resolve().parent.parent
SHIPPED = {
    "claude_code": "roles/claude_code/defaults/main.yml",
    "antigravity": "roles/antigravity/defaults/main.yml",
}
MARKER = "SQUAD_ONLY ="

G = "git"
SQ = chr(39)
DQ = chr(34)
BT = chr(96)
PULLS = "repos/{owner}/{repo}/pulls"

# (command, label) - every one of these must be denied.
DENY = [
    (f"{G} commit -m {SQ}fix: thing{SQ}", "raw commit"),
    (f"{G} commit -F /tmp/msg", "commit from a file"),
    (f"{G} commit -m {DQ}$(cat /tmp/msg) {BT}date{BT}{DQ}", "commit with quotes and substitutions"),
    (f"printf {SQ}fix{SQ} | {G} commit -F -", "commit from a pipe"),
    (f"{G} commit", "editor commit"),
    (f"{G} commit --amend --no-edit", "amend without a merge"),
    (f"{G} commit --amend -m x", "amend with a message"),
    (f"{G} commit --no-edit", "--no-edit with no merge in progress"),
    (f"{G} commit -am x", "commit all"),
    (f"{G} -C /tmp commit -m x", "-C before the subcommand"),
    (f"{G} -c user.name=x commit -m x", "-c before the subcommand"),
    (f"/usr/bin/{G} commit -m x", "absolute path"),
    (f"GIT_EDITOR=true {G} commit", "env prefix"),
    (f"sudo {G} commit -m x", "sudo"),
    (f"{G} add -A && {G} commit -m x", "after git add"),
    (f"squad_commit; {G} commit --amend -m x", "amend after squad_commit"),
    (f"({G} commit -m x)", "inside a subshell"),
    (f'bash -c "{G} commit -m x"', "bash -c"),
    (f'eval "{G} commit -m x"', "eval"),
    (f"{G} commit-tree HEAD^{{tree}} -m x", "commit-tree"),
    ("gh pr create --title x --body y", "gh pr create"),
    ("gh pr create --fill", "gh pr create --fill"),
    ("gh pr new -t x -b y", "gh pr new"),
    ("gh pr create -t x -F body.md", "gh pr create from a file"),
    ("gh pr edit 12 --title x", "gh pr edit title"),
    ("gh pr edit --body y", "gh pr edit body"),
    ("gh pr edit 12 -b y", "gh pr edit short body"),
    ("gh pr edit 12 --body-file b.md", "gh pr edit body file"),
    ("gh pr edit 12 --title=x", "gh pr edit title with ="),
    ("gh-axi pr create --title x --body y", "gh-axi pr create"),
    ("gh-axi pr edit 12 --body y", "gh-axi pr edit body"),
    (f"gh api {PULLS} -f title=x -f head=b -f base=main", "gh api fields default to POST"),
    (f"gh api -X POST {PULLS} --input body.json", "gh api -X POST"),
    (f"gh api --method PATCH {PULLS}/12 -f body=y", "gh api PATCH pull"),
    (f"gh api /{PULLS}/12 -X PATCH -f title=x", "gh api leading slash"),
    (f"gh-axi api POST /{PULLS} --field title=x", "gh-axi api POST"),
    (f"gh-axi api PATCH /{PULLS}/12 --raw-field body=y", "gh-axi api PATCH"),
    ("gh api graphql -f query=" + SQ + "mutation { updatePullRequest(input: {}) { clientMutationId } }" + SQ,
     "graphql updatePullRequest"),
    (f'bash -c "gh pr edit 12 --body y"', "gh inside a wrapper"),
    (f"{G} merge -m {SQ}hand text{SQ} feature", "merge with a message"),
    (f"{G} merge --message=x feature", "merge --message="),
    (f"{G} merge -F msg.txt feature", "merge message from a file"),
    (f"{G} merge --file=msg.txt feature", "merge --file="),
    (f"{G} merge --no-edit -m x feature", "merge --no-edit with a message"),
    (f"{G} merge --edit feature", "merge with an edited message"),
    (f"{G} revert --no-edit HEAD", "revert"),
    (f"{G} revert HEAD", "revert with its default message"),
    (f"{G} revert -m 1 HEAD", "revert -m is mainline, not --no-commit"),
    (f"{G} revert -n -e HEAD", "revert --no-commit with --edit"),
    (f"{G} cherry-pick 0123abc", "cherry-pick"),
    (f"{G} cherry-pick -x 0123abc", "cherry-pick -x"),
    (f"{G} cherry-pick --edit 0123abc", "cherry-pick --edit"),
    (f'{G} rebase -x "{G} commit --amend -m x" HEAD~1', "rebase -x"),
    (f"{G} rebase --exec=true main", "rebase --exec="),
    ("gh pr merge 12 --squash --subject x --body y", "gh pr merge subject and body"),
    ("gh pr merge 12 --squash -t x", "gh pr merge -t"),
    ("gh pr merge 12 --body-file=b.md", "gh pr merge body file"),
    ("gh-axi pr merge 12 --squash --body y", "gh-axi pr merge body"),
    (f"gh api -X PUT {PULLS}/12/merge -f commit_title=x -f commit_message=y", "gh api merge with commit text"),
    ("gh api graphql -f query=" + SQ + "mutation { mergePullRequest(input: {commitHeadline: x}) { clientMutationId } }" + SQ,
     "graphql mergePullRequest with a headline"),
    (f"cat > NOTES.md <<EOF\nfine\nEOF\n{G} commit -m x", "commit after a heredoc"),
]

SEQUENCER_DENY = [cmd for cmd, _ in DENY if f"{G} revert" in cmd or f"{G} cherry-pick" in cmd]

# (command, label) - none of these may be denied.
ALLOW = [
    ("squad_commit", "squad_commit"),
    ("squad_pr", "squad_pr"),
    ("cd /tmp && squad_commit", "squad_commit after cd"),
    (f"{G} add -A && squad_commit", "squad_commit after git add"),
    ("squad_commit && squad_pr", "squad_commit then squad_pr"),
    (f"{G} ds | squad_gen commit", "previewing the generated message"),
    (f"{G} status --short", "git status"),
    (f"{G} log --oneline -n 5", "git log"),
    (f"{G} diff main...HEAD", "git diff"),
    (f"{G} show HEAD --stat", "git show"),
    (f"{G} log -1 --format=%B", "reading a commit message"),
    (f"{G} rebase --continue", "rebase --continue"),
    (f"{G} merge --continue", "merge --continue"),
    (f"{G} merge feature", "plain merge"),
    (f"{G} merge --no-edit feature", "merge --no-edit"),
    (f"{G} pull --no-rebase origin main", "git pull"),
    (f"{G} rebase main", "plain rebase"),
    (f"{G} rebase --skip", "rebase --skip"),
    (f"{G} rebase --abort", "rebase --abort"),
    (f"{G} revert -n HEAD", "revert -n"),
    (f"{G} revert --no-commit -m 1 HEAD", "revert --no-commit with mainline"),
    (f"{G} revert --continue", "revert --continue"),
    (f"{G} revert --abort", "revert --abort"),
    (f"{G} cherry-pick --no-commit 0123abc && squad_commit", "cherry-pick --no-commit then squad_commit"),
    (f"{G} cherry-pick --skip", "cherry-pick --skip"),
    (f"{G} cherry-pick --quit", "cherry-pick --quit"),
    ("gh pr merge 12 --squash --delete-branch", "gh pr merge with GitHub's message"),
    ("gh-axi pr merge 12 --squash", "gh-axi pr merge with GitHub's message"),
    (f"cat > NOTES.md <<{SQ}EOF{SQ}\nNever run {G} commit by hand; use squad_commit.\nEOF", "heredoc documenting git commit"),
    (f"cat <<-EOF > NOTES.md\n\tgh pr create and gh pr edit --body are squad_pr's job\n\tEOF\n{G} status", "<<- heredoc then a command"),
    (f"{G} push -u origin HEAD", "git push"),
    (f"{G} add -A", "git add"),
    (f"{G} -C /tmp status", "git -C status"),
    ("gh pr view 12", "gh pr view"),
    ("gh pr view --json title,body", "gh pr view json"),
    ("gh pr list --state open", "gh pr list"),
    ("gh pr checks 12", "gh pr checks"),
    ("gh pr diff 12", "gh pr diff"),
    ("gh pr edit 12 --add-label bug", "gh pr edit label only"),
    ("gh pr ready 12", "gh pr ready"),
    ("gh run list", "gh run list"),
    ("gh-axi pr view 12", "gh-axi pr view"),
    ("gh-axi pr checks 12", "gh-axi pr checks"),
    (f"gh api {PULLS}", "gh api GET pulls"),
    (f"gh api {PULLS}/12 --jq .body", "gh api GET one pull"),
    (f"gh api -X GET {PULLS} -f state=open", "gh api explicit GET with fields"),
    (f"gh api -X POST {PULLS}/12/comments -f body=x", "gh api review comment"),
    (f"gh api -X PUT {PULLS}/12/merge", "gh api merge"),
    ("gh-axi api /" + PULLS, "gh-axi api GET pulls"),
    (f"rg -n {SQ}{G} commit{SQ} roles/", "searching for git commit"),
    (f"rg -n {DQ}gh pr create{DQ} .", "searching for gh pr create"),
    (f"echo {SQ}never run {G} commit by hand{SQ} >> README.md", "documenting the rule"),
    (f'bash -c "echo {SQ}{G} commit{SQ}"', "doc line inside a wrapper"),
    (f'python3 -c "print({SQ}{G} commit{SQ})"', "python printing a doc line"),
    ("ls -la", "unrelated command"),
    (f"echo {DQ}$(date) {BT}whoami{BT}{DQ} > out.txt", "quotes and substitutions outside git"),
]

# Deliberately not caught: each has to be constructed to slip past.
KNOWN_GAPS = [
    (f"{G} ci -m x", "git alias for commit"),
    (f"{BT}echo {G}{BT} commit -m x", "backtick substitution"),
    (f"$(echo {G}) commit -m x", "command substitution"),
    (f"bash -c {SQ}bash -c {DQ}{G} commit -m x{DQ}{SQ}", "two levels of wrapping"),
    (f"echo {SQ}{G} commit -m x{SQ} | sh", "script piped into sh"),
    ("curl -X PATCH https://api.github.com/repos/o/r/pulls/1 -d @b.json", "curl to the API"),
    ("gh api -X PATCH repos/{owner}/{repo}/issues/12 -f body=y", "PR body through the issues endpoint"),
    (f"sh <<EOF\n{G} commit -m x\nEOF", "script fed to sh through a heredoc"),
]

# Attribution must still be blocked on commands the squad rule does not deny.
ATTRIBUTION = [
    ("gh pr comment 12 --body " + SQ + "Generated with Claude Code" + SQ, "attribution in a PR comment"),
    (f"{G} tag -a v1 -m {SQ}Co-Authored-By: Claude{SQ}", "attribution in a tag"),
]


def block_at(lines, start):
    """Return the dedented body of the block scalar opened on line `start`."""
    base = len(lines[start]) - len(lines[start].lstrip())
    body = []
    for line in lines[start + 1:]:
        if not line.strip():
            body.append("")
            continue
        if len(line) - len(line.lstrip()) <= base:
            break
        body.append(line)
    cut = min(len(x) - len(x.lstrip()) for x in body if x.strip())
    return "\n".join(x[cut:] for x in body)


def extract(rel):
    """Pull the one `command:` block scalar holding the squad-only rule."""
    lines = (REPO / rel).read_text().split("\n")
    blocks = [
        block_at(lines, i)
        for i, line in enumerate(lines)
        if re.match(r"^\s*command:\s*\|\s*$", line)
    ]
    found = [b for b in blocks if MARKER in b]
    if len(found) != 1:
        raise SystemExit(f"{rel}: expected 1 squad-only block, found {len(found)}")
    return found[0]


def run_hook(body, cmd, cwd):
    """Run the hook the way its harness does. Returns (2 if denied else 0, message).

    Claude Code passes `tool_input.command` plus `cwd` and reads a block off exit 2;
    antigravity passes `toolCall.args` (CommandLine, Cwd) and reads a JSON decision
    on stdout, failing closed on anything else. Both are normalized to one verdict.
    """
    json_protocol = "toolCall" in body
    payload = (
        {"toolCall": {"name": "run_command", "args": {"CommandLine": cmd, "Cwd": cwd}}}
        if json_protocol
        else {"tool_input": {"command": cmd}, "cwd": cwd}
    )
    proc = subprocess.run(
        ["sh", "-c", body],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        timeout=30,
    )
    if json_protocol:
        if proc.returncode != 0:
            raise SystemExit(f"hook exited {proc.returncode} for {cmd!r}: {proc.stderr[:300]}")
        try:
            out = json.loads(proc.stdout.strip())
        except ValueError as exc:
            raise SystemExit(f"hook returned no JSON decision for {cmd!r}: {exc}")
        if out.get("decision") == "deny":
            if "BLOCKED" not in out.get("reason", ""):
                raise SystemExit(f"deny without the hook message for {cmd!r}: {out}")
            return 2, out["reason"]
        if out != {"decision": "allow"}:
            raise SystemExit(f"hook neither allowed nor denied {cmd!r}: {out}")
        return 0, ""
    # `sh` also exits 2 on a syntax error, which would otherwise read as a block.
    if proc.returncode not in (0, 2):
        raise SystemExit(f"hook exited {proc.returncode} for {cmd!r}: {proc.stderr[:300]}")
    if proc.returncode == 2 and "BLOCKED" not in proc.stderr:
        raise SystemExit(f"exit 2 without the hook message for {cmd!r}: {proc.stderr[:300]}")
    return proc.returncode, proc.stderr


def git(repo, *args):
    env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@example.com",
               GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@example.com")
    return subprocess.run([G, "-C", repo, *args], capture_output=True, text=True, env=env)


def conflicted_merge(root):
    """A repository stopped in a conflicted merge, so MERGE_HEAD exists."""
    repo = os.path.join(root, "repo")
    os.makedirs(repo)
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "commit.gpgsign", "false")
    pathlib.Path(repo, "f").write_text("base\n")
    git(repo, "add", "f")
    git(repo, "commit", "-q", "-m", "base")
    git(repo, "checkout", "-q", "-b", "side")
    pathlib.Path(repo, "f").write_text("side\n")
    git(repo, "commit", "-q", "-am", "side")
    git(repo, "checkout", "-q", "main")
    pathlib.Path(repo, "f").write_text("main\n")
    git(repo, "commit", "-q", "-am", "main")
    git(repo, "merge", "side")
    if git(repo, "rev-parse", "-q", "--verify", "MERGE_HEAD").returncode != 0:
        raise SystemExit("fixture: merge did not stop with MERGE_HEAD")
    return repo


def check_copy(name, body, root, verdicts):
    """Run the whole matrix against one shipped copy; record each verdict."""
    failures = []

    def verdict(cmd, cwd, label):
        rc, err = run_hook(body, cmd, cwd)
        verdicts.setdefault(label, {})[name] = rc
        return rc, err

    plain = os.path.join(root, "plain")
    os.makedirs(plain, exist_ok=True)

    for cmd, label in DENY:
        rc, err = verdict(cmd, plain, label)
        if rc != 2:
            failures.append(f"{name}: not denied - {label}")
        elif "squad_commit or squad_pr" not in err:
            failures.append(f"{name}: deny message does not name squad_commit or squad_pr - {label}")
        elif cmd in SEQUENCER_DENY and "--no-commit (-n), then squad_commit" not in err:
            failures.append(f"{name}: deny message does not point at --no-commit - {label}")
    for cmd, label in ALLOW:
        rc, err = verdict(cmd, plain, label)
        if rc != 0:
            failures.append(f"{name}: false positive - {label}: {err.strip()[:120]}")
    for cmd, label in KNOWN_GAPS:
        if verdict(cmd, plain, label)[0] != 0:
            failures.append(f"{name}: KNOWN_GAPS case now denied - {label}. If intended, move it into DENY.")
    for cmd, label in ATTRIBUTION:
        rc, err = verdict(cmd, plain, label)
        if rc != 2 or "forbidden content" not in err:
            failures.append(f"{name}: attribution not blocked - {label}")

    # The merge exemption: only the exact conclusion, only mid-merge.
    repo = conflicted_merge(os.path.join(root, name))
    merge_cases = [
        (f"{G} commit --no-edit", 0, "concluding a merge with --no-edit"),
        (f"{G} add f && {G} commit --no-edit", 0, "stage then conclude"),
        (f"{G} commit --no-edit -q", 0, "quiet conclusion"),
        (f"{G} commit -m x", 2, "hand-written message mid-merge"),
        (f"{G} commit --no-edit -m x", 2, "--no-edit plus a message mid-merge"),
        (f"{G} commit --amend --no-edit", 2, "amend mid-merge"),
        (f"cd {repo} && {G} commit --no-edit", 0, "cd into the merging repo"),
        (f"{G} -C {repo} commit --no-edit", 0, "git -C into the merging repo"),
    ]
    for cmd, want, label in merge_cases:
        cwd = plain if cmd.startswith(("cd ", f"{G} -C ")) else repo
        if verdict(cmd, cwd, "merge: " + label)[0] != want:
            failures.append(f"{name}: merge exemption wrong - {label}")
    return failures


def main():
    failures = []
    bodies = {name: extract(rel) for name, rel in SHIPPED.items()}
    verdicts = {}

    with tempfile.TemporaryDirectory() as root:
        for name, body in bodies.items():
            failures.extend(check_copy(name, body, root, verdicts))

        # Antigravity may omit Cwd; the hook then falls back to the workspace root.
        repo = os.path.join(root, "antigravity", "repo")
        payload = {"toolCall": {"name": "run_command", "args": {"CommandLine": f"{G} commit --no-edit"}},
                   "workspacePaths": [repo]}
        proc = subprocess.run(["sh", "-c", bodies["antigravity"]], input=json.dumps(payload),
                              capture_output=True, text=True, timeout=30)
        if proc.stdout.strip() != json.dumps({"decision": "allow"}):
            failures.append(f"antigravity: merge exemption ignores workspacePaths: {proc.stdout.strip()}")
        gemini = f"{G} tag -a v1 -m {SQ}Co-Authored-By: Gemini{SQ}"
        rc, err = run_hook(bodies["antigravity"], gemini, root)
        if rc != 2 or "forbidden content" not in err:
            failures.append("antigravity: Gemini attribution not blocked")

    for label, seen in verdicts.items():
        if len(set(seen.values())) != 1:
            failures.append(f"copies disagree on {label}: {seen}")

    if failures:
        for line in failures:
            print(f"FAIL {line}", file=sys.stderr)
        print(f"{len(failures)} failure(s)", file=sys.stderr)
        return 1

    print(
        f"squad-only OK: {len(DENY)} denied + {len(ALLOW)} allowed + "
        f"{len(KNOWN_GAPS)} known gaps + {len(ATTRIBUTION)} attribution + merge exemption "
        f"across {len(bodies)} shipped copies"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
