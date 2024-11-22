from typing import Any, Dict, List, Optional, Type, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="StandardMagentaVehicleDTO")


@_attrs_define
class StandardMagentaVehicleDTO:
    """The vehicle data transfer object

    Attributes:
        active_time (int):
        coord_x (float):
        coord_y (float):
        customer_id (UUID):
        distance_travelled (float):
        id (UUID):
        is_available (bool):
        number_of_trips (int):
        remaining_travel_time (int):
        vehicle_speed (float):
    """

    active_time: int
    coord_x: float
    coord_y: float
    customer_id: Optional[UUID]
    distance_travelled: float
    id: UUID
    is_available: bool
    number_of_trips: int
    remaining_travel_time: int
    vehicle_speed: float
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        active_time = self.active_time

        coord_x = self.coord_x

        coord_y = self.coord_y

        customer_id = str(self.customer_id)

        distance_travelled = self.distance_travelled

        id = str(self.id)

        is_available = self.is_available

        number_of_trips = self.number_of_trips

        remaining_travel_time = self.remaining_travel_time

        vehicle_speed = self.vehicle_speed

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "activeTime": active_time,
                "coordX": coord_x,
                "coordY": coord_y,
                "customerId": customer_id,
                "distanceTravelled": distance_travelled,
                "id": id,
                "isAvailable": is_available,
                "numberOfTrips": number_of_trips,
                "remainingTravelTime": remaining_travel_time,
                "vehicleSpeed": vehicle_speed,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        active_time = d.pop("activeTime")

        coord_x = d.pop("coordX")

        coord_y = d.pop("coordY")

        customer_id_raw = d.pop("customerId")
        customer_id = UUID(customer_id_raw) if customer_id_raw else None

        distance_travelled = d.pop("distanceTravelled")

        id = UUID(d.pop("id"))

        is_available = d.pop("isAvailable")

        number_of_trips = d.pop("numberOfTrips")

        remaining_travel_time = d.pop("remainingTravelTime")

        vehicle_speed = d.pop("vehicleSpeed")

        standard_magenta_vehicle_dto = cls(
            active_time=active_time,
            coord_x=coord_x,
            coord_y=coord_y,
            customer_id=customer_id,
            distance_travelled=distance_travelled,
            id=id,
            is_available=is_available,
            number_of_trips=number_of_trips,
            remaining_travel_time=remaining_travel_time,
            vehicle_speed=vehicle_speed,
        )

        standard_magenta_vehicle_dto.additional_properties = d
        return standard_magenta_vehicle_dto

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
