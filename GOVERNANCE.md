# Governance

sidecar is a small project, so governance is light. The goal is that anyone can
understand how decisions get made and how to take part in them.

## Roles

- **Users** run sidecar and report what happens on their TV.
- **Contributors** send device reports, fixes, docs, translations or blocklist entries.
- **Maintainers** review and merge changes, cut releases and keep the project safe.
  Right now that is the repository owner.

## How decisions are made

1. Anything non-trivial starts as an **issue or discussion**, in the open.
2. Maintainers look for rough consensus. Objections should be technical and specific.
3. If consensus isn't reached, the maintainers decide and explain the reasoning in the
   thread.

Some decisions are fixed, because they protect users, and are only changed by a
documented, public discussion:

- sidecar stays **read-only**: no installing apps, no writing files on the TV, no
  commands accepted from the network.
- sidecar stays **dependency-free** (standard library only).
- Reports and logs stay **local and redacted**; nothing is uploaded anywhere.

## Becoming a maintainer

Contributors who have sent several good changes, reviewed other people's work and
followed the [Code of Conduct](CODE_OF_CONDUCT.md) can be invited by the existing
maintainers. You can also ask in a discussion. Maintainers who are no longer active may
step back at any time and are thanked in the changelog.

## Releases

Releases follow [Semantic Versioning](https://semver.org/). A maintainer bumps the
version in `pyproject.toml`, updates `CHANGELOG.md` and pushes a `vX.Y.Z` tag; CI builds
the release and attaches signed build provenance.

## Changing this document

Open a pull request. Governance changes stay open for at least a week for comments.
