import unittest
import grpc
from concurrent import futures

# Import gRPC modules generated from .proto
import restaurant_service_pb2
import restaurant_service_pb2_grpc

# Import your actual RestaurantServiceServicer class
from restaurant_server import RestaurantServiceServicer

class TestRestaurantService(unittest.TestCase):
    def setUp(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        restaurant_service_pb2_grpc.add_RestaurantServiceServicer_to_server(
            RestaurantServiceServicer(),
            self.server
        )
        port = self.server.add_insecure_port('localhost:0')
        self.server.start()

        self.channel = grpc.insecure_channel(f'localhost:{port}')
        self.stub = restaurant_service_pb2_grpc.RestaurantServiceStub(self.channel)

    def tearDown(self):
        self.server.stop(None)

    def test_update_menu(self):
        menu_req = restaurant_service_pb2.UpdateMenuRequest(
            restaurant_id="rest_001",
            items=[
                restaurant_service_pb2.MenuItem(
                    item_id="food_1",
                    name="Burger",
                    price=8.99,
                    description="A delicious burger"
                ),
                restaurant_service_pb2.MenuItem(
                    item_id="food_2",
                    name="Fries",
                    price=2.99,
                    description="Crispy fries"
                )
            ]
        )
        menu_res = self.stub.UpdateMenu(menu_req)
        self.assertEqual("SUCCESS", menu_res.status)

    def test_accept_order(self):
        accept_req = restaurant_service_pb2.AcceptOrderRequest(
            restaurant_id="rest_001",
            order_id="order_123"
        )
        accept_res = self.stub.AcceptOrder(accept_req)
        self.assertEqual("order_123", accept_res.order_id)
        self.assertEqual("ACCEPTED", accept_res.status)

    def test_reject_order(self):
        reject_req = restaurant_service_pb2.RejectOrderRequest(
            restaurant_id="rest_002",
            order_id="order_456"
        )
        reject_res = self.stub.RejectOrder(reject_req)
        self.assertEqual("order_456", reject_res.order_id)
        self.assertEqual("REJECTED", reject_res.status)

if __name__ == '__main__':
    unittest.main()









# import grpc
# import restaurant_service_pb2
# import restaurant_service_pb2_grpc
#
# def run():
#     """
#     Connect to the RestaurantService gRPC server and invoke each RPC.
#     """
#
#     with grpc.insecure_channel('restaurant_service:50052') as channel:
#         stub = restaurant_service_pb2_grpc.RestaurantServiceStub(channel)
#
#         # 1. Update the menu with a new item
#         update_menu_response = stub.UpdateMenu(restaurant_service_pb2.UpdateMenuRequest(
#             restaurant_id="test_restaurant",
#             items=[
#                 restaurant_service_pb2.MenuItem(
#                     item_id="menu_item_1",
#                     name="Cheese Pizza",
#                     price=8.99,
#                     description="A delicious cheese pizza"
#                 ),
#                 restaurant_service_pb2.MenuItem(
#                     item_id="menu_item_2",
#                     name="Veggie Burger",
#                     price=6.99,
#                     description="A healthy veggie burger"
#                 )
#             ]
#         ))
#         print("=== UpdateMenu Response ===")
#         print(f"Status: {update_menu_response.status}")
#         print("")
#
#         # 2. Accept an order
#         accept_order_response = stub.AcceptOrder(restaurant_service_pb2.AcceptOrderRequest(
#             restaurant_id="test_restaurant",
#             order_id="order_1"  # Example ID; in real usage, you'd pass an actual order ID
#         ))
#         print("=== AcceptOrder Response ===")
#         print(f"Order ID: {accept_order_response.order_id}")
#         print(f"Status  : {accept_order_response.status}")
#         print("")
#
#         # 3. Reject an order
#         reject_order_response = stub.RejectOrder(restaurant_service_pb2.RejectOrderRequest(
#             restaurant_id="test_restaurant",
#             order_id="order_2"
#         ))
#         print("=== RejectOrder Response ===")
#         print(f"Order ID: {reject_order_response.order_id}")
#         print(f"Status  : {reject_order_response.status}")
#
# if __name__ == '__main__':
#     run()
