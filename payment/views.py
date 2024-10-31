from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib import messages
from store.models import Product


def payment_success(request):
    return render(request, 'payment_success.html', {})


def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()

    if request.user.is_authenticated:
        # Intentar obtener la dirección de envío
        try:
            shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
            shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        except ShippingAddress.DoesNotExist:
            shipping_user = None
            shipping_form = ShippingForm(request.POST or None)  # Crear un nuevo formulario en blanco
            messages.warning(request, "No tiene una dirección de envío. Por favor, añádala.")

        return render(request, 'checkout.html', {
            'cart_products': cart_products,
            'quantities': quantities,
            'totals': totals,
            'shipping_form': shipping_form
        })
    else:
        shipping_form = ShippingForm(request.POST or None)
        return render(request, 'checkout.html', {
            'cart_products': cart_products,
            'quantities': quantities,
            'totals': totals,
            'shipping_form': shipping_form
        })


def billing_info(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        totals = cart.cart_total()

        # Crear una sesion con la info de envio
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        # Revisar si el Usuario Inicio Sesion
        if request.user.is_authenticated:
            billing_form = PaymentForm()  
            return render(request, 'billing_info.html', {'cart_products':cart_products, 'quantities':quantities, 'totals':totals, 'shipping_info':request.POST, 'billing_form':billing_form})
        else:
            billing_form = PaymentForm()
            return render(request, 'billing_info.html', {'cart_products':cart_products, 'quantities':quantities, 'totals':totals, 'shipping_info':request.POST,'billing_form':billing_form})

        shipping_form = request.POST
        return render(request, 'billing_info.html', {'cart_products':cart_products, 'quantities':quantities, 'totals':totals, 'shipping_form':shipping_form})
    else:
        messages.success(request, "Acceso Denegado")
        return redirect('home')
    

def process_order(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        totals = cart.cart_total()

        # Obtener Billing Info de la Ultima Pagina
        payment_form = PaymentForm(request.POST or None)
        # Obtener Datos de la Shipping Session
        my_shipping = request.session.get('my_shipping')

        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        # Crear Shipping Address de la info de la sesion
        shipping_address = f"{my_shipping['shipping_address']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_zipcode']}"
        amount_paid = totals
        
        # Crear una Orden
        if request.user.is_authenticated:
            user = request.user
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            # Id de la Orden
            order_id = create_order.pk

            # Info del producto
            for product in cart_products:
                # ID Producto
                product_id = product.id
                # Precio Producto
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                # Cantidad
                for key, value in quantities.items():
                    if int(key) == product.id:
                        # Crear Orden-Item
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, quantity=value, price=price)
                        create_order_item.save()

            # Borrar el Carrito
            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]

            messages.success(request, "Pedido Realizado")
            return redirect('home')
        else:
            # Sin Iniciar Sesion
            create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            # Id de la Orden
            order_id = create_order.pk

            # Info de la Orden
            for product in cart_products:
                # ID Producto
                product_id = product.id
                # Precio Producto
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                # Cantidad
                for key, value in quantities.items():
                    if int(key) == product.id:
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=value, price=price)
                        create_order_item.save()

            # Borrar el Carrito
            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]

            messages.success(request, "Pedido Realizado")
            return redirect('home')
    else:
        messages.success(request, "Acceso Denegado")
        return redirect('home')