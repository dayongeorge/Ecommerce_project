from .import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home,name="home"),
    path('login_view',views.login_view,name="login_view"),
    path('signup',views.signup,name="signup"),
    path('signout',views.signout,name="signout"),
    path('phone_verify',views.phone_verify, name="phone_verify"),
    path('verify/', views.verify_code, name="verify"),

    
    path('product_details/<int:id>/',views.product_details,name="product_details"),
    path('shop',views.shop,name="shop"),
    # path('cart',views.cart,name="cart"),
    path('brand',views.brand,name="brand"),
    path('category',views.category,name="category"),
    # path('sidebar',views.sidebar,name="sidebar"),
    path('featured',views.featured,name="featured"),
    path('filter_data',views.filter_data,name="filter_data"),

    path('category/<int:category_id>/', views.products_by_category, name='products_by_category'),


#####################################################
    path('Add_address',views.Add_address.as_view(),name="Add_address"),
    path('edit_addresss/<int:id>/',views.edit_addresss,name="edit_addresss"),
    path('del_address/<int:id>/',views.del_address,name="del_address"),








  
    # path('add_address',views.add_address,name="add_address"),

  

    path('search',views.search,name="search"),
    path('error_404',views.error_404,name="error_404"),



    path('address_list',views.address_list,name="address_list"),









    # path('cart',views.cart,name="cart"),


]
urlpatterns +=static (settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)