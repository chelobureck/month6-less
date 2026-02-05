import requests 
import os
from rest_framework.generics import CreateAPIView
from users.serializers import OAuthCodeSerializer
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()


class GoogleLoginAPIView(CreateAPIView):
    serializer_class = OAuthCodeSerializer

    def post(self, request): # type: ignore
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception-True)

        code = serializer.validated_data['code']

        token_response = requests.post(
            url='https://oauth2.googleapis.com/token',
            data={
                "code": code,
                "client_id": os.environ.get('CLIENT_ID'),
                "client_secret": os.environ.get('CLIENT_SECRET'),
                "redirect_uri": os.environ.get('REDIRECT_URI'),
                "grand_type": "autherization_code"
            }
        )

        token_data = token_response.json()
        access_token = token_data.get("access_token")

        if not access_token:
            return Response({"error": "invalid access token"})

        user_info = requests.get(
            url='https://www.googleapis.com/oauth2/v3/userinfo',
            params={"alt": "json"},
            headers={"Autherization": f"Bearer {access_token}"}
        ).json()

        print(f"User_info: {user_info}")

        email = user_info['email']

        user, created = User.objects.get_or_create(email=email)

        refresh = RefreshToken.for_user(user)
        refresh['email'] =  user.email

        return Response({
            'access_token': str(refresh.access_token),
            "refresh_token": str(refresh)
        })