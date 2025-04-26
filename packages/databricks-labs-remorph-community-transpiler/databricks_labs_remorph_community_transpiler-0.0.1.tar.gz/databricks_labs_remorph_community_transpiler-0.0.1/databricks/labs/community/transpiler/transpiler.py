import logging
import typing as t
from collections.abc import Sequence
from dataclasses import dataclass

from lsprotocol.types import Diagnostic, DiagnosticSeverity

from sqlglot import expressions as exp, transpile as sqlglot_transpile, Dialect
from sqlglot.errors import ErrorLevel, ParseError, TokenError, UnsupportedError
from sqlglot.expressions import Expression
from sqlglot.tokens import Token, TokenType

from databricks.labs.community.transpiler import lca_utils
from databricks.labs.community.transpiler.common_types import TranspileOptions
from databricks.labs.community.transpiler.dialect_utils import get_write_dialect
from databricks.labs.community.transpiler.helpers import format_error_message, full_range

logger = logging.getLogger(__name__)


@dataclass
class ParsedExpression:
    original_sql: str
    parsed_expression: Expression


def _partial_transpile(options: TranspileOptions, source_code: str) -> tuple[list[str], list[Diagnostic]]:
    rng = full_range(source_code)
    transpiled_sqls: list[str] = []
    parsed_expressions, diagnostics = safe_parse(options, source_code)
    for parsed_expression in parsed_expressions:
        try:
            write_dialect = get_write_dialect(options.experimental)
            transpiled_sql = write_dialect.generate(parsed_expression.parsed_expression, pretty=True)
            # Checking if the transpiled SQL is a comment and raise an error
            if transpiled_sql.startswith("--"):
                raise UnsupportedError("Unsupported SQL")
            transpiled_sqls.append(transpiled_sql)
        except TokenError as e:
            diagnostics.append(
                Diagnostic(
                    range=rng,
                    code="PARSING-TOKEN_ERROR",
                    severity=DiagnosticSeverity.Error,
                    message=format_error_message("Token Error", e, parsed_expression.original_sql),
                )
            )
        except ParseError as e:
            diagnostics.append(
                Diagnostic(
                    range=rng,
                    code="PARSING-PARSING_ERROR",
                    severity=DiagnosticSeverity.Error,
                    message=format_error_message("Parsing Error", e, parsed_expression.original_sql),
                )
            )
        except UnsupportedError as e:
            diagnostics.append(
                Diagnostic(
                    range=rng,
                    code="PARSING-INTERNAL_ERROR",
                    severity=DiagnosticSeverity.Error,
                    message=format_error_message("Unsupported SQL Error", e, parsed_expression.original_sql),
                )
            )
    return transpiled_sqls, diagnostics


def transpile(options: TranspileOptions, file_name: str, source_code: str) -> tuple[str, Sequence[Diagnostic]]:
    errors = _check_supported(options, file_name, source_code)
    if errors:
        return source_code, errors
    write_dialect = get_write_dialect(options.experimental)
    try:
        transpiled_expressions = sqlglot_transpile(
            source_code, read=options.dialect, write=write_dialect, pretty=True, error_level=ErrorLevel.RAISE
        )
        transpiled_code = "\n".join(transpiled_expressions)
        return transpiled_code, []
    except (ParseError, TokenError, UnsupportedError) as e:
        logger.error(f"Exception caught for file {file_name!s}: {e}")
        transpiled_expressions, diagnostics = _partial_transpile(options, source_code)
        transpiled_code = "\n".join(transpiled_expressions)
        return transpiled_code, diagnostics


def safe_parse(options: TranspileOptions, source_code: str) -> tuple[list[ParsedExpression], list[Diagnostic]]:
    try:
        tokens = options.dialect.tokenize(sql=source_code)
        return _safe_parse(options.dialect, tokens, source_code)
    except TokenError as e:
        diagnostic = Diagnostic(
            range=full_range(source_code),
            code="PARSING-TOKEN_ERROR",
            severity=DiagnosticSeverity.Error,
            message=format_error_message("Token Error", e, source_code),
        )
        return [], [diagnostic]


def _safe_parse(
    read_dialect: Dialect,
    all_tokens: list[Token],
    source_code: str,
) -> tuple[list[ParsedExpression], list[Diagnostic]]:
    rng = full_range(source_code)
    chunks = _make_chunks(all_tokens)
    parsed_expressions: list[ParsedExpression] = []
    diagnostics: list[Diagnostic] = []
    parser_opts = {"error_level": ErrorLevel.RAISE}
    parser = read_dialect.parser(**parser_opts)
    for sql, tokens in chunks:
        try:
            expressions = parser.parse(tokens)
            expression = t.cast(Expression, expressions[0])
            parsed_expressions.append(ParsedExpression(sql, expression))
        except ParseError as e:
            diagnostics.append(
                Diagnostic(
                    range=rng,
                    code="PARSING-PARSING_ERROR",
                    severity=DiagnosticSeverity.Error,
                    message=format_error_message("Parsing Error", e, source_code),
                )
            )
        except UnsupportedError as e:
            diagnostics.append(
                Diagnostic(
                    range=rng,
                    code="PARSING-INTERNAL_ERROR",
                    severity=DiagnosticSeverity.Error,
                    message=format_error_message("Unsupported SQL Error", e, source_code),
                )
            )
        finally:
            parser.reset()
    return parsed_expressions, diagnostics


def _make_chunks(tokens: list[Token]) -> list[tuple[str, list[Token]]]:
    chunks: list[tuple[str, list[Token]]] = []
    current_chunk: list[Token] = []
    # Split tokens into chunks based on semicolons(or other separators)
    # Need to define the separator in Class Tokenizer
    for token in tokens:
        current_chunk.append(token)
        if token.token_type in {TokenType.SEMICOLON}:
            original_sql = " ".join([token.text for token in current_chunk]).strip()
            chunks.append((original_sql, current_chunk))
            # reset
            current_chunk = []
    # don't forget the last chunk
    if current_chunk:
        original_sql = " ".join([token.text for token in current_chunk]).strip()
        chunks.append((original_sql, current_chunk))
    return chunks


def _find_root_table(expression) -> str:
    table = expression.find(exp.Table, bfs=False)
    return table.name if table else ""


def _check_supported(transpile_options: TranspileOptions, file_name: str, source_code: str) -> Sequence[Diagnostic]:
    return lca_utils.check_for_unsupported_lca(transpile_options, file_name, source_code)
