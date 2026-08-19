from carrito.models import Cart


def cart_count(request):
    count = 0
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        count = cart.total_items
    elif request.session.session_key:
        cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
        count = cart.total_items
    return {'cart_count': count}
