from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UpdateMenuRequest(_message.Message):
    __slots__ = ("restaurant_id", "items")
    RESTAURANT_ID_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    restaurant_id: str
    items: _containers.RepeatedCompositeFieldContainer[MenuItem]
    def __init__(self, restaurant_id: _Optional[str] = ..., items: _Optional[_Iterable[_Union[MenuItem, _Mapping]]] = ...) -> None: ...

class UpdateMenuResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: str
    def __init__(self, status: _Optional[str] = ...) -> None: ...

class MenuItem(_message.Message):
    __slots__ = ("item_id", "name", "price", "description")
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    item_id: str
    name: str
    price: float
    description: str
    def __init__(self, item_id: _Optional[str] = ..., name: _Optional[str] = ..., price: _Optional[float] = ..., description: _Optional[str] = ...) -> None: ...

class AcceptOrderRequest(_message.Message):
    __slots__ = ("restaurant_id", "order_id")
    RESTAURANT_ID_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    restaurant_id: str
    order_id: str
    def __init__(self, restaurant_id: _Optional[str] = ..., order_id: _Optional[str] = ...) -> None: ...

class AcceptOrderResponse(_message.Message):
    __slots__ = ("order_id", "status")
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    order_id: str
    status: str
    def __init__(self, order_id: _Optional[str] = ..., status: _Optional[str] = ...) -> None: ...

class RejectOrderRequest(_message.Message):
    __slots__ = ("restaurant_id", "order_id")
    RESTAURANT_ID_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    restaurant_id: str
    order_id: str
    def __init__(self, restaurant_id: _Optional[str] = ..., order_id: _Optional[str] = ...) -> None: ...

class RejectOrderResponse(_message.Message):
    __slots__ = ("order_id", "status")
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    order_id: str
    status: str
    def __init__(self, order_id: _Optional[str] = ..., status: _Optional[str] = ...) -> None: ...
