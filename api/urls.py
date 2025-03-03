# from django.urls import path, include
# from rest_framework_nested import routers
# from products.views import ProductViewset, CategoryViewset 
# from orders.views import CartViewset
# from rest_framework.routers import DefaultRouter
# from products.views import ReviewViewset
# from orders.views import CartItemViewset

# router = routers.DefaultRouter()
# router.register("products", ProductViewset)
# router.register("category", CategoryViewset)
# router.register("carts", CartViewset, basename="carts")

# product_router = routers.NestedDefaultRouter(router, "products", lookup = "product") # lookup - relation making field
# product_router.register("reviews", ReviewViewset, basename="product-reviews")

# cart_router = routers.NestedDefaultRouter(router, "carts", lookup = "cart")
# cart_router.register("items", CartItemViewset, basename="cart-item")

# urlpatterns = [
#     path("", include(router.urls)),
#     path("", include(product_router.urls)),
#     path("", include(cart_router.urls))
# ]





# urlpatterns = [
#     path("products/", include("products.product_urls")),
#     path("category/", include("products.category_urls"))
# ]














from django.urls import path, include
# from products.views import ProductViewSet, CategoryViewSet, ReviewViewSet
from products.views import ProductViewset, CategoryViewset 
from orders.views import CartViewset
from products.views import ReviewViewset
from orders.views import CartItemViewset
# from orders.views import CartViewSet, CartItemViewSet
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('products', ProductViewset, basename='products')
router.register('categories', CategoryViewset)
router.register('carts', CartViewset, basename='carts')

product_router = routers.NestedDefaultRouter(
    router, 'products', lookup='product')
product_router.register('reviews', ReviewViewset, basename='product-review')

cart_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cart_router.register('items', CartItemViewset, basename='cart-item')

# urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
    path('', include(product_router.urls)),
    path('', include(cart_router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]