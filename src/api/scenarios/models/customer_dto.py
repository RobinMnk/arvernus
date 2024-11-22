from typing import Any, Dict, List, Type, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CustomerDTO")


@_attrs_define
class CustomerDTO:
    """The customer data transfer object

    Attributes:
        awaiting_service (bool):
        coord_x (float):
        coord_y (float):
        destination_x (float):
        destination_y (float):
        id (UUID):
    """

    awaiting_service: bool
    coord_x: float
    coord_y: float
    destination_x: float
    destination_y: float
    id: UUID
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        awaiting_service = self.awaiting_service

        coord_x = self.coord_x

        coord_y = self.coord_y

        destination_x = self.destination_x

        destination_y = self.destination_y

        id = str(self.id)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "awaitingService": awaiting_service,
                "coordX": coord_x,
                "coordY": coord_y,
                "destinationX": destination_x,
                "destinationY": destination_y,
                "id": id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        awaiting_service = d.pop("awaitingService")

        coord_x = d.pop("coordX")

        coord_y = d.pop("coordY")

        destination_x = d.pop("destinationX")

        destination_y = d.pop("destinationY")

        id = UUID(d.pop("id"))

        customer_dto = cls(
            awaiting_service=awaiting_service,
            coord_x=coord_x,
            coord_y=coord_y,
            destination_x=destination_x,
            destination_y=destination_y,
            id=id,
        )

        customer_dto.additional_properties = d
        return customer_dto

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
