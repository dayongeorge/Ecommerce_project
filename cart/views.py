import json
from django.shortcuts import render,redirect,get_object_or_404

from  orders.models import Coupon
from .models import *
from accounts.models import *
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
# Create your views here.


def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart




#############################################
# og functions for remove and add
@login_required(login_url='login_view')
def add_cart(request, product_id):
    if 'total' in request.session:
        del request.session['total']
    product = Product.objects.get(id=product_id)
    user = request.user

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
    cart.save()
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()

        success_condition = True
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            user=user,
            product=product,
            cart=cart,
            quantity=1,
        )
        cart_item.save()
        success_condition = True
    
    if success_condition:
        response={'success':True}
        # return redirect('cart')
    else:
        response = {'status': 'error', 'message': 'Error message goes here'}

    return JsonResponse(response)


def remove_cart(request,product_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    product=get_object_or_404(Product,id=product_id)
    cart_item=CartItem.objects.get(product=product,cart=cart)
    if cart_item.quantity>1:
        cart_item.quantity -=1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')
#######################################################








def remove_cart_item(request,product_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    product=get_object_or_404(Product,id=product_id)
    cart_item=CartItem.objects.get(product=product,cart=cart)
    cart_item.delete()
    return redirect('cart')

def cart(request,total=0,quantity=0,cart_items=None):
    

    try:
        tax = 0
        total_price = 0
        total=0
        user=request.user
        
        cart=Cart.objects.get(cart_id=_cart_id(request))
            # print(cart)
        cart_items=CartItem.objects.filter(cart=cart,is_active=True)
      
        #    (filter inside )
        
        for cart_item in cart_items:
            total += (cart_item.product.offer_price * cart_item.quantity)
            quantity +=cart_item.quantity
            tax=(2*total)/100
            total_price=total+tax
            if request.session.get('total'):
                 total_price=request.session.get('total')
            else:
                total_price=total+tax
    except ObjectDoesNotExist:
        total_price=0
        quantity=0
        tax=0
        total=0

    context={
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax' :tax,
        'cart_total': total_price,
    }
    if not cart_items:
        context['empty_cart'] = True
    return render(request,"user_templates/cart.html",context)



def update_cart_item_quantity(request):
     
        cart_item_id = request.GET.get('cart_item_id')
        action = request.GET.get('action')

        # cart_item = Cartitem.objects.get(id=cart_item_id)
        try:
           cart_item = CartItem.objects.get(id=cart_item_id) 
        except cart_item.DoesNotExist:
            return JsonResponse({'status': 404, 'error': 'Cart item not found'})

        if action == 'increase':
          
            if cart_item.quantity < cart_item.product.quantity:
                 cart_item.quantity += 1
            else:
                return JsonResponse({'status': 400, 'error': 'Product is out of stock'})
        elif action == 'decrease':
            if cart_item.quantity>1:
                cart_item.quantity -=1
                # cart_item.save()

        cart_item.save()

        
       
  

        return JsonResponse({'status': 200,'quantity': cart_item.quantity,'subtotal': cart_item.sub_total() })







#############################################################################################

##   wishlist   ##3

def wishlist(request):
    user = request.user
    try:
        wishlist = WishList.objects.get(user=user)
        products = wishlist.products.all()
    except WishList.DoesNotExist:
        # If the wishlist does not exist, create a new empty wishlist
        wishlist = WishList.objects.create(user=user)
        products = []
    
    context = {
        'wishlist': wishlist,
        'products': products
    }

    return render(request, 'user_templates/wishlist.html', context)

def add_to_wishlist(request, product_id):
    user = request.user
    wishlist, created = WishList.objects.get_or_create(user=user)
    product = Product.objects.get(id=product_id)
    wishlist.products.add(product)
    return redirect('wishlist')

def remove_from_wishlist(request, product_id):
    user = request.user
    wishlist = WishList.objects.get(user=user)
    product = Product.objects.get(id=product_id)
    wishlist.products.remove(product)
    return redirect('wishlist')


def apply_coupon(request):
    if request.method == 'POST':
        data = {}
        body = json.loads(request.body)
        coupon_code = body.get('coupon')
        total_price = body.get('total_price')

        try:
            coupon = Coupon.objects.get(coupon_code__iexact=coupon_code, is_expired=False)
        except Coupon.DoesNotExist:
            data['message'] = 'Not a Valid Coupon'
            data['total'] = total_price
        else:
            minimum_amount = coupon.minimum_amount
            discount_price = coupon.discount_price
            if total_price >= minimum_amount:
                total_price -= discount_price
                request.session['total'] = total_price
                data['message'] = f'{coupon.coupon_code} Applied'
            else:
                data['message'] = 'Not a Valid Coupon'
            data['total'] = total_price

        return JsonResponse(data)
    






    