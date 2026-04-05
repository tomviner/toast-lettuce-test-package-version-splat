from __future__ import annotations

from dataclasses import dataclass
from itertools import product
import sys
from typing import Iterable, Sequence


@dataclass(frozen=True)
class VersionParts:
    epoch: str
    release: str
    pre: str
    post: str
    dev: str
    local: str

    def render(self) -> str:
        return f"{self.epoch}{self.release}{self.pre}{self.post}{self.dev}{self.local}"


DEFAULT_RELEASES = ("1.0.0",)


def _normalize_releases(releases: Sequence[str]) -> tuple[str, ...]:
    normalized = tuple(release.strip() for release in releases if release.strip())
    if not normalized:
        raise ValueError("at least one release must be provided")
    return normalized


def canonical_public_versions(
    releases: Sequence[str] = DEFAULT_RELEASES,
    *,
    include_epoch: bool = True,
    include_local: bool = False,
) -> list[str]:
    """Return representative canonical PEP 440 combinations.

    The returned matrix varies only the presence of canonical version parts.
    Numbered segments use `1` as a representative value.
    """

    releases = _normalize_releases(releases)

    epochs = ("", "1!") if include_epoch else ("",)
    pres = ("", "a1", "b1", "rc1")
    posts = ("", ".post1")
    devs = ("", ".dev1")
    locals_ = ("", "+local.1") if include_local else ("",)

    versions: list[str] = []
    seen: set[str] = set()
    for release in releases:
        for epoch, pre, post, dev, local in product(epochs, pres, posts, devs, locals_):
            rendered = VersionParts(
                epoch=epoch,
                release=release,
                pre=pre,
                post=post,
                dev=dev,
                local=local,
            ).render()
            if rendered not in seen:
                seen.add(rendered)
                versions.append(rendered)
    return versions


def format_version_matrix(
    releases: Sequence[str] = DEFAULT_RELEASES,
    *,
    include_epoch: bool = True,
    include_local: bool = False,
) -> str:
    versions = canonical_public_versions(
        releases=releases,
        include_epoch=include_epoch,
        include_local=include_local,
    )
    return "\n".join(versions)


def _parse_bool_flag(args: Iterable[str], flag: str) -> bool:
    return any(arg == flag for arg in args)


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    releases = list(DEFAULT_RELEASES)

    if "--release" in args:
        releases = []
        index = 0
        while index < len(args):
            if args[index] != "--release":
                index += 1
                continue
            try:
                releases.append(args[index + 1])
            except IndexError as exc:
                raise SystemExit("--release requires a value") from exc
            index += 2

    include_epoch = not _parse_bool_flag(args, "--no-epoch")
    include_local = _parse_bool_flag(args, "--include-local")
    print(
        format_version_matrix(
            releases=releases,
            include_epoch=include_epoch,
            include_local=include_local,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
