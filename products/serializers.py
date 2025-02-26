from rest_framework import serializers
from products.models import Product, Category, Review
from decimal import Decimal

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description", "product_count"]
        # fields = ["id", "name", "description"]

    product_count = serializers.IntegerField(read_only=True)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product 
        fields = ['id', "name", "description", "price", "stock", "category", "price_with_tax"]
    
    # category = CategorySerializer()
    price_with_tax = serializers.SerializerMethodField(method_name="calculate_tax")

    def calculate_tax(self, product):
        return round(product.price * Decimal(1.1))
    
    def validate_price(self, price):
        if price < 0:
            raise serializers.ValidationError("Price can't be negative.")
        return price
    

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "name", "description", "product"]
        read_only_fields = ['product']


    def create(self, validated_data):
        id = self.context["product_id"]
        return Review.objects.create(product_id = id, **validated_data)