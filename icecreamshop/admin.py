from django.contrib import admin
from django.db.models import F
from django.utils.translation import ngettext
from django.contrib import messages
from icecreamshop.models import *


class ProductAdmin(admin.ModelAdmin):
    list_display = ['flavor', 'recipe', 'unit_price']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['flavor', 'recipe', 'unit_price', 'remaining_quantity', 'max_quantity', 'get_filling_rate']
    actions = ['fulfill_pots', 'delete_selected']

    def get_recipe(self, obj):
        return obj.product.recipe

    def get_filling_rate(self, obj):
        return "%.1f %%" %((obj.remaining_quantity / obj.max_quantity)*100)

    get_recipe.short_description = 'Recipe'
    get_filling_rate.short_description = "Filling rate"

    @admin.action(description='Fulfill selected product pots')
    def fulfill_pots(self, request, queryset):
        updated = queryset.update(remaining_quantity=F('max_quantity'))
        self.message_user(request, ngettext(
            '%d pot was successfully fulfilled.',
            '%d pots were successfully fulfilled.',
            updated,
        ) % updated, messages.SUCCESS)

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'order_date', 'client_name', 'total_price']
    readonly_fields = ["total_price"]

class ProductOrderAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']
    readonly_fields = ["price"]

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing a existing order is not allowed, concerning to stock management
            return ['order', 'product', 'quantity', 'price']
        return self.readonly_fields

admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(ProductOrder, ProductOrderAdmin)