from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import uuid
from icecreamshop.models import *
from icecreamshop.api.serializer import *
from icecreamshop.api.validators import order_data_validator

class OrderListApiView(APIView):
    http_method_names = ['get', 'post']
    def get(self, request, *args, **kwargs):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Create an order
        :param request data:
            {
                "client_name": "me",
                "product_orders": [
                    {
                        "product": 1,
                        "quantity": 8
                    },
                    {
                        "product": 2,
                        "quantity": 10
                    }
                ]
            }
        """
        order_number = uuid.uuid4().hex.upper()[0:6]
        try:
            order_data_validator(request.data)
            data = {
                'product_orders': request.data.get('product_orders'),
                'client_name': request.data.get('client_name'),
                'order_number': order_number
            }
            if data['product_orders']:
                order_obj = Order(**{
                    "order_number": data["order_number"],
                    "client_name": data["client_name"],
                })
                order_obj.save()
                for product_order_data in data["product_orders"]:
                    product_obj = Product.objects.get(pk=product_order_data["product"])
                    product_order_data["product"] = product_obj
                    product_order_data["order"] = order_obj
                    p_order = ProductOrder(**product_order_data)
                    p_order.save()

                serializer = OrderSerializer(order_obj)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as err:
            return Response({"res": str(err)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"res": "Data is not valid."}, status=status.HTTP_400_BAD_REQUEST)

class ProductListApiView(APIView):
    http_method_names = ['get']
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderDetailApiView(APIView):
    http_method_names = ['get']
    def get_object(self, order_number):
        try:
            return Order.objects.get(order_number=order_number)
        except Order.DoesNotExist:
            return None

    def get(self, request, order_number, *args, **kwargs):
        order_instance = self.get_object(order_number)
        if not order_instance:
            return Response(
                {"res": "Order with number %s does not exists"%order_number},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = OrderSerializer(order_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
