from django.urls import path
from .views import CartView, AddItemView, RemoveItemView

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('add-item/', AddItemView.as_view(), name="add_item"),
    path('remove-item/', RemoveItemView.as_view(), name="remove_item")
]
