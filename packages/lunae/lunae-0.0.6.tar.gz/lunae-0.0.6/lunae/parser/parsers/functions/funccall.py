"""
This module provides functionality for parsing function calls.
"""

from lunae.language.ast.base.expr import Expr
from lunae.language.ast.functions.funccall import FuncCall
from lunae.language.ast.values.var import Var
from lunae.parser.parsers.base.expr import parse_expr
from lunae.parser.reader import ParserReader
from lunae.tokenizer.grammar import TokenKind

Callee = Var | FuncCall


def parse_func_call(reader: ParserReader, callee: Callee) -> Callee:
    """
    Parses function calls after a callee.

    Args:
        reader (ParserReader): The parser reader instance.
        callee (Var | FuncCall): The name of the function being called.

    Returns:
        Var | FuncCall: The parsed function call.
    """
    while reader.match(TokenKind.LPAREN):
        args = []
        if not reader.is_followed(TokenKind.RPAREN):
            args.append(parse_expr(reader))
            while reader.match(TokenKind.COMMA):
                args.append(parse_expr(reader))
        reader.expect(TokenKind.RPAREN)
        callee = FuncCall(callee, args)

    return callee
