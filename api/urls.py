from django.urls import path, include
from rest_framework_nested import routers
from products import views 
from rest_framework.routers import DefaultRouter
from products.views import ReviewViewset

router = routers.DefaultRouter()
router.register("products", views.ProductViewset)
router.register("category", views.CategoryViewset)

product_router = routers.NestedDefaultRouter(router, "products", lookup = "product") # lookup - relation making field
product_router.register("reviews", ReviewViewset, basename="product-reviews")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(product_router.urls))
]




# urlpatterns = [
#     path("products/", include("products.product_urls")),
#     path("category/", include("products.category_urls"))
# ]
