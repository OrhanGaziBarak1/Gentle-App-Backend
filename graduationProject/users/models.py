from django.db import models
from django.contrib.auth.models import AbstractUser

class SkinProblem(models.Model):

    SKIN_PROBLEMS = [
        ('problem_1','Cilt Problemi 1'),
        ('problem_2','Cilt Problemi 2'),
        ('problem_3','Cilt Problemi 3'),
        ('problem_4','Cilt Problemi 4'),
    ]

    skin_problem_name = models.CharField(max_length=50,
                                         choices=SKIN_PROBLEMS,
                                         null=True,
                                         blank=True)

    def __str__(self):
        return self.skin_problem_name

class SkinType(models.Model):

    SKIN_TYPES = [
        ('type_1','Cilt Tipi 1'),
        ('type_2','Cilt Tipi 2'),
        ('type_3','Cilt Tipi 3'),
        ('type_4','Cilt Tipi 4'),
    ]

    skin_type_name = models.CharField(max_length=50,
                                      choices=SKIN_TYPES,
                                      null=True,
                                      blank=True)

    def __str__(self):
        return self.skin_type_name

class User(AbstractUser):
    age = models.IntegerField(null=True, blank=True)
    skin_problem = models.ForeignKey(SkinProblem, on_delete=models.SET_NULL, null=True, blank=True)
    skin_type = models.ForeignKey(SkinType, on_delete=models.SET_NULL, null=True, blank=True)
    password_reset_code = models.CharField(max_length=6, blank=True, null=True)
    reset_code_created_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"""{self.username} - {self.first_name} {self.last_name} -
                {self.skin_problem} - {self.skin_type}"""
