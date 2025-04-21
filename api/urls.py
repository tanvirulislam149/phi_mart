from django.urls import path, include
from rest_framework_nested import routers
from products.views import ProductViewset, CategoryViewset, ProductImageViewset
from orders.views import CartViewset
from products.views import ReviewViewset
from orders.views import CartItemViewset, OrderViewset

router = routers.DefaultRouter()
router.register("products", ProductViewset)
router.register("category", CategoryViewset)
router.register("carts", CartViewset, basename="carts")
router.register("orders", OrderViewset, basename="orders")

product_router = routers.NestedDefaultRouter(router, "products", lookup = "product") # lookup - relation making field
product_router.register("reviews", ReviewViewset, basename="product-reviews")
product_router.register("images", ProductImageViewset, basename='product-images')

cart_router = routers.NestedDefaultRouter(router, "carts", lookup = "cart")
cart_router.register("items", CartItemViewset, basename="cart-item")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(product_router.urls)),
    path("", include(cart_router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]