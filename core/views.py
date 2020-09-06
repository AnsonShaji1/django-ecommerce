from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from .serializers import ItemSerializer, OrderSerializer, OrderItemSerializer
from .models import Item, Order, OrderItem
from accounts.models import Profile
from django.views.generic.detail import DetailView
from django.http import JsonResponse


class ItemsView(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Return a list of all items.
        """
        
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

    def fetch_one_item(self, request, *args, **kwargs):
        try:
            item_slug = kwargs.get('slug', None)
            item_obj = Item.objects.get(slug=item_slug)
            serializer = ItemSerializer(item_obj)
            return JsonResponse({'data': serializer.data}, status=200)
        except:
            return JsonResponse({'error': 'Some error'}, status=401)


    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            item = ItemSerializer(data=data)
            if item.is_valid():
                item.save()
                return Response(item.data)
        except:
            return Response({})

    def put(self, request, *args, **kwargs):
        try:
            slug = kwargs.get('slug', None)
            update_item = Item.objects.get(slug=slug)
            serializer = ItemSerializer(update_item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        except:
            return Response({})





class CartView(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        try:
            items = OrderItem.objects.filter(is_ordered=False)
            serializer = OrderItemSerializer(items, many=True)
            # return JsonResponse({'data': serializer.data}, status=200)
            return Response(serializer.data)
        except:
            # return JsonResponse({'error': 'Some error'}, status=401)
            return Response({})


    def post(self, request, *args, **kwargs):
        """
        Add items to cart
        """
        user_profile = Profile.objects.get_or_create(user=request.user)
        product = Item.objects.filter(id=kwargs.get('item_id', '')).first()

        for item in user_profile.product.all():
            if item.id == product.id:
                print("You already own this product")
                return

        order_item = OrderItem.objects.get_or_create(item=product)
        order = Order.objects.get_or_create(owner=user_profile)
        order.item.add(product)
        order.save()
        print("item is added to cart")
        serializer = OrderSerializer(order, many=True)

        return Response(serializer.data)

    
    def delete_from_cart(self, request):
        items_to_delete = OrderItem.objects.filter(pk=request.data['item_id'])
        if items_to_delete.exists():
            items_to_delete[0].delete()
            print("One item is deleted")

        return Response({})



