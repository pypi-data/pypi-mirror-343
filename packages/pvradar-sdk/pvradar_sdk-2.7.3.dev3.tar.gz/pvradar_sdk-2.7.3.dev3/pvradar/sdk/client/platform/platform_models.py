from typing import Annotated
from pydantic import Field
from ...modeling.decorators import standard_resource_type
from .pvradar_project import PvradarProject
from ...modeling import resource_types as R


@standard_resource_type(R.soiling_loss_factor)
def project_soiling_loss_factor(
    context: Annotated[PvradarProject, Field()],
):
    pass
