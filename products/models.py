from django.db import models
from django.core.validators import MinValueValidator
from django.utils.text import slugify
import uuid
import os

# Create your models here.
class ProductCategory(models.Model):
    """ Категории товаров. """
    is_sub = models.BooleanField(
        verbose_name="Под категория ли",
        default=False,
        help_text="Является ли под категорией"
    )

    parent = models.ForeignKey(
        'self', null=True, blank=True,
        on_delete=models.CASCADE,
        related_name="sub"
    )

    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Название категории",
        help_text="Например: Телефоны, Ноутбуки"
    )

    slug = models.SlugField(
        max_length=200,
        unique=True,
        db_index=True,
        verbose_name="URL-адрес (slug)",
        help_text="Используется в ссылке. Например: phones, laptops"
    )

    class Meta:
        verbose_name = "Категория товара"
        verbose_name_plural = "Категории товаров"
        ordering = ['name']

    def __str__(self):
        return self.name


class Brand(models.Model):
    """ Бренды товаров. """
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Название бренда",
        help_text="Например: Apple, Samsung, Xiaomi"
    )

    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="URL-адрес (slug)",
        help_text="Используется в ссылке. Например: apple, samsung"
    )

    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"
        ordering = ['name']

    def __str__(self):
        return self.name


def generate_sku():
    """Генерация уникального артикула на основе UUID."""
    return uuid.uuid4().hex[:12].upper()  # берём первые 12 символов hex и делаем их заглавными

def generate_path(instance, filename):
    """Генерация пути в котором будет храниться картина товара"""
    ext = filename.split('.')[-1]

    # Если вдруг слаг пустой, можно сгенерировать его из имени или оставить дефолтным
    slug = instance.slug if instance.slug else slugify(instance.name)

    # Собираем новое имя файла: 'slug.extension' (например, 'mylo.jpg')
    new_filename = f"{slug}.{ext}"

    # Возвращаем полный путь относительно кодовой папки MEDIA_ROOT
    return os.path.join('products/', new_filename)

class Product(models.Model):
    """Основная информация о товаре."""
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Категория",
        related_name="product"
    )
    name = models.CharField(max_length=255, unique=True, verbose_name="Наименование")
    slug = models.SlugField(max_length=200, db_index=True, unique=True, verbose_name="Ссылка (slug)")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Цена'
    )
    affiliate_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Партнёрская цена'
    )

    is_active = models.BooleanField(default=True, verbose_name='Наличие')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    sku = models.CharField(
        max_length=12,
        unique=True,
        editable=False,
        default=generate_sku,
        verbose_name='Артикул'
    )

    image = models.ImageField(upload_to=generate_path)


    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.sku})"

