from rest_framework import serializers
from .models import (
    Coats, Shirts, Pants, Tshirt,
    Watches, Perfumes, Shoes,
    Sandals, Cart
)
from django.contrib.auth.models import User
from .models import UserProfile


class CoatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coats
        fields = "__all__"


class ShirtsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shirts
        fields = "__all__"


class PantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pants
        fields = "__all__"


class TshirtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tshirt
        fields = "__all__"


class WatchesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watches
        fields = "__all__"


class PerfumesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfumes
        fields = "__all__"


class ShoesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shoes
        fields = "__all__"


class SandalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sandals
        fields = "__all__"


class CartSerializer(serializers.ModelSerializer):
    total_price = serializers.ReadOnlyField()
    class Meta:
        model = Cart
        fields = "__all__"

class RegisterSerializer(serializers.Serializer):

    full_name = serializers.CharField()
    username = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.CharField()
    password = serializers.CharField()

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )

        UserProfile.objects.create(
            user=user,
            full_name=validated_data["full_name"],
            phone=validated_data["phone"]
        )

        return user