from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User


admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

class OrderItemInLine(admin.StackedInline):
    model = OrderItem
    extra = 0

# Ampliar el model de Order
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ["date_order"]
    fields = ["user", "full_name", "email", "shipping_address", "amount_paid", "date_order", "shipped", "date_shipped"]
    inlines = [OrderItemInLine]

# Cancelar el Registro del model de aoarder
admin.site.unregister(Order)

# Volver a registrar Order y OrderItems
admin.site.register(Order, OrderAdmin)