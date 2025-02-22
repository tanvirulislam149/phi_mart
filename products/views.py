from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from products.models import Product, Category
from django.db.models import Count
from products.serializers import ProductSerializer, CategorySerializer

# Create your views here.

@api_view()
def view_products(request):
    products = Product.objects.select_related("category").all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view()
def view_specific_product(request, id):
    product = get_object_or_404(Product, pk = id)
    product_dict = {"id": product.id, "name": product.name, "price": product.price}
    return Response(product_dict)

@api_view()
def view_category(request):
    category = Category.objects.annotate(product_count = Count("products")).all()
    serializer = CategorySerializer(category, many=True)
    return Response(serializer.data)