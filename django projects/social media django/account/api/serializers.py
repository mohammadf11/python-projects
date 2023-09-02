from rest_framework import serializers
from django.contrib.auth import get_user_model
from ..models import Profile
User = get_user_model()

# class UserSerializer(serializers.ModelSerializer):
#     password2 = serializers.CharField(write_only=True)
#     class Meta:
#         model = User
#         fields = ('phone_number' , 'email' , 'password' , 'password2')

#     def create(self, validated_data):
#         del validated_data['password2']
#         return User.objects.create_user(**validated_data)

#     def validate(self, data):
#             if data['password'] != data['password2']:
#                 raise serializers.ValidationError('password not match')
#             return data


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

    

    def get_fields(self):
        request = self.context.get('request')
        view = self.context.get('view')
        fields = super().get_fields()
        if request and view:
            if not request.user.is_staff  and  view.action in ['update' , 'partial_update']:
                fields.pop('user')
        else:
            fields.pop('user')
        return fields
        
