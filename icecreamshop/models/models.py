from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

IMAGE_FOLDER = "images"
class Product(models.Model):
    flavor = models.CharField(max_length=50)
    unit_price = models.FloatField(validators=[MinValueValidator(0)])
    recipe = models.CharField(max_length=500, blank=True)
    image = models.ImageField(upload_to=IMAGE_FOLDER, null=True, blank=True)
    remaining_quantity = models.PositiveIntegerField()
    max_quantity = models.PositiveIntegerField()

    def clean(self):
        if (not self.remaining_quantity or not self.max_quantity):
            return False
        if self.remaining_quantity > self.max_quantity:
            raise ValidationError('Remaining quantity must be less than max quantity.')

    def __str__(self):
        return self.flavor

class Order(models.Model):
    order_number = models.CharField(primary_key=True, max_length=6, unique=True)
    order_date = models.DateTimeField(auto_now=True)
    total_price = models.FloatField(validators=[MinValueValidator(0)],  default=0, null=True, blank=True)
    client_name = models.CharField(null=True, blank=True, max_length=50)

    def __str__(self):
        return self.order_number

    def update_total_price(self):
        self.total_price = ProductOrder.objects.filter(order=self).aggregate(models.Sum('price'))["price__sum"]

    def save(self, *args, **kwargs):
        self.update_total_price()
        super().save(*args, **kwargs)

class ProductOrder(models.Model):
    order = models.ForeignKey(Order, related_name='product_orders', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    price = models.FloatField(validators=[MinValueValidator(0)], default=0, null=True, blank=True)

    def calculate_price(self):
        self.price = self.product.unit_price * self.quantity

    def clean(self):
        if not hasattr(self, 'product'):
            return False
        if self.quantity > self.product.remaining_quantity:
            raise ValidationError("Order quantity must not be greater than remaining quantity. %s remaining."\
                                  %self.product.remaining_quantity)

    def save(self, *args, **kwargs):
        #if new order
        if not self.pk:
            new_create = True
        self.calculate_price()
        super().save(*args, **kwargs)
        self.order.save()
        if new_create:
            self.product.remaining_quantity = self.product.remaining_quantity - self.quantity
            self.product.save()
            if self.product.remaining_quantity == 0:
                print("Message to admin: Pot %s is empty. Please fulfill the pot."%self.product.flavor)



