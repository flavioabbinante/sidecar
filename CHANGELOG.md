# Changelog

All notable changes are listed here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses
[Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- CI: lint and format check, package build and wheel smoke test, secret scan, CodeQL,
  OpenSSF Scorecard, and a tag-driven release workflow with build provenance
- Governance, support and issue forms for feature requests and blocklist entries

### Fixed
- The README banner no longer cuts off its tagline
- Removed an unused import

## [0.1.0]

### Added
- `sidecar dns`: DNS server that answers the bridge name locally, blocks listed names,
  forwards the rest and logs every decision
- `sidecar web`: HTTPS server with a read-only probe page and redacted reports
- `sidecar summarize`: counts the names in a DNS log
- Example blocklist, tests, CI and contributor documentation
