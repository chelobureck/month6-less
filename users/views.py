from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from users.serializers import ConfirmUserSerializer, UserAuthSerializer, UserCreateSerializer, CustomTokenObtainPairSerializer
from users.email import send_confirm_email
from users.models import CustomUser
from rest_framework_simplejwt.views import TokenObtainPairView



class CustomTokenObtainPairView(TokenObtainPairView):
	serializer_class = CustomTokenObtainPairSerializer 


class RegisterAPIView(CreateAPIView):
	serializer_class = UserCreateSerializer
	
	def create(self, request,):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = CustomUser.objects.create_user(**serializer.validated_data, is_active=False) # type: ignore
		return Response(status=status.HTTP_201_CREATED, data={"user_id": user.id}) # type: ignore


class AutherizationAPIView(CreateAPIView):
	serializer_class = UserAuthSerializer
	# permission_classes = 
	
	def create(self, request,):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = authenticate(**serializer.validated_data) # type: ignore
		if user:
			token, _ = Token.objects.get_or_create(user=user)
			return Response(status=status.HTTP_200_OK, data={"key": token.key})


class UserConfirmAPIView(APIView):
	def get(self, request):
		pass
	
	def post(self, request):
		serializer = ConfirmUserSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		email = request.data.get('email')
		try: 
			user = CustomUser.objects.get(email=email)
			send_confirm_email(user)
			return Response(status=status.HTTP_200_OK)
		except CustomUser.DoesNotExist:
			return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": 'incorrect email'})


# @api_view(['POST'])
# def register_api_view(request):
#     serializer = UserCreateSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#
#     user = User.objects.create_user(**serializer.validated_data, is_active=False) # type: ignore
#
#     return Response(status=status.HTTP_201_CREATED, data={"user_id": user.id}) # type: ignore
#
#
# @api_view(['POST'])
# def autherization_api_view(request):
#     serializer = UserAuthSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     user = authenticate(**serializer.validated_data) # type: ignore
#
#     if user:
#         token, _ = Token.objects.get_or_create(user=user)
#         return Response(status=status.HTTP_200_OK, data={"key": token.key})
#
#
# @api_view(['GET', 'POST'])
# def user_confirm_api_view(request):
#     if request.method == 'GET':
#         token = request.query_params.get('token')
#         if not token:
#             return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "token is not"})
#         
#         try:
#             payload = jwt.decode(token, sign_key, do_time_check=True)
#
#             user_id = payload.get('user_id')
#             user = User.objects.get(id=user_id)
#             user.is_active = True
#             user.save()
#
#             return Response(status=status.HTTP_200_OK, data={'response': 'user is active'})
#         except Exception as error:
#             return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': str(error)})
#     if request.method == 'POST':
#         serializer = ConfirmUserSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": 'incorrect email'})
#
#         email = request.data.get('email')
#         try: 
#             user = User.objects.get(email=email)
#             send_confirm_email(user)
#         except User.DoesNotExist:
#             return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": 'incorrect email'})   
#         except:
#             return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": str()})
