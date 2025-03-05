from django.contrib import admin
from products.models import Product, Review, Category

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Review)