from rest_framework.response import Response

from user.decorators import check_permission
from user.models import CUser, EvaluationExpert as evModels, Insurer
from rest_framework import status
from rest_framework.views import APIView
from customer.models import Company
from user.serializer.user import Evaluation_serializer, Insurser_serializer, CompanySerializer, UserCompanySerializer
from rest_framework.parsers import JSONParser
from user.models import Evalution
from user.models import Permission
from user.serializer.user import PermissionSerialzer
from user.models import UserPermission
from user.serializer.user import UserPermissionSerializer
from rest_framework.generics import GenericAPIView


class EvaluationExpert(GenericAPIView):
    serializer_class = Evaluation_serializer
    def get(self, request):
        quaryset = evModels.objects.all()
        output = Evaluation_serializer(quaryset, many=True)
        return Response(output.data)

    def post(self, request):
        data = JSONParser().parse(request)
        try:
            _ = CUser.objects.get(email=data['email'])
            return Response({"message": "user_name or email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        except:
            u = CUser.objects.create(
                email=data['email'], username=data['username'],
                gender=data['gender'],
                name=data['name'], is_active=True
            )

            u.set_password(data['password'])
            u.save()


            e = evModels.objects.create(user=u)
            s = Evaluation_serializer(e)
            return Response(s.data, status=status.HTTP_200_OK)


class InsurserView(APIView):
    serializer_class = Insurser_serializer

    ''' THE DATA MUST POST TO IT IS email, gender, username, name,
    # password , insurer_start and insurer_end'''

    def get(self, requet):
        queryset = Insurer.objects.all()
        s = Insurser_serializer(queryset, many=True)
        return Response(s.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = JSONParser().parse(request)
        try:
            _ = CUser.objects.get(email=data['email'])
            return Response({"message": "username or email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        except:
            u = CUser(
                email=data['email'], username=data['username'],
                gender=data['gender'], name=data['name'], is_active=True
            )

            u.set_password(data['password'])
            u.save()

            e = Insurer.objects.create(user=u,
                                       insurer_start=data['insurer_start'],
                                       insurer_end=data['insurer_end'])

            s = Insurser_serializer(e)
            return Response(s.data, status=status.HTTP_200_OK)


class CompaniView(GenericAPIView):
    serializer_class = CompanySerializer
    def get(self, request):
        queryset = Company.objects.all()
        s = CompanySerializer(queryset, many=True)
        return Response(s.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = JSONParser().parse(request)
        c = Company.objects.create(name=data['name'], address=data['address']
                                   , phone_number=data['phone_number'])
        s = CompanySerializer(c)
        return Response(s.data, status=status.HTTP_200_OK)


class CompanyUSerView(GenericAPIView):
    serializer_class = UserCompanySerializer
    def get(self, request):
        queryset = Evalution.objects.all()
        s = UserCompanySerializer(queryset, many=True)
        return Response(s.data, status=status.HTTP_200_OK)


    def post(self, request):
        data = JSONParser().parse(request)
        c = Company.objects.get(name=data['companyname'])
        E = Evalution.objects.create(location=data['location'], evalution_time=data['evalution_time'],
                                     user=CUser.objects.get(email=data['email']), company=c)
        s = UserCompanySerializer(E)
        return Response(s.data, status=status.HTTP_200_OK)


class PermissionView(GenericAPIView):
    serializer_class = PermissionSerialzer
    @check_permission("list_permission")
    def get(self, request):
        queryset = Permission.objects.all()
        s = PermissionSerialzer(queryset, many=True)
        return Response(s.data, status=status.HTTP_200_OK)

    @check_permission("create_permission")
    def post(self, request):
        data = JSONParser().parse(request)
        check = Permission.objects.filter(name=data['name']).first()
        if check:
            return Response({"message": "permission name is duplicate"}, status=status.HTTP_400_BAD_REQUEST)

        query_data = {
            "name": data["name"]
        }
        if "parent" in data.keys():
            query_data["parent"] = Permission.objects.get(name=data['parent'])

        p = Permission.objects.create(**query_data)

        s = PermissionSerialzer(p)
        return Response(s.data, status=status.HTTP_200_OK)


class UserPermissionView(GenericAPIView):
    serializer_class = UserPermissionSerializer
    def get(self, request):
        queryset = UserPermission.objects.all()
        s = UserPermissionSerializer(queryset, many=True)
        return Response(s.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = JSONParser().parse(request)
        check = UserPermission.objects.filter(user__username=data['username'], permission__name=data['name']).first()

        if check:
            return Response({"message": "permissionUser is exsist"})

        user = CUser.objects.get(username=data['username'])
        permission = Permission.objects.get(name=data['name'])

        up = UserPermission.objects.create(user=user, permission=permission)
        s = UserPermissionSerializer(up)
        return Response(s.data, status=status.HTTP_200_OK)
