from django.contrib import admin
from .models import Order, OrderItem, Product, Category, ProductImage, Size

# Order Admin with Inline Items
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'created_at']
    inlines = [OrderItemInline]

# Product Admin with Gallery Images
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'sale_price', 'category']
    filter_horizontal = ('available_sizes',)
    inlines = [ProductImageInline]
    fields = (
        'name', 'description', 'image', 'category',
        'price', 'sale_price', 'sale_start', 'sale_end',
        'shipping_rate', 'available_sizes','stock',
    )

# Register Remaining Models
admin.site.register(Category)
admin.site.register(Order, OrderAdmin)
admin.site.register(Size)
