from django.urls import path
from .views import register, logout, perfil
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', TokenObtainPairView.as_view()),
    path('logout/', logout),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('perfil/', perfil, name='perfil')
]