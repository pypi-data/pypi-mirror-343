from typing import override
from ..modeling.base_model_context import BaseModelContext
from ..modeling.library_manager import BaseLibraryHandler
from .client_binder import PvradarClientBinder, pvradar_client_models


class ClientLibraryHandler(BaseLibraryHandler):
    @override
    def get_models(self):
        return list(pvradar_client_models.values())

    @override
    def enrich_context(self, context: BaseModelContext) -> None:
        super().enrich_context(context)
        context.binders.append(PvradarClientBinder())


pvgis_handler = ClientLibraryHandler()
