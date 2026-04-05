# toast-lettuce-test-package-version-splat

This package is for exercising canonical PEP 440 version forms.

Canonical public-version shape:

```text
[N!]N(.N)*[{a|b|rc}N][.postN][.devN]
```

Optional local-version label:

```text
[N!]N(.N)*[{a|b|rc}N][.postN][.devN][+LABEL]
```

Representative canonical parts used by this project:

- Epoch: absent or `1!`
- Release: configurable, default set `1.0.0`
- Pre-release: absent, `a1`, `b1`, `rc1`
- Post-release: absent or `.post1`
- Development release: absent or `.dev1`
- Local version: absent or `+local.1`

Generate the default publishable matrix for the `1.0.0` family:

```sh
uv run canonical-version-matrix
```

Use a different base release, exclude epoch forms, or include local versions:

```sh
uv run canonical-version-matrix --release 2026.4
uv run canonical-version-matrix --release 1 --release 1.0.0
uv run canonical-version-matrix --no-epoch
uv run canonical-version-matrix --include-local
```

Publish the default TestPyPI-safe matrix using the token in `token.test-pypi`:

```sh
./scripts/publish-testpypi.sh
```

Query published TestPyPI versions that match a specifier:

```sh
./scripts/matching-versions.sh '==1.0.0.*'
./scripts/matching-versions.sh '>=1!1.0.0rc1,<1!1.0.1' minmax
```

Set the project version only through `uv version`:

```sh
uv version 1.0rc1.post1.dev1
uv version 1!2026.4.post1+local.1
```

Wheel build tags are separate from the version string. They belong in the wheel
filename, not in the PEP 440 version itself.
