"""Submodule defining the available CLI for this library."""

import functools
import importlib.metadata
import logging
import os
import sys
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from types import ModuleType
from typing import Literal, Self

import cyclopts
import rich
import tree_sitter
from cyclopts import App, Parameter
from cyclopts.types import ExistingFile
from rich import print  # noqa: A004
from rich.console import Console
from rich.logging import RichHandler
from rich.pretty import pprint
from rich.traceback import install

from hdl_block_design import Block, vhdl

CONSOLE = Console()
PACKAGE_NAME = __package__.split(".")[0]
SUPPRESS: list[ModuleType | str] = [cyclopts, functools, rich, sys.argv[0]]


def get_version() -> str:
    return importlib.metadata.version(PACKAGE_NAME)


def get_file_path_or_file_content(
    input_data: str | Path | None = None,
) -> str | Path:
    # If we have no input, read stdin
    if input_data is None:
        input_data = sys.stdin.read()
        input_data = input_data.strip()

    # If we have an empty string, raise
    if isinstance(input_data, str) and len(input_data) == 0:
        message = f"Input '{input_data}' is empty"
        raise RuntimeError(message)

    # If the string is a path that exists, convert it to Path type
    stdin_path = Path(input_data)
    if stdin_path.exists():
        input_data = stdin_path

    return input_data


def get_data(
    input_data: str | Path | None = None,
) -> str:
    input_data = get_file_path_or_file_content(input_data)
    if isinstance(input_data, Path):
        with input_data.open(encoding="utf-8") as f:
            return f.read()
    return input_data


def get_bytes(
    input_data: str | Path | None = None,
) -> bytes:
    return bytes(get_data(input_data), "utf-8")


def get_tree(
    input_data: str | Path | None,
    parser: tree_sitter.Parser,
) -> tree_sitter.Tree:
    return parser.parse(get_bytes(input_data))


@Parameter(name="*")
@dataclass
class LoggingCommon:
    """Common parameters related to logging."""

    verbose: bool = False

    @classmethod
    def create_if_none(cls, current: Self | None) -> Self:
        """Create this class, or return the current one."""
        if current is None:
            return cls()
        return current

    def __post_init__(self) -> None:
        if self.verbose:
            level = logging.DEBUG
            handler = RichHandler(console=CONSOLE, rich_tracebacks=True)
        else:
            level = logging.INFO
            handler = RichHandler(
                console=CONSOLE,
                rich_tracebacks=True,
                tracebacks_suppress=SUPPRESS,
            )
        install(console=CONSOLE, show_locals=True, suppress=SUPPRESS)
        logging.basicConfig(
            level=level,
            format="%(message)s",
            datefmt="[%X]",
            handlers=[handler],
        )

    @cached_property
    def logger(self) -> logging.Logger:
        """Get the current logger."""
        return logging.getLogger(PACKAGE_NAME)


app = App(console=CONSOLE, version=get_version)


parse_app = App(console=CONSOLE, name="parse")
app.command(parse_app)


parse_block_app = App(console=CONSOLE, name="block")
parse_app.command(parse_block_app)


@parse_block_app.command(name="vhdl")
def parse_block_vhdl(
    input_data: str | ExistingFile | None = None,
    common: LoggingCommon | None = None,
) -> None:
    # Common
    common = LoggingCommon.create_if_none(common)
    common.logger.debug("parse block vhdl '%s'", input_data)

    input_data = get_file_path_or_file_content(input_data)

    if isinstance(input_data, Path):
        block = Block.from_vhdl_file(input_data)
    else:
        block = Block.from_vhdl_string(input_data)
    pprint(block)


@parse_block_app.command
def yaml(
    input_data: str | ExistingFile | None = None,
    common: LoggingCommon | None = None,
) -> None:
    # Common
    common = LoggingCommon.create_if_none(common)
    common.logger.debug("parse block vhdl '%s'", input_data)

    input_data = get_file_path_or_file_content(input_data)

    if isinstance(input_data, Path):
        block = Block.from_yaml_file(input_data)
    else:
        block = Block.from_yaml_string(input_data)

    pprint(block)


parse_vhdl_app = App(console=CONSOLE, name="vhdl")
parse_app.command(parse_vhdl_app)


parse_vhdl_entity_app = App(console=CONSOLE, name="entity")
parse_vhdl_app.command(parse_vhdl_entity_app)


@parse_vhdl_entity_app.command()
def ports(
    input_data: str | ExistingFile | None = None,
    common: LoggingCommon | None = None,
) -> None:
    # Common
    common = LoggingCommon.create_if_none(common)
    common.logger.debug("tree-sitter parse vhdl entity '%s'", input_data)

    try:
        tree = get_tree(input_data, vhdl.PARSER)
    except RuntimeError as err:
        message = "No ports found"
        raise RuntimeError(message) from err
    common.logger.debug("Tree: %s", str(tree.root_node))

    captures = vhdl.ENTITY_PORTS_QUERY.captures(tree.root_node)
    common.logger.debug("Entity port captures: %s", captures)

    if len(captures) == 0:
        message = "No ports found"
        raise RuntimeError(message)

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
    for name, direction, port_type in zip(names, directions, types, strict=True):
        pprint({"name": name, "direction": direction, "type": port_type})


tree_sitter_app = App(console=CONSOLE, name="tree-sitter")
app.command(tree_sitter_app)


tree_sitter_dump_app = App(console=CONSOLE, name="dump")
tree_sitter_app.command(tree_sitter_dump_app)

LB = "("
RB = ")"
TAB = " " * 4


def sexpr_pformat(s: str) -> str:
    formatted_clips_str = ""
    tab_count = 0
    for c in s:
        if c == LB:
            formatted_clips_str += f"{os.linesep}{TAB * tab_count}{c}"
            tab_count += 1
        elif c == RB:
            formatted_clips_str += c
            tab_count -= 1
        else:
            formatted_clips_str += c
    return formatted_clips_str.strip()


@tree_sitter_dump_app.command(name="vhdl")
def tree_sitter_dump_vhdl(
    input_data: str | ExistingFile | None = None,
    output_format: Literal["sexpr", "sexpr-pretty", "sexpr-with-location"] = "sexpr",
    common: LoggingCommon | None = None,
) -> None:
    # Common
    common = LoggingCommon.create_if_none(common)
    common.logger.debug("tree-sitter dump vhdl %s", input_data)

    def print_tree(node: tree_sitter.Node, indent: int = 0) -> None:
        print("  " * indent + f"({node.type} [{node.start_point} - {node.end_point}])")
        for child in node.children:
            print_tree(child, indent + 1)

    tree = get_tree(input_data, vhdl.PARSER)
    common.logger.debug("Tree: %s", str(tree.root_node))
    if output_format == "sexpr":
        print(str(tree.root_node))
    if output_format == "sexpr-pretty":
        print(sexpr_pformat(str(tree.root_node)))
    if output_format == "sexpr-with-location":
        print_tree(tree.root_node)


tree_sitter_query_app = App(console=CONSOLE, name="query")
tree_sitter_app.command(tree_sitter_query_app)


@tree_sitter_query_app.command(name="vhdl")
def tree_sitter_query_vhdl(
    query: str,
    input_data: str | ExistingFile | None = None,
    output_format: Literal["raw", "tree"] = "raw",
    common: LoggingCommon | None = None,
) -> None:
    # Common
    common = LoggingCommon.create_if_none(common)
    common.logger.debug("tree-sitter query vhdl '%s' '%s'", input_data, query)

    tree = get_tree(input_data, vhdl.PARSER)
    common.logger.debug("Tree: %s", str(tree.root_node))

    query_object = vhdl.LANGUAGE.query(query)
    captures = query_object.captures(tree.root_node)

    if output_format == "raw":
        for k, v in captures.items():
            print(f"{k}: {[e.text.decode('utf-8') for e in v if e.text is not None]}")
    if output_format == "tree":
        for k, v in captures.items():
            print(f"{k}: {[str(e) for e in v]}")
