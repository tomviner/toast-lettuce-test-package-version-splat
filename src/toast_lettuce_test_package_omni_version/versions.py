from __future__ import annotations

from dataclasses import dataclass
from itertools import product
import sys
from typing import Iterable


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


def canonical_public_versions(
    release: str = "1.0",
    *,
    include_epoch: bool = True,
    include_local: bool = True,
) -> list[str]:
    """Return representative canonical PEP 440 combinations.

    The returned matrix varies only the presence of canonical version parts.
    Numbered segments use `1` as a representative value.
    """

    release = release.strip()
    if not release:
        raise ValueError("release must be non-empty")

    epochs = ("", "1!") if include_epoch else ("",)
    pres = ("", "a1", "b1", "rc1")
    posts = ("", ".post1")
    devs = ("", ".dev1")
    locals_ = ("", "+local.1") if include_local else ("",)

    versions: list[str] = []
    seen: set[str] = set()
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
    release: str = "1.0",
    *,
    include_epoch: bool = True,
    include_local: bool = True,
) -> str:
    versions = canonical_public_versions(
        release=release,
        include_epoch=include_epoch,
        include_local=include_local,
    )
    return "\n".join(versions)


def _parse_bool_flag(args: Iterable[str], flag: str) -> bool:
    return any(arg == flag for arg in args)


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    release = "1.0"

    if "--release" in args:
        index = args.index("--release")
        try:
            release = args[index + 1]
        except IndexError as exc:
            raise SystemExit("--release requires a value") from exc

    include_epoch = not _parse_bool_flag(args, "--no-epoch")
    include_local = not _parse_bool_flag(args, "--no-local")
    print(
        format_version_matrix(
            release=release,
            include_epoch=include_epoch,
            include_local=include_local,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
