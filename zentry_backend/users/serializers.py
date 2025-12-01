from rest_framework import serializers
from .models import User

class RegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'dni', 'password', 'card_number']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'], # Usamos email como username
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            dni=validated_data['dni'],
            card_number=validated_data.get('card_number', '')
        )
        return user
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'dni', 'card_number']
        # Bloqueamos el DNI para que no lo puedan editar, ya que el arbol BST depende de el DNI
        read_only_fields = ['dni']