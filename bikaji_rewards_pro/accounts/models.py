from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class Role(models.TextChoices):
        CUSTOMER = "CUSTOMER", "Customer"
        ADMINISTRATOR = "ADMINISTRATOR", "Administrator"
        SYSTEM = "SYSTEM", "System"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CUSTOMER,
    )

    # Avoid reverse-accessor clashes with Django's default User model.
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="accounts_users",
        blank=True,
        help_text="Groups this user belongs to.",
        verbose_name="groups",
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="accounts_users",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    @property
    def is_customer(self):
        return self.role == self.Role.CUSTOMER

    @property
    def is_admin(self):
        return self.role == self.Role.ADMINISTRATOR

    @property
    def is_system(self):
        return self.role == self.Role.SYSTEM

    def __str__(self):
        return f"{self.username} ({self.role})"
