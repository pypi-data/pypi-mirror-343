from pydantic import Field

from pyshipstation.common.base_model import ShipStationBaseModel


class _ShipStationOrderItemBase(ShipStationBaseModel):
    """
    https://www.shipstation.com/docs/api/models/order-item/
    """

    sku: str = Field(..., examples=["Company0005"])
    quantity: int = Field(..., examples=[5])
    name: str = Field(..., examples=["Water Bottle"])


class ShipStationOrderItemRead(_ShipStationOrderItemBase):
    pass


class ShipStationOrderItemCreate(_ShipStationOrderItemBase):
    pass
