from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.customer_dto import CustomerDTO
    from ..models.standard_magenta_vehicle_dto import StandardMagentaVehicleDTO


T = TypeVar("T", bound="ScenarioDTO")


@_attrs_define
class ScenarioDTO:
    """The scenario data transfer object

    Attributes:
        customers (List['CustomerDTO']):
        end_time (str):
        id (UUID):
        start_time (str):
        status (str):
        vehicles (List['StandardMagentaVehicleDTO']):
    """

    customers: List["CustomerDTO"]
    end_time: str
    id: UUID
    start_time: str
    status: str
    vehicles: List["StandardMagentaVehicleDTO"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        customers = []
        for customers_item_data in self.customers:
            customers_item = customers_item_data.to_dict()
            customers.append(customers_item)

        end_time = self.end_time

        id = str(self.id)

        start_time = self.start_time

        status = self.status

        vehicles = []
        for vehicles_item_data in self.vehicles:
            vehicles_item = vehicles_item_data.to_dict()
            vehicles.append(vehicles_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "customers": customers,
                "endTime": end_time,
                "id": id,
                "startTime": start_time,
                "status": status,
                "vehicles": vehicles,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.customer_dto import CustomerDTO
        from ..models.standard_magenta_vehicle_dto import StandardMagentaVehicleDTO

        d = src_dict.copy()
        customers = []
        _customers = d.pop("customers")
        for customers_item_data in _customers:
            customers_item = CustomerDTO.from_dict(customers_item_data)

            customers.append(customers_item)

        end_time = d.pop("endTime")

        id = UUID(d.pop("id"))

        start_time = d.pop("startTime")

        status = d.pop("status")

        vehicles = []
        _vehicles = d.pop("vehicles")
        for vehicles_item_data in _vehicles:
            vehicles_item = StandardMagentaVehicleDTO.from_dict(vehicles_item_data)

            vehicles.append(vehicles_item)

        scenario_dto = cls(
            customers=customers,
            end_time=end_time,
            id=id,
            start_time=start_time,
            status=status,
            vehicles=vehicles,
        )

        scenario_dto.additional_properties = d
        return scenario_dto

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
