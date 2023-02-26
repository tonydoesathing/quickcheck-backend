from django.urls import path
# from . import views
# from rest_framework.authtoken import views as authviews

from knox import views as knox_views
from auth.views import LoginView

urlpatterns = [
     path('login/', LoginView.as_view(), name='knox_login'),
     path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
     path('logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
]