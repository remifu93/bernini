from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User
from .serializers import UserSerializer, TokenObtainSerializer


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create(
            email=request.data['email'],
            first_name=request.data['first_name'],
            last_name=request.data['last_name'],
            birth_date=request.data['birth_date'],
            phone=request.data['phone'],
            id_number=request.data['id_number']
        )
        user.set_password(request.data['password'])
        user.save()
        return Response(UserSerializer(user).data)


class TokenObtainView(TokenObtainPairView):
    serializer_class = TokenObtainSerializer