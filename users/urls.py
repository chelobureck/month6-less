from django.urls import path
from users.views import AutherizationAPIView, RegisterAPIView
from users.google_oauth import GoogleLoginAPIView

urlpatterns = [
	path('register/', RegisterAPIView.as_view()),
	path('autherization/', AutherizationAPIView.as_view()),
    
	
	path("google-login/", GoogleLoginAPIView.as_view())
]
