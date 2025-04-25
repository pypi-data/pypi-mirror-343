from typing import Callable
from maleo_foundation.models.transfers.parameters.general import BaseGeneralParametersTransfers

class BaseGeneralExpandedTypes:
    #* Expansion processor related types
    FieldExpansionProcessor = Callable[[BaseGeneralParametersTransfers.FieldExpansionProcessor], None]