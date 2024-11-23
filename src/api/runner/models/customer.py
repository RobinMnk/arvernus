from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from api.scenarios.models.customer_dto import CustomerDTO

from ...types import UNSET, Unset

T = TypeVar("T", bound="Customer")


@_attrs_define
class Customer:
    """
    Attributes:
        id (str): Customer ID
        coord_x (Union[Unset, float]): Customer X coordinate
        coord_y (Union[Unset, float]): Customer Y coordinate
        destination_x (Union[Unset, float]): Customer destination X coordinate
        destination_y (Union[Unset, float]): Customer destination Y coordinate
        awaiting_service (Union[Unset, bool]): Whether the customer is awaiting service
    """

    id: str
    coord_x: Union[Unset, float] = UNSET
    coord_y: Union[Unset, float] = UNSET
    destination_x: Union[Unset, float] = UNSET
    destination_y: Union[Unset, float] = UNSET
    awaiting_service: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        coord_x = self.coord_x

        coord_y = self.coord_y

        destination_x = self.destination_x

        destination_y = self.destination_y

        awaiting_service = self.awaiting_service

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
            }
        )
        if coord_x is not UNSET:
            field_dict["coordX"] = coord_x
        if coord_y is not UNSET:
            field_dict["coordY"] = coord_y
        if destination_x is not UNSET:
            field_dict["destinationX"] = destination_x
        if destination_y is not UNSET:
            field_dict["destinationY"] = destination_y
        if awaiting_service is not UNSET:
            field_dict["awaitingService"] = awaiting_service

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        coord_x = d.pop("coordX", UNSET)

        coord_y = d.pop("coordY", UNSET)

        destination_x = d.pop("destinationX", UNSET)

        destination_y = d.pop("destinationY", UNSET)

        awaiting_service = d.pop("awaitingService", UNSET)

        customer = cls(
            id=id,
            coord_x=coord_x,
            coord_y=coord_y,
            destination_x=destination_x,
            destination_y=destination_y,
            awaiting_service=awaiting_service,
        )

        customer.additional_properties = d
        return customer

    @classmethod
    def from_dto(cls: Type[T], src_dto: CustomerDTO):
        customer = cls(
            id=str(src_dto.id),
            coord_x=src_dto.coord_x,
            coord_y=src_dto.coord_y,
            destination_x=src_dto.destination_x,
            destination_y=src_dto.destination_y,
            awaiting_service=src_dto.awaiting_service,
        )

        customer.additional_properties = dict()
        return customer

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
