from django.contrib import admin
from .models import Store, Category, Product, Stock, SalesTransaction, InventoryAlert, UserProfile


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'manager_name', 'contact_email']
    search_fields = ['name', 'location', 'manager_name']
    filter_horizontal = ['users']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'category', 'selling_price', 'supplier']
    list_filter = ['category']
    search_fields = ['name', 'sku', 'supplier']


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['store', 'product', 'quantity', 'reorder_level', 'max_stock_level']
    list_filter = ['store']
    search_fields = ['product__name', 'store__name']


@admin.register(SalesTransaction)
class SalesTransactionAdmin(admin.ModelAdmin):
    list_display = ['store', 'product', 'quantity', 'total_amount', 'transaction_date', 'payment_method']
    list_filter = ['store', 'payment_method', 'transaction_date']
    search_fields = ['product__name', 'store__name']
    date_hierarchy = 'transaction_date'


@admin.register(InventoryAlert)
class InventoryAlertAdmin(admin.ModelAdmin):
    list_display = ['alert_type', 'store', 'product', 'severity', 'is_resolved', 'created_at']
    list_filter = ['alert_type', 'severity', 'is_resolved', 'store']
    search_fields = ['product__name', 'store__name', 'message']
    date_hierarchy = 'created_at'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'company', 'phone', 'default_store']
    search_fields = ['user__username', 'company']
    list_filter = ['default_store']
