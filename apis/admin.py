from django.contrib import admin
from .models import Assessment, Group, Student, StudentScore, GroupScore

admin.site.register([Assessment, Group, Student, StudentScore, GroupScore])
