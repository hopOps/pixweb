# portfolio/serializers.py

from rest_framework import serializers
from .models import Picture, Category


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = ('id', 'name', 'user', 'category', 'description', 'pub_date', 'photo', 'public')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'public')

