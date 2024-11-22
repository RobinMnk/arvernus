from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ...types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.vehicle_update import VehicleUpdate


T = TypeVar("T", bound="UpdateScenario")


@_attrs_define
class UpdateScenario:
    """
    Attributes:
        vehicles (Union[Unset, List['VehicleUpdate']]): List of updated vehicles
    """

    vehicles: Union[Unset, List["VehicleUpdate"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        vehicles: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.vehicles, Unset):
            vehicles = []
            for vehicles_item_data in self.vehicles:
                vehicles_item = vehicles_item_data.to_dict()
                vehicles.append(vehicles_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if vehicles is not UNSET:
            field_dict["vehicles"] = vehicles

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.vehicle_update import VehicleUpdate

        d = src_dict.copy()
        vehicles = []
        _vehicles = d.pop("vehicles", UNSET)
        for vehicles_item_data in _vehicles or []:
            vehicles_item = VehicleUpdate.from_dict(vehicles_item_data)

            vehicles.append(vehicles_item)

        update_scenario = cls(
            vehicles=vehicles,
        )

        update_scenario.additional_properties = d
        return update_scenario

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
