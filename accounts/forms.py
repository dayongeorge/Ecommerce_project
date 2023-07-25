from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Address, CustomUser,UserProfile
from phonenumber_field.formfields import PhoneNumberField


class CustomUserCreationForm(UserCreationForm):
    phone_number = PhoneNumberField(region="IN",max_length=15, required=True, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Phone Number'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm Password'}))
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'phone_number')


class VerifyForm(forms.Form):
    code = forms.CharField(max_length=8, required=True, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Code'}))



class UserForm(forms.ModelForm):
    class Meta:
        model=CustomUser
        fields=('username','phone_number')

    def __init__(self,*args,**kwargs):
        super(UserForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'

class UserProfileForm(forms.ModelForm):
    profile_picture=forms.ImageField(required=False,error_messages ={'invalid':("image files only")},widget=forms.FileInput)
    class Meta:
        model=UserProfile
        fields=('address_line_1','city','state','country')

    def __init__(self,*args,**kwargs):
        super(UserProfileForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["name", "house_name", "address_line_1", "city", "state", "country", "phone", "pincode"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'house_name': forms.Textarea(attrs={'class': 'form-control mb-3'}),
            'address_line_1': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'city': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'state': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'country': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
            'pincode': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
        }