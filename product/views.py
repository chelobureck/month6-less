from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from product.models import ProductModel, CategoryModel, ReviewModel
from product.serializers import CategoryListSerializer, ProductListSerializer, ReviewListSerializer
from common.permissions import IsAnonymous, IsOwner
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import status

class ProductsListAPIView(ListCreateAPIView):
	queryset = ProductModel.objects.all()
	serializer_class = ProductListSerializer
	permission_classes = [IsOwner | IsAnonymous]

	def get(self, request, *args, **kwargs):
		cached_data = cache.get('list_of_product')
		if cached_data:
			print("REDIS")
			return Response(data=cached_data, status=status.HTTP_200_OK)
		print("DB")
		response = super().get(self, request, *args, **kwargs)
		if response.data.get('total', 0) > 0: # type: ignore
			cache.set("list_of_product", response.data, timeout=60)

	def perform_create(self, serializer):
		category_data = self.request.data.get('category') # type: ignore
		category, _ = CategoryModel.objects.get_or_create(**category_data)
		serializer.save(
			owner=self.request.user,
			category=category
		)
		category_data = self.request





class ProductsDetailAPIView(RetrieveUpdateDestroyAPIView):
	queryset = ProductModel.objects.all()
	serializer_class = ProductListSerializer
	permission_classes = [IsOwner | IsAnonymous]



class CategoriesListAPIView(ListCreateAPIView):
	queryset = CategoryModel.objects.all()
	serializer_class = CategoryListSerializer


class CategoriesDetailAPIView(RetrieveUpdateDestroyAPIView):
	queryset = CategoryModel.objects.all()
	serializer_class = CategoryListSerializer
	permission_classes = [IsOwner | IsAnonymous]



class ReviewsListAPIView(ListCreateAPIView):
	queryset = ReviewModel.objects.all()
	serializer_class = ReviewListSerializer


class ReviewsDetailAPIView(RetrieveUpdateDestroyAPIView):
	queryset = ReviewModel.objects.all()
	serializer_class = ReviewListSerializer
	


# @api_view(['GET', 'POST'])
# def products_list_api_view(request):
#     if request.method == 'GET':
#         products = ProductModel.objects.all()
#         data = ProductListSerializer(products, many=True).data
#         return Response(data=data, status=status.HTTP_200_OK)
#     
#     if request.method == 'POST':
#         print("пользователь создает продукт:\n" + request.data)
#         serializer = ProductValidateSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
#         title = serializer.validated_data.get("title") # type: ignore
#         description = serializer.validated_data.get("description") # type: ignore
#         price = serializer.validated_data.get("price") # type: ignore
#         category_id = serializer.validated_data.get("category_id") # type: ignore
#         rating = serializer.validated_data.get("rating") # type: ignore
#
#         product = ProductModel.objects.create(
# 		title=title,
# 		description=description,
# 		price=price,
# 		category_id=category_id
# )
#         product.rating.set(rating) # type: ignore
#         return Response(status=status.HTTP_200_OK, data=ProductDetailSerializer(product).data)
#
#
# 	
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def products_detail_api_view(request, product_id):
#     try:
#
#         product = ProductModel.objects.get(id=product_id)
#     
#     except ProductModel.DoesNotExist:
#
#         return Response(data={
#             'error': 'product does not exist'
#         }, status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         data = ProductListSerializer(product, many=False).data
#         return Response(data=data, status=status.HTTP_200_OK)
#     if request.method == 'PUT':
#         serializer = ProductValidateSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
#         
#         product.title = serializer.validated_data.get('title') # type: ignore
#         product.description = serializer.validated_data.get('description') # type: ignore
#         product.price = serializer.validated_data.get('price') # type: ignore
#         product.category_id = serializer.validated_data.get('category_id') # type: ignore
#         product.rating.set(serializer.validated_data.get('rating')) # type: ignore
#         product.save()
#         return Response(status=status.HTTP_201_CREATED, data=ProductDetailSerializer(product).data)
#     if request.method == 'DELETE':
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
# @api_view(['GET', 'POST'])
# def categories_list_api_view(request):
#     if request.method == 'GET':
#         categories = CategoryModel.objects.all()
#         data = CategoryListSerializer(categories, many=True).data
#         return Response(data=data, status=status.HTTP_200_OK)
#     if request.method == 'POST':
#         serializer = CategoryValidateSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
#         print(f"пользователь создает категорию:\n {request.data}")
#         name = serializer.validated_data.get("name") # type: ignore
#         category = CategoryModel.objects.create(
#             name=name
#         )
#         return Response(status=status.HTTP_201_CREATED, data=CategoryListSerializer(category, many=False).data)
#     
# 
# 
# 
# 
# @api_view(['GET', 'PUT', 'DELETE'])
# def categories_detail_api_view(request, category_id):
#     try:
#         category = CategoryModel.objects.get(id=category_id)
#     except CategoryModel.DoesNotExist:
#         return Response(data={
#             'error': 'category does mot exist'
#         }, status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         data = CategoryListSerializer(category, many=False).data
#         return Response(data=data, status=status.HTTP_200_OK)
#     if request.method == 'PUT':
#         serializer = CategoryValidateSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
#         category.name = serializer.validated_data.get('name') # type: ignore
#         category.save()
#         return Response(status=status.HTTP_201_CREATED, data=CategoryListSerializer(category, many=False).data)
#     if request.method == 'DELETE':
#         category.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
# @api_view(['GET', 'POST'])
# def reviews_list_api_view(request, product_id=None):
#     if product_id is None:
#         if request.method == 'GET':
#             reviews = ReviewModel.objects.all()
#             data = ReviewListSerializer(reviews, many=True).data
#             return Response(data=data, status=status.HTTP_200_OK)
#         if request.method == 'POST':
#             return Response(status=status.HTTP_400_BAD_REQUEST,
#                             data={
#                                 "error": "You can't create a review without a product."
#                             })
#     
#     if request.method == 'GET':
#         reviews = ReviewModel.objects.filter(product__id=product_id)
#         data = ProductReviewSerializer(reviews, many=True).data
#         return Response(data=data, status=status.HTTP_200_OK)
#     if request.method == 'POST':
#         serializer = ReviewValidateSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
#         text = serializer.validated_data.get('text') # type: ignore
#         rating = serializer.validated_data.get('rating') # type: ignore
#         review = ReviewModel.objects.create(
#             text=text,
#             rating=rating,
#             product_id=product_id
#         )
#         return Response(status=status.HTTP_201_CREATED, data=ReviewListSerializer(review, many=False).data)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def reviews_detail_api_view(request, review_id):
#     try:
#         review = ReviewModel.objects.get(id=review_id)
#     except ReviewModel.DoesNotExist:
#         return Response(data={
#             'error': 'review does mot exist'
#         }, status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         data = ReviewListSerializer(review, many=False).data
#         return Response(data=data, status=status.HTTP_200_OK)
#     if request.method == 'PUT':
#         serializer = ReviewValidateSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
#         
#         review.text = serializer.validated_data.get('text') # type: ignore
#         review.rating = serializer.validated_data.get('rating') # type: ignore
#         review.product_id = serializer.validated_data.get('product_id') # type: ignore
#         review.save()
#         return Response(status=status.HTTP_201_CREATED, data=ReviewListSerializer(review, many=False).data)
#     if request.method == 'DELETE':
#         review.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)