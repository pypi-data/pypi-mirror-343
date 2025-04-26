import logging
from collections.abc import Sequence
from pathlib import Path
from typing import Any, Literal
from uuid import uuid4

import attrs

from lsprotocol import types as types_module

from lsprotocol.types import (
    InitializeParams,
    INITIALIZE,
    RegistrationParams,
    Registration,
    TextEdit,
    TEXT_DOCUMENT_DID_OPEN,
    DidOpenTextDocumentParams,
    TEXT_DOCUMENT_DID_CLOSE,
    DidCloseTextDocumentParams,
    METHOD_TO_TYPES,
    Diagnostic,
    LanguageKind,
)
from pygls.lsp.server import LanguageServer
from sqlglot import Dialect

from databricks.labs.community.transpiler.common_types import TranspileOptions
from databricks.labs.community.transpiler.dialect_utils import get_dialect
from databricks.labs.community.transpiler.helpers import full_range
from databricks.labs.community.transpiler.transpiler import transpile

logging.basicConfig(filename='test-lsp-server.log', filemode='w', level=logging.DEBUG)

logger = logging.getLogger(__name__)

# the below code also exists in lsp_engine.py
# it will be factorized as part of https://github.com/databrickslabs/remorph/issues/1304
TRANSPILE_TO_DATABRICKS_METHOD = "document/transpileToDatabricks"
TRANSPILE_TO_DATABRICKS_CAPABILITY = {"id": str(uuid4()), "method": TRANSPILE_TO_DATABRICKS_METHOD}


@attrs.define
class TranspileDocumentParams:
    uri: str = attrs.field()
    language_id: LanguageKind | str = attrs.field()


@attrs.define
class TranspileDocumentRequest:
    # 'id' is mandated by LSP
    # pylint: disable=invalid-name
    id: int | str = attrs.field()
    params: TranspileDocumentParams = attrs.field()
    method: Literal["document/transpileToDatabricks"] = "document/transpileToDatabricks"
    jsonrpc: str = attrs.field(default="2.0")


@attrs.define
class TranspileDocumentResult:
    uri: str = attrs.field()
    language_id: LanguageKind | str = attrs.field()
    changes: Sequence[TextEdit] = attrs.field()
    diagnostics: Sequence[Diagnostic] = attrs.field()


@attrs.define
class TranspileDocumentResponse:
    # 'id' is mandated by LSP
    # pylint: disable=invalid-name
    id: int | str = attrs.field()
    result: TranspileDocumentResult = attrs.field()
    jsonrpc: str = attrs.field(default="2.0")


def install_special_properties():
    is_special_property = getattr(types_module, "is_special_property")

    def customized(cls: type, property_name: str) -> bool:
        if cls is TranspileDocumentRequest and property_name in {"method", "jsonrpc"}:
            return True
        return is_special_property(cls, property_name)

    setattr(types_module, "is_special_property", customized)


install_special_properties()

METHOD_TO_TYPES[TRANSPILE_TO_DATABRICKS_METHOD] = (
    TranspileDocumentRequest,
    TranspileDocumentResponse,
    TranspileDocumentParams,
    None,
)


class Server(LanguageServer):

    def __init__(self, name, version):
        super().__init__(name, version)
        self.initialization_options: Any = None

    @property
    def dialect(self) -> Dialect:
        name = self.initialization_options["remorph"]["source-dialect"]
        return get_dialect(name)

    @property
    def experimental(self) -> bool:
        return self.initialization_options["custom"]["experimental"] == "true"

    @property
    def options(self) -> TranspileOptions:
        return TranspileOptions(self.dialect, self.experimental)

    async def did_initialize(self, init_params: InitializeParams) -> None:
        self.initialization_options = init_params.initialization_options
        logger.debug(f"dialect={server.dialect}")
        logger.debug(f"experimental={server.experimental}")
        # TODO check whether the client supports dynamic registration
        registrations = [
            Registration(
                id=TRANSPILE_TO_DATABRICKS_CAPABILITY["id"], method=TRANSPILE_TO_DATABRICKS_CAPABILITY["method"]
            )
        ]
        register_params = RegistrationParams(registrations)
        await self.client_register_capability_async(register_params)

    def transpile_to_databricks(self, params: TranspileDocumentParams) -> TranspileDocumentResult:
        source_sql = self.workspace.get_text_document(params.uri).source
        transpiled_sql, diagnostics = transpile(self.options, Path(params.uri).name, source_sql)
        changes = [TextEdit(range=full_range(source_sql), new_text=transpiled_sql)]
        return TranspileDocumentResult(
            uri=params.uri, language_id=LanguageKind.Sql, changes=changes, diagnostics=diagnostics
        )


server = Server("remorph-sqlglot-transpiler", "v0.1")


@server.feature(INITIALIZE)
async def lsp_did_initialize(params: InitializeParams) -> None:
    await server.did_initialize(params)


@server.feature(TEXT_DOCUMENT_DID_OPEN)
async def lsp_text_document_did_open(params: DidOpenTextDocumentParams) -> None:
    logger.debug(f"open-document-uri={params.text_document.uri}")


@server.feature(TEXT_DOCUMENT_DID_CLOSE)
async def lsp_text_document_did_close(params: DidCloseTextDocumentParams) -> None:
    logger.debug(f"close-document-uri={params.text_document.uri}")


@server.feature(TRANSPILE_TO_DATABRICKS_METHOD)
def transpile_to_databricks(params: TranspileDocumentParams) -> TranspileDocumentResult:
    return server.transpile_to_databricks(params)


if __name__ == "__main__":
    server.start_io()
