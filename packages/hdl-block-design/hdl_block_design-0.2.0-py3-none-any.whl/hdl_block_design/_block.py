"""Submodule defining blocks within a design."""

from __future__ import annotations

import dataclasses
import enum
from pathlib import Path
from typing import TYPE_CHECKING, overload

from . import vhdl
from ._yamllable import ToFromYAML

if TYPE_CHECKING:
    from typing import Any, Self

    from ._yamllable import PathLike, YAMLMapping, YAMLValue


class DocEnum(enum.StrEnum):
    def __new__(cls, value: str, doc: str | None = None) -> Self:
        """Create a new string enum."""
        self = str.__new__(cls, value)
        self._value_ = value
        if doc is not None:
            self.__doc__ = doc
        return self


@enum.unique
class Direction(DocEnum):
    """Class representing the direction of a pin."""

    IN = "in", "The pin is an input."
    OUT = "out", "The pin is an output."
    INOUT = "inout", "The pin is an input and an output."

    @classmethod
    def _missing_(cls, value: Any) -> Self | None:  # noqa: ANN401
        """Interpret values that don't completely match an enum value."""
        if not isinstance(value, str):
            return None
        value = value.lower()
        for member in cls:
            if member.value == value:
                return member
        return None

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}.{self.value.upper()}"


@overload
def ensure_existence_and_type(
    dct: YAMLMapping,
    key: str,
    klass: type[str],
) -> str: ...


@overload
def ensure_existence_and_type(
    dct: YAMLMapping,
    key: str,
    klass: type[list[YAMLMapping]],
) -> list[YAMLMapping]: ...


@overload
def ensure_existence_and_type(
    dct: YAMLMapping,
    key: str,
    klass: type[YAMLMapping],
) -> YAMLMapping: ...


def ensure_existence_and_type(
    dct: YAMLMapping,
    key: str,
    klass: type[YAMLValue],
) -> YAMLValue:
    """
    Ensure that a key in a given dictionary, both exists, and has the requested type.

    Raises
    ------
    KeyError
        If `key` is not a valid key in `dct`.
    TypeError
        If the value of `key` is not of the requested type.

    """
    value = dct.get(key)
    if value is None:
        message = f"Dictionary does not contain `{key}` key: {dct}"
        raise KeyError(message)
    if not isinstance(value, klass):
        message = f"Value `{value}` with key `{key}` has the wrong type: {type(value)}"
        raise TypeError(message)
    return value


@dataclasses.dataclass
class Pin(ToFromYAML):
    """Class representing a pin on a block."""

    name: str
    """The name of the pin."""
    type: str
    """The type of the pin. This maps to the VHDL type."""
    direction: Direction | str
    """The direction of the pin."""

    def __post_init__(self) -> None:
        self.direction = Direction(self.direction)

    @classmethod
    def from_dict(cls, dct: YAMLMapping) -> Self:
        """Create a Pin from a dictionary."""
        name = ensure_existence_and_type(dct, "name", str)
        t = ensure_existence_and_type(dct, "type", str)
        direction = ensure_existence_and_type(dct, "direction", str)
        return cls(name=name, type=t, direction=direction)

    def to_dict(self) -> YAMLMapping:
        """Convert a Pin to a dictionary."""
        return {
            "name": self.name,
            "type": self.type,
            "direction": str(self.direction),
        }

    def to_vhdl_entity_port_definition(
        self,
        prefix: str | None = None,
        prefix_separator: str = "_",
    ) -> str:
        """Return the VHDL entity port definition for this pin."""
        if prefix is not None and len(prefix) != 0:
            return (
                f"{prefix}{prefix_separator}{self.name}: {self.direction} {self.type}"
            )
        return f"{self.name}: {self.direction} {self.type}"


@dataclasses.dataclass
class Block(ToFromYAML):
    """Class representing an available block in a block design."""

    name: str
    """The name of the block."""

    pins: dict[str, Pin]
    """The pins on the block."""

    @classmethod
    def from_dict(cls, dct: YAMLMapping) -> Self:
        """Create a Block from a dictionary."""
        name = ensure_existence_and_type(dct, "name", str)
        pins = ensure_existence_and_type(dct, "pins", dict)
        pins_as_objects = {
            k: Pin.from_dict(ensure_existence_and_type(pins, k, dict)) for k in pins
        }
        return cls(name=name, pins=pins_as_objects)

    @classmethod
    def from_vhdl_file(cls, path: PathLike) -> Self:
        """Create a Block from a VHDL file."""
        return cls.from_vhdl_string(Path(path).read_bytes())

    @classmethod
    def from_vhdl_string(cls, s: str | bytes) -> Self:
        """
        Create a Block from a VHDL string or bytes string.

        Raises
        ------
        RuntimeError
            If `s` contains 0 or > 1 entity declarations.

        """
        if isinstance(s, str):
            s = bytes(s, "utf-8")
        tree = vhdl.PARSER.parse(s)

        captures = vhdl.ENTITY_NAME_QUERY.captures(tree.root_node)
        entity_name = [
            e.text.decode("utf-8")
            for e in captures.get("entity.name", [])
            if e.text is not None
        ]
        if len(entity_name) != 1:
            message = (
                f"'{s.decode('utf-8')}' doesn't contain exactly one entity declaration"
            )
            raise RuntimeError(message)
        captures = vhdl.ENTITY_PORTS_QUERY.captures(tree.root_node)

        names = [
            n.text.decode("utf-8")
            for n in captures.get("port.name", [])
            if n.text is not None
        ]
        directions = [
            d.text.decode("utf-8")
            for d in captures.get("port.direction", [])
            if d.text is not None
        ]
        types = [
            t.text.decode("utf-8")
            for t in captures.get("port.type", [])
            if t.text is not None
        ]
        ports = []
        for name, direction, port_type in zip(names, directions, types, strict=True):
            ports.append({"name": name, "direction": direction, "type": port_type})
        pins = {
            port["name"]: Pin(
                name=port["name"],
                direction=port["direction"],
                type=port["type"],
            )
            for port in ports
        }

        return cls(name=entity_name[0], pins=pins)

    def to_dict(self) -> YAMLMapping:
        """Convert a Block to a dictionary."""
        return {
            "name": self.name,
            "pins": {k: v.to_dict() for k, v in self.pins.items()},
        }
