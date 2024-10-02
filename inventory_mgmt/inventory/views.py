from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import InventoryItem
from .serializers import InventoryItemSerializer, LoginSerializer
import logging
from django.utils import timezone
from rest_framework.generics import GenericAPIView


# Create your views here.

logger = logging.getLogger(__name__)

class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)

            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])

        

            return Response({
                "message": "Login Successful",
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid Email or Password"}, status=status.HTTP_400_BAD_REQUEST)


class InventoryItemList(generics.ListCreateAPIView):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        logger.info('Created inventory item: %s', serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class InventoryItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return super().get_object()
        except InventoryItem.DoesNotExist:
            logger.error('Inventory item not found')
            return Response({"error": "Inventory item not found"}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        logger.info('Updated inventory item: %s', serializer.data)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        logger.info('Deleted inventory item: %s', instance.id)
        return Response(status=status.HTTP_204_NO_CONTENT)