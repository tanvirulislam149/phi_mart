from django.urls import path, include
from products import views 

urlpatterns = [
    path("", views.view_category, name="view_category")
]
