from django import forms
# from.models import Amodel
from accounts.models import *
from django.contrib.auth.models import User
from orders.models import Order,Coupon

# class Aforms(forms.ModelForm):
#     class Meta:
#         model = User
#         fields =['username','first_name','last_name','email','password']
#         widgets={
#             'username':forms.TextInput(attrs={'class':'form-control'}),
#             'first_name':forms.TextInput(attrs={'class':'form-control'}),
#             'last_name':forms.TextInput(attrs={'class':'form-control'}),
#             'email':forms.EmailInput(attrs={'class':'form-control'}),
#             'password':forms.PasswordInput(render_value=True, attrs={'class':'form-control'}),
#         } 


class CategoryForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'name'}))
    #offer = forms.ModelChoiceField(required = False,queryset=Offer.objects.all() ,widget=forms.Select(attrs={'class':'form-select'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control','id':'formFile'}),required=False)
    description = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'description'}))
    status = forms.BooleanField(required=False)

    class Meta:
        model = Category
        fields = ['name','image', 'description','status']




class BrandForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'name'}))
    model = forms.CharField(required = False, widget=forms.TextInput(attrs={'class':'form-control','id':'name'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'description'}))
    status = forms.BooleanField(required=False)

    class Meta:
        model = Brand
        fields = ['name','model', 'description','status']






class ProductForm(forms.ModelForm):
   
    category = forms.ModelChoiceField(queryset=Category.objects.all() ,widget=forms.Select(attrs={'class':'form-select'}))
    brand = forms.ModelChoiceField(queryset=Brand.objects.all() ,widget=forms.Select(attrs={'class':'form-select'}))
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control' ,'id':'name'}))
    vendor = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control' ,'id':'vendor'}))
    product_image = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control','id':'formFile',}),required=False)
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control','id':'quantity'}))
    selling_price = forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control','id':'selling_price'}))
    original_price = forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control','id':'original_price'}))
    offer_price=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control','id':'offer_price'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'description'}))
    status = forms.BooleanField(required=False)
    is_available = forms.BooleanField(required=False)
    
    
    class Meta:
        model = Product
        fields = ['category','brand','name', 'vendor', 'product_image', 'quantity','selling_price','original_price','offer_price', 'description','status',  'is_available']

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImages
        fields = ['image']

class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['coupon_code', 'is_expired', 'discount_price', 'minimum_amount']
        widgets = {
            'coupon_code': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
            # 'is_expired': forms.Textarea(attrs={'class': 'form-control mb-3'}),
            'is_expired': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'discount_price': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
            'minimum_amount': forms.DateInput(attrs={'class': 'form-control datepicker mb-3'}),
        }