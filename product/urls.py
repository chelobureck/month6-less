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
	path('<int:product_id>/', ProductsDetailAPIView.as_view()),
	path('<int:product_id>/reviews/', ReviewsListAPIView.as_view()),
	path('categories/', CategoriesListAPIView.as_view()),
	path('categories/<int:category_id>/', CategoriesDetailAPIView.as_view()),
	path('reviews/', ReviewsListAPIView.as_view()),
	path('reviews/<int:review_id>/', ReviewsDetailAPIView.as_view())
]