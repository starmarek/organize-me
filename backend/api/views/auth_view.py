from django.contrib.auth import logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView

from ..serializers.auth_serializer import CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@api_view(("POST",))
def logout_view(request):
    try:
        requestRefreshToken = request.data["refresh"]
    except KeyError:
        return Response("You need to include your refresh token", status=400)

    try:
        refreshTokenObject = RefreshToken(requestRefreshToken)
    except TokenError:
        return Response("You have provided an invalid token", status=400)

    logout(request)
    refreshTokenObject.blacklist()

    return Response("Successful logout", status=200)
