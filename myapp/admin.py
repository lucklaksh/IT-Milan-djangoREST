from django.contrib import admin
from .models import Milan, Responsibility, User, Address, Reports, CommonUser

@admin.register(Milan)
class MilanAdmin(admin.ModelAdmin):
    list_display = ('milan_name', 'valaya', 'khand', 'prakhand', 'nagar', 'created_at', 'updated_at')
    search_fields = ('milan_name',)

@admin.register(Responsibility)
class ResponsibilityAdmin(admin.ModelAdmin):
    list_display = ('role_name', 'created_at', 'updated_at')
    search_fields = ('role_name',)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'contact', 'milan', 'role', 'created_at', 'updated_at')
    search_fields = ('name', 'email', 'contact')
    list_filter = ('milan', 'role')

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('address', 'city', 'district', 'state', 'pincode', 'country', 'address_type', 'user', 'created_at', 'updated_at')
    search_fields = ('address', 'city', 'district', 'state', 'pincode', 'country', 'address_type')
    list_filter = ('address_type', 'user')

@admin.register(Reports)
class ReportsAdmin(admin.ModelAdmin):
    list_display = ('milan', 'user', 'common_user', 'role', 'created_at', 'updated_at')
    search_fields = ('milan', 'user', 'common_user', 'role')
    list_filter = ('milan', 'role')

@admin.register(CommonUser)
class CommonUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact', 'milan', 'address', 'role', 'created_at', 'updated_at')
    search_fields = ('name', 'contact', 'address')
    list_filter = ('milan', 'role')
