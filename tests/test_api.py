from rest_framework import status
from rest_framework.test import APITestCase
from icecreamshop.models import Product, Order, ProductOrder

class ProductListViewApiTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        p1 = Product.objects.create(flavor='Flavor1', unit_price=2, max_quantity=40, remaining_quantity=40)
        p2 = Product.objects.create(flavor='Flavor2', unit_price=2, max_quantity=40, remaining_quantity=40)
        p3 = Product.objects.create(flavor='Flavor3', unit_price=2, max_quantity=40, remaining_quantity=40)

    def test_get_products(self):
        url = '/api/products/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]["flavor"], "Flavor1")


class OrderListViewApiTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        p1 = Product.objects.create(flavor='Flavor1', unit_price=2, max_quantity=40, remaining_quantity=40)
        p2 = Product.objects.create(flavor='Flavor2', unit_price=2, max_quantity=40, remaining_quantity=40)
        o = Order.objects.create(order_number="123ABC", client_name="me")
        ProductOrder(product=p1, order=o, quantity=5).save()
        ProductOrder(product=p2, order=o, quantity=5).save()

    def test_get_orders(self):
        url = '/api/orders/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        o = response.data[0]
        self.assertEqual(o["order_number"], "123ABC")
        self.assertEqual(len(o["product_orders"]), 2)
        self.assertEqual(o["total_price"], 20)

    def test_post_create_order(self):
        url = '/api/orders/'
        data = {
            "client_name": "joe",
            "product_orders": [
                {
                    "product": Product.objects.get(flavor ="Flavor1").id,
                    "quantity": 3,
                },
                {
                    "product": Product.objects.get(flavor ="Flavor2").id,
                    "quantity": 7,
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["client_name"], "joe")
        onum = response.data["order_number"]
        self.assertEqual(Order.objects.filter(order_number=onum).count(), 1)

    def test_post_bad_request(self):
        url = '/api/orders/'
        data = {
            "client_name": "joe",
            "product_orders": [
                {
                    "product": Product.objects.get(flavor ="Flavor1").id,
                    "quantity": 3,
                },
                {
                    "product": Product.objects.get(flavor ="Flavor2").id,
                    "quantity": 41,
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DetailOrderViewApiTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        p1 = Product.objects.create(flavor='Flavor1', unit_price=2, max_quantity=40, remaining_quantity=40)
        p2 = Product.objects.create(flavor='Flavor2', unit_price=2, max_quantity=40, remaining_quantity=40)
        o = Order.objects.create(order_number="123ABC", client_name="me")
        ProductOrder(product=p1, order=o, quantity=5).save()
        ProductOrder(product=p2, order=o, quantity=5).save()

    def test_get_order_by_number(self):
        url = '/api/orders/123ABC/'
        response = self.client.get(url, format='json')
        o = response.data
        self.assertEqual(o["order_number"], "123ABC")
        self.assertEqual(len(o["product_orders"]), 2)
        self.assertEqual(o["total_price"], 20)
