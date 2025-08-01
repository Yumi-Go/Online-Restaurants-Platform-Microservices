import unittest
import grpc
from concurrent import futures
import delivery_service_pb2
import delivery_service_pb2_grpc
from delivery_server import DeliveryServiceHandler

class TestDeliveryService(unittest.TestCase):
    def setUp(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        delivery_service_pb2_grpc.add_DeliveryServiceServicer_to_server(
            DeliveryServiceHandler(),
            self.server
        )
        port = self.server.add_insecure_port('localhost:0')
        self.server.start()

        self.channel = grpc.insecure_channel(f'localhost:{port}')
        self.stub = delivery_service_pb2_grpc.DeliveryServiceStub(self.channel)

    def tearDown(self):
        self.server.stop(None)

    def test_assign_driver(self):
        assign_req = delivery_service_pb2.AssignDriverRequest(
            order_id="order_111",
            driver_id="driver_ABC"
        )
        assign_res = self.stub.AssignDriver(assign_req)
        self.assertIn("assignment_", assign_res.assignment_id)
        self.assertEqual("ASSIGNED", assign_res.status)

    def test_update_delivery_status(self):
        # First assign a driver
        assign_req = delivery_service_pb2.AssignDriverRequest(
            order_id="order_222",
            driver_id="driver_XYZ"
        )
        assign_res = self.stub.AssignDriver(assign_req)

        # Now update the delivery status
        update_req = delivery_service_pb2.UpdateDeliveryStatusRequest(
            order_id="order_222",
            status="OUT_FOR_DELIVERY"
        )
        update_res = self.stub.UpdateDeliveryStatus(update_req)
        self.assertEqual("order_222", update_res.order_id)
        self.assertEqual("OUT_FOR_DELIVERY", update_res.status)

    def test_get_driver_assignments(self):
        # Assign multiple orders to the same driver
        self.stub.AssignDriver(
            delivery_service_pb2.AssignDriverRequest(order_id="order_300", driver_id="driver_ABC")
        )
        self.stub.AssignDriver(
            delivery_service_pb2.AssignDriverRequest(order_id="order_301", driver_id="driver_ABC")
        )
        self.stub.AssignDriver(
            delivery_service_pb2.AssignDriverRequest(order_id="order_302", driver_id="driver_123")
        )

        # Now fetch only for driver_ABC
        get_req = delivery_service_pb2.GetDriverAssignmentsRequest(driver_id="driver_ABC")
        get_res = self.stub.GetDriverAssignments(get_req)
        self.assertEqual(2, len(get_res.assignments))
        # Make sure the order IDs match what we assigned
        order_ids = {a.order_id for a in get_res.assignments}
        self.assertEqual({"order_300", "order_301"}, order_ids)

if __name__ == '__main__':
    unittest.main()
