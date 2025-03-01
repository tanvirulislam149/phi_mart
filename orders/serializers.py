from rest_framework import serializers
from orders.models import Cart, CartItem
from products.models import Product

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "price"]


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    items_price = serializers.SerializerMethodField(method_name="get_items_price")

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "items_price"]

    def get_items_price(self, cartItem: CartItem):
        return cartItem.product.price * cartItem.quantity

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(method_name="get_total_price")

    class Meta:
        model = Cart
        fields = ["id", "user", "items", "total_price"]

    def get_total_price(self, cart: Cart):
        return sum([item.product.price * item.quantity for item in cart.items.all()])

