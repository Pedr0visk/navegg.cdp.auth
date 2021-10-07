from rest_framework.decorators import api_view, throttle_classes, authentication_classes, permission_classes
from rest_framework.throttling import UserRateThrottle
from rest_framework import status
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import UserImpersonation, User

from rest_framework_jwt.settings import api_settings
from datetime import datetime as dt, timezone

from django.conf import settings


class OncePerMinuteUserThrottle(UserRateThrottle):
    rate = '1/minute'


# @throttle_classes([OncePerMinuteUserThrottle])
@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def user_impersonation(request):
    token = request.user.impersonate()
    url = settings.IMPERSONATION_REDIRECT_URL
    return Response({"url": "%s/%s/" % (url, token)})


@api_view(['GET'])
def user_impersonate(request, token):
    obj = UserImpersonation.objects.filter(token=token).first() or None

    if not obj:
        return Response({"message": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)

    diff = dt.now(tz=timezone.utc) - obj.expire_date
    if diff.seconds > 300:
        return Response({"message": "Token expired"}, status=status.HTTP_400_BAD_REQUEST)

    user = obj.user

    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)

    obj.delete()

    # generate jwt token
    return Response({"token": token})


@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def user_current(request):
    return Response({
        'user_id': request.user.id,
        'email': request.user.email
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
def user_batch_insert(request):
    for user in request.data:
        User.objects.create(
            id=user['id'],
            first_name=user['first_name'],
            email=user['email'],
            password=user['password'],
            is_active=True,
            is_staff=False,
            is_superuser=False
        )

    return Response({'message': 'Success!'}, status=status.HTTP_201_CREATED)
