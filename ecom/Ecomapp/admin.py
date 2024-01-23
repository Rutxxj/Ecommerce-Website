from django.contrib import admin
from .models import Product,Cart,Order

# Register your models here.
class EcomAdmin(admin.ModelAdmin):
    list_display=['id','name','category','price']

admin.site.register(Product,EcomAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display=['product','quantity','user']

admin.site.register(Cart)

class OrderAdmin(admin.ModelAdmin):
    list_display=['order_id','product_id',"quantity","user","is_completed"]

admin.site.register(Order,OrderAdmin)