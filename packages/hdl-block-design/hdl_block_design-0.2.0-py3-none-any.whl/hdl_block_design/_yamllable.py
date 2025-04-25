"""Submodule defining base utilities for objects that can be written as YAML."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Protocol

import yaml

if TYPE_CHECKING:
    import os
    from collections.abc import Mapping, Sequence
    from typing import Self

    PathLike = Path | os.PathLike[str] | str

type YAMLValue = str | Sequence[YAMLMapping] | YAMLMapping
type YAMLMapping = Mapping[
    str,
    YAMLValue,
]


class FromYAML(Protocol):
    """Base class for objects that can be read from YAML."""

    # Protocol methods
    @classmethod
    def from_dict(cls, dct: YAMLMapping) -> Self:
        """Create an object from a dictionary."""

    # Stuff you get for free
    @classmethod
    def from_yaml_string(cls, string: str) -> Self:
        """
        Create an object from a YAML string.

        Raises
        ------
        TypeError
            If `yaml` returns a non-`dict`.

        """
        dct = yaml.safe_load(string)
        if not isinstance(dct, dict):
            message = f"YAML file parses to `{type(dct)}`, not `dict`: {string}"
            raise TypeError(message)
        return cls.from_dict(dct)

    @classmethod
    def from_yaml_file(cls, path: PathLike) -> Self:
        """Create an object from a YAML file."""
        return cls.from_yaml_string(Path(path).read_text(encoding="utf-8"))


class ToYAML(Protocol):
    """Base class for objects that can be written to YAML."""

    # Protocol methods
    def to_dict(self) -> YAMLMapping:
        """Convert an object to a dictionary."""

    # Stuff you get for free
    def to_yaml_string(self) -> str:
        """Write an object to a YAML file."""
        return yaml.dump(self.to_dict())

    def write_yaml_file(self, path: PathLike) -> None:
        """Write an object to a YAML file."""
        with Path(path).open(mode="wt", encoding="utf-8") as f:
            yaml.dump(self.to_dict(), f)


class ToFromYAML(FromYAML, ToYAML):
    """Base class for objects that can be read from and written to YAML."""
