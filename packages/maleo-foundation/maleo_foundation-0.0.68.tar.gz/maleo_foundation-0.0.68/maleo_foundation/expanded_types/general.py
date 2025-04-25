from typing import Callable, List, Optional
from maleo_foundation.models.transfers.parameters.general import BaseGeneralParametersTransfers

class BaseGeneralExpandedTypes:
    #* Expansion processor related types
    FieldExpansionProcessor = Callable[
        [BaseGeneralParametersTransfers.FieldExpansionProcessor],
        None
    ]

    ListOfFieldExpansionProcessor = List[
        Callable[
            [BaseGeneralParametersTransfers.FieldExpansionProcessor],
            None
        ]
    ]

    OptionalListOfFieldExpansionProcessor = Optional[
        List[
            Callable[
                [BaseGeneralParametersTransfers.FieldExpansionProcessor],
                None
            ]
        ]
    ]