import os
import redis
import grpc
from concurrent import futures

import restaurant_service_pb2
import restaurant_service_pb2_grpc

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = os.environ.get("REDIS_PORT", "6379")

# Initialize a Redis connection (db=0 by default)
redis_conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

"""
Handles restaurant-specific data: menus, order acceptance/rejection,
and publishes events via Redis Pub/Sub.
"""
class RestaurantServiceHandler(restaurant_service_pb2_grpc.RestaurantServiceServicer):
    def __init__(self):
        self.menus = {}
        self.order_statuses = {}

    def UpdateMenu(self, request, context):
        """
        Adds or updates menu items for a specific restaurant.
        """
        rest_id = request.restaurant_id
        if rest_id not in self.menus:
            self.menus[rest_id] = []

        for item in request.items:
            self.menus[rest_id].append({
                'item_id': item.item_id,
                'name': item.name,
                'price': item.price,
                'description': item.description
            })
        return restaurant_service_pb2.UpdateMenuResponse(status="SUCCESS")

    def AcceptOrder(self, request, context):
        """
        Accepts a given order and publishes a message to the 'order_events' channel.
        """
        self.order_statuses[request.order_id] = "ACCEPTED"
        message_body = f"ORDER_ACCEPTED:{request.order_id}"
        redis_conn.publish("order_events", message_body)
        return restaurant_service_pb2.AcceptOrderResponse(
            order_id=request.order_id,
            status="ACCEPTED"
        )

    def RejectOrder(self, request, context):
        """
        Marks an order as 'REJECTED'.
        """
        self.order_statuses[request.order_id] = "REJECTED"
        return restaurant_service_pb2.RejectOrderResponse(
            order_id=request.order_id,
            status="REJECTED"
        )


def run_restaurant_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    restaurant_service_pb2_grpc.add_RestaurantServiceServicer_to_server(
        RestaurantServiceHandler(),
        server
    )
    server.add_insecure_port('[::]:50052')
    server.start()
    print("[RestaurantService] Listening on port 50052...")
    server.wait_for_termination()


if __name__ == "__main__":
    run_restaurant_server()
