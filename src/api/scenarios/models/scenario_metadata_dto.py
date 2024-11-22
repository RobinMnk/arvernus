from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ...types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.vehicle_data_dto import VehicleDataDto


T = TypeVar("T", bound="ScenarioMetadataDTO")


@_attrs_define
class ScenarioMetadataDTO:
    """The scenario metadata data transfer object

    Attributes:
        end_time (str):
        id (UUID):
        start_time (str):
        status (str):
        vehicle_data (Union[Unset, List['VehicleDataDto']]):
    """

    end_time: str
    id: UUID
    start_time: str
    status: str
    vehicle_data: Union[Unset, List["VehicleDataDto"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        end_time = self.end_time

        id = str(self.id)

        start_time = self.start_time

        status = self.status

        vehicle_data: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.vehicle_data, Unset):
            vehicle_data = []
            for vehicle_data_item_data in self.vehicle_data:
                vehicle_data_item = vehicle_data_item_data.to_dict()
                vehicle_data.append(vehicle_data_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "endTime": end_time,
                "id": id,
                "startTime": start_time,
                "status": status,
            }
        )
        if vehicle_data is not UNSET:
            field_dict["vehicleData"] = vehicle_data

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.vehicle_data_dto import VehicleDataDto

        d = src_dict.copy()
        end_time = d.pop("endTime")

        id = UUID(d.pop("id"))

        start_time = d.pop("startTime")

        status = d.pop("status")

        vehicle_data = []
        _vehicle_data = d.pop("vehicleData", UNSET)
        for vehicle_data_item_data in _vehicle_data or []:
            vehicle_data_item = VehicleDataDto.from_dict(vehicle_data_item_data)

            vehicle_data.append(vehicle_data_item)

        scenario_metadata_dto = cls(
            end_time=end_time,
            id=id,
            start_time=start_time,
            status=status,
            vehicle_data=vehicle_data,
        )

        scenario_metadata_dto.additional_properties = d
        return scenario_metadata_dto

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
