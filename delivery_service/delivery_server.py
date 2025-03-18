import grpc
from concurrent import futures

import delivery_service_pb2
import delivery_service_pb2_grpc

class DeliveryServiceServicer(delivery_service_pb2_grpc.DeliveryServiceServicer):
    def __init__(self):
        # Tracking all assignments in memory
        self.assignments = {}
        self.counter = 0

    def AssignDriver(self, request, context):
        self.counter += 1
        assignment_id = f"assignment_{self.counter}"
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
        context.set_details("Assignment not found for order.")
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

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    delivery_service_pb2_grpc.add_DeliveryServiceServicer_to_server(
        DeliveryServiceServicer(),
        server
    )
    server.add_insecure_port('[::]:50053')
    server.start()
    print("Delivery Service running on port 50053...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
