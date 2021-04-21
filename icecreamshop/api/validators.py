from icecreamshop.models import *
from django.core.exceptions import ValidationError


def order_data_validator(order_data):
    """
    :param order_data:     {
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
    :return: True or False
    """
    if "product_orders" not in order_data or not order_data["product_orders"]:
        raise ValidationError("product_orders is mandatory.")
    for p_order_data in order_data["product_orders"]:
        if "product" not in p_order_data:
            raise ValidationError("product pk is required")
        if "quantity" not in p_order_data:
            raise ValidationError("quantity is required")
        try:
            p = Product.objects.get(pk=p_order_data["product"])
        except Product.DoesNotExist:
            raise ValidationError("Product %s does not exist"%p_order_data["product"])
        if p.remaining_quantity < p_order_data["quantity"]:
            raise ValidationError("Order quantity must not be greater than remaining quantity. Product %s: %s remaining."
                                  %(p.pk, p.remaining_quantity))

    return True
