from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Dish, Category

def home(request):
    return render(request, 'menu/home.html')

def menu_list(request):
    dishes = Dish.objects.all()
    categories = Category.objects.all()
    selected_category = request.GET.get('category')
    search_query = request.GET.get('search')

    # Фільтрація за категорією
    if selected_category:
        dishes = dishes.filter(category__slug=selected_category)

    # Пошук по назві та опису
    if search_query:
        dishes = dishes.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )

    context = {
        'dishes': dishes,
        'categories': categories,
        'selected_category': selected_category,
        'search_query': search_query,
    }
    return render(request, 'menu/menu_list.html', context)

def dish_detail(request, slug):
    dish = get_object_or_404(Dish, slug=slug)
    return render(request, 'menu/dish_detail.html', {'dish': dish})