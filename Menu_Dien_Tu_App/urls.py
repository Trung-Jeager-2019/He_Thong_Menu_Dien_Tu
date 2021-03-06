from django.urls import path
from Menu_Dien_Tu_App import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('select', views.select, name='select'),
    path('home', views.home, name='home'),
    path('login', views.loginUser, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('signup', views.signup, name='signup'),
    path('our-team', views.aboutTeams, name='aboutTeams'),

    path('specials', views.specials, name='specials'),
    path('offers', views.offers, name='offers'),
    path('support', views.support, name='support'),
    path('cart', views.cart, name='cart'),
    path('add-item-to-cart', views.addToCart, name='addItemToCart'),
    path('remove-item-from-cart', views.removeFromCart, name='remove_item_from_cart'),
    path('profile', views.profile, name='profile'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('partner-with-us', views.partnerWithUs, name='partner_with_us'),

    path('restaurant-details', views.restaurantDetails, name='restaurant_details'),
    path('add-menu', views.addMenu, name='add_menu'),
    path('view-menu', views.viewMenu, name='view_menu'),
    path('view-describe', views.viewDescribe, name='view_describe'),
    path('delete-menu', views.deleteMenu, name='delete_menu'),
    path('view-table', views.viewTable, name='view_table'),
    path('status-table', views.statusTable, name='status_table'),
    path('add-table', views.addTable, name='add_table'),
    path('create-table', views.createTable, name='create_table'),
    path('delete-table', views.deleteTable, name='delete_table'),
    path('create-table-item', views.createTableItem, name='create_table_item'),
    path('category-product-view', views.categoryProductView, name='category_product_view'),
    path('category-item', views.categoryItem, name='category_item'),
    path('category-product', views.categoryProduct, name='category_product'),
    path('category-product-delete', views.categoryProductDelete, name='category_product_delete'),
    path('category-product-create', views.categoryProductCreate, name='category_product_create'),
    path('revenue', views.revenue, name='revenue'),
    path('revenue-date', views.revenueDate, name='revenue_date'),
    path('revenue-date-details', views.revenueDateDetails, name='revenue_date_details'),
    path('order-history', views.orderHistory, name='order_history'),
    path('owner-history', views.ownerHistory, name='owner_history'),
    path('owner-history-table', views.ownerHistoryTable, name='owner_history_table'),

    path('get-order', views.getOrder, name='get_order'),
    path('take-for-delivery', views.takeForDelivery, name='take_for_delivery'),
    path('complete-delivery', views.completeDelivery, name='complete_delivery'),
    path('delivery-history', views.deliveryHistory, name='delivery_history'),
    path('checkout', views.checkout, name='checkout'),
    path('pay', views.pay, name='pay'),
    path('complete-pay', views.completePay, name='complete_pay'),

    path('contact-us/', views.contactView, name='contact-us'),
    path('success-send/', views.successView, name='success-send'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
