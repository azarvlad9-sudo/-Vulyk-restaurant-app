from django.contrib import admin
from .models import Category, Dish, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_available', 'is_popular', 'is_new']
    list_filter = ['category', 'is_available', 'is_popular', 'is_new']
    list_editable = ['price', 'is_available', 'is_popular', 'is_new']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['dish', 'user', 'rating', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'rating']
    list_editable = ['is_approved']