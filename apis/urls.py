from django.urls import path
from . import views

urlpatterns=[
    path('assessments/',views.assessments),
    path('assessments/<int:id>',views.assessment),
    path('groups/',views.groups),
    path('groups/<int:id>',views.group),
    path('students/',views.students),
    path('students/<int:id>',views.student),
    path('classes/',views.student_classes),
    path('classes/<int:id>',views.student_class),
]