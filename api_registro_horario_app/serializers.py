from rest_framework import serializers
from .models import RegistroHorario

# class RegistroHorarioSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = RegistroHorario
#         fields = ["id","usuario","fecha","entrada","salida","pausa_inicio","pausa_fin","created_at"]
        

from django.contrib.auth.models import User

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', '')
        )
        return user




class RegistroHorarioSerializer(serializers.ModelSerializer):
    usuario = serializers.StringRelatedField()  # Muestra el username en vez del ID

    class Meta:
        model = RegistroHorario
        fields = ["id", "usuario", "fecha", "entrada", "salida", "pausa_inicio", "pausa_fin", "created_at"]
