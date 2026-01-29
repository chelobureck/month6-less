from rest_framework import serializers
from product.models import ProductModel, CategoryModel, ReviewModel
from rest_framework.exceptions import ValidationError
from users.models import CustomUser


class CustomUserSeializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = 'id email'.split()


class CategoryListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CategoryModel
        fields = 'id name'.split()

class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewModel
        fields = 'id text rating product'.split()

class ProductReviewSerializer(serializers.ModelSerializer):
    rating_count = serializers.SerializerMethodField()
    class Meta:
        model = ReviewModel
        fields = 'id text rating rating_count'.split()

    def get_rating_count(self, review):
        product = review.product
        all_ratings = ReviewModel.objects.filter(product=product)
        if not all_ratings:
            return 0
        ratings = [r.rating for r in all_ratings if r.rating is not None]
        return sum(ratings) / len(ratings)

class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategoryListSerializer()
    class Meta:
        model = ProductModel
        fields = '__all__'


class ProductListSerializer(serializers.ModelSerializer):
    category = CategoryListSerializer(read_only=True)
    # owner = CustomUserSeializer()
    class Meta:
        model = ProductModel
        fields = 'id title price category'.split()




class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=1000)
    price = serializers.FloatField(min_value=0.0)
    category_id = serializers.IntegerField()
    rating = serializers.ListField(child=serializers.IntegerField())

    def validate_category_id(self, category_id):
        try:
            CategoryModel.objects.get(id=category_id)
        except CategoryModel.DoesNotExist:
            raise ValidationError('Category is not exist')
        return category_id
    
    def validate_ratings(self, rating):
        ratings_from_db = ReviewModel.objects.filter(id__in=rating)
        if len(rating) != len(ratings_from_db):
            raise ValidationError('rating is not exist')
        return rating
    

class CategoryValidateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)


class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=500)
    rating = serializers.IntegerField(min_value=1, max_value=5, required=False)
    product_id = serializers.IntegerField()