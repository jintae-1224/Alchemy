"""alchemy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import include
from django.urls import path
from trade.views import (
    index,
    register,
    login_view,
    logout_view,
    board_list,
    condition_create,
    condition_change,
    run,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name="index"),
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("alchemy/", board_list, name="board_list"),
    path("alchemy/create/", condition_create, name="condition_create"),
    path("alchemy/run/", run, name="run"),
    path("alchemy/<str:action>/<int:condition_id>", condition_change, name="condition_change"),
    path("logout/", logout_view, name="logout"),
]
