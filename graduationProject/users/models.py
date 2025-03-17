from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    full_name = models.CharField(max_length=150, blank=True, null=True)
    first_name = None
    last_name = None
    age = models.IntegerField(null=True, blank=True)
    skin_problem = models.CharField(max_length=150, null=True, blank=True)
    skin_type = models.CharField(max_length=150, null=True, blank=True)
    password_reset_code = models.CharField(max_length=6, blank=True, null=True)
    reset_code_created_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"""{self.full_name} - {self.username} -
                {self.skin_problem} - {self.skin_type}"""
