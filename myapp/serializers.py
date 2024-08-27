from rest_framework import serializers
from .models import Milan, Responsibility, User, Address, Reports, CommonUser

from django.core.mail import send_mail
from django.conf import settings
import secrets
import string


class RoleCountSerializer(serializers.Serializer):
    role_name = serializers.CharField()
    count = serializers.IntegerField()

class ViewProfileSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    email = serializers.EmailField()
    contact= serializers.CharField()
    milan = serializers.CharField(source='milan.milan_name')
    role = serializers.CharField(source='role.role_name')

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'contact', 'milan', 'role']
    # id = serializers.IntegerField()
    # name = serializers.CharField()
    # email = serializers.EmailField()
    # contact= serializers.CharField()
    # milan = serializers.CharField()
    # role = serializers.CharField()




class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'contact', 'milan', 'role']

    def create(self, validated_data):
        # Define the alphabet for password generation
        alphabet = string.ascii_letters + string.digits
        
        # Generate a random password
        password = ''.join(secrets.choice(alphabet) for _ in range(8))
        
        # Create the user with the generated password
        user = User.objects.create(
            **validated_data,
            password=password  # Store the plain password (you should hash it before storing in production)
        )
        
        # Send an email to the user with their password
        self.send_password_email(user.email, password)
        
        return user

    def send_password_email(self, email, password):
        subject = 'Your New Account Password'
        message = f'Your account has been created successfully. Your password is: {password}'
        from_email = settings.DEFAULT_FROM_EMAIL
        send_mail(subject, message, from_email, [email])


class MembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','name', 'email', 'contact']

class CommonUserMembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommonUser
        fields = ['id', 'name', 'contact']

class MilanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Milan
        fields = '__all__'

class ResponsibilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsibility
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class ReportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reports
        fields = '__all__'

class CommonUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommonUser
        fields = '__all__'
