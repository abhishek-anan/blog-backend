from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password, check_password


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'password', 'name', 'email',
                  'mobile', 'created', 'modified')
        extra_kwargs = {
            'password': {'write_only': True}
        }
        read_only_fields = ('created', 'modified')

    def create(self, validated_data):
        user = super().create(validated_data)
        user.password = make_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.mobile = validated_data.get('mobile', instance.mobile)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = "__all__"
        read_only_fields = ('created', 'modified')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        # fields = ('name', 'id')
        fields = '__all__'
        read_only_fields = ('created', 'modified')


class BlogSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.UUIDField(write_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.UUIDField(write_only=True)
    created_by = UserSerializer(read_only=True)
    created_by_id = serializers.UUIDField(write_only=True)
    modified_by = UserSerializer(read_only=True)
    modified_by_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Blog
        fields = ('id', 'title', 'image', 'user_id', 'sub_desc',
                  'user', 'category_id', 'category', 'created_by_id', 'created_by', 'modified_by', 'modified_by_id')


class BlogTagSerializer(serializers.ModelSerializer):
    blog = BlogSerializer(read_only=True)
    blog_id = serializers.UUIDField(write_only=True)
    tag = TagSerializer(read_only=True)
    tag_id = serializers.UUIDField(write_only=True)
    created_by = UserSerializer(read_only=True)
    created_by_id = serializers.UUIDField(write_only=True)
    modified_by = UserSerializer(read_only=True)
    modified_by_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = BlogTag
        fields = ('id', 'blog_id', 'blog', 'tag_id', 'tag',
                  'created_by_id', 'created_by', 'modified_by_id', 'modified_by')


class BlogDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogDetail
        fields = ('id', 'blog', 'heading', 'text_type',
                  'text', 'created_by', 'modified_by')
        # fields = '__all__'
