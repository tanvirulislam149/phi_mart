from rest_framework import serializers
from orders.models import Cart, CartItem, Order, OrderItem
from products.models import Product
from orders.services import OrderServices

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "price"]

class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    class Meta:
        model = CartItem
        fields = ["id", "product_id", "quantity"]

    def save(self, **kwargs):
        cart_id = self.context["cart_id"]
        product_id = self.validated_data["product_id"]
        quantity = self.validated_data["quantity"]

        try:
            cart_item = CartItem.objects.get(cart_id = cart_id, product_id = product_id)
            cart_item.quantity += quantity
            self.instance = cart_item.save()
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id = cart_id, product_id=product_id, quantity = quantity)

        return self.instance


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["quantity"]

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
        read_only_fields = ["user"]

    def get_total_price(self, cart: Cart):
        return sum([item.product.price * item.quantity for item in cart.items.all()])


class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity", "price", "total_price"]

class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError('No cart found with this id')

        if not CartItem.objects.filter(cart_id=cart_id).exists():
            raise serializers.ValidationError('Cart is empty')

        return cart_id
    
    def create(self, validated_data):
        user_id = self.context["user_id"]
        cart_id = validated_data["cart_id"]

        try:
            order = OrderServices.create_order(user_id=user_id, cart_id=cart_id)
            return order
        except ValueError as e:
            return serializers.ValidationError(str(e))
    
    def to_representation(self, instance):
        return OrderSerializer(instance).data



class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ["id", "user", "status", "total_price", "created_at", "items"]

class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']

    def update(self, instance, validated_data):
        new_status = validated_data['status']
        user = self.context['user']

        if new_status == Order.CANCELED:
            return OrderServices.update_order(order = instance, user = user)
        
        if not user.is_staff:
            raise serializers.ValidationError({"details": "You don't have permission to update status"})
        
        return super().update(instance, validated_data)