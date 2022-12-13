from django.urls import path
from . import views
from rest_framework.authtoken import views as authviews

urlpatterns=[
    path('api-token-auth/', authviews.obtain_auth_token),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
]