from django.contrib import admin
from django.utils.html import format_html
from .models import Product, ProductCategory, Brand

from django.urls import reverse

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'edit_button')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


    def edit_button(self, obj):
        url = reverse('admin:products_productcategory_change', args=[obj.id])
        return format_html('<a class="button" href="{}">Изменить</a>', url)

    edit_button.short_description = "Действие"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = [
        'name', 'sku', 'category', 'price_display',
        'is_active', 'image_preview', 'created_at'
    ]
    list_filter = ['is_active', 'category', 'created_at']
    search_fields = ['name', 'sku', 'description']
    list_per_page = 25
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['sku', 'created_at', 'image_preview']

    @admin.display(description='Цена', ordering='price')
    def price_display(self, obj):
        return format_html('<b>{} сом</b>', obj.price)

    @admin.display(description='Фото')
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:60px; border-radius:4px;" />',
                obj.image.url
            )
        return '—'



