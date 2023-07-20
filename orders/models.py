from django.db import models
from accounts.models import *

from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Payment(models.Model):
    payment_choices=(
        ('COD','COD'),
        ('Razorpay','Razorpay'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100,choices=payment_choices)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"{self.user.name}--{self.payment_method}"
    
class Order(models.Model):
    STATUS = (
        ('New','New'),
        ('Pending','Pending'),
        ('Confirmed','Confirmed'),
        ('Shipped','Shipped'),
        ('Delivered','Delivered'),
        ('Cancelled','Cancelled'),
       )

    user    = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null= True) 
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    order_number = models.CharField(max_length=50)
    order_note = models.CharField(max_length=50, blank=True)
    order_total = models.FloatField()
    tax = models.FloatField(null=True)
    status = models.CharField(max_length=50,choices=STATUS,default='New')
    ip = models.CharField(max_length=50,blank=True)
    is_ordered = models.BooleanField(default= False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    # def _str_(self):
    #     return self.address.name
    
    # def full_address(self):
    #     return f'{self.address_line_1} {self.address_line_2}'
    
    
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="myorders")
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL,blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # variation = models.ForeignKey(ProductVariant,on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    product_price = models.FloatField(null=True)
    ordered = models.BooleanField(default=False)
    
    
    def str(self):
        return f"{self.product} - {self.quantity}"

    
class Coupon(models.Model): 
    coupon_code = models.CharField(max_length = 10)
    is_expired = models.BooleanField(default=False)
    discount_price = models.IntegerField(default = 100)
    minimum_amount = models.IntegerField(default=500)
