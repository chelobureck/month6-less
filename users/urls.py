from django.urls import path
from users.views import AutherizationAPIView, RegisterAPIView, UserConfirmAPIView

urlpatterns = [
	path('register/', RegisterAPIView.as_view()),
	path('autherization/', AutherizationAPIView.as_view()),
	path('confirm/', UserConfirmAPIView.as_view())
]
