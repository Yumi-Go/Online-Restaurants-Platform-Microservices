import unittest
import grpc
from concurrent import futures
import restaurant_service_pb2
import restaurant_service_pb2_grpc
from restaurant_server import RestaurantServiceHandler

class TestRestaurantService(unittest.TestCase):
    def setUp(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        restaurant_service_pb2_grpc.add_RestaurantServiceServicer_to_server(
            RestaurantServiceHandler(),
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
