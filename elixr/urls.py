"""elixr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/',views.SignUp.as_view(),name='signup'),
    path('',views.ShipList.as_view(),name='index'),
    path('ships/<slug>',views.ShipDetail.as_view(),name='ship_detail'),
    path('suits',views.SuitList.as_view(),name='suits'),
    path('suits/<slug>',views.SuitDetail.as_view(),name='suit_detail'),
    path('login/',LoginView.as_view(template_name='elixr/login.html'),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('order/',views.order_view,name='cart'),
    path('add_suit_to_cart/<slug>',views.add_suit_to_cart,name='add_st_to_cart'),
    path('add_ship_to_cart/<slug>',views.add_ship_to_cart,name="add_sp_to_cart"),
    path('remove_ship/<slug>',views.remove_ship_finally,name='remove_ship'),
    path('remove_suit/<slug>',views.remove_suit_finally,name='remove_suit'),
    path('remove_suit_one/<slug>',views.remove_suit_single,name='remove_suit_single'),
    path('remove_ship_one/<slug>',views.remove_ship_single,name='remove_ship_single'),
    path('paystack/',include(('paystack.urls','paystack'),namespace='paystack')),
    path('payment',views.customer_info,name='customer_info'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
