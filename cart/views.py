from django.shortcuts import render, redirect, get_object_or_404
from menu.models import Dish

def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for dish_id, quantity in cart.items():
        dish = get_object_or_404(Dish, id=dish_id)
        item_total = dish.price * quantity
        total_price += item_total
        cart_items.append({
            'dish': dish,
            'quantity': quantity,
            'total_price': item_total,
        })

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'cart/cart_detail.html', context)

def add_to_cart(request, dish_id):
    cart = request.session.get('cart', {})
    dish_id_str = str(dish_id)
    cart[dish_id_str] = cart.get(dish_id_str, 0) + 1
    request.session['cart'] = cart
    return redirect('cart:cart_detail')

def remove_from_cart(request, dish_id):
    cart = request.session.get('cart', {})
    dish_id_str = str(dish_id)
    if dish_id_str in cart:
        del cart[dish_id_str]
        request.session['cart'] = cart
    return redirect('cart:cart_detail')