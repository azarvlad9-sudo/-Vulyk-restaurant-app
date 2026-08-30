from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва категорії")
    slug = models.SlugField(unique=True, verbose_name="URL-слаг")

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def __str__(self):
        return self.name


class Dish(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='dishes', verbose_name="Категорія")
    name = models.CharField(max_length=200, verbose_name="Назва страви")
    slug = models.SlugField(unique=True, verbose_name="URL-слаг")
    description = models.TextField(verbose_name="Опис")
    ingredients = models.TextField(blank=True, verbose_name="Інгредієнти")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Ціна (грн)")
    image = models.ImageField(upload_to='dishes/', blank=True, null=True, verbose_name="Фото страви")
    is_available = models.BooleanField(default=True, verbose_name="В наявності")
    is_popular = models.BooleanField(default=False, verbose_name="Популярна страва")
    is_new = models.BooleanField(default=False, verbose_name="Новинка")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата додавання")

    class Meta:
        verbose_name = "Страва"
        verbose_name_plural = "Страви"

    def __str__(self):
        return self.name


class Review(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name='reviews', verbose_name="Страва")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Користувач")
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name="Оцінка (1-5)")
    comment = models.TextField(verbose_name="Коментар")
    is_approved = models.BooleanField(default=False, verbose_name="Схвалено модератором")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата")

    class Meta:
        verbose_name = "Відгук"
        verbose_name_plural = "Відгуки"

    def __str__(self):
        return f"Відгук від {self.user.username} на {self.dish.name}"