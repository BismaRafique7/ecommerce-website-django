from django.urls import path
from . import views
from .views import home_view

urlpatterns = [
    path('', home_view, name='home'),
    path('frontpage/', views.frontpage, name='frontpage'),
    path('category/<slug:slug>/', views.category_products, name='category'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cart/', views.cart_view, name='cart'),  
    path('search/', views.search_view, name='search'),
    path('category/<slug:slug>/', views.category_products, name='category'),
    


    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

    path('cart/update/<int:product_id>/', views.update_cart_quantity, name='update_cart_quantity'),

    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
     
    path('confirm-order/', views.confirm_order, name='confirm_order'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),
    path('order-success/', views.order_success, name='order_success'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),
    path('my-orders/', views.user_orders, name='my_orders'),

    path('admin/orders/', views.admin_orders, name='admin_orders'),
    path('admin/update-order-status/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('admin/products/', views.admin_products, name='admin_products'),
    
    path('admin/products/add/', views.add_product, name='add_product'),

    path('admin/products/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('admin/products/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('orders/', views.user_orders, name='user_orders'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),


]
