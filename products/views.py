from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from .models import Product, ProductCategory
from cart.models import Cart, CartItem

# Create your views here.
class HomeView(View):
    def get(self, request):
        products = Product.objects.all()
        categories = ProductCategory.objects.all()
        context = {
            'current_slug': 'all',
            'categories': categories,
            'products': products,
        }
        return render(request, 'index.html', context)


class HomeCategoryView(View):
    def get(self, request, slug):
        category = get_object_or_404(ProductCategory, slug=slug)
        products = Product.objects.filter(category=category)
        categories = ProductCategory.objects.all()
        context = {
            'current_slug': slug,
            'categories': categories,
            'products': products,
        }
        return render(request, 'index.html', context)


class ProductView(View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)

        in_cart = False
        session_key = request.session.session_key

        if session_key:
            try:
                # Пытаемся получить корзину для текущей сессии
                cart = Cart.objects.get(session_key=session_key)
                # Проверяем, есть ли связанный CartItem с этим товаром
                in_cart = CartItem.objects.filter(cart=cart, product=product).exists()

            except Cart.DoesNotExist:
                # Если корзины в базе данных еще нет, значит и товара в ней быть не может
                in_cart = False


        context = {
            'product': product,
            'in_cart': in_cart
        }

        return render(request, 'product.html', context)


class CartView(View):
    def get(self, request):
        return render(request, 'cart.html')

