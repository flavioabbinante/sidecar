# Changelog

All notable changes are listed here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses
[Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.1.0] - 2026-10-25

First public release.

### Added
- `sidecar dns`: DNS server that answers the bridge name locally, blocks listed names,
  forwards the rest and logs every decision
- `sidecar web`: HTTPS server with a read-only probe page and redacted reports
- `sidecar summarize`: counts the names in a DNS log
- Example blocklist and unit tests
- CI: lint and format check, tests on Python 3.9 to 3.13, package build and wheel smoke
  test, secret scan, CodeQL, OpenSSF Scorecard
- Tag-driven release workflow with signed build provenance
- Contributor documentation: contributing guide, code of conduct, security policy,
  governance, support, issue forms and a pull request template

[Unreleased]: https://github.com/flavioabbinante/sidecar/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/flavioabbinante/sidecar/releases/tag/v0.1.0
