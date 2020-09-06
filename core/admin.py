from django.contrib import admin
from .models import Order, CartItem, Item


admin.site.register(Item)
admin.site.register(CartItem)
admin.site.register(Order)

