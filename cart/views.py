from django.shortcuts import render, redirect, get_object_or_404
from menu.models import Dish


def cart_add(request, dish_id):
    cart = request.session.get('cart', {})
    dish_id_str = str(dish_id)

    if dish_id_str in cart:
        cart[dish_id_str]['quantity'] += 1
    else:
        dish = get_object_or_404(Dish, id=dish_id)
        cart[dish_id_str] = {
            'name': dish.name,
            'price': float(dish.price),
            'quantity': 1,
            'image': dish.image.url if dish.image else ''
        }

    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart:cart_detail')


def cart_increase(request, dish_id):
    cart = request.session.get('cart', {})
    dish_id_str = str(dish_id)
    if dish_id_str in cart:
        cart[dish_id_str]['quantity'] += 1
        request.session['cart'] = cart
        request.session.modified = True
    return redirect('cart:cart_detail')


def cart_decrease(request, dish_id):
    cart = request.session.get('cart', {})
    dish_id_str = str(dish_id)
    if dish_id_str in cart:
        cart[dish_id_str]['quantity'] -= 1
        # Якщо кількість стала менше 1 — видаляємо страву повністю
        if cart[dish_id_str]['quantity'] <= 0:
            del cart[dish_id_str]
        request.session['cart'] = cart
        request.session.modified = True
    return redirect('cart:cart_detail')


def cart_remove(request, dish_id):
    cart = request.session.get('cart', {})
    dish_id_str = str(dish_id)
    if dish_id_str in cart:
        del cart[dish_id_str]
        request.session['cart'] = cart
        request.session.modified = True
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = request.session.get('cart', {})

    for item in cart.values():
        item['total_price'] = item['price'] * item['quantity']

    total_price = sum(item['total_price'] for item in cart.values())

    return render(request, 'cart/detail.html', {
        'cart': cart,
        'total_price': total_price
    })