from rest_framework import serializers
from ..models import Todo
from django.contrib.auth import get_user_model

User = get_user_model()


class AdminTodoserializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'


class UserTodoserializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        exclude = ('user', )



class UserRegisterserializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('username' , 'password' , 'password2')
    

    def create(self, validated_data):
        del validated_data['password2']
        return User.objects.create_user(**validated_data)

    def validate(self, data):
            if data['password'] != data['password2']:
                raise serializers.ValidationError('password not match')
            return data

