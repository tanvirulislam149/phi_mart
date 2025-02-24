from django.urls import path, include
from products import views 

urlpatterns = [
    path("<int:id>/", views.ProductDetails.as_view(), name="view_specific_product"),
    path("", views.ViewProduct.as_view(), name="view_products")
]
