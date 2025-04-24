from pydantic import Field, HttpUrl, model_validator

from pyshipstation.common.base_model import ShipStationBaseModel


class Money(ShipStationBaseModel):
    amount: float
    currency: str


class InventoryItem(ShipStationBaseModel):
    sku: str
    on_hand: int
    allocated: int | None = Field(None)
    available: int
    average_cost: Money
    inventory_warehouse_id: str | None = Field(None)
    inventory_location_id: str | None = Field(None)


class Link(ShipStationBaseModel):
    href: HttpUrl | None = Field(None)

    @model_validator(mode="before")
    def allow_empty_dict(cls, values):
        if values == {}:
            return {"href": None}
        return values


class Links(ShipStationBaseModel):
    first: Link | None
    last: Link | None
    prev: Link | None
    next: Link | None


class InventoryResponse(ShipStationBaseModel):
    inventory: list[InventoryItem]
    total: int
    page: int
    pages: int
    links: Links
