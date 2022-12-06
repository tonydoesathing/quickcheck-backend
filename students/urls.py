from django.urls import path
from . import views

urlpatterns=[
    path('',views.students),
    path('<int:id>',views.student),
]