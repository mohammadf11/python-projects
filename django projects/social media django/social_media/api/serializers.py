from rest_framework import serializers
from ..models import Post , Like , Follow


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        
    def get_fields(self):
        request = self.context.get('request')
        view = self.context.get('view')
        fields = super().get_fields()
        if request and view:
            if not request.user.is_staff  and not view.action in ['list' , 'retrieve']:
                fields.pop('user')
        else:
            fields.pop('user')
        return fields
        


class Likeserializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

    def get_fields(self):
        request = self.context.get('request')
        view = self.context.get('view')
        fields = super().get_fields()
        if request and view:
            if not request.user.is_staff  and  view.action == 'create':
                fields.pop('user')
        else:
            fields.pop('user')
        return fields
    
            



class Followserializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'

    def get_fields(self):
        request = self.context.get('request')
        view = self.context.get('view')
        fields = super().get_fields()
        if request and view:
            if not request.user.is_staff  and   view.action == 'create':
                fields.pop('follower')
        else:
            fields.pop('follower')
        return fields
    