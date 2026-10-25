# Contributing to sidecar

Thanks for helping. sidecar is small on purpose, so most contributions are either a
**device report**, a **bug fix**, or a **careful, small feature**.

## The most useful thing you can send: a device report

Open a [device report](../../issues/new?template=device_report.yml) with:

- TV model and the software version from the TV's system info screen
- Whether the bridge page loaded and how many functions the probe found
- Anything that failed

**Never post** serial numbers, MAC addresses, device IDs, advertising IDs, or your
public IP. sidecar redacts reports, but read yours before attaching it.

## Setting up

```sh
git clone https://github.com/flavioabbinante/sidecar.git
cd sidecar
python3 -m unittest discover -s tests
```

There is nothing to install. Python 3.9+ is enough.

## Ground rules

- **Standard library only.** A new dependency needs a strong reason, discussed in an
  issue first.
- **Read-only stays read-only.** The probe page must never call anything but
  `Hisense_Get…` functions, and nothing in sidecar may accept commands from the network.
  Pull requests that add install, write, reset or remote-execution features will be
  declined.
- **Keep it small.** Prefer the shortest change that fully solves the problem.
  Don't add options or abstractions nobody has asked for.
- **Test new logic.** A new branch, parser or loop gets a small test in `tests/`.
- **Match the surrounding code**: naming, comment density and style.
- **Comment the why**, not the what. A shortcut with a known limit gets a comment of the
  form `shortcut: <limit>, <when to upgrade>`.

## Blocklist contributions

Blocklists are shared state, so they are held to a higher bar:

- One name per line, each with a comment saying what it is and **how you verified** the
  TV still works without it (model and firmware).
- Only names that are tracking or advertising. Never names the TV needs to operate.
- No personal or household-specific names.

## Pull requests

1. Fork, then branch from `main`.
2. Keep the PR focused: one fix or feature.
3. Make sure `python3 -m unittest discover -s tests` passes.
4. Fill in the pull request template.
5. Make sure the diff contains **no logs, reports, certificates or keys**.

Commit messages: a short imperative summary line (`Fix IPv6 lookups`), then a body
explaining why if it isn't obvious.

## Reporting security problems

Please don't open a public issue. See [SECURITY.md](SECURITY.md).

## Code of conduct

Everyone taking part is expected to follow the [Code of Conduct](CODE_OF_CONDUCT.md).
