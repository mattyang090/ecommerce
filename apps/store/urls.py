from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^product_page/(?P<product_id>\d+)$', views.product_page),
    url(r'^category_page/(?P<product_category>\w+)$', views.categorypg),
    url(r'^category_page/(?P<product_category>\w+)/(?P<product_sub_category>\w+)$', views.sub_categorypg),
    url(r'^category_page$', views.category_page),
    url(r'^cart_page$', views.cart_page),
    url(r'^checkout_page$', views.checkout_page),
    url(r'^contact_page$', views.contact_page),
    url(r'^login_register_page$', views.login_register_page),
    url(r'^register_user$', views.register_user),
    url(r'^login_user$', views.login_user),
    url(r'^admin_page$', views.admin_page),
    url(r'^add_product$', views.add_product),
    url(r'^log_out$', views.log_out),
    url(r'^delete_user/(?P<user_id>\d+)$', views.delete_user),
    url(r'^edit_user/(?P<user_id>\d+)$', views.edit_user),
    url(r'^edit_user_page/(?P<user_id>\d+)$', views.edit_user_page),
    url(r'^delete_product/(?P<product_id>\d+)$', views.delete_product),
    url(r'^edit_product_page/(?P<product_id>\d+)$', views.edit_product_page),
    url(r'^edit_product/(?P<product_id>\d+)$', views.edit_product),
    url(r'^categorize/(?P<product_category>\w+)$', views.category),
    url(r'^categorize/(?P<product_category>\w+)/(?P<product_sub_category>\w+)$', views.sub_category),
    url(r'^categorizebrand/(?P<product_brand>\w+)$', views.brand),
    url(r'^review_product/(?P<product_id>\d+)$', views.review_product),
    url(r'^add_to_cart/(?P<product_id>\d+)$', views.add_to_cart),
    url(r'^checkout$', views.checkout),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)