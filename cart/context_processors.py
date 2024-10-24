from .cart import Cart


# crear un contexto para que el carrito funcione en todas las páginas
def cart(request):
    return {'cart': Cart(request)}