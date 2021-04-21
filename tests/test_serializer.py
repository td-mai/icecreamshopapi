from icecreamshop.models import Product, Order, ProductOrder
from icecreamshop.api.serializer import ProductSerializer, OrderSerializer, ProductOrderSerializer
from django.test import TestCase

class ProductSerializerTestClass(TestCase):

    def test_serializer(self):
        p = Product.objects.create(flavor='Flavor1', unit_price=2, max_quantity=40, remaining_quantity=40)
        s = ProductSerializer(p)
        self.assertDictEqual(s.data, {
                            "id": p.id,
                            "flavor": "Flavor1",
                            "recipe": "",
                            "unit_price": p.unit_price,
                            "remaining_quantity": 40,
                            "max_quantity": 40,
                            "image": None
                                  })


class DetailOrderSerializerTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        p1 = Product.objects.create(flavor='Flavor1', unit_price=2, max_quantity=40, remaining_quantity=40)
        p2 = Product.objects.create(flavor='Flavor2', unit_price=2, max_quantity=40, remaining_quantity=40)
        o = Order.objects.create(order_number="123ABC", client_name="me")
        ProductOrder(product=p1, order=o, quantity=5).save()
        ProductOrder(product=p2, order=o, quantity=5).save()

    def test_serializer(self):
        o = Order.objects.get(order_number="123ABC")
        s = OrderSerializer(o)
        po = ProductOrder.objects.filter(order=o)
        s_po = ProductOrderSerializer(po, many=True)
        self.assertEqual(s.data["order_number"], o.order_number)
        self.assertEqual(s.data["total_price"], o.total_price)
        self.assertEqual(s.data["client_name"], o.client_name)
        self.assertEqual(len(s.data["product_orders"]), 2)
        self.assertEqual(s.data["product_orders"], s_po.data)


class ProductOrderSerializerTestClass(TestCase):

    def test_serializer(self):
        p1 = Product.objects.create(flavor='Flavor1', unit_price=2, max_quantity=40, remaining_quantity=40)
        o = Order.objects.create(order_number="123ABC", client_name="me")
        po= ProductOrder.objects.create(product=p1, order=o, quantity=5)
        sp = ProductSerializer(p1)
        s_po = ProductOrderSerializer(po)
        self.assertEqual(s_po.data["product"], sp.data)
        self.assertEqual(s_po.data["quantity"], 5)
        self.assertEqual(s_po.data["price"], 5*p1.unit_price)