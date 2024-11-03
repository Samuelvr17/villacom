from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('update_user/', views.update_user, name='update_user'),
    path('update_info/', views.update_info, name='update_info'),
    path('update_password/', views.update_password, name='update_password'),
    path('product/<int:pk>', views.product, name='product'),
    path('category/<str:foo>', views.category, name='category'),
    path('category_summary/', views.category_summary, name='category_summary'),
    path('search/', views.search, name='search'),
    path('lista_tiendas/', views.lista_tiendas, name='lista_tiendas'),

    # CRUD de Productos
    path('categoria/nueva/', views.crear_categoria, name='crear_categoria'),
    path('producto/nuevo/', views.crear_producto, name='crear_producto'),
    path('producto/editar/<int:pk>/', views.editar_producto, name='editar_producto'),
    path('producto/editar/', views.editar_producto, name='buscar_producto'),
    path('producto/eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),
    path('producto/eliminar/', views.eliminar_producto, name='buscar_producto_eliminar'),

    # CRUD de Tiendas
    path('tienda/nueva/', views.crear_tienda, name='crear_tienda'),
    path('tienda/editar/<int:pk>/', views.editar_tienda, name='editar_tienda'),
    path('tienda/editar/', views.editar_tienda, name='buscar_tienda'),
    path('tienda/eliminar/<int:pk>/', views.eliminar_tienda, name='eliminar_tienda'),
    path('tienda/eliminar/', views.eliminar_tienda, name='buscar_tienda_eliminar'),
]