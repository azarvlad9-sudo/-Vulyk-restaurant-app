from django.shortcuts import render

def cart_detail(request):
    return render(request, 'cart/detail.html')  # Або інша назва шаблону, якщо є