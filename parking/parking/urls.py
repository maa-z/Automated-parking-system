"""
URL configuration for parking project.

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
from django.contrib import admin
from django.urls import path
from home.views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    path('',home,name='home'),

    path('login/',login_page,name='login_page'),
    path('register/',register,name='register'), # 500
    path('logout/',logout_page,name='logout'),

    path('cars/',cars,name='cars'), # wb9393 honda

    path('account/',account,name='account'), # money and cars registerd

    path('parking/',parking,name='parking'),

    # path('find/<int:id>',entry_exit,name="entry_exit"),
    #  entry/<int>
    path('data', receive_data, name='receive_data'),  # localhost:2732.3434/data

    path('account/money/<int:amount>', money, name='money'),  # 
]
