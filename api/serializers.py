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
            uswrname=v_dicionary['username'],
            email=v_dicionary['email'],
            password=v_dicionary['password']
        )
        
        v_dicionary.pop('password')
        
        return user
