#!/usr/bin/env python3
"""Test the dangerous_flags PreToolUse hook in every file that ships it.

The hook guards against a careless shortcut - skipping pre-commit hooks when
they are inconvenient - not against someone determined to evade it. So it must
block the forms anyone would actually reach for, including the ways of turning
hooks off that never name a flag, while leaving alone commands that merely
search for or document one.

KNOWN_GAPS records what is deliberately not caught. Those cases have to be
constructed on purpose, and closing them means reimplementing a shell inside a
YAML block scalar. They are asserted to pass so the boundary stays explicit:
if one starts blocking, that is a decision, not a drive-by change.

The detector body is extracted from the shipped YAML and executed through `sh`
exactly as the hook harness runs it, so block-scalar embedding and shell
escaping are covered too.
"""

from __future__ import annotations

import json
import pathlib
import re
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
MARKER = "HOOK_ENV ="

SHIPPED = {
    "claude_code": "roles/claude_code/defaults/main.yml",
    "antigravity": "roles/antigravity/defaults/main.yml",
    "host_vars": "playbooks/workstation/host_vars/MacBook-Pro-4/main.yml",
}

G = "git"
NV = "--no-verify"
NG = "--no-gpg-sign"
NPR = "--no-post-rewrite"
SQ = chr(39)
BS = chr(92)
BT = chr(96)
TAB = chr(9)

# (command, label) - every one of these must be blocked.
BLOCK = [
    (f'{G} commit -m "x" {NV}', "direct"),
    (f"{G} commit {NV} -F -", "flag before other arguments"),
    (f"{G} commit -n -m x", "short form"),
    (f"{G} commit {NG} -m x", "gpg flag"),
    (f"{G} rebase {NPR} main", "post-rewrite flag"),
    (f"/usr/bin/{G} commit {NV}", "absolute path"),
    (f'"{G}" commit {NV}', "quoted command name"),
    (f"{G}{TAB}commit{TAB}{NV}", "tab separated"),
    (f"{G} push --force && {G} commit {NV}", "second clause"),
    (f"echo x | {G} commit {NV} -F -", "after a pipe"),
    (f"{G} commit {NV}; echo done", "after a semicolon"),
    (f"({G} commit {NV})", "inside a subshell"),
    # Exec-style prefixes, none of them enumerated in the detector.
    (f"sudo {G} commit {NV}", "sudo"),
    (f"sudo -u dev {G} commit {NV}", "sudo with an option"),
    (f"env {G} commit {NV}", "env"),
    (f"nohup {G} commit {NV}", "nohup"),
    (f"timeout 5 {G} commit {NV}", "timeout"),
    (f"flock /tmp/{G}.lock {G} commit {NV}", "flock"),
    # Turning hooks off without ever naming a flag - the easier shortcut.
    (f"{G} -c core.hooksPath=/dev/null commit -m x", "hooksPath to /dev/null"),
    (f"{G} -c core.hooksPath=$(mktemp -d) commit -m x", "hooksPath to a temp dir"),
    (f"SKIP=all {G} commit -m x", "pre-commit SKIP"),
    (f"SKIP=ansible-lint {G} commit -m x", "pre-commit SKIP for one hook"),
    (f"HUSKY=0 {G} commit -m x", "husky disabled"),
    (f"PRE_COMMIT_ALLOW_NO_CONFIG=1 {G} commit -m x", "pre-commit config bypass"),
    # One level of wrapping, which still reads as habit rather than evasion.
    (f'bash -c "{G} commit {NV}"', "bash -c"),
    (f"sh -c {SQ}{G} commit {NV}{SQ}", "sh -c"),
    (f'bash -lc "{G} commit {NV}"', "bash -lc"),
    (f'eval "{G} commit {NV}"', "eval"),
    (f'sudo -u dev bash -c "{G} commit {NV}"', "wrapper behind an exec prefix"),
    # posix word joining puts this back together before the check sees it
    (f"{G} commit --no-verif{SQ}y{SQ}", "quote spliced into the flag"),
]

# (command, label) - none of these may be blocked.
ALLOW = [
    (f"rg -n -- {SQ}{NV}{SQ} --hidden -g {SQ}!.{G}{SQ} .", "ripgrep search"),
    (f"grep -rn {SQ}{NV}{SQ} roles/", "grep search"),
    (f"echo {SQ}never use {NV}{SQ} >> README.md", "documenting the flag"),
    (f"echo {SQ}{G} commit {NV} is banned{SQ} >> R.md", "documenting a whole command"),
    (f"{G} commit -m {SQ}note about {NV} policy{SQ}", "flag named in a commit message"),
    (f"{G} commit -m {SQ}add -n flag to the parser{SQ}", "-n inside a commit message"),
    (f"{G} log --oneline -n 5", "legitimate -n"),
    (f"{G} status --short", "plain status"),
    (f"{G} status && echo {NV} >> notes.md", "status then documenting the flag"),
    (f"rg {NV} $PWD && {G} status", "search with a variable, then status"),
    (f"{G} status && echo {NV} > $TMPDIR/n.md", "status then a doc file under a variable"),
    (f"rg {NV} . ; {G} status", "search then an unrelated status"),
    (f"sed -i {SQ}{SQ} {SQ}s/a/b/{SQ} roles/{G}hub/x.yml", "path containing the name"),
    ("ls -la", "unrelated command"),
    ("echo hello world", "no mention at all"),
    (f'bash -c "echo {SQ}{G} commit {NV} is banned{SQ}"', "doc line inside a wrapper"),
    (f'bash -c "rg -n -- {SQ}{NV}{SQ} ."', "search inside a wrapper"),
    (f'eval "echo {SQ}{G} commit {NV}{SQ}"', "eval echoing a doc line"),
    (f'python3 -c "print({SQ}never use {NV}{SQ})"', "python printing a doc line"),
    (f"SKIP=ansible-lint pre-commit run --all-files", "SKIP with no git invocation"),
    (f"SKIP=ansible-lint pre-commit run && {G} status", "SKIP in an unrelated clause"),
    ("cat README.md | sh", "unrelated pipe into a shell"),
]

# Deliberately not caught. Each has to be constructed on purpose, and catching
# them costs a hand-written shell. Asserted to pass so the boundary is explicit.
KNOWN_GAPS = [
    (f"{G} commit ${SQ}{NV}{SQ}", "ANSI-C quoted flag"),
    (f"g{BS}it commit {NV}", "escape spliced into the command name"),
    (f"{BT}{G} commit {NV}{BT}", "backtick substitution"),
    (f"{G} commit $(echo {NV})", "command substitution"),
    (f"echo {NV} | xargs {G} commit", "xargs from stdin"),
    (f'x={NV}; {G} commit "$x"', "flag stored in a variable"),
    (f"perl -we {SQ}system(\"{G} commit {NV}\"){SQ}", "perl payload"),
    (f"echo {SQ}{G} commit {NV}{SQ} | sh", "script piped into sh"),
    (f"bash -c {SQ}bash -c \"{G} commit {NV}\"{SQ}", "two levels of wrapping"),
]

# Positive control: the pre-fix substring scanner. It must fail the ALLOW
# matrix, otherwise that matrix cannot fail and proves nothing.
_LEGACY_BODY = """
import json, sys, re
d = json.load(sys.stdin)
cmd = d.get('tool_input', {}).get('command', '')
if 'GG' not in cmd:
    sys.exit(0)
f = next((x for x in ['VV', 'PP', 'RR'] if x in cmd), None)
if f:
    sys.stderr.write('BLOCKED: Cannot use ' + f)
    sys.exit(2)
sys.exit(0)
"""

LEGACY = "python3 -c " + chr(34) + (
    _LEGACY_BODY.replace("GG", G).replace("VV", NV).replace("PP", NG).replace("RR", NPR)
) + chr(34)


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
    """Pull the one `command:` block scalar holding the detector."""
    lines = (REPO / rel).read_text().split("\n")
    blocks = [
        block_at(lines, i)
        for i, line in enumerate(lines)
        if re.match(r"^\s*command:\s*\|\s*$", line)
    ]
    found = [b for b in blocks if MARKER in b]
    if len(found) != 1:
        raise SystemExit(f"{rel}: expected 1 detector block, found {len(found)}")
    return found[0]


def run_hook(body, cmd):
    """Execute the hook the way its harness does. True means it blocked.

    Claude Code passes `tool_input.command` and reads a block off exit 2;
    antigravity passes `toolCall.args` and reads a JSON decision on stdout.
    The detection core is shared, so both wire contracts get the same matrix.
    """
    json_protocol = "toolCall" in body
    payload = (
        {"toolCall": {"args": {"CommandLine": cmd}}}
        if json_protocol
        else {"tool_input": {"command": cmd}}
    )
    proc = subprocess.run(
        ["sh", "-c", body],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        timeout=30,
    )
    if json_protocol:
        try:
            return json.loads(proc.stdout.strip())["decision"] == "deny"
        except (ValueError, KeyError) as exc:
            raise SystemExit(f"hook returned no decision for {cmd!r}: {exc}")
    # `sh` also exits 2 on a syntax error, which would otherwise read as a block.
    if proc.returncode not in (0, 2):
        raise SystemExit(f"hook exited {proc.returncode} for {cmd!r}: {proc.stderr[:200]}")
    if proc.returncode == 2 and "Cannot use" not in proc.stderr:
        raise SystemExit(f"exit 2 without the hook message for {cmd!r}: {proc.stderr[:200]}")
    return proc.returncode == 2


def main():
    failures = []
    bodies = {name: extract(rel) for name, rel in SHIPPED.items()}

    # The detector is embedded in a `python3 -c "..."` shell string, so a bare
    # double quote anywhere in it would close that string early.
    for name, body in bodies.items():
        tail = body[body.index(MARKER):].split(chr(10))
        # the lone trailing quote is the legitimate close of `python3 -c "`
        detector = chr(10).join(x for x in tail if x.strip() != chr(34))
        for ch, what in ((chr(34), "double quote"), (BT, "backtick")):
            if ch in detector:
                failures.append(f"{name}: detector body contains a bare {what}")

    for name, body in bodies.items():
        for cmd, label in BLOCK:
            if not run_hook(body, cmd):
                failures.append(f"{name}: not blocked - {label}")
        for cmd, label in ALLOW:
            if run_hook(body, cmd):
                failures.append(f"{name}: false positive - {label}")
        for cmd, label in KNOWN_GAPS:
            if run_hook(body, cmd):
                failures.append(
                    f"{name}: KNOWN_GAPS case now blocks - {label}. If that is "
                    f"intended, move it into BLOCK."
                )

    for cmd, label in BLOCK + ALLOW + KNOWN_GAPS:
        verdicts = {name: run_hook(body, cmd) for name, body in bodies.items()}
        if len(set(verdicts.values())) != 1:
            failures.append(f"copies disagree on {label}: {verdicts}")

    legacy_fp = [lbl for cmd, lbl in ALLOW if run_hook(LEGACY, cmd)]
    if not legacy_fp:
        failures.append("control: substring scanner cleared ALLOW, so it cannot fail")

    if failures:
        for line in failures:
            print(f"FAIL {line}", file=sys.stderr)
        print(f"{len(failures)} failure(s)", file=sys.stderr)
        return 1

    print(
        f"dangerous_flags OK: {len(BLOCK)} blocked + {len(ALLOW)} allowed + "
        f"{len(KNOWN_GAPS)} known gaps across {len(bodies)} shipped copies; "
        f"substring control fails {len(legacy_fp)} of the allowed cases"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
