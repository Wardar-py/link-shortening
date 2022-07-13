from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import update_last_login
from drf_yasg2.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from auth_user.serializers import LoginSerializer, SendTokenSerializer, TokenRefreshCustomSerializer, \
    RefreshResponseSwaggerSerializer, RegisterSerializer

User = get_user_model()


class LoginView(APIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_description='Sign In',
        request_body=LoginSerializer,
        responses={200: SendTokenSerializer()},
        security=[],
    )
    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = None
            if User.objects.filter(username=serializer.validated_data['email']).exists():
                user = authenticate(
                    username=serializer.validated_data['email'],
                    password=serializer.validated_data['password']
                )

            if user is not None and user.is_active:
                # To update last login of user
                update_last_login(None, user)
                # Get user token, include refresh and access token
                token = RefreshToken.for_user(user)

                access = token.access_token
                status = {
                    'refresh': str(token),
                    'refresh_exp': token.get('exp'),
                    'access': str(access),
                    'access_exp': access.get('exp'),
                }

                return Response(status, status=200)
            else:
                status_error = {
                    "detail": "Ошибка аутентификации",
                }
                return Response(status_error, status=403)
        else:
            status_error = {
                "detail": "Ошибка валидации",
            }
            status_error.update(serializer.errors)
            return Response(status_error, status=422)


class TokenRefreshViewCustom(TokenRefreshView):
    serializer_class = TokenRefreshCustomSerializer

    @swagger_auto_schema(
        operation_description='Takes a refresh type JSON web token and returns access and refresh'
                              ' types JSON web token if the refresh token is valid.',
        responses={200: RefreshResponseSwaggerSerializer()},
        security=[],
    )
    def post(self, request, *args, **kwargs):
        return super(TokenRefreshView, self).post(request, *args, **kwargs)


class RegisterView(APIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_description='Register',
        request_body=RegisterSerializer,
        responses={201: ""},
        security=[],
    )
    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            if not User.objects.filter(email=email).exists():
                user = User.objects.create_user(username=email, email=email, password=password)
                user.first_name = serializer.validated_data['first_name']
                user.last_name = serializer.validated_data['last_name']

                user.is_active = False
                user.save()

                return Response(
                    {"msg": "Вы зареганы"},
                    status=201
                )
            else:
                status_error = {
                    "detail": "Пользователь уже существует",
                }
                return Response(status_error, status=400)
        else:
            status_error = {
                "detail": "Ошибка валидации",
            }
            status_error.update(serializer.errors)
            return Response(status_error, status=422)
