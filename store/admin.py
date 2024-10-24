from django.contrib import admin
from .models import Business, Category, Customer, Product, Order, Profile
from django.contrib.auth.models import User


admin.site.register(Business)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Profile)


# Unir la Info de Profile y User
class ProfileInline(admin.StackedInline):
	model = Profile 
	
# Ampliar Modelo de Usuario
class UserAdmin(admin.ModelAdmin):
	model = User
	field = ["username", "first_name", "last_name", "email"]
	inlines = [ProfileInline]

# Anular Registro Anterior forma
admin.site.unregister(User)

# Hacer Registro Nueva Forma
admin.site.register(User, UserAdmin)
