from rest_framework import serializers
from .models import Product, Photo, Category


class PhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photo
        many = True
        fields = ['id', 'photo', 'product']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        many = True
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    photo = PhotoSerializer(many=True)
    # category_set = CategorySerializer(many=True)
    # should send many = True as it may be more than image related to every product
    class Meta:
        many = True
        model = Product
        fields = ['id', 'name', 'prod_count', 'price', 'photo', 'category']


