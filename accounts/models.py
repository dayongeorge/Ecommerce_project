import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

import datetime
from django.utils.text import slugify 
from django.utils.html import mark_safe
from django.urls import reverse
from decimal import Decimal
from django.contrib.auth import get_user_model

STATUS_CHOICE =(
    ("process","Processing"),
    ("shipped","Shipped"),
    ("delivered","Delivered"),

)



STATUS =(
    ("draft","Draft"),
    ("disabled","Disabled"),
    ("rejected","Rejected"),
    ("in_review","In Review"),
    ("published","Published"),

)


RATING =(
    (1,"★☆☆☆☆"),
    (2,"★★☆☆☆"),
    (3,"★★★☆☆"),
    (4,"★★★★☆"),
    (5,"★★★★★"),

)


def user_directory_path(instance,filename):
    return 'user_{0}/{1}'.format(instance.user.id,filename)
def getFileName(request, filename):
    now_time = datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    new_filename = "%s%s"%(now_time, filename)
    return os.path.join('uploads/',new_filename)

    
class CustomUser(AbstractUser, models.Model):
    username = models.CharField(null=True, blank=True, max_length=100, unique=True)
    phone_number = PhoneNumberField(max_length=15, blank=True)
    email = models.EmailField(null=True, blank=True, max_length=255, unique=True)
    # joined_on = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default= True)
    is_active = models.BooleanField(default= True)
    # is_guest = models.BooleanField(default=False)
    # guest_token = models.CharField(max_length=255, null=True, blank=True)



class Category(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    image = models.ImageField(upload_to="category",null=True,blank=True)
    description = models.TextField(max_length=150, null=False, blank=False) 
    status = models.BooleanField(default=False,help_text="0-show,1-Hidden",blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
       


    def __str__(self):
        return self.name
    
# class Tags(models.Model):
#     pass

class Brand(models.Model):
    name = models.CharField(max_length=100, null= False, blank=False)
    description = models.TextField(max_length=150, null=True, blank=True)
    model = models.CharField(max_length=150, null=True, blank=True)
    status = models.BooleanField(default=False,help_text="0-show,1-Hidden",blank=True)

    def __str__(self):
        return self.name
    

# class Color(models.Model):
#     title=models.CharField(max_length=100)
#     color_code=models.CharField(max_length=100)
    

#     def color_bg(self):
#         return mark_safe('<div style="width:50px; height:50px; background-color:%s"></div>' %(self.color_code))
#     def __str__(self):
#         return self.title



    
class Product(models.Model): 
    # user=models.ForeignKey(CustomUser,on_delete=models.SET_NULL,null=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE,default=1)
    # color=models.ForeignKey(Color,on_delete=models.CASCADE,default=1)
   
    name = models.CharField(max_length=100, null=False, blank=False)
    slug = models.SlugField(unique=True, max_length=255, null=True, blank=True)
    vendor = models.CharField(max_length=100, null=False, blank=False)
    product_image = models.ImageField(upload_to='product/',null=True,blank=True)
    quantity = models.PositiveIntegerField(default=0)
    original_price = models.DecimalField(null=False,max_digits=10,default=Decimal('0.00'),decimal_places=2)
    selling_price = models.DecimalField(null=False,max_digits=10,default=Decimal('0.00'),decimal_places=2)
    offer_price = models.DecimalField(null=False,max_digits=10,default=Decimal('0.00'),decimal_places=2)
    # tags= models.ForeignKey(Tags,on_delete=models.SET_NULL,null=True)
    # product_status=models.CharField(choices=STATUS,max_length=10,default="in_review")

    description = models.TextField(max_length=350, null=False, blank=False)
    status = models.BooleanField(default=False,help_text="0-show,1-Hidden",blank=True)
    trending = models.BooleanField(default=False,help_text="0-default,1-Trending",blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    offer_status = models.BooleanField(default=False)
    updated=models.DateTimeField(null=True,blank=True)
    is_featured=models.BooleanField(default=False)
  
    class Meta:
        ordering = ['id']

    # def product_image(self):
    #     return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    def get_percentage(self):
        new_price=(self.selling_price/self.original_price)*100
        return new_price
    
    def get_url(self):
        return reverse('product_details',args=[self.id])
    
class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_pictures")
    image = models.ImageField(upload_to='product/', blank=True)
    date=models.DateTimeField(auto_now_add=True)
   
   
    class Meta:
        verbose_name_plural="Product Images"

   
    # def __str__(self):
    #     return self.image.url
    


User = get_user_model()
class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    house_name=models.CharField(max_length=100)
    address_line_1 = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    

    def _str_(self):
        return self.user.username 

class UserProfile(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    address_line_1=models.CharField(blank=True,max_length=100)
    profile_picture=models.ImageField(blank=True,upload_to="uploads")
    city = models.CharField(blank=True,max_length=100)
    state = models.CharField(blank=True,max_length=100)
    country = models.CharField(blank=True,max_length=100)

    def __str__(self):
        return self.user.first_name 
    def full_address(self):
        return self.address_line_1






