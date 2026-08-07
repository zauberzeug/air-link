# AI Agent Guidelines for Air Link

This file gives AI assistants project-specific behavioral guidance.

## The Project

Air Link is a small NiceGUI app that runs as a systemd service on a Linux edge device.
It manages remote access via [NiceGUI On Air](https://on-air.nicegui.io) and installs user apps.
Keep two things in mind when changing it:

- **It runs next to user apps.** Deploying or breaking a user app must never take remote access down, so avoid coupling Air Link to anything a user app installs.
- **The target is not your laptop.** Docker, `systemctl`, `~/.ssh/authorized_keys` and raw sockets exist on the device but usually not in tests. Code that touches them has to degrade gracefully.

## Toolchain

We use [uv](https://docs.astral.sh/uv/):

```bash
uv sync                              # create the environment
uv run pytest                        # run the tests
uv run mypy air_link                 # check the types
uv run pre-commit run --all-files    # check the formatting
```

See the "Testing Locally" section in [README.md](README.md) for running Air Link against a local On Air server.

## Writing

Markdown files in this repository use semantic line breaks:
every sentence starts on a new line, and long sentences are broken at natural boundaries like the end of a subordinate clause.
This keeps diffs small and reviewable, so never reflow a paragraph you did not change.
Do not wrap at a fixed column, and do not join sentences into one long line —
the `mdformat` hook runs with `--wrap keep` and preserves whatever breaks you write.

## Pair Programming

Work as a pair programmer, not a silent code generator:

- **Think from first principles**: Don't settle for the first solution; question assumptions about the true nature of the problem.
- **Requirements first**: Verify requirements before implementing, especially when writing or changing tests.
- **Research before guessing**: Search the codebase for similar patterns; check online sources for verification.
- **Discuss before deciding**: When strategy is unclear, present options and trade-offs to the user instead of choosing silently.
- **Step-by-step for large changes**: Break down significant refactorings and get confirmation along the way.
- **Challenge assumptions**: If the user states something untrue, correct them directly.

## What to Avoid

- **Overwriting `.env` files** without explicit user confirmation
- **Creating new files** when editing existing ones would suffice
- **Unnecessary dependencies** — this app should stay installable on a small device; check if existing code suffices first
- **Refactoring for testability alone** — a fake for Docker or the filesystem is cheaper than reshaping production code around a test
- **Reflexive regression tests** — not every bug fix earns a test, and a test coupled to implementation details can be worse than none.
  Assert observable behavior, not internals: no private attributes, no patched machinery, no fake objects mirroring the code under test.
  If you catch yourself building scaffolding to observe an internal mechanism, stop — find the user-visible effect to assert on, or skip the test and give the reason in the pull request.

## Before Claiming a Task Complete

Run the tests and linters listed under "Toolchain" and review your own diff for unintended scope creep.
