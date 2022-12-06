from django.urls import path
from . import views

urlpatterns=[
    path('',views.assessments),
    path('<int:id>',views.assessment),
]