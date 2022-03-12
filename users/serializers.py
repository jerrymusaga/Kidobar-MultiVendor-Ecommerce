from rest_framework import serializers 
from .models import User 
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User 
        fields = ['id','first_name','last_name','is_staff','is_active']

    

class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User 
        fields = ['id','email','first_name','last_name','is_staff','is_active','token']

    def get_token(self,obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)