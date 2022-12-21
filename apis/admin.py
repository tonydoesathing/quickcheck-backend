from django.contrib import admin
from .models import Assessment, Group, Student, StudentScore, GroupScore,StudentClass

admin.site.register([Assessment, Group, Student, StudentScore, GroupScore,StudentClass])
