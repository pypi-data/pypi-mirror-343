from lsprotocol.types import Range, Position


def format_error_message(error_type: str, exception: Exception, error_sql: str) -> str:
    """
    Formats the error message with the error SQL.
    :param error_type: Error Type
    :param exception:  Raised exception
    :param error_sql: Error SQL
    :return: Formatted error message
    """
    return (
        f"------------------------ {error_type} Start:------------------------\n"
        f"/*\n{str(exception)}\n*/\n\n"
        f"/*\nOriginal Query:\n\n{str(error_sql)}\n*/\n"
        f"------------------------- {error_type} End:-------------------------"
    ).strip()


def full_range(source_code: str) -> Range:
    source_lines = source_code.split("\n")
    return Range(start=Position(0, 0), end=Position(len(source_lines), len(source_lines[-1])))
