from django.contrib.auth.models import User
from rest_framework import serializers

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,min_length=8)

    class Meta:
        model = User
        fields = ["username","email","password"]
    
    def validate_username(self,value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exits.")
        return value
    
    def validate_email(self,value):
        if value and User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value
    
    def create(self, validate_data):
        user = User.objects.create_user(
            username=validate_data["username"],
            email=validate_data.get("email",""),
            password=validate_data["password"]
        )
        return user