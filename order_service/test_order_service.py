import unittest
import grpc
from concurrent import futures
import order_service_pb2
import order_service_pb2_grpc
from order_server import OrderServiceHandler

class TestOrderService(unittest.TestCase):
    def setUp(self):
        # Create a gRPC server and add the OrderServiceHandler
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        order_service_pb2_grpc.add_OrderServiceServicer_to_server(
            OrderServiceHandler(),
            self.server
        )
        port = self.server.add_insecure_port('localhost:0')
        self.server.start()

        # Create a channel using the actual port that was assigned
        self.channel = grpc.insecure_channel(f'localhost:{port}')
        self.stub = order_service_pb2_grpc.OrderServiceStub(self.channel)

    def tearDown(self):
        # Stop the server
        self.server.stop(None)

    def test_place_order(self):
        request = order_service_pb2.PlaceOrderRequest(
            customer_id="cust_001",
            items=["item1", "item2"],
            total_price=25.50
        )
        response = self.stub.PlaceOrder(request)
        self.assertIn("order_", response.order_id)
        self.assertEqual("PLACED", response.status)

    def test_get_order_status_found(self):
        # Place an order
        place_req = order_service_pb2.PlaceOrderRequest(
            customer_id="cust_002",
            items=["itemA"],
            total_price=10.0
        )
        place_res = self.stub.PlaceOrder(place_req)

        # Fetch its status
        status_req = order_service_pb2.GetOrderStatusRequest(order_id=place_res.order_id)
        status_res = self.stub.GetOrderStatus(status_req)
        self.assertEqual(place_res.order_id, status_res.order_id)
        self.assertEqual("PLACED", status_res.status)

    def test_get_order_status_not_found(self):
        status_req = order_service_pb2.GetOrderStatusRequest(order_id="nonexistent")
        with self.assertRaises(grpc.RpcError) as context:
            self.stub.GetOrderStatus(status_req)
        self.assertEqual(grpc.StatusCode.NOT_FOUND, context.exception.code())

    def test_cancel_order(self):
        # Place an order
        place_req = order_service_pb2.PlaceOrderRequest(
            customer_id="cust_003",
            items=["itemX"],
            total_price=5.0
        )
        place_res = self.stub.PlaceOrder(place_req)

        # Cancel it
        cancel_req = order_service_pb2.CancelOrderRequest(order_id=place_res.order_id)
        cancel_res = self.stub.CancelOrder(cancel_req)
        self.assertEqual(place_res.order_id, cancel_res.order_id)
        self.assertEqual("CANCELED", cancel_res.status)

        # Try canceling again
        # It should fail or return COULD_NOT_CANCEL
        cancel_res2 = self.stub.CancelOrder(cancel_req)
        self.assertEqual("COULD_NOT_CANCEL", cancel_res2.status)

if __name__ == '__main__':
    unittest.main()
