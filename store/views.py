from django.shortcuts import render, redirect
from .models import Product, Profile, Category, Business
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
import json
from cart.cart import Cart
from django.db.models import Q


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
        
        # Formulario de Usuario (sin shipping info)
        form = UserInfoForm(request.POST or None, instance=current_user)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Su información ha sido actualizada")
            return redirect('home')
        
        return render(request, 'update_info.html', {'form': form})
    
    else:
        messages.success(request, "Debe iniciar sesión para acceder a esta página")
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


def tienda_summary(request):
    businesses = Business.objects.all()  
    return render(request, 'tienda_summary.html', {'businesses':businesses})


def tienda(request, foo):
    # reemplazar guiones con espacios
    foo = foo.replace('-', ' ')
    try:
        business = Business.objects.get(name=foo)
        products = Product.objects.filter(business=business)
        return render(request, 'tienda.html', {'products': products, 'business': business})
    except:
        messages.success(request, ("La Categoría No Existe"))
        return redirect('home')


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