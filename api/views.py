from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer , ChangePasswordSerializer, UpdateProfileSerializer
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

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def ChangePasswordView(request):
    
    try:
       serializer = ChangePasswordSerializer(data=request.data)
       
       if serializer.is_valid():
           user = request.user
           old_password = serializer.validated_data.get('old_password')
           new_password = serializer.validated_data.get('new_password')
           
           if not user.check_password(old_password):
               return Response(
                   {
                       "error": "old password is incorrect"
                   }, status=status.HTTP_400_BAD_REQUEST
               )
           user.set_password(new_password)
           user.save()
           return Response(
               {
                   "message": "Password changed successfully"
               }, status=status.HTTP_200_OK
           )
       else:
           return Response(
               {
                   "error": serializer.errors
               }, 
               status=status.HTTP_400_BAD_REQUEST
           )
               
    except Exception as e:
        return Response(
            {
                "error": str(e)
            },
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def UpdateProfileView(request):
    try:
        serializer = UpdateProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
            {
                "message": "Profile updated successfully",
                "user": serializer.data
            }, status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {
                "error": str(e)
            },
            status=status.HTTP_400_BAD_REQUEST
        )

from django.core.mail import send_mail

@api_view(['GET'])
def test_email(request):

    send_mail(
        'Test Email',
        'Se você recebeu isso, SMTP está funcionando',
        'benilsonbenito12@gmail.com',
        ['teuemail@gmail.com'],
        fail_silently=False,
    )

    return Response({"message": "Email sent"})