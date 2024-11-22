from typing import Any, Dict, List, Type, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="VehicleDataDto")


@_attrs_define
class VehicleDataDto:
    """The vehicle data transfer object

    Attributes:
        id (UUID):
        total_travel_time (int):
        total_trips (int):
        travel_times (str):
    """

    id: UUID
    total_travel_time: int
    total_trips: int
    travel_times: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = str(self.id)

        total_travel_time = self.total_travel_time

        total_trips = self.total_trips

        travel_times = self.travel_times

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "totalTravelTime": total_travel_time,
                "totalTrips": total_trips,
                "travelTimes": travel_times,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = UUID(d.pop("id"))

        total_travel_time = d.pop("totalTravelTime")

        total_trips = d.pop("totalTrips")

        travel_times = d.pop("travelTimes")

        vehicle_data_dto = cls(
            id=id,
            total_travel_time=total_travel_time,
            total_trips=total_trips,
            travel_times=travel_times,
        )

        vehicle_data_dto.additional_properties = d
        return vehicle_data_dto

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
