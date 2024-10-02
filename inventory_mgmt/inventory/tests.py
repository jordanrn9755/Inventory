from django.test import TestCase

# Create your tests here.
# inventory/tests.py
from rest_framework import status
from rest_framework.test import APITestCase
from .models import InventoryItem
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.models import User

class InventoryItemTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = RefreshToken.for_user(self.user)

    def test_create_inventory_item(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))
        data = {'name': 'Test Item', 'quantity': 10, 'price': 5.99}
        response = self.client.post(reverse('inventory-item-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_inventory_items(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))
        response = self.client.get(reverse('inventory-item-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_inventory_item(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))
        item = InventoryItem.objects.create(name='Test Item', quantity=10, price=5.99)
        data = {'name': 'Updated Item', 'quantity': 15, 'price': 6.99}
        response = self.client.put(reverse('inventory-item-detail', args=[item.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_inventory_item(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))
        item = InventoryItem.objects.create(name='Test Item', quantity=10, price=5.99)
        response = self.client.delete(reverse('inventory-item-detail', args=[item.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
