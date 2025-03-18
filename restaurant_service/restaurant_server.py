import grpc
from concurrent import futures

import restaurant_service_pb2
import restaurant_service_pb2_grpc

class RestaurantServiceServicer(restaurant_service_pb2_grpc.RestaurantServiceServicer):
    def __init__(self):
        # Example data structures:
        self.menus = {}
        self.order_statuses = {}  # Just a placeholder if you want to track changes

    def UpdateMenu(self, request, context):
        if request.restaurant_id not in self.menus:
            self.menus[request.restaurant_id] = []
        for item in request.items:
            self.menus[request.restaurant_id].append({
                'item_id': item.item_id,
                'name': item.name,
                'price': item.price,
                'description': item.description
            })
        return restaurant_service_pb2.UpdateMenuResponse(status="SUCCESS")

    def AcceptOrder(self, request, context):
        # Here you might integrate with the OrderService, or simply store the acceptance.
        self.order_statuses[request.order_id] = "ACCEPTED"
        return restaurant_service_pb2.AcceptOrderResponse(
            order_id=request.order_id,
            status="ACCEPTED"
        )

    def RejectOrder(self, request, context):
        self.order_statuses[request.order_id] = "REJECTED"
        return restaurant_service_pb2.RejectOrderResponse(
            order_id=request.order_id,
            status="REJECTED"
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    restaurant_service_pb2_grpc.add_RestaurantServiceServicer_to_server(
        RestaurantServiceServicer(),
        server
    )
    server.add_insecure_port('[::]:50052')
    server.start()
    print("Restaurant Service running on port 50052...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
