from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, render,redirect
from .forms import *
from orders.models import Order,Payment,OrderProduct
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User 
from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
# from.forms import Aforms
from django.db.models import Q
from accounts.models import *
from accounts.forms import CustomUserCreationForm
from django.db.models.functions import ExtractMonth,ExtractDay,ExtractYear
from django.db.models import Count
from datetime import date
from django.contrib.auth.decorators import login_required




# Create your views here.


def admin_index(request):
    
    if request.user.is_superuser:
        total_users = CustomUser.objects.count()
        total_orders = Order.objects.count()
        recent_orders = Order.objects.order_by('-created_at')[:10]
        orders = OrderProduct.objects.all().order_by('id')[:6]
        
    
    
    # }    
        context={
            'recent_orders': recent_orders,  'totalUsers': total_users, 'total_orders': total_orders,
            'orders':orders
            }
        return render( request,'admin_templates/admin_index.html',context)
    else:
        return render(request,'admin_templates/admin_login.html')



@login_required(login_url='admin_login')
def display_user(request):
    user = CustomUser.objects.all()
    return render(request, 'admin_templates/display_user.html', {'user':user})
  

def admin_login(request):
    print("inadminlogin")

    if request.method=='POST':
        
        username=request.POST['username']
        print(username)
        password=request.POST['password']
        adminuser=authenticate(username=username,password=password)
        if adminuser is not None:
            print(adminuser)
            if adminuser.is_superuser:
                auth_login(request,adminuser)
                return redirect(admin_index)
            else:
               return render(request,'admin_templates/admin_login.html',{'error':'Invalid Credentials'})
    else:
         return render(request,'admin_templates/admin_login.html')
   
#admin logout
@never_cache
def Admin_logout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('admin_login')


# @never_cache
# @login_required(login_url='admin_login')
# def add_user(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         print('hi')
#         if form.is_valid():
#             print("hello")
#             form.save()
#             return redirect(element)
#     else:
#         form = CustomUserCreationForm()
#         print('h')
#     return render(request, 'custom_admin/add_user.html',{'form':form})

#this function edit or update user

# def update_data(request,id):
#     if request.method =='POST':
#         pi = CustomUser.objects.get(pk=id)
#         fm =Aforms(request.POST, instance=pi)
#         if fm.is_valid():
#             fm.save()
#     else:
#             pi = CustomUser.objects.get(pk=id)
#             fm =Aforms(instance=pi)
#     return render(request,"admin_templates/update.html",{'form':fm})



#this function delete user
def delete_data(request,id):
    if request.method == 'POST':
        pi = CustomUser.objects.get(pk=id)
        pi.delete()
        return redirect('add')

#search a user

def search(request):
    if request.method == 'POST':
      query = request.POST['query']
      user = CustomUser.objects.filter(Q(username__icontains=query)|Q(email__icontains=query)|Q(id__contains=query))

    return render(request,"admin_templates/search.html",{'user':user})

@never_cache
@login_required(login_url='admin_login')
def block_user(request, id):
        user = get_object_or_404(CustomUser, id=id)
        user.is_active = False
        user.save()
        return redirect(display_user)

@never_cache
@login_required(login_url='admin_login')
def unblock_user(request, id):
       user = get_object_or_404(CustomUser, id = id)
       user.is_active = True
       user.save()
       return redirect(display_user)



# Brand section ----------------------------------------------


@never_cache
@login_required(login_url='admin_login')
def add_brand(request):
    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES)
        
        if form.is_valid():
            
            form.save()
            return redirect(display_brand)
    else:
        form = BrandForm()
       
    return render(request, 'admin_templates/add_brand.html',{'form':form})



@login_required(login_url='admin_login')
def display_brand(request):
    if request.user.is_superuser:
        brand = Brand.objects.all()
        return render(request, 'admin_templates/display_brand.html', {'categories': brand})
    else:
        return redirect(admin_login)
    

@never_cache
@login_required(login_url='admin_login')
def update_brand(request, id):
    brand = get_object_or_404(Brand, id=id)
    if request.method == "POST":
        form = BrandForm(request.POST, request.FILES, instance=brand)
        if form.is_valid():
            brand = form.save()
            return redirect(display_brand)
    else:
        form = CategoryForm(instance = brand)
    return render(request, "admin_templates/update_brand.html",{'form':form})  

@never_cache
@login_required(login_url='admin_login')
def delete_brand(request, id):
    get_object_or_404(Brand, id=id).delete()
    return redirect(display_brand)



#  product session---------------------------------------------------

ImageFormSet = ProductImageFormSet = inlineformset_factory(Product, ProductImages, form=ProductImageForm, extra=5)
@never_cache
@login_required(login_url='admin_login')
def add_product(request):
    
    if request.method == 'POST':
        
        form = ProductForm(request.POST, request.FILES)
        image_form = ProductImageFormSet(request.POST, request.FILES,instance=Product())
        if form.is_valid() and image_form.is_valid():
            product = form.save(commit=False)
            product.save()
            image_form.instance = product
            image_form.save()
            return redirect(display_product)
    else:
        form = ProductForm()
        image_form = ProductImageFormSet(instance=Product())
    return render(request, 'admin_templates/add_product.html',{'form': form,'image_form':image_form})

@login_required(login_url='admin_login')
def display_product(request):
    products = Product.objects.all()
    return render(request, 'admin_templates/display_product.html',{'products':products})


@never_cache
@login_required(login_url='admin_login')
def update_product(request,id):
    product = get_object_or_404(Product, id= id)
    image_form = ImageFormSet(request.POST or None, request.FILES or None, instance=product )
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid() and image_form.is_valid():
            product = form.save()
            image_form.save()
            return redirect(display_product)
    else:
        form = ProductForm(instance=product)
    return render(request, 'admin_templates/update_product.html', {'form': form, 'image_form':image_form})





@never_cache
@login_required(login_url='admin_login')
def delete_product(request, id):
    get_object_or_404(Product, id=id).delete()
    return redirect(display_product)



#Category section -------------------------------------------------------------------------------------

@never_cache
@login_required(login_url='admin_login')
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        print('hi')
        if form.is_valid():
            print("hello")
            form.save()
            return redirect(display_category)
    else:
        form = CategoryForm()
        print('h')
    return render(request, "admin_templates/add_category.html",{'form':form})

@never_cache
@login_required(login_url='admin_login')
def display_category(request):
    categories = Category.objects.all()
    return render(request, "admin_templates/display_category.html", {'categories': categories})


@never_cache
@login_required(login_url='admin_login')
def update_category(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            category = form.save()
            return redirect(display_category)
    else:
        form = CategoryForm(instance = category)
    return render(request, "admin_templates/update_category.html",{'form':form})

@never_cache
@login_required(login_url='admin_login')
def delete_category(request, id):
    get_object_or_404(Category, id=id).delete()
    return redirect(display_category)

def t404(request):
    return render (request,'admin_templates/404.html')


def admin_orders(request):
    orders = OrderProduct.objects.all().order_by('-id')
    

    context = {
        'orders': orders
    }
    return render(request,'admin_templates/orders.html',context)

def edit_order(request, id):
    if request.method == "POST":
        status = request.POST.get("status")
        try:
            order = Order.objects.get(pk=id)
            order.status = status
            order.save()
        except Order.DoesNotExist:
            pass
    return redirect("admin_orders")



def coupon_manage(request):
    coupon = Coupon.objects.all()
    context = {
        "coupon" : coupon,
    }
    return render(request,'admin_templates/coupon.html', context)


def add_coupon(request):
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('coupon_manage')
    else:
        form = CouponForm()

    context = {'form': form}
    return render(request, 'admin_templates/add_coupon.html', context)



def del_coupon(request,id):
    if request.method == "POST":
        coup = Coupon.objects.get(id=id)
        coup.delete()
    return redirect('coupon_manage')


def edit_coupon(request,id):
    if request.method == "POST":
        coup = Coupon.objects.get(id=id)
        form = CouponForm(request.POST, instance=coup)
        if form.is_valid:
            form.save()
        return redirect('coupon_manage')
    else:
        coup = Coupon.objects.get(id=id)
        form = CouponForm(instance=coup)
        context = {
            "form" : form
        }
    return render(request, 'admin_templates/edit_coupon.html',context)


def singleorder_details(request,id):
    order=Order.objects.get(id=id)
    orderproduct=OrderProduct.objects.get(id=id)
    print("order")
    print(order)
    context={
        'order':order,
        'orderproduct':orderproduct
    }
    return render(request,'admin_templates/singleorder_details.html',context)