"""
URL configuration for itmilan project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from myapp.views import index, login_view, members_view, profile_view, report_view, roles_count_view, commonuser_members_view, address_view, milan_members_view, register_user_view, commonuser_milan_members_view
from rest_framework.routers import DefaultRouter
from myapp.views import MilanViewSet, ResponsibilityViewSet, UserViewSet, AddressViewSet, ReportsViewSet, CommonUserViewSet


router = DefaultRouter()
router.register(r'milan', MilanViewSet)
router.register(r'responsibility', ResponsibilityViewSet)
router.register(r'user', UserViewSet)
router.register(r'address', AddressViewSet)
router.register(r'reports', ReportsViewSet)
router.register(r'commonuser', CommonUserViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("index/", index),
    path("login/", login_view),
    path("api/", include('api.urls')),
    path('', include(router.urls)),
    path("members/", members_view),
    path("profile/", profile_view),
    path("report/", report_view),
    path("rolecount/", roles_count_view),
    path("common-members/", commonuser_members_view),
    path("user-address/", address_view),
    path("milan-members/", milan_members_view),
    path("register-user/", register_user_view),
    path("common-milan-members/", commonuser_milan_members_view),

]
