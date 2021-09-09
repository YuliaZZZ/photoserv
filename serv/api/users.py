from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework import mixins, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from serv.serializers.users import CreateUserSerializer, LoginUserSerializer


class CreateUserView(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    model = User
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny,)
    parser_classes = (JSONParser,)

    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        context = self.get_serializer_context()
        user = CreateUserSerializer(data=request.data, context=context)
        if user.is_valid(raise_exception=True):
            new_user = User.objects.create_user(
                username=user.initial_data["username"],
                password=user.initial_data["password"]
            )
            Token.objects.create(user=new_user)
            login(request, new_user)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class LoginUserView(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    model = User
    serializer_class = LoginUserSerializer
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser,)

    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        user = authenticate(
            request, username=request.data["username"],
            password=request.data["password"]
        )
        if user:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
