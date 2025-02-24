from django.urls import path, include
from products import views 
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("products", views.ProductViewset)
router.register("category", views.CategoryViewset)

urlpatterns = router.urls




# urlpatterns = [
#     path("products/", include("products.product_urls")),
#     path("category/", include("products.category_urls"))
# ]
