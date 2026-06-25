from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from .models import Cart, CartItem
from products.models import Product

import json
from django.http import JsonResponse

# Create your views here.
class CartView(View):
    def get(self, request):
        if not request.session.session_key:
            request.session.create()

        session_key = request.session.session_key
        cart, _ = Cart.objects.get_or_create(session_key=session_key)
        items = cart.cart_items.all()

        context = {
            "items": items
        }

        return render(request, "cart.html", context=context)

# class AddItemView(View):
#     def post(self, request):
#         product_slug = request.POST.get("product_slug")
#         action = request.POST.get("action")
#         product = get_object_or_404(Product, slug=product_slug, is_active=True)
#
#         if not request.session.session_key:
#             request.session.create()
#
#         session_key = request.session.session_key
#         cart, _ = Cart.objects.get_or_create(session_key=session_key)
#
#         if action == "add_item":
#             # try:
#             item = CartItem.objects.create(
#                 cart = cart,
#                 product = product,
#             )
#             # except IntegrityError, ValueError, TypeError:
#             #     return "gg"
#
#         print("Susses")
#
#         return redirect("product", product.slug)

class AddItemView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            product_slug = data.get("product_slug")
            action = data.get("action")
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Invalid JSON"}, status=400)

        product = get_object_or_404(Product, slug=product_slug, is_active=True)

        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key

        cart, _ = Cart.objects.get_or_create(session_key=session_key)

        if action == "add_item":
            CartItem.objects.get_or_create(cart=cart, product=product)

        return JsonResponse({"success": True})


class RemoveItemView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            product_slug = data.get("product_slug")
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Invalid JSON"}, status=400)

        product = get_object_or_404(Product, slug=product_slug, is_active=True)

        if not request.session.session_key:
            return JsonResponse({"success": False, "error": "No session"}, status=400)

        session_key = request.session.session_key

        try:
            cart = Cart.objects.get(session_key=session_key)
            CartItem.objects.filter(cart=cart, product=product).delete()
        except Cart.DoesNotExist:
            return JsonResponse({"success": False, "error": "Cart not found"}, status=404)

        return JsonResponse({"success": True})
