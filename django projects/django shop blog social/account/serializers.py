from rest_framework import serializers
from .models import User , Profile
from social_media.models import Follow

class UserRegisterSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)
    email = serializers.EmailField(required=True )
    password1 = serializers.CharField(style={'input_type': 'password'})
    password2 = serializers.CharField(style={'input_type': 'password'})

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("password not same")
        return data

class UserVerifycodeSerializer(serializers.Serializer):
    code = serializers.IntegerField()

class UserInformationsSerializer(serializers.ModelSerializer): 
    # profile = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = '__all__'

    # def get_profile(self , obj):
    #     return ProfileSerializer(instance=obj.profile).data


        
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ('user',)

# class FollowSerializer(serializers.Serializer):
#     follower = serializers.IntegerField()
#     following = serializers.IntegerField()