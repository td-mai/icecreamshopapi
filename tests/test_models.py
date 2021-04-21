from django.test import TestCase
from icecreamshop.models import Product, ProductOrder, Order
from django.core.exceptions import ValidationError
from django.db.models import Sum

import io
import unittest.mock

class ProductTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        Product.objects.create(flavor='Flavor1', unit_price=2, max_quantity=40, remaining_quantity=40)

    def test_clean(self):
        with self.assertRaises(ValidationError):
            Product.objects.create(flavor='Flavor1', unit_price=2, max_quantity=40, remaining_quantity=50)

class ProductOrderTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        p1 = Product.objects.create(flavor='Flavor1', unit_price=2, max_quantity=40, remaining_quantity=40)
        p2 = Product.objects.create(flavor='Flavor2', unit_price=2, max_quantity=40, remaining_quantity=40)
        o = Order.objects.create(order_number="123ABC")
        ProductOrder.objects.create(order=o, product=p1, quantity=2)

    def test_calculate_price(self):
        po = ProductOrder.objects.filter(order__order_number="123ABC").first()
        self.assertEqual(po.price, po.product.unit_price * po.quantity)

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_message_empty_pot(self, mock_stdout):
        p2 = Product.objects.get(flavor='Flavor2')
        o = Order.objects.get(order_number="123ABC")
        po2 = ProductOrder.objects.create(order=o, product=p2, quantity=40)
        self.assertEqual(mock_stdout.getvalue(), "Message to admin: Pot %s is empty. Please fulfill the pot.\n"%p2.flavor)

    def test_order_total_price(self):
        p2 = Product.objects.get(flavor='Flavor1')
        o = Order.objects.get(order_number="123ABC")
        po3 = ProductOrder.objects.create(order=o, product=p2, quantity=5)
        total_price = ProductOrder.objects.filter(order=o).aggregate(Sum("price"))["price__sum"]
        self.assertEqual(total_price, o.total_price)

    def test_order_greater_than_remaining(self):
        p1 = Product.objects.get(flavor='Flavor1')
        o = Order.objects.get(order_number="123ABC")
        remain = p1.remaining_quantity
        with self.assertRaises(ValidationError):
            ProductOrder.objects.create(order=o, product=p1, quantity=remain+1)