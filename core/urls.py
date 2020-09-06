"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from .views import ItemsView, CartView

urlpatterns = [
    path('', ItemsView.as_view(), name="item-list"),
    re_path('product-detail/(?P<slug>[-\w]+)/', ItemsView().fetch_one_item,  name="fetch-one-item"),
    path('add-to-cart/<int:item_id>/', CartView.as_view(), name="cart_details"),
    path('delete_from_cart/', CartView().delete_from_cart, name="delete-from-cart"),
    path('add-product', ItemsView.as_view(), name="add_product"),
    path('update-product/<slug>', ItemsView.as_view(), name="update_product")
    
]
