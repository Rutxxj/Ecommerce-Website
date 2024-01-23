from typing import Any
from django.db import models
from django.db.models.query import QuerySet
from django.contrib.auth.models import User

# Create your models here.
#custom manager
class CustomManager(models.Manager):
     def get_price_range(self,r1,r2):
         return self.filter(price__range=(r1,r2))
     
     def watch_list(self):
          return self.filter(category__exact="watch")
     def mobile_list(self):
          return self.filter(category__exact="mobile")
     def price_order(self) -> QuerySet:
          return super().get_queryset().order_by("-price")


class Product(models.Model):
     id=models.IntegerField(primary_key=True)
     name=models.CharField(max_length=50)
     description = models.CharField(max_length=255,default='null')
     category_choices=(("mobile","mobile"),("watch","watch"))
     category=models.CharField(max_length=50,choices=category_choices, default="watch")
     image=models.ImageField(upload_to="images/", height_field=None, width_field=None, max_length=None)
     price=models.IntegerField()
     user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)

     prod = CustomManager()
     objects=models.Manager()

class Cart(models.Model):
     product = models.ForeignKey(Product,on_delete=models.CASCADE)
     quantity= models.PositiveIntegerField(default=0)
     date_added=models.DateTimeField(auto_now_add=True)
     user = models.ForeignKey(User,on_delete=models.CASCADE, default = 1)

class Order(models.Model):
     order_id= models.IntegerField()
     product = models.ForeignKey(Product,on_delete=models.CASCADE)
     quantity= models.PositiveIntegerField(default=0)
     date_added=models.DateTimeField(auto_now_add=True)
     user = models.ForeignKey(User,on_delete=models.CASCADE, default = 1)
     is_completed=models.BooleanField(default=False)