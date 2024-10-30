from django.db import models
from django.contrib.auth.models import User
from store.models import Product
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import datetime

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shipping_full_name = models.CharField(max_length=200)
    shipping_email = models.CharField(max_length=200)
    shipping_address = models.CharField(max_length=200)
    shipping_city = models.CharField(max_length=200)
    shipping_country = models.CharField(max_length=200)
    shipping_zipcode = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Dirección Envio'

    def _str_(self):
        return f'Dirección Envio - {str(self.id)}'
    

# Crear Direccion de Envio (Shipping Address) Por Defecto Cuando el Usuario Se Registra 
def create_shipping(sender, instance, created, **kwargs):
	if created:
		user_shipping = ShippingAddress(user=instance)
		user_shipping.save()

# Automatizar Los Perfiles
post_save.connect(create_shipping, sender=User)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    shipping_address = models.TextField(max_length=15000)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    # Fecha de la Orden
    date_order = models.DateTimeField(auto_now_add=True)
    # Enviado o No
    shipped = models.BooleanField(default=False)
    # Fecha de Envio
    date_shipped = models.DateTimeField(blank=True, null=True)

    def _str_(self):
        return f'Orden - {str(self.id)}'
    
    class Meta:
        verbose_name_plural = 'Ordenes'
    
# añadir automáticamente la Fecha de Envío
@receiver(pre_save, sender=Order)
def set_shipped_date_on_update(sender, instance, **kwargs):
     if instance.pk:
          now = datetime.datetime.now()
          obj = sender._default_manager.get(pk=instance.pk)
          if instance.shipped and not obj.shipped:
               instance.date_shipped = now


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def _str_(self):
        return f'Orden Item - {str(self.id)}'
    
    class Meta:
        verbose_name_plural = 'Orden Items'