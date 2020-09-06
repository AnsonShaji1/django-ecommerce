from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from .models import Profile
#from .serializers import ItemSerializer
from core.models import Item, Order, CartItem
from dj_rest_auth.registration.views import RegisterView


from rest_framework.permissions import AllowAny
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC
from django.http import HttpResponseRedirect


class MyProfileView(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        """
        Return a list of items in user profile.
        """
        try:
            profile = Profile.objects.filter(user=request.user).first()
            order_list = Order.objects.filter(owner=profile, ordered=True)
        except:
            pass
        # serializer = ItemSerializer(items, many=True)
        # return Response(serializer.data)

        return Response({})


class ConfirmEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, *args, **kwargs):
        self.object = confirmation = self.get_object()
        confirmation.confirm(self.request)
        # A React Router Route will handle the failure scenario
        # return HttpResponseRedirect('/api/rest-auth/login/')
        return Response(data={'data': "Email is successfully verified"}, status=200)

    def get_object(self, queryset=None):
        key = self.kwargs['key']
        email_confirmation = EmailConfirmationHMAC.from_key(key)
        if not email_confirmation:
            if queryset is None:
                queryset = self.get_queryset()
            try:
                email_confirmation = queryset.get(key=key.lower())
            except EmailConfirmation.DoesNotExist:
                # A React Router Route will handle the failure scenario
                # return HttpResponseRedirect('/login/failure/')
                return Response(data={'data': "Verification link expired"}, status=404)
        return email_confirmation

    def get_queryset(self):
        qs = EmailConfirmation.objects.all_valid()
        qs = qs.select_related("email_address__user")
        return qs