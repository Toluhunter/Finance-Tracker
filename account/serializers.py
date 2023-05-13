
from django.conf import settings

from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

User = get_user_model()


class AccountSerializer(serializers.ModelSerializer):
    '''
    AccountSerilizer Serializes the data for the authenticated user and handles creation of users and updating of user details
    It includes the id, username, email, first_name, last_name and password
    Sets id to read only and password to write only
    '''
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password"
        ]

    def __init__(self, instance=None, **kwargs):
        super().__init__(instance, **kwargs)

        self.fields["password"].write_only = True

    def create(self, validated_data):
        '''
        Creates new user
        '''
        return self.Meta.model.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        '''
        Update user details, users can only update email, first_name and last_name
        '''
        instance.email = validated_data.get("email", instance.email)
        instance.first_name = validated_data.get(
            "first_name", instance.first_name)
        instance.last_name = validated_data.get(
            "last_name", instance.last_name)
        instance.username = validated_data.get("username", instance.username)

        instance.save()

        return instance


class LoginSerializer(serializers.Serializer):
    '''
    LoginSerilizer Handles user credential validation
    '''

    username = serializers.CharField(max_length=60, required=True)
    password = serializers.CharField(max_length=60, required=True)

    def validate(self, attrs):
        '''
        Verifies Username and Password
        '''
        user = authenticate(
            username=attrs["username"], password=attrs["password"])

        if not user:
            raise serializers.ValidationError("invalid Credentials")

        attrs["user"] = user

        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    '''
    ChangePasswordSerilizer Handles changing of users password
    '''

    old_password = serializers.CharField(required=True, max_length=100)
    new_password = serializers.CharField(required=True, max_length=100)

    def validate(self, attrs):
        '''
        Validates old password
        '''
        user = self.context["request"].user
        if not user.check_password(attrs["old_password"]):
            # validates old password
            raise serializers.ValidationError("Wrong Password")

        if attrs["new_password"] == attrs["old_password"]:
            # verifies new password is different from old password
            raise serializers.ValidationError(
                "Old and New Password cannot be the same")

        return attrs
