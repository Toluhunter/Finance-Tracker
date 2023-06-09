from uuid import uuid4

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()


class Track(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4)

    categories = [
        ("unsorted", "Unsorted"),
        ("education", "Education"),
        ("food", "Food"),
        ("wallet", "Wallet")
    ]

    category = models.CharField(
        choices=categories,
        default="unsorted",
        null=False,
        blank=False,
        max_length=10
    )
    amount = models.FloatField(
        validators=[MinValueValidator(-100000000),
                    MaxValueValidator(100000000)],
        null=False,
        blank=False
    )
    date = models.DateField(
        auto_now_add=True,
        null=False
    )

    user = models.ForeignKey(
        to=User,
        blank=False,
        null=False,
        related_name="transactions",
        on_delete=models.CASCADE
    )

    def save(self, *args, **kwargs):
        self.full_clean()

        return super().save(*args, **kwargs)
