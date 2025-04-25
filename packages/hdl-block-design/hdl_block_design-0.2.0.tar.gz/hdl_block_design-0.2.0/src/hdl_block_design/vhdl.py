"""Submodule defining utilities for interacting with VHDL source code."""

import tree_sitter
import tree_sitter_vhdl

LANGUAGE = tree_sitter.Language(tree_sitter_vhdl.language())
PARSER = tree_sitter.Parser(LANGUAGE)

ENTITY_NAME_QUERY_TEXT = """
(design_file
    (design_unit
        (entity_declaration
            (identifier) @entity.name
        )
    )
)
"""
ENTITY_NAME_QUERY = LANGUAGE.query(ENTITY_NAME_QUERY_TEXT)

ENTITY_PORTS_QUERY_TEXT = """
(design_file
    (design_unit
        (entity_declaration
            (entity_head
                (port_clause
                    (interface_list
                        (interface_declaration
                            (identifier_list (identifier) @port.name)
                            (simple_mode_indication
                                (mode) @port.direction
                                (subtype_indication
                                    (name) @port.type
                                )
                            )
                        )
                    )
                )
            )
        )
    )
)
"""
ENTITY_PORTS_QUERY = LANGUAGE.query(ENTITY_PORTS_QUERY_TEXT)
