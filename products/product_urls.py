from django.urls import path, include
from products import views 

urlpatterns = [
    path("<int:id>/", views.view_specific_product, name="view_specific_product"),
    path("", views.view_products, name="view_products")
]
