import calendar
from django.conf import settings
from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.views import View
from cart.models import CartItem
from cart.models import Cart
from.forms import *
import datetime
from accounts.models import Product
from . models import Order,Payment,OrderProduct
import json
from django.urls import reverse
import uuid
# Create your views here.
from django.http import JsonResponse
import razorpay
from django.db.models.functions import ExtractMonth,ExtractDay,ExtractYear
from django.db.models import Count
from datetime import date
from django.contrib.auth.decorators import login_required




def total_amount(request):
    total=0
    cart_items = CartItem.objects.filter(user=request.user)
    for cart_item in cart_items:
        total += (cart_item.product.offer_price * cart_item.quantity)
        return int(total)
def grand_totall(request):
    total=0
    grand_total=0
    tax=0
    cart_items = CartItem.objects.filter(user=request.user)
    for cart_item in cart_items:
        total += (cart_item.product.offer_price * cart_item.quantity)
        tax=(2*total)/100
        grand_total=total+tax
    return int(grand_total)
    

class Checkout(View):
    def get(self, request):
        # cart = Cart.objects.get(user=request.user)
        # cart_items = CartItem.objects.filter(user=request.user)
        # address = Address.objects.filter(user=request.user)
        # if not cart_items.exists():
        #     return redirect('Checkout')
        # sum = cart.get_total_price()
        # total = cart.get_total_products()

        # context = {
        #     'cart_items': cart_items,
        #     'address': address,
        #     'sum': sum,
        #     'total': total,
        # }
        # return render(request, 'checkout.html', context)
        try:
            # cart = Cart.objects.get(user=request.user)
            cart_items = CartItem.objects.filter(user=request.user)
            address = Address.objects.filter(user=request.user)

            if cart_items.exists():
                current_user=request.user
                # if (request.session.get('total')):
                #     sum = request.session.get('total')
                # else:
                # # prod = cart_items.get_subtotal()
                #     sum = cart.get_total_price()
                # # sum = cart.get_total_price()
                # total = cart.get_total_products()

                cart_items=CartItem.objects.filter(user=current_user)
                print(cart_items)
                cart_count=cart_items.count()
                if cart_count <=0:
                    return redirect('shop')
                total=0
                quantity=0
                grand_total=0
                tax=0
                for cart_item in cart_items:
                    total += (cart_item.product.offer_price * cart_item.quantity)
                    quantity +=cart_item.quantity
                tax=(2*total)/100
                if request.session.get('total'):
                    grand_total=request.session.get('total')
                else:
                    grand_total=total+tax

                context = {
                    'cart_items': cart_items,
                    'address': address,
                    'cart_items':cart_items,
                    'total':total,
                    'tax':tax,
                    'grand_total':grand_total,
                }
                return render(request, 'user_templates/checkout.html', context)
            else:
                return redirect('cart')  # Redirect to cart page if there are no cart items
        except Cart.DoesNotExist:
            return redirect('cart')



def order_complete(request):
    return render (request,'order_templates/order_complete.html')
   



def payment(request, id):
    cart = CartItem.objects.filter(user=request.user)
    address = Address.objects.get(pk=id)
    current_user=request.user
    cart_items=CartItem.objects.filter(user=current_user)
    cart_count=cart_items.count()
    client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
    if cart_count <=0:
        return redirect('shop')
    total=0
    quantity=0
    grand_total=0
    tax=0
    for cart_item in cart_items:
        total =total_amount(request)
        payment = client.order.create({ "amount": total*100, "currency": "INR", "receipt": "order_rcptid_11"})
        quantity +=cart_item.quantity
        tax=(2*total)/100
        if request.session.get('total'):
            grand_total=request.session.get('total')
        else:
            grand_total=total+tax
        print(grand_total)
        print(cart_items)
        context= {
            'cart_items': cart_items,
            'tax':tax,
            'total1':total,
            'sum': grand_total,
            'total': quantity,
            'address': address,
            'payment':payment,
            }
    return render(request, 'order_templates/payments.html',context)



##cod payment function which add all necesary model datas..
class PlaceOrderView(View):

    def get(self, request, id,payment_method):
        # Retrieve user, address, and other necessary data from the request
        user = request.user
        address = Address.objects.get(id=id)
        payment_method = payment_method  
        order_number="#1578641"
        payment_id=str(uuid.uuid4()),
        status=''
        if payment_method=='Online':
            status='Success'
        else:
            status='Pending'

        # Retrieve the user's cart or order items
        cart_items = CartItem.objects.filter(user=request.user)
        total_price=total_amount(request)
        grand_total=grand_totall(request)
        # total_price = calculate_cart_total(cart_items)

        # Create a new payment entry
        payment = Payment.objects.create(
            user=user,
            payment_method=payment_method,
            amount_paid=total_price, 
            status=status  # Set initial status to Pending
        )

        # Create a new order
        order = Order.objects.create(
            user=user,
            payment=payment,
            address=address,
            order_number='...',  
            order_note='...',  
            order_total=total_price,  
            tax=0.0,  
            status='New',  
            ip='...', 
            is_ordered=True  
        )

        # Create OrderProduct instances for each cart item and update the order total
        for cart_item in cart_items:
            OrderProduct.objects.create(
                order=order,
                payment=payment,
                user=user,
                product=cart_item.product,
                quantity=cart_item.quantity,
                product_price=cart_item.product.offer_price,
                ordered=False
            )
          
            order.save()
           
            product = cart_item.product
            product.quantity -= cart_item.quantity
            product.save()
            

        # Clear the user's cart or order items
        # Assuming you have a way to clear the cart items for the user
        cart_items.delete()
        if 'total' in request.session:
            del request.session['total']

        # Redirect to a success page or show a success message
        return redirect('order_complete')
    


## Paypal payment method with all data adding 
def Paypal_payments(request):
    body=json.loads(request.body)
    order=Order.objects.get(user=request.user,is_ordered=False,order_number=body['orderID'])
    # store transaction details inside payment model
    print(body['transID'])
    payment=Payment(
        user=request.user,
        payment_id=body['transID'],
        payment_method=body['payment_method'],
        
        amount_paid=order.order_total,
        orderstatuses=body['status'],
    )
    payment.save()
    print("payment printing")
    print(payment)
    order.payment=payment
    order.is_ordered=True
    order.save()

    # move the cart items to Order Product table

    cart_items=CartItem.objects.filter(user=request.user)

    for item in cart_items:
        orderproduct=OrderProduct()
        orderproduct.payment=payment
        orderproduct.quantity=item.quantity
        orderproduct.product_price=item.product.offer_price
        orderproduct.ordered=True
        orderproduct.save()
        print("order product")
        print(orderproduct)


    #Reduce the quantity of the sold products
        product=Product.objects.get(id=item.product_id)
        product.quantity-=item.quantity
        product.save()
    #clear cart
    CartItem.objects.filter(user=request.user).delete()
    print(request.user)
    #send order recieved email to customer
    # send order number and transaction id back to sendData method via Jsonresponse
    data={
         'order_number':order.order_number,
         'transID':payment.payment_id,
    }
    return JsonResponse(data)

    # return redirect('order_complete')

    # return render (request,'order_templates/payments.html')
    


def order_complete(request):
        # order_number=request.GET.get('order_number')
        # transID=request.GET.get('payment_id')

        # # if not order_number:
        # #     order_number = request.session['order_number']
        
        # # if not transID: 
        # #     transID = request.session['transID']

        # # try:
        # order=Order.objects.get(id=order_number,is_ordered=True)
        # ordered_products=OrderProduct.objects.filter(order_id=order.id)
        # payment=Payment.objects.get(payment_id=transID)
        # amount_paid=payment.amount_paid
        # context={
        #         'order':order,
        #         'ordered_products':ordered_products,
        #         'order_number':order.order_number,
        #         'transID':payment.payment_id,
        #         'payment':payment,
        #         'amount_paid':amount_paid,
        #         'user': request.user,
        #     }
        return render(request,'order_templates/order_complete.html')
    # except (Payment.DoesNotExist,Order.DoesNotExist):
    #     return redirect('home')


def admin_orders(request):

    orders = OrderProduct.objects.filter(user=request.user,ordered=False)
    context = {'orders': orders}
    
    return render(request,'user_templates/orders.html',context)  


def cancel_order(request, order_id):
    # Retrieve the order object
    order = get_object_or_404(Order, id=order_id, user=request.user)
    print(order.status)

    if order.status != 'New':
        # Check if the order can be canceled (e.g., if it's still pending)
        messages.error(request, 'This order cannot be canceled.')
        return redirect(reverse('orders'))

    # Cancel the order
    order.status = 'CANCELED'
    order.save()

    # Add a success message
    messages.success(request, 'Order has been canceled successfully.')

    return redirect(reverse('orders'))


@login_required(login_url='admin_login')
def admin_panel(request):
    today = date.today()
    
    delivered_orders = Order.objects.filter(status='Delivered')
    
    delivered_orders_by_months = delivered_orders.annotate(
        delivered_month=ExtractMonth('created_at'),
        delivered_day=ExtractDay('created_at')
    ).values('delivered_month', 'delivered_day').annotate(delivered_count=Count('id')).values('delivered_month', 'delivered_day', 'delivered_count')
    
    delivered_orders_month = []
    delivered_orders_number = []
    for d in delivered_orders_by_months:
        month_name = calendar.month_name[d['delivered_month']]
        day_number = d['delivered_day']
        delivered_orders_month.append(f"{month_name} {day_number}")
        delivered_orders_number.append(d['delivered_count'])

    order_by_months = Order.objects.annotate(
        month=ExtractMonth('created_at'),
        day=ExtractDay('created_at')
    ).values('month', 'day').annotate(count=Count('id')).values('month', 'day', 'count')
    
    monthNumber = []
    dayNumber = []
    totalOrders = []
    for o in order_by_months:
        month_name = calendar.month_name[o['month']]
        day_number = o['day']
        monthNumber.append(f"{month_name} {day_number}")
        dayNumber.append(day_number)
        totalOrders.append(o['count'])

    delivered_orders_by_years = delivered_orders.annotate(delivered_year=ExtractYear('created_at')).values('delivered_year').annotate(delivered_count=Count('id')).values('delivered_year', 'delivered_count')
    delivered_orders_year = []
    delivered_orders_year_number = []
    for d in delivered_orders_by_years:
        delivered_orders_year.append(d['delivered_year'])
        delivered_orders_year_number.append(d['delivered_count'])
    
    order_by_years = Order.objects.annotate(year=ExtractYear('created_at')).values('year').annotate(count=Count('id')).values('year', 'count')
    yearNumber = []
    totalOrdersYear = []
    for o in order_by_years:
        yearNumber.append(o['year'])
        totalOrdersYear.append(o['count'])
    
    context ={
        'delivered_orders': delivered_orders,
        'order_by_months': order_by_months,
        'monthNumber': monthNumber,
        'dayNumber': dayNumber,
        'totalOrders': totalOrders,
        'delivered_orders_number': delivered_orders_number,
        'delivered_orders_month': delivered_orders_month,
        'delivered_orders_by_months': delivered_orders_by_months,
        'today': today,
        'order_by_years': order_by_years,
        'yearNumber': yearNumber,
        'totalOrdersYear': totalOrdersYear,
        'delivered_orders_year': delivered_orders_year,
        'delivered_orders_year_number': delivered_orders_year_number,
        'delivered_orders_by_years': delivered_orders_by_years,
    }
    return render(request, 'admin_templates/report.html',context)








































   








# def payments(request):
#     body=json.loads(request.body)
#     order=Order.objects.get(user=request.user,is_ordered=False,order_number=body['orderID'])
#     # store transaction details inside payment model
#     print(body['transID'])
#     payment=Payment(
#         user=request.user,
#         payment_id=body['transID'],
#         payment_method=body['payment_method'],
        
#         amount_paid=order.order_total,
#         orderstatuses=body['status'],
#     )
#     payment.save()
#     print("payment printing")
#     print(payment)
#     order.payment=payment
#     order.is_ordered=True
#     order.save()

#     # move the cart items to Order Product table

#     cart_items=CartItem.objects.filter(user=request.user)

#     for item in cart_items:
#         orderproduct=OrderProduct()
#         orderproduct.order_id=order.id
#         print(orderproduct.order_id)
#         orderproduct.payment=payment
#         orderproduct.user_id=request.user.id
#         orderproduct.product_id=item.product_id
#         orderproduct.quantity=item.quantity
#         orderproduct.product_price=item.product.offer_price
#         orderproduct.ordered=True
#         orderproduct.save()
#         print("order product")
#         print(orderproduct)


#     #Reduce the quantity of the sold products
#         product=Product.objects.get(id=item.product_id)
#         product.quantity-=item.quantity
#         product.save()
#     #clear cart
#     CartItem.objects.filter(user=request.user).delete()
#     print(request.user)
#     #send order recieved email to customer
#     #send order number and transaction id back to sendData method via Jsonresponse
#     # data={
#     #     'order_number':order.order_number,
#     #     'transID':payment.payment_id,
#     # }
#     return JsonResponse(data)

#     return redirect('order_complete')

#     # return render (request,'order_templates/payments.html')



# def place_order(request,total=0,quantity=0):
#     current_user=request.user
#     print(current_user)
#     #if the cart count is less than or equal to 0, then redirect back to shop
#     cart_items=CartItem.objects.filter(user=current_user)
#     print(cart_items)
#     cart_count=cart_items.count()
#     if cart_count <=0:
#         return redirect('shop')
#     grand_total=0
#     tax=0
#     for cart_item in cart_items:
#         total += (cart_item.product.offer_price * cart_item.quantity)
#         quantity +=cart_item.quantity
#     tax=(2*total)/100
#     grand_total=total+tax
#     print(grand_total)

  

#     if request.method =='POST':
#         print(request.POST)
#         form=OrderForm(request.POST)
#         if form.is_valid():
#             #store all the billing information inside Order table
#             data= Order()
#             data.user=current_user
#             data.first_name=form.cleaned_data['first_name']
#             print(data.first_name)
#             data.last_name=form.cleaned_data['last_name']
#             data.phone=form.cleaned_data['phone']
#             data.email=form.cleaned_data['email']
#             data.address_line_1=form.cleaned_data['address_line_1']
#             data.address_line_2=form.cleaned_data['address_line_2']
#             data.country=form.cleaned_data['country']
#             data.state=form.cleaned_data['state']
#             data.city=form.cleaned_data['city']
#             data.order_note=form.cleaned_data['order_note']
#             data.order_total=grand_total
#             data.tax=tax
#             data.ip=request.META.get('REMOTE_ADDR')
#             data.save()
#             #generata order number
#             yr=int(datetime.date.today().strftime('%Y'))
#             dt=int(datetime.date.today().strftime('%d'))
#             mt=int(datetime.date.today().strftime('%m'))
#             d=datetime.date(yr,mt,dt)
#             current_date=d.strftime("%Y%m%d")
#             order_number=current_date+str(data.id)
#             data.order_number=order_number
#             data.save()


           
#             userprofile = Userprofile.objects.filter(user=request.user)

#             order=Order.objects.get(user=current_user,is_ordered=False, order_number=order_number)
#             context={
#                 'order':order,
#                 'cart_items':cart_items,
#                 'total':total,
#                 'tax':tax,
#                 'grand_total':grand_total,
#                 'userprofile': userprofile,
#                 'user':request.user,

#             }
#             return render(request,'order_templates/payments3.html',context)
#         else:
#             return redirect('checkout')


# def order_complete(request):
#     order_number=request.GET.get('order_number')
#     transID=request.GET.get('payment_id')

#     if not order_number:
#         order_number = request.session['order_number']
    
#     if not transID: 
#         transID = request.session['transID']

#     try:
#         order=Order.objects.get(order_number=order_number,is_ordered=True)
#         ordered_products=OrderProduct.objects.filter(order_id=order.id)
#         payment=Payment.objects.get(payment_id=transID)
#         amount_paid=payment.amount_paid
#         context={
#             'order':order,
#             'ordered_products':ordered_products,
#             'order_number':order.order_number,
#             'transID':payment.payment_id,
#             'payment':payment,
#             'amount_paid':amount_paid,
#             'user': request.user,
#         }
#         return render(request,'order_templates/order_complete.html',context)
#     except (Payment.DoesNotExist,Order.DoesNotExist):
#         return redirect('home')
    
  
    





# from .forms import ReturnForm

# def return_order(request, order_id):
#     # Retrieve the order object
#     order = get_object_or_404(Order, id=order_id, user=request.user)
    
#     if order.status != 'New':
#         # Check if the order can be returned (e.g., if it's still in an accepted state)
#         messages.error(request, 'This order cannot be returned.')
#         return redirect(reverse('orders'))

#     if request.method == 'POST':
#         form = ReturnForm(request.POST)
#         if form.is_valid():
#             reason = form.cleaned_data['reason']
            
#             # Save the reason for return in the database
#             Return.objects.create(order=order, reason=reason)
            
#             # Update the order status to "Return Processing"
#             order.status = 'Return Processing'
#             order.save()
            
#             messages.success(request, 'Return request has been submitted successfully.')
#             return redirect(reverse('orders'))
#     else:
#         form = ReturnForm()
    
#     return render(request, 'return_order.html', {'order': order, 'form': form})







# class place_order(View):

#         def dispatch(self, request, *args, **kwargs):
#                 # Declare and assign instance attributes
                
#                 self.flag = 0
#                 print("place")
#                 self.current_user = request.user
#                 print(self.current_user)

#                 self.cart = Cart.objects.get(user=self.current_user)
#                 self.cart_items = CartItem.objects.filter(user=self.current_user)
#                 self.cart_count = self.cart_items.count()
                
#                 self.total_price = self.cart.get_total_price()
#                 print(self.cart_count)
#                 self.default_address_id = None
#                 # Call the default dispatch method
#                 return super().dispatch(request, *args, **kwargs)
                        
                
            
#         def get(self,request):
            
            
#           # if cart count is less than or equal to zero redirect back to homepage
#             if self.cart_count <= 0:
#                     return redirect('home')
#             else:
#                 print("else")
#                 try:
#                         current_order = Order.objects.get(user=self.current_user)
#                         print(current_order,"current")
#                         if current_order:
#                                 data = self.current_order
#                         else:
#                                 raise Exception("order not formed")
#                 except Exception as e:
#                         print("exception")
#                         data = Order()
#                         print(data)

                        
#                         data.user = self.current_user
#                         selected_option = request.GET.get('selectedOption')
#                         payment_method_mapping = {
#                                         'cod': 'COD',
#                                         'razorpay': 'Razorpay',
#                                         # Add more mappings as needed
#                                 }
#                         print(selected_option)
#                         payment_method_selected = payment_method_mapping.get(selected_option)
#                         # status =''
#                         # if payment_method_selected == 'COD':
#                         #         status = 'Pending'
#                         # else:
#                         #         status = 'Success'

#                         print(payment_method_selected)
#                         if selected_option == 'cod':
#                                 print("first one")
#                                 payment_method = Payment.objects.create(user=self.current_user,payment_method=payment_method_selected,amount_paid=self.total_price,status="Pending")
                                
#                                 data.payment = payment_method
                                
#                                 self.default_address_id = request.GET.get('defaultAddressId')
#                                 print(self.default_address_id)
#                                 data.shipping_address =  Address.objects.get(id=self.default_address_id)
#                                 print(data.shipping_address)
#                                 data.order_total = self.total_price
#                                 print(data.user,data.payment,data.shipping_address,data.order_total)
#                                 data.save()
#                                 print(data)
#                                 # generate order number
#                                 yr = int(datetime.date.today().strftime('%Y'))
#                                 dt = int(datetime.date.today().strftime('%d'))
#                                 mt = int(datetime.date.today().strftime('%m'))
#                                 d = datetime.date(yr,mt,dt)
#                                 current_date = d.strftime("%Y%m%d")
#                                 order_number= current_date + str(data.id)
#                                 data.order_number = order_number
#                                 print(data.order_number,current_date)
#                                 data.save()
#                                 for item in self.cart_items:
#                                         order = OrderProduct.objects.create(product=item.product,
#                                                 variation=item.product_variant,
#                                                 payment=payment_method,
#                                                 order=data,
#                                                 quantity=item.quantity,
#                                                 product_price=item.product_variant.price,
#                                                 user=self.current_user,
#                                                 ordered=True)
#                                         print(order)
#                                         print(item.product.stock)
#                                         product = item.product
#                                         product.stock -= item.quantity
#                                         print(item.product.stock)
#                                         product.save()
#                                         item.delete()
#                                         flag = 1
                                
#                                 return JsonResponse({'message': 'Order placed successfully.','flag':flag})
#                         elif selected_option == 'razorpay':
#                                     print("elif")
#                                     import razorpay
#                                     client = razorpay.Client(auth=("rzp_test_9PWZXmd88RGOGY", "CMlBW52kdSRZWeoUu5Dlt3Qv"))
                
#                                     razorpay_order = client.order.create(
#                                     {"amount": int(self.total_price), "currency": "INR", "payment_capture": "1"}
#                                     )
#                                     print(razorpay_order)
                                    
#                                     order_id = razorpay_order['id']
                                    
#                                     print(order_id)
                                        

#                                     payment_method = Payment.objects.create(user=self.current_user,payment_method=payment_method_selected,amount_paid=self.total_price,status="Success")
                                        
#                                     data.payment = payment_method
                                        
#                                     default_address_id = request.GET.get('defaultAddressId')
#                                     data.shipping_address =  Address.objects.get(id=default_address_id)
#                                     print(data.shipping_address)
#                                     data.order_total = self.total_price
#                                     print(data.user,data.payment,data.shipping_address,data.order_total)
#                                     data.save()
#                                     print(data)
#                                     # generate order number
#                                     yr = int(datetime.date.today().strftime('%Y'))
#                                     dt = int(datetime.date.today().strftime('%d'))
#                                     mt = int(datetime.date.today().strftime('%m'))
#                                     d = datetime.date(yr,mt,dt)
#                                     current_date = d.strftime("%Y%m%d")
#                                     order_number= current_date + str(data.id)
#                                     data.order_number = order_number
#                                     print(data.order_number,current_date)
#                                     data.save()
#                                     for item in self.cart_items:
#                                         order = OrderProduct.objects.create(product=item.product,
#                                                 variation=item.product_variant,
#                                                 payment=payment_method,
#                                                 order=data,
#                                                 quantity=item.quantity,
#                                                 product_price=item.product_variant.price,
#                                                 user=self.current_user,
#                                                 ordered=True)
#                                         print(order)
#                                         item.delete()
#                                         item.product.stock -= item.quantity
                                    
#                                 #     cart = Cart.objects.get(user=request.user)
#                                 #     total_price = cart.get_total_price()
#                                     payment_id = payment_method.id
#                                     redirect_url = reverse('razorpay') + f'?total={self.total_price}&id={order_id}&order_number={order_number}&payment_id={payment_id}'
    
#                                     return JsonResponse({'message': 'razorpay entered.','redirect':redirect_url})





# def cash_on_delivery(request):
    
#         order = Order.objects.get(user=request.user, is_ordered=False, order_number=request.POST.get('orderID'))
        
#         # Create a payment instance for cash on delivery
#         payment = Payment(
#             user=request.user,
#             payment_id='COD',  # Set a custom payment ID for cash on delivery
#             payment_method='Cash on Delivery',
#             amount_paid=order.order_total,
#             status='Paid'  # Assuming the cash on delivery payment is considered paid immediately
#         )
#         payment.save()

#         # Update order and order product details
#         order.payment = payment
#         order.is_ordered = True
#         order.save()

#         cart_items = CartItem.objects.filter(user=request.user)

#         for item in cart_items:
#             orderproduct = OrderProduct(
#                 order_id=order.id,
#                 payment=payment,
#                 user_id=request.user.id,
#                 product_id=item.product_id,
#                 quantity=item.quantity,
#                 product_price=item.product.offer_price,
#                 ordered=True
#             )
#             orderproduct.save()

#             # Reduce the quantity of the sold products
#             product = Product.objects.get(id=item.product_id)
#             product.quantity -= item.quantity
#             product.save()

#         # Clear the cart
#         CartItem.objects.filter(user=request.user).delete()

#         # Send order received email to the customer

#         # Send order number and transaction ID back to sendData method via JsonResponse
#         # data = {
#         #     'order_number': order.order_number,
#         #     'transID': payment.payment_id,
#         # }
#         # return JsonResponse(data)


#         # return to order complete page

#         return redirect('order_complete')
#     # return render(request, 'order_templates/payments1.html')