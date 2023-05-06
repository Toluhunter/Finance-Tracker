from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers

from .models import Track


class TrackSerializer(serializers.ModelSerializer):
    
    '''
    TrackSerializer serializes Track objects and includes the id, category, amount, and date fields.
    It also sets the user field to the authenticated user and makes the id field read-only.
    '''
    class Meta:
        model = Track
        fields = [
            "id",
            "category",
            "amount",
            "date",
        ]
        read_only_fields = ["id"]

    def validate(self, attrs):
        attrs["user"] = self.context["request"].user

        return attrs


class CreateTransactionSerializer(serializers.ModelSerializer):
    '''
    CreateTransactionSerializer serializes Track objects for creating new transactions.
    It includes the category and amount fields, sets the user field to the authenticated user,
    and validates the category choice field using the available categories in Track model.
    '''

    category = serializers.ChoiceField(
        choices=Track.categories,
    )

    class Meta:
        model = Track
        fields = [
            "category",
            "amount",
        ]

    def validate(self, attrs):
        attrs["user"] = self.context["request"].user

        return attrs
