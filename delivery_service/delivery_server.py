import os
import time
import redis
import threading
import grpc
from concurrent import futures

import delivery_service_pb2
import delivery_service_pb2_grpc

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = os.environ.get("REDIS_PORT", "6379")

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

"""
Handles driver assignments, delivery status, and reacts to 'ORDER_ACCEPTED' events from Redis Pub/Sub.
"""
class DeliveryServiceHandler(delivery_service_pb2_grpc.DeliveryServiceServicer):
    def __init__(self):
        # Tracking all assignments in memory
        self.assignments = {}
        self.assign_counter = 0

    def AssignDriver(self, request, context):
        self.assign_counter += 1
        assignment_id = f"assignment_{self.assign_counter}"
        self.assignments[assignment_id] = {
            "order_id": request.order_id,
            "driver_id": request.driver_id,
            "status": "ASSIGNED"
        }
        return delivery_service_pb2.AssignDriverResponse(
            assignment_id=assignment_id,
            status="ASSIGNED"
        )

    def UpdateDeliveryStatus(self, request, context):
        # Find the assignment by order_id
        for assignment_id, data in self.assignments.items():
            if data["order_id"] == request.order_id:
                data["status"] = request.status
                return delivery_service_pb2.UpdateDeliveryStatusResponse(
                    order_id=request.order_id,
                    status=request.status
                )
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details("No matching assignment for this order.")
        return delivery_service_pb2.UpdateDeliveryStatusResponse()

    def GetDriverAssignments(self, request, context):
        result = []
        for assignment_id, data in self.assignments.items():
            if data["driver_id"] == request.driver_id:
                result.append(delivery_service_pb2.DeliveryAssignment(
                    assignment_id=assignment_id,
                    order_id=data["order_id"],
                    status=data["status"]
                ))
        return delivery_service_pb2.GetDriverAssignmentsResponse(assignments=result)

    # Triggered whenever "ORDER_ACCEPTED" is detected
    def auto_assign_driver(self, order_id):
        print(f"[DeliveryService] Detected accepted order {order_id}. Assigning default driver.")
        self.assign_counter += 1
        assignment_id = f"assignment_{self.assign_counter}"
        self.assignments[assignment_id] = {
            "order_id": order_id,
            "driver_id": "driver_auto",
            "status": "ASSIGNED"
        }
        print(f"[DeliveryService] Auto-assigned 'driver_auto' to {order_id}.")

"""
Runs in a separate background thread to listen for events from 'order_events'
"""
def background_subscriber(handler: DeliveryServiceHandler):
    pubsub = redis_client.pubsub()
    pubsub.subscribe("order_events")
    print("[DeliveryService] Subscribed to 'order_events' channel in Redis.")

    for message in pubsub.listen():
        # message is a dict
        # e.g. {'type': 'message', 'pattern': None, 'channel': b'order_events', 'data': b'ORDER_ACCEPTED:order_1'}
        if message["type"] == "message":
            data = message["data"].decode("utf-8")
            # Check if it's an ORDER_ACCEPTED event
            if data.startswith("ORDER_ACCEPTED:"):
                order_id = data.split(":")[1]
                # auto-assign driver
                handler.auto_assign_driver(order_id)



def run_delivery_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    delivery_service_pb2_grpc.add_DeliveryServiceServicer_to_server(
        DeliveryServiceHandler(),
        server
    )
    server.add_insecure_port('[::]:50053')

    # Start a background thread for Redis subscription
    subscriber_thread = threading.Thread(
        target=background_subscriber, args=(DeliveryServiceHandler(),), daemon=True)
    subscriber_thread.start()

    server.start()
    print("[DeliveryService] Listening on port 50053...")
    server.wait_for_termination()

if __name__ == "__main__":
    run_delivery_server()
