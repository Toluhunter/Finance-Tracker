from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import status


from .serializers import AccountSerializer, LoginSerializer, ChangePasswordSerializer


class RegisterView(generics.CreateAPIView):
    '''
    RegisterView handles POST request to register new users with provided details
    Makes use of AccountSerilizer
    '''

    serializer_class = AccountSerializer


class AccountView(generics.RetrieveUpdateAPIView):
    '''
    AccountView handles GET and PATCH requests to retrieve and update user details respectively
    It requires Authentication and makes use of AccountSerializer to retrieve and update account details
    '''

    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # returns authenticated user object
        return self.request.user


class LoginView(generics.GenericAPIView):
    '''
    LoginView Handles POST request to validate credentials, returning token on success
    It Requires Authentication and makes use of LoginSerializer to serialize and validate credentials
    '''

    serializer_class = LoginSerializer

    def post(self, request):
        # post method verifies credentials and returns user token if valid

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        response = {
            "token": str(token)
        }

        return Response(response, status=status.HTTP_200_OK)

class ChangePasswordView(generics.GenericAPIView):
    '''
    ChangePasswordView handles PUT requests to change the password for the currently authenticated user.
    It requires authentication and uses the ChangePasswordSerializer class to validate the new password entered by the user.
    '''
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def put(self, request):
        # put method sets the new password for the user and deletes their authentication token from the database.

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        user.set_password(serializer.validated_data["new_password"])
        user.save()

        token, _ = Token.objects.get_or_create(user=user)
        token.delete()

        return Response({"message": "Password Updated"}, status=status.HTTP_200_OK)