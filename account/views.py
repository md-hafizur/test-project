from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from account.models import User, Session
from account.serializers import LoginSerializer
from django.contrib.auth import get_user_model
from .serializers import (
    UserRegistrationSerializer,
    UserSerializer,
    UserUpdateSerializer,
)

User = get_user_model()

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': UserSerializer(user).data,
        }, status=status.HTTP_201_CREATED)
    


class login(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        email = request.data.get("email")
        if serializer.is_valid():
            user = User.objects.filter(
                email=email
            ).first()
            if not user:
                return Response(
                    {"errors": {"user": ["User not found"]}},
                    status=status.HTTP_404_NOT_FOUND,
                )
            if not user.check_password(serializer.validated_data["password"]):
                return Response(
                    {"errors": {"password": ["Invalid credentials"]}},
                    status=status.HTTP_401_UNAUTHORIZED,
                )



            session = Session.objects.filter(user=user).first()

            if session:
                session.remember = serializer.validated_data.get("remember", False)
                session.user_agent = request.META.get("HTTP_USER_AGENT")
                session.ip = request.META.get("REMOTE_ADDR")
                session.update_access_token() # This will also update refresh_token and their expiry
                session.save()
            else:
                session = Session.objects.create(
                    user=user,
                    remember=serializer.validated_data.get("remember", False),
                    user_agent=request.META.get("HTTP_USER_AGENT"),
                    ip=request.META.get("REMOTE_ADDR")
                )

            response = {
                "user": UserSerializer(user, context={"request": request}).data,
                "session": {
                    "access_token": session.access_token,
                    "refresh_token": session.refresh_token,
                }
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserSerializer

    def get_object(self):
        return self.request.user if self.kwargs.get('pk') == 'me' else super().get_object()

    def update(self, request, *args, **kwargs):
        partial = True  # 👈 Force partial update for both PUT and PATCH
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
