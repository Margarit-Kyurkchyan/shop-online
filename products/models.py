# import os
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# from PIL import Image
from django.utils.html import mark_safe

# def images_path():
#     return os.path.join(settings.LOCAL_FILE_DIR, 'images')


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

    def __str__(self):
        return self.name


class Photo(models.Model):
    file_path = models.ImageField(upload_to='uploads/')
    products = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE, related_name='photos')

    def image_tag(self):
        if self.file_path != '':
            return mark_safe('<img src="%s%s" width="150" />' % (f'{settings.MEDIA_URL}', self.file_path))
    image_tag.short_description = 'Photo'
    image_tag.allow_tags = True

    # image_tag.short_description = 'Image'
    # def __str__(self):  # __unicode__ on Python 2
    #     return self.photo_title



