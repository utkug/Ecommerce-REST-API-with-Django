from django.contrib import admin

from .models import Category, Product, Store, Customer, User, Cart, Address, Order, OrderDetails, Status
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin



# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug":("name",)}

# class StoreInLine(admin.StackedInline):
#     model = Store
#     can_delete = False
#     verbose_name_plural = "Stores"

# class CustomerInLine(admin.StackedInline):
#     model = Customer    
#     can_delete = False
#     verbose_name_plural = "Customers"

# class UserAdmin(BaseUserAdmin):
#     inlines = [StoreInLine, CustomerInLine]

class UserAdmin(BaseUserAdmin):
    #inlines = [StoreInLine, CustomerInLine]
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_store', 'is_customer', 'phone')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Custom info', {'fields': ('is_store', 'is_customer')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('username', 'password1', 'password2', 'phone', 'is_store', 'is_customer')}),
    )

#admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Store)
admin.site.register(Customer)
admin.site.register(Cart)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(OrderDetails)

admin.site.register(Status)



