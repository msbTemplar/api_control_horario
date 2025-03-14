from django.shortcuts import render
from rest_framework import generics,status,viewsets
from rest_framework.response import Response
from .models import RegistroHorario
from .serializers import RegistroHorarioSerializer
from rest_framework.views import APIView
from django.utils.dateparse import parse_time
from rest_framework.decorators import action
from rest_framework import viewsets
from django.utils.timezone import now
from rest_framework.permissions import IsAuthenticated
from django.db import models
from rest_framework.permissions import AllowAny
# Create your views here.

from django.db.models import Sum
from rest_framework.decorators import api_view

from .serializers import UserRegisterSerializer
from django.contrib.auth.models import User

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser

class UserRegisterViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]  # Permite el registro sin autenticación

@api_view(['GET'])
def resumen_horas(request):
    usuario = request.user
    total_horas = RegistroHorario.objects.filter(usuario=usuario).aggregate(
        total=Sum(models.F('salida') - models.F('entrada'))
    )
    return Response({"horas_trabajadas": total_horas["total"]})


class RegistroHorarioViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    serializer_class = RegistroHorarioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filtra por el usuario autenticado
        return RegistroHorario.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    @action(detail=True, methods=['post'])
    def marcar_entrada(self, request, pk=None):
        registro = self.get_object()
        hora_entrada = request.data.get("entrada")
        
        if not hora_entrada:
            return Response({"error": "Debes proporcionar la hora de entrada."}, status=status.HTTP_400_BAD_REQUEST)

        hora_entrada = parse_time(hora_entrada)
        if not hora_entrada:
            return Response({"error": "Formato inválido. Usa HH:MM."}, status=status.HTTP_400_BAD_REQUEST)

        registro.entrada = hora_entrada
        registro.save()

        serializer = RegistroHorarioSerializer(registro)
        return Response({
            "message": "Entrada registrada correctamente.",
            "registro": serializer.data
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def marcar_salida(self, request, pk=None):
        registro = self.get_object()
        hora_salida = request.data.get("salida")
        
        if not registro.entrada:
            return Response({"error": "Primero debes registrar la entrada."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not hora_salida:
            return Response({"error": "Debes proporcionar la hora de salida."}, status=status.HTTP_400_BAD_REQUEST)
        
        hora_salida = parse_time(hora_salida)
        if not hora_salida:
            return Response({"error": "Formato inválido. Usa HH:MM."}, status=status.HTTP_400_BAD_REQUEST)
        
        registro.salida = hora_salida
        registro.save()

        serializer = RegistroHorarioSerializer(registro)
        return Response({
            "message": "Salida registrada correctamente.",
            "registro": serializer.data
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def iniciar_pausa(self, request, pk=None):
        registro = self.get_object()
        hora_pausa_inicio = request.data.get("pausa_inicio")
        
        if not registro.entrada:
            return Response({"error": "Primero debes registrar la entrada."}, status=status.HTTP_400_BAD_REQUEST)

        if not hora_pausa_inicio:
            return Response({"error": "Debes proporcionar la hora de inicio de pausa."}, status=status.HTTP_400_BAD_REQUEST)
        
        hora_pausa_inicio = parse_time(hora_pausa_inicio)
        if not hora_pausa_inicio:
            return Response({"error": "Formato inválido. Usa HH:MM."}, status=status.HTTP_400_BAD_REQUEST)

        registro.pausa_inicio = hora_pausa_inicio
        registro.save()

        serializer = RegistroHorarioSerializer(registro)
        return Response({
            "message": "Inicio de pausa registrado correctamente.",
            "registro": serializer.data
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def finalizar_pausa(self, request, pk=None):
        registro = self.get_object()
        hora_pausa_fin = request.data.get("pausa_fin")
        
        if not registro.pausa_inicio:
            return Response({"error": "Primero debes iniciar la pausa."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not hora_pausa_fin:
            return Response({"error": "Debes proporcionar la hora de fin de pausa."}, status=status.HTTP_400_BAD_REQUEST)
        
        hora_pausa_fin = parse_time(hora_pausa_fin)
        if not hora_pausa_fin:
            return Response({"error": "Formato inválido. Usa HH:MM."}, status=status.HTTP_400_BAD_REQUEST)

        registro.pausa_fin = hora_pausa_fin
        registro.save()

        serializer = RegistroHorarioSerializer(registro)
        return Response({
            "message": "Fin de pausa registrado correctamente.",
            "registro": serializer.data
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='consultar-usuario')
    def consultar_usuario(self, request):
        """
        Devuelve los registros horarios del usuario autenticado.
        """
        registros = self.get_queryset()
        serializer = self.get_serializer(registros, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Nuevo endpoint para administradores
    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser], url_path='consultar-todos')
    def consultar_todos(self, request):
        """
        Permite al administrador consultar los registros horarios de todos los usuarios.
        """
        registros = RegistroHorario.objects.all()
        serializer = self.get_serializer(registros, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




class RegistroHorarioViewSetOLD2(viewsets.ModelViewSet):
    #queryset = RegistroHorario.objects.all()
    serializer_class = RegistroHorarioSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Filtra por el usuario autenticado
        return RegistroHorario.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    @action(detail=True, methods=['post'])
    def marcar_entrada(self, request, pk=None):
        registro = self.get_object()
        hora_entrada = request.data.get("entrada")
        
        if not hora_entrada:
            return Response({"error": "Debes proporcionar la hora de entrada"}, status=status.HTTP_400_BAD_REQUEST)

        hora_entrada = parse_time(hora_entrada)
        if not hora_entrada:
            return Response({"error": "Formato de hora inválido. Usa HH:MM."}, status=status.HTTP_400_BAD_REQUEST)

        registro.entrada = hora_entrada
        registro.save()
        return Response({"message": "Entrada registrada correctamente"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def marcar_salida(self, request, pk=None):
        registro = self.get_object()
        hora_salida = request.data.get("salida")
        
        if not registro.entrada:
            return Response({"error": "Primero debes registrar la entrada."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not hora_salida:
            return Response({"error": "Debes proporcionar la hora de salida"}, status=status.HTTP_400_BAD_REQUEST)
        
        hora_salida = parse_time(hora_salida)
        if not hora_salida:
            return Response({"error": "Formato de hora inválido. Usa HH:MM."}, status=status.HTTP_400_BAD_REQUEST)
        
        registro.salida = hora_salida
        registro.save()
        return Response({"message": "Salida registrada correctamente"}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def iniciar_pausa(self, request, pk=None):
        registro = self.get_object()
        hora_pausa_inicio = request.data.get("pausa_inicio")
        
        if not registro.entrada:
            return Response({"error": "Primero debes registrar la entrada."}, status=status.HTTP_400_BAD_REQUEST)

        if not hora_pausa_inicio:
            return Response({"error": "Debes proporcionar la hora de inicio de pausa"}, status=status.HTTP_400_BAD_REQUEST)
        
        hora_pausa_inicio = parse_time(hora_pausa_inicio)
        if not hora_pausa_inicio:
            return Response({"error": "Formato inválido. Usa HH:MM."}, status=status.HTTP_400_BAD_REQUEST)

        registro.pausa_inicio = hora_pausa_inicio
        registro.save()
        return Response({"message": "Inicio de pausa registrado correctamente"}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def finalizar_pausa(self, request, pk=None):
        registro = self.get_object()
        hora_pausa_fin = request.data.get("pausa_fin")
        
        if not registro.pausa_inicio:
            return Response({"error": "Primero debes iniciar la pausa."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not hora_pausa_fin:
            return Response({"error": "Debes proporcionar la hora de fin de pausa"}, status=status.HTTP_400_BAD_REQUEST)
        
        hora_pausa_fin = parse_time(hora_pausa_fin)
        if not hora_pausa_fin:
            return Response({"error": "Formato inválido. Usa HH:MM."}, status=status.HTTP_400_BAD_REQUEST)
        
        registro.pausa_fin = hora_pausa_fin
        registro.save()
        return Response({"message": "Fin de pausa registrado correctamente"}, status=status.HTTP_200_OK)
    
    

class RegistroHorarioViewSetOLD(viewsets.ModelViewSet):
    queryset = RegistroHorario.objects.all()
    serializer_class = RegistroHorarioSerializer
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden acceder
    
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)  # Guarda el usuario actual
    
    @action(detail=True, methods=['post'])
    def marcar_entrada(self, request, pk=None):
        registro = self.get_object()
        if registro.entrada:
            return Response({"error": "Entrada ya registrada"}, status=status.HTTP_400_BAD_REQUEST)
        registro.entrada = now().time()
        registro.save()
        return Response({"message": "Entrada registrada"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def marcar_salida(self, request, pk=None):
        registro = self.get_object()
        if not registro.entrada:
            return Response({"error": "No puedes marcar salida sin haber registrado entrada."}, status=status.HTTP_400_BAD_REQUEST)
        if registro.salida:
            return Response({"error": "Salida ya registrada"}, status=status.HTTP_400_BAD_REQUEST)
        registro.salida = now().time()
        registro.save()
        return Response({"message": "Salida registrada"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def iniciar_pausa(self, request, pk=None):
        registro = self.get_object()
        if not registro.entrada:
            return Response({"error": "No puedes iniciar una pausa sin haber registrado entrada."}, status=status.HTTP_400_BAD_REQUEST)
        if registro.pausa_inicio:
            return Response({"error": "Pausa ya iniciada"}, status=status.HTTP_400_BAD_REQUEST)
        registro.pausa_inicio = now().time()
        registro.save()
        return Response({"message": "Inicio de pausa registrado"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def finalizar_pausa(self, request, pk=None):
        registro = self.get_object()
        if not registro.pausa_inicio:
            return Response({"error": "No puedes finalizar una pausa sin haberla iniciado."}, status=status.HTTP_400_BAD_REQUEST)
        if registro.pausa_fin:
            return Response({"error": "Pausa ya finalizada"}, status=status.HTTP_400_BAD_REQUEST)
        registro.pausa_fin = now().time()
        registro.save()
        return Response({"message": "Fin de pausa registrado"}, status=status.HTTP_200_OK)

class RegistroHorarioListCreate(generics.ListCreateAPIView):
    queryset = RegistroHorario.objects.all()
    serializer_class = RegistroHorarioSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return RegistroHorario.objects.filter(usuario=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        RegistroHorario.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


class  RegistroHorarioList(APIView):
    def get(self, request, format=None):
        usuario = request.query_params.get("usuario","")
        
        if usuario:
            registro_horarios = RegistroHorario.objects.filter(usuario__icontains=usuario)
        else:
            registro_horarios = RegistroHorario.objects.all()
        
        serializer = RegistroHorarioSerializer(registro_horarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    

class RegistroHorarioRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = RegistroHorario.objects.all()
    serializer_class = RegistroHorarioSerializer
    lookup_field = "pk"
    
    
    
    
