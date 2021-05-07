from rest_framework import serializers
from user.models import EvaluationExpert, CUser, Insurer
from customer.models import Company
from user.models import Evalution
from user.models import Permission
from user.models import UserPermission

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CUser
        fields = (
            'email',
            'username',
            'name',
            'start_date',
            'is_staff',
            'is_active',
            'gender',
            'companies'
        )


class Evaluation_serializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)
    class Meta:
        model = EvaluationExpert
        fields = ('user', )


class Insurser_serializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Insurer
        fields = ('insurer_start', 'insurer_end', 'user')


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = '__all__'


class UserCompanySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    companies = CompanySerializer(read_only=True)

    class Meta:
        model = Evalution
        fields = ('location', 'evalution_time', 'user', 'companies')


class SubPermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = ('name',)


class PermissionSerialzer(serializers.ModelSerializer):

    parent= serializers.PrimaryKeyRelatedField(read_only=True)
    subpermission = SubPermissionSerializer(read_only=True)

    class Meta:
        model = Permission
        fields = ('parent', 'name', 'subpermission')

class UserPermissionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    permission = PermissionSerialzer(read_only=True)
    class Meta:
        model = UserPermission
        fields = ('user', 'permission')