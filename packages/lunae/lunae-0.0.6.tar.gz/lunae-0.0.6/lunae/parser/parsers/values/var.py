"""
This module provides functionality for parsing variables and function calls.
"""

from ast import Expr

from lunae.language.ast.functions.funccall import FuncCall
from lunae.language.ast.values.var import Var
from lunae.parser.parsers.functions.funccall import parse_func_call
from lunae.parser.reader import ParserReader
from lunae.tokenizer.grammar import TokenKind


def parse_var(reader: ParserReader) -> Var | FuncCall:
    """
    Parses a variable or a function call.

    Args:
        reader (ParserReader): The parser reader instance.

    Returns:
        Var | FuncCall: The parsed variable or function call.
    """
    name = reader.expect(TokenKind.IDENT).match

    return parse_func_call(reader, Var(name))
