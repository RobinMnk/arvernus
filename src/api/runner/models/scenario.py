from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from api.scenarios.models.scenario_dto import ScenarioDTO

from ...types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.customer import Customer
    from ..models.vehicle import Vehicle


T = TypeVar("T", bound="Scenario")


@_attrs_define
class Scenario:
    """
    Attributes:
        id (str): Scenario ID
        start_time (Union[Unset, str]): Start time of the scenario
        end_time (Union[Unset, str]): End time of the scenario
        status (Union[Unset, str]): Status of the scenario
        vehicles (Union[Unset, List['Vehicle']]): List of vehicles
        customers (Union[Unset, List['Customer']]): List of customers
    """

    id: str
    start_time: Union[Unset, str] = UNSET
    end_time: Union[Unset, str] = UNSET
    status: Union[Unset, str] = UNSET
    vehicles: Union[Unset, List["Vehicle"]] = UNSET
    customers: Union[Unset, List["Customer"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        start_time = self.start_time

        end_time = self.end_time

        status = self.status

        vehicles: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.vehicles, Unset):
            vehicles = []
            for vehicles_item_data in self.vehicles:
                vehicles_item = vehicles_item_data.to_dict()
                vehicles.append(vehicles_item)

        customers: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.customers, Unset):
            customers = []
            for customers_item_data in self.customers:
                customers_item = customers_item_data.to_dict()
                customers.append(customers_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
            }
        )
        if start_time is not UNSET:
            field_dict["startTime"] = start_time
        if end_time is not UNSET:
            field_dict["endTime"] = end_time
        if status is not UNSET:
            field_dict["status"] = status
        if vehicles is not UNSET:
            field_dict["vehicles"] = vehicles
        if customers is not UNSET:
            field_dict["customers"] = customers

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.customer import Customer
        from ..models.vehicle import Vehicle

        d = src_dict.copy()
        id = d.pop("id")

        start_time = d.pop("startTime", UNSET)

        end_time = d.pop("endTime", UNSET)

        status = d.pop("status", UNSET)

        vehicles = []
        _vehicles = d.pop("vehicles", UNSET)
        for vehicles_item_data in _vehicles or []:
            vehicles_item = Vehicle.from_dict(vehicles_item_data)

            vehicles.append(vehicles_item)

        customers = []
        _customers = d.pop("customers", UNSET)
        for customers_item_data in _customers or []:
            customers_item = Customer.from_dict(customers_item_data)

            customers.append(customers_item)

        scenario = cls(
            id=id,
            start_time=start_time,
            end_time=end_time,
            status=status,
            vehicles=vehicles,
            customers=customers,
        )

        scenario.additional_properties = d
        return scenario

    @classmethod
    def from_dto(cls: Type[T], src_dto: ScenarioDTO):
        scenario = cls(
            id=str(src_dto.id),
            start_time=src_dto.start_time,
            end_time=src_dto.end_time,
            status=src_dto.status,
            vehicles=[Vehicle.from_dto(vehicle) for vehicle in src_dto.vehicles],
            customers=[Customer.from_dto(customer) for customer in src_dto.customers],
        )

        scenario.additional_properties = dict()
        return scenario

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
