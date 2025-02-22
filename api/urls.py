from django.urls import path, include
from products import views 

urlpatterns = [
    path("products/", include("products.product_urls")),
    path("category/", include("products.category_urls"))
]
