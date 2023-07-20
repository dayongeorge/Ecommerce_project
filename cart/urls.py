from .import views

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('cart',views.cart,name="cart"),
    path('add_cart/<int:product_id>/',views.add_cart,name="add_cart"),
    path('remove_cart/<int:product_id>/',views.remove_cart,name="remove_cart"),
    path('remove_cart_item/<int:product_id>/',views.remove_cart_item,name="remove_cart_item"),
    path('update_cart_item_quantity',views.update_cart_item_quantity,name="update_cart_item_quantity"),

   
     path('apply_coupon',views.apply_coupon,name="apply_coupon"),



    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
  



]

urlpatterns +=static (settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
