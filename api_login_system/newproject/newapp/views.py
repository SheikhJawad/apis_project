from rest_framework import generics, permissions
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.response import Response
from .models import Token

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer



class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            token, created = Token.objects.get_or_create(user=user)
            token.key = access_token
            token.save()

            return Response({
                'token': access_token,
                'hashed_password': user.password  
            })
        return Response({'error': 'Invalid Credentials'}, status=400)

