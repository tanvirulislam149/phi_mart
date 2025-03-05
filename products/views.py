from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from products.models import Product, Category, Review
from django.db.models import Count
from products.serializers import ProductSerializer, CategorySerializer, ReviewSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from products.filters import ProductFilter
from products.paginations import DefaultPagination 


class ProductViewset(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    search_fields = ["name", "description"]
    ordering_fields = ["price", "stock"]


    def destroy(self, request, *args, **kwargs):     # just customizing a method
        product = self.get_object()
        if product.stock > 10:
            return Response({"message": "Product having stock more than 10 can't be deleted."})
        self.perform_destroy(product)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CategoryViewset(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ReviewViewset(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id = self.kwargs["product_pk"])

    def get_serializer_context(self):
        return {"product_id": self.kwargs["product_pk"]}


# Create your views here.

# @api_view(["GET", "POST"])
# def view_products(request):
#     if request.method == "GET":
#         products = Product.objects.select_related("category").all()
#         serializer = ProductSerializer(products, many=True)
#         return Response(serializer.data)
#     if request.method == "POST":
#         serializer = ProductSerializer(data = request.data)
#         serializer.is_valid(raise_exception=True)
#         print(serializer.validated_data)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
    
# @api_view(["GET", "PUT", "DELETE"])
# def view_specific_product(request, id):
#     if request.method == "GET":
#         product = get_object_or_404(Product, pk = id)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
#     if request.method == "PUT":
#         product = get_object_or_404(Product, pk = id)
#         serializer = ProductSerializer(product, data = request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     if request.method == "DELETE":
#         product = get_object_or_404(Product, pk = id)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
# @api_view()
# def view_category(request):
#     # category = Category.objects.annotate(product_count = Count("products")).all()
#     category = Category.objects.all()
#     serializer = CategorySerializer(category, many=True)
#     return Response(serializer.data)

# @api_view()
# def view_specific_category(request, id):
#     category = get_object_or_404(Category, pk = id)
#     serializer = CategorySerializer(category)
#     return Response(serializer.data)



# --------------------------- using class based views --------------------------

class ProductList(APIView):
    def get(self, request):
        products = Product.objects.select_related("category").all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ProductSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ViewSpecificProduct(APIView):
    def get(self, request, id):
        product = get_object_or_404(Product, pk = id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    def put(self, request, id):
        product = get_object_or_404(Product, pk = id)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, id):
        product = get_object_or_404(Product, pk = id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    



class CategoryList(APIView):
    def get(self, request):
        categories = Category.objects.annotate(product_count = Count("products")).all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = CategorySerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ViewSpecificCategory(APIView):
    def get(self, request, id):
        category = get_object_or_404(Category.objects.annotate(product_count = Count("products")).all(), pk = id)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    
    def put(self, request, id):
        category = get_object_or_404(Category.objects.annotate(product_count = Count("products")).all(), pk = id)
        serializer = CategorySerializer(category, request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, id):
        category = get_object_or_404(Category, pk = id)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


    # -----------------------  using mixin --------------------------------


class ViewProduct(ListCreateAPIView):    # using class based views mixin
    queryset = Product.objects.select_related("category").all()
    serializer_class = ProductSerializer

    # def get_queryset(self):              # does the same as above code
    #     return Product.objects.select_related("category").all()
    
    # def get_serializer_class(self):
    #     return ProductSerializer

class ProductDetails(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()        # search for all the data
    serializer_class = ProductSerializer
    lookup_field = "id"


class ViewCategory(ListCreateAPIView):
    queryset = Category.objects.annotate(product_count = Count("products")).all()
    serializer_class = CategorySerializer


class CategoryDetails(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.annotate(product_count = Count("products")).all()
    serializer_class = CategorySerializer
    lookup_field = "id"