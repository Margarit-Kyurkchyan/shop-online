from rest_framework import serializers
from .models import Product, Photo, Category, Order as OrderModel, OrderProduct


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
    photo = PhotoSerializer(many=True, allow_null=True, required=False)

    class Meta:
        many = True
        model = Product
        fields = ['id', 'name', 'prod_count', 'price', 'category', 'photo']

    # def create(self, validated_data):
    #     # print(validated_data.FILES.getlist('pictures'))
    #     product = Product.objects.create(**validated_data)
    #     product.save_file(validated_data, product)
    #     # p = validated_data
    #     # print(validated_data.FILES.getlist('photo'))
    #     # # print(product)
    #     # # pictures = request.FILES.getlist('photo')
    #     # # for picture in pictures:
    #     # #     Photo.objects.create(product=product, image=picture)
    #     return product


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['order', 'product', 'count']


class OrderSerializer(serializers.ModelSerializer):
    order_product = OrderProductSerializer(many=True)

    class Meta:
        model = OrderModel
        fields = ['user', 'user_email', 'user_phone', 'total_price', 'order_product']

    def create(self, validated_data):
        order_product_data = validated_data.pop('order_product')
        order = OrderModel.objects.create(**validated_data)
        # print(validated_data)
        # print(order_product_data)
        total_price = 0
        for order_data in order_product_data:
            total_price += order_data['count'] * order_data['product'].price
            # print(order_data['product'].price)
            OrderProduct.objects.create(order=order, **order_data)
        order.total_price = total_price
        order.save()
        return order
