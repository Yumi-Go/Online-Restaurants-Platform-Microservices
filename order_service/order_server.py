import grpc
from concurrent import futures

import order_service_pb2
import order_service_pb2_grpc


"""
Handles order placement, status retrieval, and cancellation.
Stores all data in an in-memory dictionary.
"""
class OrderServiceHandler(order_service_pb2_grpc.OrderServiceServicer):
    def __init__(self):
        # Using a dictionary keyed by order_id
        self._orders = {}

    def PlaceOrder(self, request, context):
        new_id = f"order_{len(self._orders) + 1}"
        self._orders[new_id] = {
            "customer_id": request.customer_id,
            "items": list(request.items),
            "status": "PLACED",
            "total_price": request.total_price
        }
        return order_service_pb2.PlaceOrderResponse(
            order_id=new_id,
            status="PLACED"
        )

    def GetOrderStatus(self, request, context):
        oid = request.order_id
        if oid in self._orders:
            details = self._orders[oid]
            return order_service_pb2.GetOrderStatusResponse(
                order_id=oid,
                status=details["status"],
                items=details["items"],
                total_price=details["total_price"]
            )

        # If the order isn't found, set a gRPC error
        if context is not None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("No order found with that ID.")
        return order_service_pb2.GetOrderStatusResponse()

    def CancelOrder(self, request, context):
        oid = request.order_id
        if oid in self._orders:
            current_status = self._orders[oid]["status"]
            # Only allow cancellation if it hasn't been accepted yet
            if current_status == "PLACED":
                self._orders[oid]["status"] = "CANCELED"
                return order_service_pb2.CancelOrderResponse(
                    order_id=oid,
                    status="CANCELED"
                )
            else:
                return order_service_pb2.CancelOrderResponse(
                    order_id=oid,
                    status="COULD_NOT_CANCEL"
                )

        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details("Unable to find the specified order.")
        return order_service_pb2.CancelOrderResponse()


def run_order_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    order_service_pb2_grpc.add_OrderServiceServicer_to_server(
        OrderServiceHandler(),
        server
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    print("[OrderService] Listening on port 50051...")
    server.wait_for_termination()


if __name__ == "__main__":
    run_order_server()
