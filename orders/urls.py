
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
    # path('order_complete',views.order_complete,name="order_complete"),

    # path('cash_on_delivery',views.cash_on_delivery,name="cash_on_delivery"),

    path('admin_orders',views.admin_orders,name="admin_orders"),
    path('admin_panel',views.admin_panel,name="admin_panel"),

    path('cancel_order<int:order_id>',views.cancel_order,name="cancel_order"),
    # path('orders/<int:order_id>/return/', views.return_order, name='return_order'),

    # path('add_address', views.add_address, name="add_address"),
    # path('address_section', views.address, name="order_address"), 
    
   

]

urlpatterns +=static (settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
