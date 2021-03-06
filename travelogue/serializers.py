from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User
from .models import Location, Review, Comment

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        depth = 1
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'locations_visited')


class UserSerializerWithToken(serializers.ModelSerializer):

    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        print(validated_data)
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('token', 'id', 'username', 'first_name', 'last_name', 'email', 'password')

class LocationSerializer(serializers.ModelSerializer):
    users_visited = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset=User.objects.all())

    class Meta:
        model = Location
        fields = ['name', 'latitude', 'longitude', 'pic_url', 'users_visited']

class ReviewSerializer(serializers.ModelSerializer):
    locations = LocationSerializer(many=True)

    class Meta:
        model = Review
        fields = ['title', 'text', 'posted_at', 'user', 'location']

class CommentSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Comment
        fields = ['text', 'posted_at', 'user', 'review']
    