from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework import  status
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone

@api_view(['POST'])
def register(requisicao):
    serializer = RegisterSerializer(data=requisicao.data)
    if serializer.is_valid():
        
        serializer.save()
        return Response(
            {
                "message": "User created successfully",
                "user": serializer.data
            },
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    
    try:
        refresh_token = request.data.get('refresh')
        token = RefreshToken(refresh_token)
        token.blacklist()
        request.user.last_login = timezone.now()
        request.user.save()
        return Response(
            {
                "message": "User logged out successfully"
            },
            status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response(
            {
                "error": str(e)
            },
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def perfil(request):
    
    try:
        user = request.user
        return Response(
        {
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "date_joined": user.date_joined,
            "last_login": user.last_login
        },status=status.HTTP_200_OK
        )
        
    except Exception as e:
        return Response(
            {
                "error": str(e)
            },
            status=status.HTTP_400_BAD_REQUEST
        )