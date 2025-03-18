# import grpc
# from order_service import order_service_pb2, order_service_pb2_grpc
# from restaurant_service import restaurant_service_pb2, restaurant_service_pb2_grpc
# from delivery_service import delivery_service_pb2, delivery_service_pb2_grpc

import sys
import grpc
sys.path.append("order_service")
sys.path.append("restaurant_service")
sys.path.append("delivery_service")

from order_service import order_service_pb2
from order_service import order_service_pb2_grpc
from restaurant_service import restaurant_service_pb2
from restaurant_service import restaurant_service_pb2_grpc
from delivery_service import delivery_service_pb2
from delivery_service import delivery_service_pb2_grpc

def test_order_service():
    """
    1) Connect to Order Service on localhost:50051
    2) Place an order
    3) Get the order status
    """
    print("----- Testing Order Service -----")
    channel = grpc.insecure_channel("localhost:50051")
    stub = order_service_pb2_grpc.OrderServiceStub(channel)

    # Place an order
    place_req = order_service_pb2.PlaceOrderRequest(
        customer_id="customer_xyz",
        items=["burger", "fries"],
        total_price=15.75
    )
    place_res = stub.PlaceOrder(place_req)
    print("PlaceOrder Response:", place_res)

    # Get order status
    status_req = order_service_pb2.GetOrderStatusRequest(order_id=place_res.order_id)
    status_res = stub.GetOrderStatus(status_req)
    print("GetOrderStatus Response:", status_res)
    print()  # blank line

def test_restaurant_service():
    """
    1) Connect to Restaurant Service on localhost:50052
    2) Update menu for a restaurant
    3) Accept an order
    4) Reject another order
    """
    print("----- Testing Restaurant Service -----")
    channel = grpc.insecure_channel("localhost:50052")
    stub = restaurant_service_pb2_grpc.RestaurantServiceStub(channel)

    # Update menu
    update_menu_req = restaurant_service_pb2.UpdateMenuRequest(
        restaurant_id="rest_123",
        items=[
            restaurant_service_pb2.MenuItem(
                item_id="itemA",
                name="Veg Pizza",
                price=9.99,
                description="Delicious vegetarian pizza"
            ),
            restaurant_service_pb2.MenuItem(
                item_id="itemB",
                name="Garlic Bread",
                price=3.49,
                description="Crusty garlic bread"
            )
        ]
    )
    update_menu_res = stub.UpdateMenu(update_menu_req)
    print("UpdateMenu Response:", update_menu_res)

    # Accept an order
    accept_req = restaurant_service_pb2.AcceptOrderRequest(
        restaurant_id="rest_123",
        order_id="order_1"  # For testing, we'll just pass a dummy order ID
    )
    accept_res = stub.AcceptOrder(accept_req)
    print("AcceptOrder Response:", accept_res)

    # Reject an order
    reject_req = restaurant_service_pb2.RejectOrderRequest(
        restaurant_id="rest_123",
        order_id="order_2"
    )
    reject_res = stub.RejectOrder(reject_req)
    print("RejectOrder Response:", reject_res)
    print()  # blank line

def test_delivery_service():
    """
    1) Connect to Delivery Service on localhost:50053
    2) Assign a driver
    3) Update delivery status
    4) Query driver assignments
    """
    print("----- Testing Delivery Service -----")
    channel = grpc.insecure_channel("localhost:50053")
    stub = delivery_service_pb2_grpc.DeliveryServiceStub(channel)

    # Assign a driver
    assign_req = delivery_service_pb2.AssignDriverRequest(
        order_id="order_1",
        driver_id="driver_007"
    )
    assign_res = stub.AssignDriver(assign_req)
    print("AssignDriver Response:", assign_res)

    # Update delivery status
    update_status_req = delivery_service_pb2.UpdateDeliveryStatusRequest(
        order_id="order_1",
        status="OUT_FOR_DELIVERY"
    )
    update_status_res = stub.UpdateDeliveryStatus(update_status_req)
    print("UpdateDeliveryStatus Response:", update_status_res)

    # Get driver assignments
    get_assign_req = delivery_service_pb2.GetDriverAssignmentsRequest(
        driver_id="driver_007"
    )
    get_assign_res = stub.GetDriverAssignments(get_assign_req)
    print("GetDriverAssignments Response:", get_assign_res)
    print()  # blank line

def main():
    test_order_service()
    test_restaurant_service()
    test_delivery_service()

if __name__ == "__main__":
    main()
