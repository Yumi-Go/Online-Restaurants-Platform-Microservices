import grpc
from concurrent import futures
import order_service_pb2
import order_service_pb2_grpc

class OrderServiceServicer(order_service_pb2_grpc.OrderServiceServicer):
    def __init__(self):
        self.orders = {}  # In-memory dictionary for demonstration

    def PlaceOrder(self, request, context):
        order_id = f"order_{len(self.orders) + 1}"
        self.orders[order_id] = {
            "customer_id": request.customer_id,
            "items": list(request.items),
            "status": "PLACED",
            "total_price": request.total_price
        }
        return order_service_pb2.PlaceOrderResponse(
            order_id=order_id,
            status="PLACED"
        )

    def GetOrderStatus(self, request, context):
        order_id = request.order_id
        if order_id in self.orders:
            order_data = self.orders[order_id]
            return order_service_pb2.GetOrderStatusResponse(
                order_id=order_id,
                status=order_data["status"],
                items=order_data["items"],
                total_price=order_data["total_price"]
            )
        if context is not None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Order not found.")
        return order_service_pb2.GetOrderStatusResponse()

    def CancelOrder(self, request, context):
        order_id = request.order_id
        if order_id in self.orders:
            # Simple logic: if it's placed but not accepted, allow cancellation
            if self.orders[order_id]["status"] == "PLACED":
                self.orders[order_id]["status"] = "CANCELED"
                return order_service_pb2.CancelOrderResponse(
                    order_id=order_id,
                    status="CANCELED"
                )
            else:
                return order_service_pb2.CancelOrderResponse(
                    order_id=order_id,
                    status="COULD_NOT_CANCEL"
                )
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details("Order not found.")
        return order_service_pb2.CancelOrderResponse()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    order_service_pb2_grpc.add_OrderServiceServicer_to_server(
        OrderServiceServicer(),
        server
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Order Service running on port 50051...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
