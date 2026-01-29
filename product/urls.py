from django.urls import path
from product.views import (
	CategoriesDetailAPIView,
	CategoriesListAPIView,
	ProductsDetailAPIView,
	ProductsListAPIView,
	ReviewsDetailAPIView,
	ReviewsListAPIView
)

urlpatterns = [
	path('', ProductsListAPIView.as_view()),
	path('<int:pk>/', ProductsDetailAPIView.as_view()),
	path('<int:pk>/reviews/', ReviewsListAPIView.as_view()),
	path('categories/', CategoriesListAPIView.as_view()),
	path('categories/<int:pk>/', CategoriesDetailAPIView.as_view()),
	path('reviews/', ReviewsListAPIView.as_view()),
	path('reviews/<int:pk>/', ReviewsDetailAPIView.as_view())
]