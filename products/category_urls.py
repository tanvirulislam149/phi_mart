from django.urls import path, include
from products import views 

urlpatterns = [
    path("", views.ViewCategory.as_view(), name="view_category"),
    path("<int:id>/", views.CategoryDetails.as_view(), name="view_specific_category")
]
