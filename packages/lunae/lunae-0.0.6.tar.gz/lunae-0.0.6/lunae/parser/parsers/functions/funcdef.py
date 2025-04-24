"""
This module provides the parser for function definitions.
"""

from lunae.language.ast.functions.funcdef import FuncDef
from lunae.parser.parsers.base.block import parse_block
from lunae.parser.reader import ParserReader
from lunae.tokenizer.grammar import TokenKind


def parse_func_def(reader: ParserReader) -> FuncDef:
    """
    Parses a function definition.

    Args:
        reader (ParserReader): The parser reader.

    Returns:
        FuncDef: The parsed function definition node.
    """
    reader.expect(TokenKind.KEYWORD, "func")
    name_token = reader.match(TokenKind.IDENT)
    name = name_token.match if name_token else None
    reader.expect(TokenKind.LPAREN)
    params: list[tuple[str, str]] = []
    if not reader.match(TokenKind.RPAREN):
        while True:
            param_name = reader.expect(TokenKind.IDENT).match
            if reader.match(TokenKind.COLON):
                param_type = reader.expect(TokenKind.IDENT).match
            else:
                param_type = "ANY"

            params.append((param_name, param_type))

            if reader.match(TokenKind.RPAREN):
                break
            reader.expect(TokenKind.COMMA)

    reader.expect(TokenKind.COLON)
    return FuncDef(name, params, parse_block(reader))
