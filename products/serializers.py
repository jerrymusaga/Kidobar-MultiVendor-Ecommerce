from rest_framework import serializers
from .models import Category, Product, Image


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image 
        fields = ('image',)

    def to_native(self, value):
        return f'{value.image.url}'

class ProductSerializer(serializers.ModelSerializer):
    # reviews = serializers.SerializerMethodField(read_only=True)
    categories = CategorySerializer(many=True)
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    # def get_reviews(self, obj):
    #     reviews = obj.review_set.all()
    #     serializer = ReviewSerializer(reviews, many=True)
    #     return serializer.data

