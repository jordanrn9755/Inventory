from django.urls import path
from .views import InventoryItemList, InventoryItemDetail

urlpatterns = [
    path('items/', InventoryItemList.as_view(), name='inventory-item-list'),
    path('items/<int:pk>/', InventoryItemDetail.as_view(), name='inventory-item-detail'),
]
