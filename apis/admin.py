from django.contrib import admin
from .models import Assessment, Group, Student

admin.site.register([Assessment, Group, Student])
