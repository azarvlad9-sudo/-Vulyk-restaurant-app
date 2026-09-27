from django.shortcuts import render, get_object_or_404
from .models import Category, Dish


def home(request):
    categories = Category.objects.all()
    popular_dishes = Dish.objects.filter(is_popular=True, is_available=True)
    new_dishes = Dish.objects.filter(is_new=True, is_available=True)

    context = {
        'categories': categories,
        'popular_dishes': popular_dishes,
        'new_dishes': new_dishes,
    }
    return render(request, 'menu/home.html', context)


def menu_list(request):
    categories = Category.objects.all()
    category_slug = request.GET.get('category')

    dishes = Dish.objects.filter(is_available=True)
    selected_category = None

    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        dishes = dishes.filter(category=selected_category)

    context = {
        'categories': categories,
        'dishes': dishes,
        'selected_category': selected_category,
    }
    return render(request, 'menu/menu_list.html', context)


def dish_detail(request, slug):
    dish = get_object_or_404(Dish, slug=slug, is_available=True)
    context = {
        'dish': dish,
    }
    return render(request, 'menu/dish_detail.html', context)