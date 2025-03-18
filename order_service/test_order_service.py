import unittest
import grpc
from concurrent import futures

# Import gRPC modules generated from .proto
import order_service_pb2
import order_service_pb2_grpc

# Import your actual OrderServiceServicer class
from order_server import OrderServiceServicer

class TestOrderService(unittest.TestCase):
    def setUp(self):
        # Create a gRPC server and add the OrderServiceServicer
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        order_service_pb2_grpc.add_OrderServiceServicer_to_server(
            OrderServiceServicer(),
            self.server
        )
        # Bind to an ephemeral port on localhost
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
        # First place an order
        place_req = order_service_pb2.PlaceOrderRequest(
            customer_id="cust_002",
            items=["itemA"],
            total_price=10.0
        )
        place_res = self.stub.PlaceOrder(place_req)

        # Now fetch its status
        status_req = order_service_pb2.GetOrderStatusRequest(order_id=place_res.order_id)
        status_res = self.stub.GetOrderStatus(status_req)
        self.assertEqual(place_res.order_id, status_res.order_id)
        self.assertEqual("PLACED", status_res.status)

    def test_get_order_status_not_found(self):
        status_req = order_service_pb2.GetOrderStatusRequest(order_id="nonexistent")
        # This call should trigger a gRPC NOT_FOUND status
        with self.assertRaises(grpc.RpcError) as context:
            self.stub.GetOrderStatus(status_req)
        self.assertEqual(grpc.StatusCode.NOT_FOUND, context.exception.code())

    def test_cancel_order(self):
        # Place an order first
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

        # Try canceling again, should fail or return COULD_NOT_CANCEL
        cancel_res2 = self.stub.CancelOrder(cancel_req)
        self.assertEqual("COULD_NOT_CANCEL", cancel_res2.status)

if __name__ == '__main__':
    unittest.main()








# import grpc
# import order_service_pb2
# import order_service_pb2_grpc
#
# def run():
#     """
#     Connect to the OrderService gRPC server and invoke each RPC
#     to verify it's functioning end-to-end.
#     """
#
#     # If you're running via Docker Compose, use the service name 'order_service'
#     # plus the port it exposes (e.g. 50051). If running locally, try 'localhost:50051'.
#     with grpc.insecure_channel('order_service:50051') as channel:
#         stub = order_service_pb2_grpc.OrderServiceStub(channel)
#
#         # 1. Place an order
#         place_response = stub.PlaceOrder(order_service_pb2.PlaceOrderRequest(
#             customer_id="test_customer",
#             items=["burger", "fries"],
#             total_price=12.99
#         ))
#         print("=== PlaceOrder Response ===")
#         print(f"Order ID  : {place_response.order_id}")
#         print(f"Status    : {place_response.status}")
#         print("")
#
#         # 2. Get the order status
#         status_response = stub.GetOrderStatus(order_service_pb2.GetOrderStatusRequest(
#             order_id=place_response.order_id
#         ))
#         print("=== GetOrderStatus Response ===")
#         print(f"Order ID  : {status_response.order_id}")
#         print(f"Status    : {status_response.status}")
#         print(f"Items     : {status_response.items}")
#         print(f"TotalPrice: {status_response.total_price}")
#         print("")
#
#         # 3. Cancel the order (if possible)
#         cancel_response = stub.CancelOrder(order_service_pb2.CancelOrderRequest(
#             order_id=place_response.order_id
#         ))
#         print("=== CancelOrder Response ===")
#         print(f"Order ID  : {cancel_response.order_id}")
#         print(f"Status    : {cancel_response.status}")
#
# if __name__ == '__main__':
#     run()