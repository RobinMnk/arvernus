"""Contains all the data models used in inputs/outputs"""

from .customer_dto import CustomerDTO
from .response_message import ResponseMessage
from .scenario_dto import ScenarioDTO
from .scenario_metadata_dto import ScenarioMetadataDTO
from .standard_magenta_vehicle_dto import StandardMagentaVehicleDTO
from .vehicle_data_dto import VehicleDataDto

__all__ = (
    "CustomerDTO",
    "ResponseMessage",
    "ScenarioDTO",
    "ScenarioMetadataDTO",
    "StandardMagentaVehicleDTO",
    "VehicleDataDto",
)
