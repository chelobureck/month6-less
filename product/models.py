from django.db import models
from users.models import CustomUser


class CategoryModel(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.name}"
    
    def products_count(self)-> int:
        return self.products.count() #type: ignore
    
class ReviewModel(models.Model):
    text = models.CharField(max_length=500)
    rating = models.IntegerField(choices=((i, i) for i in range(1, 5+1)), default=3) # type: ignore
    product = models.ForeignKey('ProductModel', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.product} - {self.rating}"
    
    

class ProductModel(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    price = models.FloatField()
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE, related_name='products')
    rating = models.ManyToManyField(ReviewModel, blank=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.title} - {self.price}"