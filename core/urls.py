from django.contrib import admin
from django.urls import path
from django.conf.urls import include

from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('auth/signin/', obtain_jwt_token),
    path('auth/refresh-token/', refresh_jwt_token),

    path('auth/', include('users.urls'))
]
