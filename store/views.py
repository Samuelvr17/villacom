from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Profile, Category, Business
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
import json
from cart.cart import Cart
from django.db.models import Q
from payment.forms import ShippingForm 
from payment.models import ShippingAddress
from .forms import ProductForm, CategoryForm, BusinessForm


def crear_tienda(request):
    if request.method == 'POST':
        form = BusinessForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tienda creada exitosamente.')
            return redirect('home')
    else:
        form = BusinessForm()
    return render(request, 'formulario_tienda.html', {'form': form})


def editar_tienda(request, pk=None):
    business = None
    form = None

    # Si el usuario ha enviado un término de búsqueda por nombre
    query = request.GET.get('query')
    if query:
        businesses = Business.objects.filter(name__icontains=query)
    else:
        businesses = None

    # Si se recibe un pk específico para edición, cargar la tienda correspondiente
    if pk:
        business = get_object_or_404(Business, pk=pk)
        if request.method == 'POST':
            form = BusinessForm(request.POST, instance=business)
            if form.is_valid():
                form.save()
                messages.success(request, 'Tienda actualizada exitosamente.')
                return redirect('home')  # Cambia 'home' por la URL a la que quieras redirigir
        else:
            form = BusinessForm(instance=business)

    return render(request, 'editar_tienda.html', {
        'form': form,
        'business': business,
        'businesses': businesses,
        'query': query,
    })


def eliminar_tienda(request, pk=None):
    business = None

    # Si el usuario ha enviado un término de búsqueda por nombre
    query = request.GET.get('query')
    if query:
        businesses = Business.objects.filter(name__icontains=query)
    else:
        businesses = None

    # Si se recibe un pk específico, buscar la tienda para confirmar la eliminación
    if pk:
        business = get_object_or_404(Business, pk=pk)
        if request.method == 'POST':
            business.delete()
            messages.success(request, 'Tienda eliminada exitosamente.')
            return redirect('home')  # Cambia 'home' por la URL adecuada para redirigir

    return render(request, 'eliminar_tienda.html', {
        'business': business,
        'businesses': businesses,
        'query': query,
    })


def crear_categoria(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada exitosamente.')
            return redirect('home')  # Redirige a la página principal o a una lista de categorías
    else:
        form = CategoryForm()
    return render(request, 'formulario_categoria.html', {'form': form})


def crear_producto(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado exitosamente.')
            return redirect('home')  # Redirige a la página principal o a una lista de productos
    else:
        form = ProductForm()
    return render(request, 'formulario_producto.html', {'form': form})


def editar_producto(request, pk=None):
    producto = None
    form = None

    # Si el usuario ha enviado un término de búsqueda por nombre
    query = request.GET.get('query')
    if query:
        productos = Product.objects.filter(name__icontains=query)
    else:
        productos = None

    # Si se recibe un pk específico para edición, cargar el producto correspondiente
    if pk:
        producto = get_object_or_404(Product, pk=pk)
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES, instance=producto)
            if form.is_valid():
                form.save()
                messages.success(request, 'Producto actualizado exitosamente.')
                return redirect('home')  
        else:
            form = ProductForm(instance=producto)

    return render(request, 'editar_producto.html', {
        'form': form,
        'producto': producto,
        'productos': productos,
        'query': query,
    })


def eliminar_producto(request, pk=None):
    producto = None

    # Si el usuario ha enviado un término de búsqueda por nombre
    query = request.GET.get('query')
    if query:
        productos = Product.objects.filter(name__icontains=query)
    else:
        productos = None

    # Si se recibe un pk específico, buscar el producto para confirmar la eliminación
    if pk:
        producto = get_object_or_404(Product, pk=pk)
        if request.method == 'POST':
            producto.delete()
            messages.success(request, 'Producto eliminado exitosamente.')
            return redirect('home')  # Cambia 'home' por la URL adecuada para redirigir

    return render(request, 'eliminar_producto.html', {
        'producto': producto,
        'productos': productos,
        'query': query,
    })


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products':products})


def register_user(request):
    form = SignUpForm
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Perfil Creado - Rellene Sus Datos De Usuario a Continuación"))
            return redirect('update_info')
        else:
            messages.success(request, ("Hubo Un Error, Inténtelo De Nuevo"))
            return redirect('register')
    else:
        return render(request, 'register.html', {'form':form})
    

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Guardar Carrito al Iniciar Sesion
            current_user = Profile.objects.get(user__id=request.user.id)
            saved_cart = current_user.old_cart
            # Covertir String a Diccionario Python
            if saved_cart:
                # Convertir a Diccionario Usando JSON
                converted_cart = json.loads(saved_cart)
                # Guardar en la Session
                cart = Cart(request)
                # Añadir los Elementos del Carrito 
                for key, value in converted_cart.items():
                     cart.db_add(product=key, quantity=value)

            messages.success(request, ('Ha Iniciado Seión'))
            return redirect('home')
        else:
            messages.success(request, ("Hubo Un Error, Inténtelo De Nuevo"))
            return redirect('login')
    else:
        return render(request, 'login.html', {})
    

def logout_user(request):
    logout(request)
    messages.success(request, ("Ha Cerrado La Sesión"))
    return redirect('home')


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)
        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, ("Su Perfil Ha Sido Actualizado"))
            return redirect('home') 
        return render(request, 'update_user.html', {'user_form':user_form})
    else:
        messages.success(request, "Debe iniciar sesión para acceder a esta página")
        return redirect('home')
    

def update_info(request):
    if request.user.is_authenticated:
        # Obtener el Usuario Actual
        current_user = Profile.objects.get(user__id=request.user.id)
        
        # Intentar obtener la dirección de envío
        try:
            shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
            shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        except ShippingAddress.DoesNotExist:
            shipping_user = None
            shipping_form = ShippingForm(request.POST or None)  # Crear un nuevo formulario en blanco

        # Formulario de Usuario
        form = UserInfoForm(request.POST or None, instance=current_user)
        
        if form.is_valid() and shipping_form.is_valid():
            form.save()
            shipping_form.save()
            messages.success(request, "Su información ha sido actualizada")
            return redirect('home')
        
        return render(request, 'update_info.html', {'form': form, 'shipping_form': shipping_form})
    else:
        messages.warning(request, "Debe iniciar sesión para acceder a esta página")
        return redirect('home')

    

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Su Contraseña ha sido actualizada")
                login(request, current_user)
                return redirect('home')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
        else:
            form = ChangePasswordForm(current_user) 
        return render(request, 'update_password.html', {'form':form})
    else:  
        messages.success(request, "Debe iniciar sesión para acceder a esta página")
    return redirect('home')


def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product})


def category(request, foo):
    # reemplazar guiones con espacios
    foo = foo.replace('-', ' ')
    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products': products, 'category': category})
    except:
        messages.success(request, ("La Categoría No Existe"))
        return redirect('home')
    

def category_summary(request):
    categories = Category.objects.all()  
    return render(request, 'category_summary.html', {'categories':categories})


def lista_tiendas(request):
    tiendas = Business.objects.all() 
    return render(request, 'lista_tiendas.html', {'tiendas': tiendas})


def search(request):
	if request.method == "POST":
		searched = request.POST['searched']
		searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
		if not searched:
			messages.success(request, "Ese Producto No Existe. Inténtelo de Nuevo.")
			return render(request, "search.html", {})
		else:
			return render(request, "search.html", {'searched':searched})
	else:
		return render(request, "search.html", {})