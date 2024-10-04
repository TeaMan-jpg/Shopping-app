from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.





class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField(default=0)
    author = models.ForeignKey(User,on_delete=models.CASCADE,default=0)
    desc = models.TextField(default="")
    quantity = models.IntegerField(default=0)
    
    # basket = models.ForeignKey(Basket,default=0,on_delete=models.CASCADE)
    
    def get_absolute_url(self):
        return reverse("shopping:product-detail",kwargs={'pk':self.pk})

class Basket(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    # products = models.ManyToManyField(Product)
    
class Review(models.Model):
    title = models.CharField(max_length=200)
    rating = models.IntegerField()
    desc = models.TextField()
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    author = models.ForeignKey(User,on_delete=models.CASCADE,default=0)

    def get_absolute_url(self):
        return reverse("product-detail",kwargs={'pk':self.pk})


class BasketItems(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('basket', 'product')


class Profiles(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=200)