# toast-lettuce-test-package-omni-version

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
- Release: configurable, default `1.0`
- Pre-release: absent, `a1`, `b1`, `rc1`
- Post-release: absent or `.post1`
- Development release: absent or `.dev1`
- Local version: absent or `+local.1`

Generate the full canonical matrix:

```sh
uv run canonical-version-matrix
```

Use a different base release, or exclude epoch/local forms:

```sh
uv run canonical-version-matrix --release 2026.4
uv run canonical-version-matrix --no-epoch --no-local
```

Set the project version only through `uv version`:

```sh
uv version 1.0rc1.post1.dev1
uv version 1!2026.4.post1+local.1
```

Wheel build tags are separate from the version string. They belong in the wheel
filename, not in the PEP 440 version itself.
