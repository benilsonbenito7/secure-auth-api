from .models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

class RegisterSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
    
    def validate(self, dicionary):
        if dicionary['password'] != dicionary['password2']:
            raise serializers.Validationerror("The password not match")
        return dicionary
    
    def create(self, v_dicionary):
        v_dicionary.pop('password2')
        
        user = User.objects.create_user(
            username=v_dicionary['username'],
            email=v_dicionary['email'],
            password=v_dicionary['password']
        )
        
        v_dicionary.pop('password')
        
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True)
    
    def validate(self, data):
        if data['old_password'] == data['new_password']:
                raise serializers.ValidationError("The new password must be different from the old password.")
        return data
class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
     