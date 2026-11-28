
from rest_framework import serializers

from .models import User


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={"input_type": "password"},
    )

    role = serializers.ChoiceField(
        choices=User.Role.choices,
        required=False,
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "role",
        ]
        read_only_fields = ["id"]

    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError(
                "A user with this username already exists."
            )
        return value

    def validate_email(self, value):
        if value and User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                "A user with this email already exists."
            )
        return value

    def validate_role(self, value):
        request = self.context.get("request")
        requester = request.user if request and request.user.is_authenticated else None

        # Public users and customers cannot assign privileged roles.
        if requester is None or not requester.is_admin:
            if value != User.Role.CUSTOMER:
                raise serializers.ValidationError(
                    "You are not allowed to create this role."
                )

        # SYSTEM identities cannot be created through this API.
        if value == User.Role.SYSTEM:
            raise serializers.ValidationError(
                "System users cannot be created through this API."
            )

        return value

    def create(self, validated_data):
        # Safe default: CUSTOMER.
        role = validated_data.pop("role", User.Role.CUSTOMER)

        return User.objects.create_user(
            role=role,
            **validated_data,
        )
