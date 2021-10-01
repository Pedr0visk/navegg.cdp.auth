from django.urls import path
from .views import user_impersonate, user_signon

urlpatterns = [
    path('signon/', user_signon, name='sign-on'),
    path('impersonate-user/<str:token>/',
         user_impersonate, name='impersonate-user'),
]
