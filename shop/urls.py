from django.urls import path
from .views import index, product_by_category, product_detail, add_to_cart

urlpatterns = [
    path('', index, name='index'),
    path('category/<slug:category_slug>/', product_by_category, name='by_category'),
    path('product/<slug:slug>/', product_detail, name='product_detail'),
    path('add-to-cart/<slug:product_slug>/<int:current_value>', add_to_cart, name=add_to_cart)
]