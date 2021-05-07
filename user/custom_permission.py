
from rest_framework.permissions import BasePermission

class MyPermissionInsurer(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True

        elif request.method == 'POST':
            return True

        elif request.method == 'PUT':
            return True

        else:
            return False


class MyPermissionEvaluattionExpert(BasePermission):
    def has_permission(self, request, view):

        if request.method == 'GET':
            return True

        elif request.method == 'POST':
            return True

        elif request.method == 'PUT':
            return True

        else:
            return False