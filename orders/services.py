from orders.models import Cart, Order, OrderItem
from django.db import transaction
from rest_framework.exceptions import PermissionDenied

class OrderServices:
    @staticmethod
    def create_order(user_id, cart_id):
        with transaction.atomic():
            cart = Cart.objects.get(pk = cart_id)
            cart_items = cart.items.select_related("product").all()

            total_price = sum([item.product.price * item.quantity for item in cart_items])

            order = Order.objects.create(user_id = user_id, total_price = total_price)

            order_items = [
                OrderItem(
                    order = order,
                    product = item.product,
                    price = item.product.price,
                    quantity = item.quantity,
                    total_price = item.product.price * item.quantity
                )
                for item in cart_items
            ]
            OrderItem.objects.bulk_create(order_items)

            cart.delete()

            return order
        
    @staticmethod
    def update_order(order, user):
        if user.is_staff:
            order.status = Order.CANCELED
            order.save()
            return order
        
        if order.user != user:
            raise PermissionDenied({'details': "You can only cancel your orders"})
        
        if order.status == Order.DELIVERED:
            raise PermissionDenied({'details': "Delivered order can't be canceled."})
        
        order.status = Order.CANCELED
        order.save()
        return order