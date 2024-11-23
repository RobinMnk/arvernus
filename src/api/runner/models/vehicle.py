import json
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from api.scenarios.models.standard_magenta_vehicle_dto import StandardMagentaVehicleDTO
from api.scenarios.models.vehicle_data_dto import VehicleDataDto

from ...types import UNSET, Response, Unset

T = TypeVar("T", bound="Vehicle")


@_attrs_define
class Vehicle:
    """
    Attributes:
        id (str): Vehicle ID
        coord_x (float): X Coordinate of the vehicle
        coord_y (float): Y Coordinate of the vehicle
        is_available (Union[Unset, bool]): Availability of the vehicle
        vehicle_speed (Union[Unset, float]): Speed of the vehicle
        customer_id (Union[Unset, str]): ID of the customer assigned to the vehicle
        remaining_travel_time (Union[Unset, float]): Remaining travel time for the vehicle
        distance_travelled (Union[Unset, float]): Total distance the vehicle has travelled
        active_time (Union[Unset, float]): Total active time of the vehicle
        number_of_trips (Union[Unset, int]): Total number of trips made by the vehicle
    """

    id: str
    coord_x: float
    coord_y: float
    is_available: bool
    vehicle_speed: Union[Unset, float] = UNSET
    customer_id: Union[Unset, str] = UNSET
    remaining_travel_time: Union[Unset, float] = UNSET
    distance_travelled: Union[Unset, float] = UNSET
    active_time: Union[Unset, float] = UNSET
    number_of_trips: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        coord_x = self.coord_x

        coord_y = self.coord_y

        is_available = self.is_available

        vehicle_speed = self.vehicle_speed

        customer_id = self.customer_id

        remaining_travel_time = self.remaining_travel_time

        distance_travelled = self.distance_travelled

        active_time = self.active_time

        number_of_trips = self.number_of_trips

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "coordX": coord_x,
                "coordY": coord_y,
                "isAvailable": is_available,
            }
        )

        if vehicle_speed is not UNSET:
            field_dict["vehicleSpeed"] = vehicle_speed
        if customer_id is not UNSET:
            field_dict["customerId"] = customer_id
        if remaining_travel_time is not UNSET:
            field_dict["remainingTravelTime"] = remaining_travel_time
        if distance_travelled is not UNSET:
            field_dict["distanceTravelled"] = distance_travelled
        if active_time is not UNSET:
            field_dict["activeTime"] = active_time
        if number_of_trips is not UNSET:
            field_dict["numberOfTrips"] = number_of_trips

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        coord_x = d.pop("coordX")

        coord_y = d.pop("coordY")

        is_available = d.pop("isAvailable", UNSET)

        vehicle_speed = d.pop("vehicleSpeed", UNSET)

        customer_id = d.pop("customerId", UNSET)

        remaining_travel_time = d.pop("remainingTravelTime", UNSET)

        distance_travelled = d.pop("distanceTravelled", UNSET)

        active_time = d.pop("activeTime", UNSET)

        number_of_trips = d.pop("numberOfTrips", UNSET)

        vehicle = cls(
            id=id,
            coord_x=coord_x,
            coord_y=coord_y,
            is_available=is_available,
            vehicle_speed=vehicle_speed,
            customer_id=customer_id,
            remaining_travel_time=remaining_travel_time,
            distance_travelled=distance_travelled,
            active_time=active_time,
            number_of_trips=number_of_trips,
        )

        vehicle.additional_properties = d
        return vehicle

    @classmethod
    def from_updated_response(cls: Type[T], src_response: Response[Any]) -> list[T]:
        updated_vehicles_raw = src_response.content.decode("UTF-8")
        updated_vehicles_decoded = json.loads(updated_vehicles_raw)
        updated_vehicles_list = updated_vehicles_decoded["updatedVehicles"] if "updatedVehicles" in updated_vehicles_decoded else []
        return [cls.from_dict(vehicle) for vehicle in updated_vehicles_list]

    @classmethod
    def from_dto(cls: Type[T], src_dto: StandardMagentaVehicleDTO):
        vehicle = cls(
            id=str(src_dto.id),
            coord_x=src_dto.coord_x,
            coord_y=src_dto.coord_y,
            is_available=src_dto.is_available,
            vehicle_speed=src_dto.vehicle_speed,
            customer_id=str(src_dto.customer_id),
            remaining_travel_time=src_dto.remaining_travel_time,
            distance_travelled=src_dto.distance_travelled,
            active_time=src_dto.active_time,
            number_of_trips=src_dto.number_of_trips,
        )

        vehicle.additional_properties = dict()
        return vehicle

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
