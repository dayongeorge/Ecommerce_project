from .import views
from django.urls import path


urlpatterns = [  


    path('admin_login',views.admin_login,name="admin_login"),
    path('Admin_logout',views.Admin_logout,name="Admin_logout"),
    path('admin_index',views.admin_index,name="admin_index"),
   
    path('search',views.search,name="search"),
    path('display_user',views.display_user,name="display_user"),
    path('block_user/<int:id>',views.block_user, name="block_user"),
    path('unblock_user/<int:id>',views.unblock_user, name="unblock_user"),

    path('add_category', views.add_category),
    path('display_category',views.display_category, name="display_category"),
    path('update_category/<str:id>',views.update_category, name="update_category"),
    path('delete_category/<str:id>',views.delete_category, name="delete_category"),




    path('add_product', views.add_product,name="add_product"),
    path('display_product',views.display_product, name="display_product"),
    path('update_product/<str:id>',views.update_product, name="update_product"),
    path('delete_product/<str:id>',views.delete_product, name="delete_product"),


    path("add_brand", views.add_brand, name="add_brand"),
    path("display_brand", views.display_brand, name="display_brand"),
    path('update_brand/<str:id>',views.update_brand, name="update_brand"),
    path('delete_brand/<str:id>',views.delete_brand, name="delete_brand"),


    path("admin_orders", views.admin_orders, name="admin_orders"),
    path("edit_order/<int:id>" , views.edit_order, name="edit_order"),


    path('coupon_manage', views.coupon_manage,name="coupon_manage"),   
    path('add_coupon', views.add_coupon,name="add_coupon"),   
    path('del_coupon/<int:id>/', views.del_coupon,name="del_coupon"),   
    path('edit_coupon/<int:id>/', views.edit_coupon,name="edit_coupon"),

    path('singleorder_details<int:id>',views.singleorder_details,name="singleorder_details"),



    path('t404', views.t404,name="t404"),




   # path('delete/<int:id>/',views.delete_data,name="delete_data"),
    #path('<int:id>/',views.update_data,name="update_data"),
]