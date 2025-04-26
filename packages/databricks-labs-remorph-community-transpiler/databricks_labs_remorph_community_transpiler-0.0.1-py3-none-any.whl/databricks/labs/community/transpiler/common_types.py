from dataclasses import dataclass
from sqlglot import Dialect


@dataclass
class TranspileOptions:
    dialect: Dialect
    experimental: bool
