from django.contrib import admin
from .models import User, SkinProblem, SkinType

admin.site.register(User)
admin.site.register(SkinProblem)
admin.site.register(SkinType)