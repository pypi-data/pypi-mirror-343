from typing import Callable, List
from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_foundation.models.transfers.parameters.general import BaseGeneralParametersTransfers

class ExtendedTypes:
    #* DateFilter-related types
    ListOfDateFilters = List[BaseGeneralSchemas.DateFilter]

    #* SortColumn-related types
    ListOfSortColumns = List[BaseGeneralSchemas.SortColumn]

    #* Expansion processor related types
    FieldExpansionProcessor = Callable[[BaseGeneralParametersTransfers.FieldExpansionProcessor], None]