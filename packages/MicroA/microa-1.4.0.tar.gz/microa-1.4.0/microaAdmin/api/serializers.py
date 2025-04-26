from rest_framework import serializers
from microaAdmin.models import *
from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField

from django.contrib.auth import get_user_model
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'phone_number', 'birth_date']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Bu email artıq istifadə olunub.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data.get("username"),
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            email=validated_data.get("email"),
            password=validated_data.get("password"),
        )

        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)
        
        instance.save()

        return instance
    
class UserSerializerGET(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        depth = 1

class PageSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Page)

    class Meta:
        model = Page
        fields = '__all__'
        depth = 1 

class SubpageSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Subpage)

    class Meta:
        model = Subpage
        fields = '__all__'
        depth = 1