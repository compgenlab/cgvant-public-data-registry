# cgtag-public-data-registry

A catalog of **annotation source/release configs** for [cgtag](https://github.com/compgenlab/cgtag).
It holds *configurations, not data* — `cgtag download` fetches the actual files.

## Layout

```
registry.toml              catalog: [[sources]] and [[releases]] entries (each has a `file`)
sources/<name>@<ver>.toml  one source's config snippet (a source + its annotations)
releases/<name>.toml       a full release bundle
```

`registry.toml` is served over HTTPS (GitHub raw, Pages, S3 — anywhere). cgtag
points at its URL; entry `file` paths resolve relative to it.

## Consuming it

```sh
cgtag registry list                                # uses this registry by default
cgtag release add <release-name>                   # create a local release first
cgtag registry add-source <release-name> clinvar   # merge a source's config into it
cgtag registry pull-release <release-name>         # or pull a whole release
```

## Contributing a source

Run `cgtag registry submit <release-name> <source>` (needs a `public_repo`
`GITHUB_TOKEN`), or open an issue with the **`source-submission`** label and the source
config in a ` ```toml ` block. A submitted source **must declare a `checksum`**
(`md5`/`sha1`/`sha256`) for its data file. The
[issue-to-pr workflow](.github/workflows/issue-to-pr.yml) parses it, writes
`sources/<name>@<version>.toml`, adds the `registry.toml` entry, and opens a PR closing
the issue — a maintainer reviews and merges.

## Setup (one-time, for maintainers)

GitHub blocks the default `GITHUB_TOKEN` from creating pull requests unless *"Allow
GitHub Actions to create and approve pull requests"* is enabled — and an org can
forbid it org-wide, in which case the repo setting can't override it (the workflow
fails with `GitHub Actions is not permitted to create or approve pull requests`: the
branch is pushed but no PR is opened).

To avoid touching org-wide policy, the workflow opens the PR with a **fine-grained
PAT** instead of `GITHUB_TOKEN` (a user token isn't subject to that restriction).
Configure it once:

1. Create a **fine-grained personal access token** scoped to this repo with
   permissions *Pull requests: read & write* and *Contents: read & write*.
2. Add it as a repo secret named **`REGISTRY_PR_SECRET`** (Settings → Secrets and
   variables → Actions → New repository secret).

The workflow passes `token: ${{ secrets.REGISTRY_PR_SECRET }}` to
`create-pull-request`. (Alternatively, if you control the org and are fine loosening
it, enable the org-level "Allow GitHub Actions to create and approve pull requests"
and drop the `token:` line.)
