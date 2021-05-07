import json
import functools

from rest_framework import status
from rest_framework.response import Response
from user.models import UserPermission

from user.models import CUser


def check_permission(Permission_name):

    def wrapper(func):
        @functools.wraps(func)
        def cash_reload(*args, **kwargs):
            request = args[1]
            user_permission = UserPermission.objects.filter(
                user__username=request.user,
                permission__name=Permission_name
            ).first()

            if request.user.is_superuser or user_permission is not None:
                return func(*args, **kwargs)

            return Response({"message": "user has'nt permission"}, status=status.HTTP_400_BAD_REQUEST)

        return cash_reload

    return wrapper