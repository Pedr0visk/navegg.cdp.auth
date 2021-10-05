from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from .views import user_impersonate, user_impersonation, user_current

# the urls are all named with account but the model is defined as User
# change this in future versions to account only
urlpatterns = [
    path('signin/', obtain_jwt_token),
    path('refresh-token/', refresh_jwt_token),
    path('currentaccount/', user_current, name='current-user'),

    # Impersonation Routes
    path('generate-impersonation-url/', user_impersonation, name='impersonation-url'),
    path('impersonate/<str:token>/',
         user_impersonate, name='impersonate-account'),
]
