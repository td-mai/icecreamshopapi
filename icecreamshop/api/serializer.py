from rest_framework import serializers
from icecreamshop.models import Product, Order, ProductOrder

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductOrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer( read_only=True)
    class Meta:
        model = ProductOrder
        fields = ['pk', 'product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    product_orders = ProductOrderSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['order_number', 'order_date', 'client_name', 'total_price', 'product_orders']