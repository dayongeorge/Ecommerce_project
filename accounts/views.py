
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as auth_login,logout
from django.views.decorators.cache import never_cache
from .forms import AddressForm, CustomUserCreationForm,UserForm
from accounts.models import *
from cart.models import *
from cart.views import _cart_id
from .import verify
from .forms import VerifyForm,UserProfileForm
from django.contrib.auth.decorators import login_required
from cart.views import _cart_id
from cart.models import CartItem
from django.core.paginator import EmptyPage, PageNotAnInteger,Paginator
import requests

from orders.models import Order,OrderProduct,Payment
from django.views import View
from django.views.generic import CreateView


                 



# Create your views here.
@never_cache
def home(request):
    product=Product.objects.all()
    latest_added_products = Product.objects.order_by('-created_at')[:3]
    return render(request,'user_templates/index.html',
                  {
                      'product':product,
                      'latest_added_products':latest_added_products,
                  })
@never_cache
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            try:
               cart=Cart.objects.get(cart_id=_cart_id(request))
               is_cart_item_exists=CartItem.objects.filter(cart=cart).exists()
               if is_cart_item_exists:
                   cart_item=CartItem.objects.filter(cart=cart)

                   for item in cart_item:
                       item.user=user
                       item.save()
            except:
               pass
            auth_login(request,user)
            messages.success(request,'You are now logged in.')
            url=request.META.get('HTTP_REFERER')
            try:
                query=requests.utils.urlparse(url).query
                params=dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage=params['next']
                    return redirect(nextPage)
                
            except:
                return redirect('home')
        else:
            messages.error(request,"User name or password is incorect")
    return render(request,"user_templates/login_view.html")
def signup(request):
      if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            phone_number = '+91' + str(form.cleaned_data.get('phone_number')) 
            form.save()
            
            return redirect('login_view')
      else:
        form = CustomUserCreationForm()
      return render(request, 'user_templates/signup.html', {'form': form})


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('signup')

# otp verification

def verify_code(request):
    if request.method == 'POST':
        form = VerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            phone_no = request.session.get('phone')
            
            
            if verify.check(phone_no, code):
                print("checked")
                
                user = CustomUser.objects.get(username = request.session.get('username'))
                userobj = CustomUser.objects.filter(username = request.session.get('username'))
                print(user)
                print(user.is_authenticated)
                print(user.is_active)
                print(user.is_superuser)
                if userobj is not None and user.is_active and user.is_superuser == False:
                    print(user.is_authenticated)
                    auth_login(request, user)
                    return redirect(home)
                print(user)
                return redirect(home)
            else:
                print("error")
    else:
        form = VerifyForm()
    return render(request, 'user_templates/verify.html', {'form': form})


def phone_verify(request):
    if request.method == "POST":
        
        phone = '+91'+  str(request.POST['phone_number'])
        if check_phone_number(phone):
            verify.send(phone)
            user = username_password(phone)
            request.session['username'] = user.username
            print(user.username)
            user.is_verified = True
            user.is_active = True
            request.session['phone'] = phone
            return redirect(verify_code)
        else:
            context = "Please register first"
            return render(request, 'phone_verify.html',{'context':context})
    return render(request, 'user_templates/phone_verify.html')

def username_password(phone):
    user = CustomUser.objects.filter(phone_number=phone)[0]
    return user

def check_phone_number(phone_number):
    try:
        phone1=CustomUser.objects.filter(phone_number=phone_number)
        print("phone1")
        print(phone1)
        phone = CustomUser.objects.filter(phone_number=phone_number)[0]
        print(phone)
        return True
    except CustomUser.DoesNotExist:
        return False





def product_details(request,id):
    try:
        single_product=Product.objects.get(id=id)
        in_cart =CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
       
    except Exception as e:
        raise e
    images=ProductImages.objects.filter(product=single_product.id)
    context={
     'single_product':single_product, 
     'in_cart'    : in_cart,
     'images'    :images
    }

    return render (request,'user_templates/product_details.html',  context)


def shop(request):
    products=Product.objects.all()
    cats=Product.objects.distinct().values('category__name','category__id')
    brands=Product.objects.distinct().values('brand__name','brand__id')
    paginator=Paginator(products,6 )
    page=request.GET.get('page')

    try:
       paged_products=paginator.page(page)
    except PageNotAnInteger:
        paged_products = paginator.page(1)
    except EmptyPage:
        paged_products = paginator.page(paginator.num_pages)
    
    product_count=products.count()
    price_high_low = Product.objects.order_by('-offer_price')
    price_low_high = Product.objects.order_by('offer_price')
   

    return render (request,'user_templates/shop.html',
    {
        'products':paged_products,
         'cats':cats,
         'brands':brands,
         'product_count':product_count,
         'price_high_low':price_high_low,
         'price_low_high':price_low_high,
          })

def brand(request):
    brand=Brand.objects.all().order_by('-id')

    return render (request,'user_templates/brand.html',{'brand':brand })

def category(request):
    category=Category.objects.all().order_by('-id')

    return render (request,'user_templates/category.html',{'category':category })



@login_required(login_url='login_view')
def user_profile(request):
    # user = CustomUser.objects.all()
    try:
        userprofile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return render (request,'user_templates/user_profile.html')
    context= {
        'userprofile':userprofile,
        'user':request.user,
    }
    return render(request,'user_templates/user_profile.html',context)



def user_profile(request):
    user_profile = None  # Set initial value to None

    try:
         user_profile =  UserProfile.objects.get( user=request.user)

    except UserProfile.DoesNotExist:
        # Handle the case when no UserProfile object is found
        return render (request,'user_templates/user_profile.html')

    context = {
        'userprofile': user_profile,
        'user': request.user,
    }
    return render(request, 'user_templates/user_profile.html', context)

def add_profile(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return redirect('user_profile')  # Redirect to user profile page after adding the profile
    else:
        form = UserProfileForm()
    
    context = {
        'form': form,
    }
    return render(request, 'user_templates/add_profile.html', context)



def edit_profile(request):
    try:
        userprofile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return HttpResponseRedirect(reverse('add_user_profile'))

    if request.method=="POST":
        user_form=UserForm(request.POST,instance=request.user)
        profile_form=UserProfileForm(request.POST,request.FILES,instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,"your profile has been updated..")
            return redirect('edit_profile')
    else:
        user_form=UserForm(instance=request.user)
        profile_form=UserProfileForm(instance=userprofile)

    context= {
       'user_form':user_form,
        'profile_form':profile_form,
        'userprofile':userprofile,
        }
    return render(request,'user_templates/edit_profile.html',context)

def addressbook(request):
    # userprofile = UserProfile.objects.get(user=request.user)
    address = Address.objects.filter(user=request.user)
    
    context = {
       
        'user':request.user,
        'address':address,
    }
    
    return render(request, 'user_templates/addressbook.html', context)


def sidebar(request):
      products=Product.objects.all()
      cats=Product.objects.distinct().values('category__name','category__id')
      brands=Product.objects.distinct().values('brand__name','brand__id')
      colors=Product.objects.distinct().values('color__title','color__id','color__color_code')

    
      return render (request,'user_templates/sidebar.html',
    {
        'products':products,
         'cats':cats,
         'brands':brands,
         'colors':colors

          })


def featured(request):
    products=Product.objects.filter(is_featured=True)
    cats=Product.objects.distinct().values('category__name','category__id')
    brands=Product.objects.distinct().values('brand__name','brand__id')
    colors=Product.objects.distinct().values('color__title','color__id','color__color_code')


    return render(request,'user_templates/featured.html',
                  {
         'products':products,
         'cats':cats,
         'brands':brands,
         'colors':colors

          })


#Filter data
def filter_data(request):
    return JsonResponse({'data':'hello'})

def products_by_category(request, category_id):
    category = Category.objects.get(id=category_id)
    products = Product.objects.filter(category=category)
    product_count=products.count()


    context = {
        'category': category,
        'products': products,
        'product_count':product_count,

    }

    return render(request, 'user_templates/categorywise.html', context)













def search(request):
    if "keyword" in request.GET:
        keyword=request.GET['keyword']
        if keyword:
            products=Product.objects.order_by('created_at').filter(Q(name__icontains=keyword) | Q(description__icontains=keyword) )
            product_count=products.count()
        context={
            'products':products,
            'product_count':product_count,
        }
    return render(request,'user_templates/shop.html',context)
def error_404(request):
    return render(request,'user_templates/error_404.html')


def address_list(request):
    return render (request,'addressbook/address_list.html')


class Add_address(CreateView):
    model = Address
    form_class = AddressForm
    template_name = 'user_templates/add_address.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('Checkout')


class Add_address_user(CreateView):
    model = Address
    form_class = AddressForm
    template_name = 'user_templates/add_address.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('addressbook')


# edit address checkout page
def edit_addresss(request, id):
    product = get_object_or_404(Address, pk=id)
    if request.method == "POST":
        product_form = AddressForm(request.POST, request.FILES, instance=product)
        if product_form.is_valid():
            product_form.save()
            return redirect('Checkout')
    else:
        product_form = AddressForm(instance=product)

    context = {
        "product_form": product_form
    }
    return render(request, 'user_templates/edit-address.html', context)



# user profile edit address
def edit_addresss_user(request, id):
    product = get_object_or_404(Address, pk=id)
    if request.method == "POST":
        product_form = AddressForm(request.POST, request.FILES, instance=product)
        if product_form.is_valid():
            product_form.save()
            return redirect('userprofile')
    else:
        product_form = AddressForm(instance=product)

    context = {
        "product_form": product_form
    }
    return render(request, 'edit-address.html', context)


def del_address(request, id):
    prod = Address.objects.get(pk=id)
    prod.delete()
    return redirect('Checkout')


def del_address_user(request, id):
    prod = Address.objects.get(pk=id)
    prod.delete()
    return redirect('user_templates/addressbook')


def forgotPassword(request):
    global mobile_number_forgotPassword
    if request.method == 'POST':
        # setting this mobile number as global variable so i can access it in another view (to verify)
        mobile_number_forgotPassword = ('+91' + str(request.POST.get('phone_number')))
        print(mobile_number_forgotPassword)
        # checking the null case
        if mobile_number_forgotPassword is '':
            messages.warning(request, 'You must enter a mobile number')
            return redirect('forgotPassword')
   
        # instead we can also do this by savig this mobile number to session and
        # access it in verify otp:
        # request.session['mobile']= mobile_number
        user = CustomUser.objects.filter(phone_number=mobile_number_forgotPassword)
        print("user")
        print(user)
        if user:  #if user exists
            verify.send(mobile_number_forgotPassword)
            return redirect('forgotPassword_otp')
        else:
            messages.warning(request,'Mobile number doesnt exist')
            return redirect('forgotPassword')
            
    return render(request, 'user_templates/forgotPassword.html')


def forgotPassword_otp(request):
    mobile_number = mobile_number_forgotPassword
    
    if request.method == 'POST':
        form = VerifyForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data.get('code')
        # otp = request.POST.get('otp')
        if verify.check(mobile_number, otp):
            user = CustomUser.objects.get(phone_number=mobile_number)
            if user:
                return redirect('resetPassword')
        else:
            messages.warning(request,'Invalid OTP')
            return redirect('forgotPassword_otp')
    else:
        form = VerifyForm()
        
    return render(request,'user_templates/forgotPassword_otp.html', {'form':form})


def resetPassword(request):
    mobile_number = mobile_number_forgotPassword
    
    if request.method == 'POST':
        password1 = request.POST.get('password')
        password2 = request.POST.get('confirm_password')
        print(str(password1)+' '+str(password2)) #checking
        
        if password1 == password2:
            user = CustomUser.objects.get(phone_number=mobile_number)
            print(user)
            print('old password  : ' +str(user.password))
            
            user.set_password(password1)
            user.save()

            print('new password  : ' +str(user.password))
            messages.success(request, 'Password changed successfully')
            return redirect('login_view')
        else:
            messages.warning(request, 'Passwords doesnot match, Please try again')
            return redirect('resetPassword')
    
    return render(request, 'user_templates/resetPassword.html')


def contact(request):
    return render(request,'user_templates/contact.html')