#!/usr/bin/env python3
"""Test the retry loop in the Molecule workflow's full_test step.

The step re-runs `molecule test` only when the failed run's output matches a
pattern of known-transient errors, and it streams that output through `tee`.
Both are easy to break silently: a pattern that misses a transient error fails
the job on a flake (a Docker API "Read timed out." in the destroy step did
exactly that), and a pipeline that reports tee's exit status instead of
molecule's turns every failure green.

The step's script is extracted from the shipped workflow and run under
`bash -eo pipefail`, the way GitHub runs `shell: bash`, with a stub `molecule`
that replays each scenario's attempts. Failure text is copied from real runs.
"""

from __future__ import annotations

import os
import pathlib
import re
import subprocess
import sys
import tempfile

REPO = pathlib.Path(__file__).resolve().parent.parent
WORKFLOW = REPO / ".github/workflows/molecule.yaml"
MARKER = "max_attempts=3"

DOCKER_READ_TIMEOUT = """\
  │ [ERROR]: Task failed: Module failed: Error removing container
  │   ce713da3497569252fca0c83c1a9ba5211ba5eb340781f7f151e3a35ef8e2138:
  │   UnixHTTPConnectionPool(host='localhost', port=None): Read timed out.
  │   (read timeout=60)"""
IDEMPOTENCE = """\
CRITICAL Idempotence test failed because of the following tasks:
*  => cowdogmoo.workstation.shell_functions : Maintain cached clone of dotfiles repo"""
RATE_LIMIT = """\
  │ [ERROR]: Task failed: Module failed: Status code was 403 and not [200]:
  │   HTTP Error 403: rate limit exceeded"""
CONNECTION_RESET = "curl: (56) Recv failure: Connection reset by peer"

# (label, [(exit code, output) per attempt], expected exit, expected attempts)
SCENARIOS = [
    ("passes first time", [(0, "ok")], 0, 1),
    ("Docker API read timeout is retried", [(1, DOCKER_READ_TIMEOUT), (0, "ok")], 0, 2),
    ("idempotence failure is not retried", [(2, IDEMPOTENCE)], 1, 1),
    ("API rate limit is not retried", [(2, RATE_LIMIT)], 1, 1),
    ("transient failure gives up after 3", [(1, CONNECTION_RESET)] * 3, 1, 3),
]

STUB_MOLECULE = """\
#!/usr/bin/env bash
case "$1" in --version | list) exit 0 ;; esac
n=$(($(cat "$STUB_DIR/count" 2>/dev/null || echo 0) + 1))
echo "$n" >"$STUB_DIR/count"
cat "$STUB_DIR/out.$n"
exit "$(cat "$STUB_DIR/rc.$n")"
"""


def extract_script() -> str:
    """Return the dedented `run: |` body of the step that holds MARKER."""
    lines = WORKFLOW.read_text().splitlines()
    marker = next(i for i, line in enumerate(lines) if MARKER in line)
    start = next(i for i in range(marker, -1, -1) if lines[i].strip() == "run: |")
    indent = re.match(r"\s*", lines[start + 1]).group()
    body = []
    for line in lines[start + 1 :]:
        if line.strip() and not line.startswith(indent):
            break
        body.append(line[len(indent) :])
    return "\n".join(body) + "\n"


def run(script: str, attempts: list[tuple[int, str]]) -> tuple[int, int, str]:
    """Run the step against a stub molecule; return (exit, attempts, output)."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = pathlib.Path(tmp)
        bin_dir = tmp_path / "bin"
        bin_dir.mkdir()
        stubs = {
            "molecule": STUB_MOLECULE,
            "docker": "#!/bin/sh\nexit 0\n",
            "sleep": "#!/bin/sh\nexit 0\n",
        }
        for name, body in stubs.items():
            stub = bin_dir / name
            stub.write_text(body)
            stub.chmod(0o755)
        for n, (rc, out) in enumerate(attempts, start=1):
            (tmp_path / f"rc.{n}").write_text(str(rc))
            (tmp_path / f"out.{n}").write_text(out + "\n")
        step = tmp_path / "step.sh"
        step.write_text(script)
        env = dict(
            os.environ, PATH=f"{bin_dir}{os.pathsep}{os.environ['PATH']}", STUB_DIR=tmp
        )
        proc = subprocess.run(
            ["bash", "--noprofile", "--norc", "-eo", "pipefail", str(step)],
            cwd=tmp,
            env=env,
            capture_output=True,
            text=True,
            timeout=60,
        )
        count = tmp_path / "count"
        made = int(count.read_text()) if count.exists() else 0
        return proc.returncode, made, proc.stdout


def main() -> int:
    failures = []

    script = extract_script()
    for label, attempts, want_rc, want_attempts in SCENARIOS:
        rc, made, stdout = run(script, attempts)
        if rc != want_rc or made != want_attempts:
            failures.append(
                f"{label}: exit {rc} after {made} attempt(s), "
                f"want exit {want_rc} after {want_attempts}"
            )
        if made > len(attempts):
            failures.append(
                f"{label}: molecule ran {made} time(s) but the scenario "
                f"defines only {len(attempts)} attempt(s)"
            )
            continue
        last_output = attempts[max(made, 1) - 1][1]
        if last_output.splitlines()[0] not in stdout:
            failures.append(f"{label}: molecule output missing from the step log")

    if failures:
        for line in failures:
            print(f"FAIL {line}", file=sys.stderr)
        print(f"{len(failures)} failure(s)", file=sys.stderr)
        return 1

    print(f"molecule retry OK: {len(SCENARIOS)} scenarios")
    return 0


if __name__ == "__main__":
    sys.exit(main())
