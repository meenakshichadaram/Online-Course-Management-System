from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login, logout
from .models import User
from .serializers import RegisterSerializer, UserSerializer


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access':  str(refresh.access_token),
    }


class RegisterView(generics.CreateAPIView):
    queryset         = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # also login the session
        login(request, user)
        tokens = get_tokens_for_user(user)
        return Response({
            'access':    tokens['access'],
            'refresh':   tokens['refresh'],
            'role':      user.role,
            'full_name': user.full_name,
            'email':     user.email,
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        email    = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response(
                {'detail': 'Email and password are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(request, email=email, password=password)

        if user is None:
            return Response(
                {'detail': 'Invalid email or password.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.is_active:
            return Response(
                {'detail': 'Your account is inactive.'},
                status=status.HTTP_403_FORBIDDEN
            )

        # login Django session too
        login(request, user)

        tokens = get_tokens_for_user(user)
        return Response({
            'access':    tokens['access'],
            'refresh':   tokens['refresh'],
            'role':      user.role,
            'full_name': user.full_name,
            'email':     user.email,
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            # also logout Django session
            logout(request)
            return Response(
                {'detail': 'Logged out successfully.'},
                status=status.HTTP_200_OK
            )
        except Exception:
            logout(request)
            return Response(
                {'detail': 'Logged out.'},
                status=status.HTTP_200_OK
            )


class ProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class   = UserSerializer

    def get_object(self):
        return self.request.user