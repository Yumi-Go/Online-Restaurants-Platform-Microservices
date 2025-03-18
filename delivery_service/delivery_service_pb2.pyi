from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AssignDriverRequest(_message.Message):
    __slots__ = ("order_id", "driver_id")
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    DRIVER_ID_FIELD_NUMBER: _ClassVar[int]
    order_id: str
    driver_id: str
    def __init__(self, order_id: _Optional[str] = ..., driver_id: _Optional[str] = ...) -> None: ...

class AssignDriverResponse(_message.Message):
    __slots__ = ("assignment_id", "status")
    ASSIGNMENT_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    assignment_id: str
    status: str
    def __init__(self, assignment_id: _Optional[str] = ..., status: _Optional[str] = ...) -> None: ...

class UpdateDeliveryStatusRequest(_message.Message):
    __slots__ = ("order_id", "status")
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    order_id: str
    status: str
    def __init__(self, order_id: _Optional[str] = ..., status: _Optional[str] = ...) -> None: ...

class UpdateDeliveryStatusResponse(_message.Message):
    __slots__ = ("order_id", "status")
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    order_id: str
    status: str
    def __init__(self, order_id: _Optional[str] = ..., status: _Optional[str] = ...) -> None: ...

class GetDriverAssignmentsRequest(_message.Message):
    __slots__ = ("driver_id",)
    DRIVER_ID_FIELD_NUMBER: _ClassVar[int]
    driver_id: str
    def __init__(self, driver_id: _Optional[str] = ...) -> None: ...

class GetDriverAssignmentsResponse(_message.Message):
    __slots__ = ("assignments",)
    ASSIGNMENTS_FIELD_NUMBER: _ClassVar[int]
    assignments: _containers.RepeatedCompositeFieldContainer[DeliveryAssignment]
    def __init__(self, assignments: _Optional[_Iterable[_Union[DeliveryAssignment, _Mapping]]] = ...) -> None: ...

class DeliveryAssignment(_message.Message):
    __slots__ = ("assignment_id", "order_id", "status")
    ASSIGNMENT_ID_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    assignment_id: str
    order_id: str
    status: str
    def __init__(self, assignment_id: _Optional[str] = ..., order_id: _Optional[str] = ..., status: _Optional[str] = ...) -> None: ...
