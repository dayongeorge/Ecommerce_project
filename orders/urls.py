
from .import views

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static





urlpatterns = [
    path('payment/<int:id>/',views.payment,name="payment"),
    path('Paypal_payments',views.Paypal_payments,name="Paypal_payments"),

    path('Checkout',views.Checkout.as_view(),name="Checkout"),
    path('place-order-cod/<int:id>/<str:payment_method>/',views.PlaceOrderView.as_view(),name='place_order'),
    # path('place_order',views.place_order,name="place_order"),
   
    path('order_complete',views.order_complete,name="order_complete"),
    

    # path('cash_on_delivery',views.cash_on_delivery,name="cash_on_delivery"),

    path('orders',views.orders,name="orders"),
    path('admin_panel',views.admin_panel,name="admin_panel"),

    path('cancel_order<int:order_id>',views.cancel_order,name="cancel_order"),
    path('return_order<int:order_id>',views.return_order,name="return_order"),
    
    path('wallet',views.wallet,name="wallet"),
    path('order_details<int:id>',views.order_details,name="order_details"),
   

]

urlpatterns +=static (settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
