from rest_framework import serializers
from products.models import Product, Category, Review, ProductImage
from decimal import Decimal
from django.contrib.auth import get_user_model

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description", "product_count"]
        # fields = ["id", "name", "description"]

    product_count = serializers.IntegerField(read_only=True)


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image"]


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only = True)
    class Meta:
        model = Product 
        fields = ['id', "name", "description", "price", "stock", "category", "price_with_tax", "images"]
    
    # category = CategorySerializer()
    price_with_tax = serializers.SerializerMethodField(method_name="calculate_tax")

    def calculate_tax(self, product):
        return round(product.price * Decimal(1.1))
    
    def validate_price(self, price):
        if price < 0:
            raise serializers.ValidationError("Price can't be negative.")
        return price
    

class SimpleUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(method_name="get_current_user")

    class Meta:
        model = get_user_model()
        fields = ["id", "name"]

    def get_current_user(self, obj):
        return obj.email


class ReviewSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only = True)

    class Meta:
        model = Review
        fields = ["id", "user", "rating", "comment", "product"]
        read_only_fields = ['product', "user"]

    def create(self, validated_data):
        id = self.context["product_id"]
        return Review.objects.create(product_id = id, **validated_data) 