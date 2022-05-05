from django.contrib import admin
from.models import Product, Category, Photo

class PhotoAdmin(admin.StackedInline):
    model = Photo
    readonly_fields = ['image_tag']
    list_display = ['image_tag']


class ProductAdmin(admin.ModelAdmin):
    inlines = [PhotoAdmin]

    class Meta:
        model = Product

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
