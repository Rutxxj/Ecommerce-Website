"""
URL configuration for ecom project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('details/<int:pid>', views.details, name='details'),
    path('cart/', views.cart, name='cart'),
    path('addcart/<int:pid>', views.add_cart, name='addcart'),
    path('delete/<int:pid>', views.delete, name='delete'),
    path('search', views.search, name='search'),
    path('range/', views.range, name='range'),
    path('watchList/', views.watchList, name='watchList'),
    path('mobileList/', views.mobileList, name='mobileList'),
    path('sort/', views.sort, name='sort'),
    path('HightoLow/', views.HightoLow, name='HightoLow'),
    path('updateqty/<int:uval>/<int:pid>/', views.updateqty, name='updateqty'),
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('viewOrder/', views.viewOrder, name='viewOrder'),
    path('payment/', views.makePayment, name='payment'),
    path('insertproducts/', views.insertproducts, name='insertproducts'),
    
]
