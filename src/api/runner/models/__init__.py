"""Contains all the data models used in inputs/outputs"""

from .customer import Customer
from .scenario import Scenario
from .update_scenario import UpdateScenario
from .vehicle import Vehicle
from .vehicle_update import VehicleUpdate

__all__ = (
    "Customer",
    "Scenario",
    "UpdateScenario",
    "Vehicle",
    "VehicleUpdate",
)
