from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib import admin
from .models import *
from django.utils.html import format_html







class CustomUserCreationForm(UserCreationForm):
    phone = forms.CharField(max_length=20, required=True, help_text='Phone number')
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm Password'}))
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'phone_number')

class CusotmUserAdmin(admin.ModelAdmin):
     list_display=('username','phone_number','email')

class ProductImagesAdmin(admin.TabularInline):
    model=ProductImages


class ProductAdmin(admin.ModelAdmin):
    inlines=(ProductImagesAdmin,)
    list_display=['id','name','product_image','selling_price','is_featured','created_at','status']
    list_editable=['status','is_featured']

# class ProductAttributeAdmin(admin.ModelAdmin):
#      list_display=['id','Product','price']

# class ColorAdmin(admin.ModelAdmin):
#      list_display=['title','color_bg']
# admin.site.register(Color,ColorAdmin)
   
class CategoryAdmin(admin.ModelAdmin):
     list_display=['name','category_image']
        
# class VendorAdmin(admin.ModelAdmin):
#      list_display=['title','vendor_image']
    

# class VendorAdmin(admin.ModelAdmin):
#      list_display=['title','vendor_image']

# class CartOrderAdmin(admin.ModelAdmin):
#      list_display=['user','price','paid_track','order_date','product_status']

# class CartOrderItemsAdmin(admin.ModelAdmin):
#      list_display=['order','product_status','item','image','qty','price','total']

# class ProductReviewAdmin(admin.ModelAdmin):
#      list_display=['user','product','review','rating']

# class wishlistAdmin(admin.ModelAdmin):
#      list_display=['user','product','date']   

# class AddressAdmin(admin.ModelAdmin):
#      list_display=['user','address','status']         

class UserProfileAdmin(admin.ModelAdmin):
     def thumbnail(self,object):
          return format_html('<img src="{}" width="30" style="border-radius:50%;">'.format(object.profile_picture.url))
     thumbnail.short_description='Profile Picture'
     list_display=('thumbnail','user','city','state','country')



# admin.site.register(Userprofile,UserProfileAdmin)
admin.site.register(Product,ProductAdmin)
# admin.site.register(ProductAttribute,ProductAttributeAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Brand)
# admin.site.unregister(Color)
# admin.site.register(Color, ColorAdmin)

admin.site.register(CustomUser,CusotmUserAdmin)
# admin.site.register(Vendor,VendorAdmin)
# admin.site.register(CartOrder,CartOrderAdmin)
# admin.site.register(CartOrderItems,CartOrderItemsAdmin)
# admin.site.register(ProductReview,ProductReviewAdmin)
# admin.site.register(wishlist,wishlistAdmin)
# admin.site.register(Address,AddressAdmin)

