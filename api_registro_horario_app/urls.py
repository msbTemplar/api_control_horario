from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegistroHorarioViewSet, RegistroHorarioListCreate, RegistroHorarioRetrieveUpdateDestroy, resumen_horas, UserRegisterViewSet

# Usa un router para manejar automáticamente las rutas del ViewSet
router = DefaultRouter()
router.register(r'registrohorario', RegistroHorarioViewSet, basename='registro-horario')
router.register(r'register', UserRegisterViewSet, basename='register')  # Registro de usuarios



urlpatterns = [
    path('', include(router.urls)),  # Rutas automáticas del ViewSet
    path('registrohorario/listar/', RegistroHorarioListCreate.as_view(), name="registrohorario-list-create"),
    path('registrohorario/<int:pk>/', RegistroHorarioRetrieveUpdateDestroy.as_view(), name="registrohorario-detail"),
    
    # Agregamos las rutas personalizadas
    path('registrohorario/<int:pk>/marcar_entrada/', RegistroHorarioViewSet.as_view({'post': 'marcar_entrada'}), name='marcar-entrada'),
    path('registrohorario/<int:pk>/iniciar_pausa/', RegistroHorarioViewSet.as_view({'post': 'iniciar_pausa'}), name='iniciar-pausa'),
    path('registrohorario/<int:pk>/finalizar_pausa/', RegistroHorarioViewSet.as_view({'post': 'finalizar_pausa'}), name='finalizar-pausa'),
    path('registrohorario/<int:pk>/marcar_salida/', RegistroHorarioViewSet.as_view({'post': 'marcar_salida'}), name='marcar-salida'),
    
    path('resumen-horas/', resumen_horas, name="resumen-horas"),
    path('api-auth/', include('rest_framework.urls')), 
]
