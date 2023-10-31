from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.html import mark_safe
from django.core.validators import RegexValidator


class Category(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=50)
    parent_category = models.ForeignKey("Category", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=150)
    category = models.ForeignKey("Category", null=True, on_delete=models.SET_NULL)
    prod_count = models.IntegerField()
    price = models.IntegerField()

    def save_model(self, request, obj, form, change):
        obj.save()
        pictures = request.FILES.getlist('pictures')
        for picture in pictures:
            Photo.objects.create(post=obj, image=picture)
        return super().save_model(request, obj, form, change)

    def save_file(self, request, obj):
        pictures = request.FILES.getlist('pictures')
        for picture in pictures:
            Photo.objects.create(post=obj, image=picture)

    def __str__(self):
        return self.name


class Photo(models.Model):
    photo = models.ImageField(upload_to='uploads/')
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE, related_name='photo')

    def image_tag(self):
        if self.photo != '':
            return mark_safe('<img src="%s%s" width="150" />' % (f'{settings.MEDIA_URL}', self.photo))

    image_tag.short_description = 'Photo'
    image_tag.allow_tags = True


class Order(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    user_email = models.EmailField(null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits "
                                         "allowed.")
    user_phone = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True)
    total_price = models.IntegerField(null=True)


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL, related_name='order_product')
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)
    count = models.IntegerField()
