from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Category, Product, ProductImage, Order, OrderProduct, ShippingAddress

admin.site.site_header = "ShopAdmin"
admin.site.site_title = "ShopAdmin"
admin.site.index_title = "Boshqaruv paneli"


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="80" style="border-radius:6px">')
        return '—'
    preview.short_description = "Ko'rinish"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'is_available', 'thumbnail')
    list_editable = ('is_available', 'stock', 'category')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]

    def thumbnail(self, obj):
        return mark_safe(f'<img src="{obj.get_main_image()}" width="60" style="border-radius:6px">')
    thumbnail.short_description = "Rasm"


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0
    readonly_fields = ('subtotal',)

    def subtotal(self, obj):
        return f"{obj.get_subtotal():,} so'm"
    subtotal.short_description = "Jami"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'payment_type', 'total_price', 'created')
    list_filter = ('status', 'payment_type')
    list_editable = ('status',)
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created', 'updated')
    inlines = [OrderProductInline]


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    list_filter = ('order__status',)
    search_fields = ('product__name',)


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'city', 'phone', 'is_default')
    list_filter = ('city', 'is_default')
    search_fields = ('full_name', 'phone', 'address')
