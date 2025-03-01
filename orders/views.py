from django.shortcuts import render
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from orders.models import Cart, CartItem
from orders.serializers import CartSerializer, CartItemSerializer
from rest_framework.viewsets import ModelViewSet

# Create your views here.

class CartViewset(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartItemViewset(ModelViewSet):
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(cart_id = self.kwargs["cart_pk"])