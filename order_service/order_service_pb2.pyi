from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class PlaceOrderRequest(_message.Message):
    __slots__ = ("customer_id", "items", "total_price")
    CUSTOMER_ID_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_PRICE_FIELD_NUMBER: _ClassVar[int]
    customer_id: str
    items: _containers.RepeatedScalarFieldContainer[str]
    total_price: float
    def __init__(self, customer_id: _Optional[str] = ..., items: _Optional[_Iterable[str]] = ..., total_price: _Optional[float] = ...) -> None: ...

class PlaceOrderResponse(_message.Message):
    __slots__ = ("order_id", "status")
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    order_id: str
    status: str
    def __init__(self, order_id: _Optional[str] = ..., status: _Optional[str] = ...) -> None: ...

class GetOrderStatusRequest(_message.Message):
    __slots__ = ("order_id",)
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    order_id: str
    def __init__(self, order_id: _Optional[str] = ...) -> None: ...

class GetOrderStatusResponse(_message.Message):
    __slots__ = ("order_id", "status", "items", "total_price")
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_PRICE_FIELD_NUMBER: _ClassVar[int]
    order_id: str
    status: str
    items: _containers.RepeatedScalarFieldContainer[str]
    total_price: float
    def __init__(self, order_id: _Optional[str] = ..., status: _Optional[str] = ..., items: _Optional[_Iterable[str]] = ..., total_price: _Optional[float] = ...) -> None: ...

class CancelOrderRequest(_message.Message):
    __slots__ = ("order_id",)
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    order_id: str
    def __init__(self, order_id: _Optional[str] = ...) -> None: ...

class CancelOrderResponse(_message.Message):
    __slots__ = ("order_id", "status")
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    order_id: str
    status: str
    def __init__(self, order_id: _Optional[str] = ..., status: _Optional[str] = ...) -> None: ...
