from rest_framework.response import Response
from user.models import CUser, EvaluationExpert as evModels, Insurer
from rest_framework import status
from rest_framework.views import APIView
from customer.models import Company
from user.serializer.user import Evaluation_serializer, Insurser_serializer
from rest_framework.parsers import JSONParser


class EvaluationExpert(APIView):

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
                email=data['email'], user_name=data['user_name'],
                gender=data['gender'],
                name=data['name']
            )

            u.set_password(data['password'])
            u.save()


            e = evModels.objects.create(user=u)
            s = Evaluation_serializer(e)
            return Response(s.data, status=status.HTTP_200_OK)

class InsurserView(APIView):

    def get(self, requet):
        queryset = Insurer.objects.all()
        s = Insurser_serializer(queryset, many=True)
        return Response(s.data, status=status.HTTP_200_OK)

    # @check_permission("create_user")
    def post(self, request):
        data = JSONParser().parse(request)
        try:
            _ = CUser.objects.get(email=data['email'])
            return Response({"message": "user_name or email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        except:
            u = CUser.objects.create(
                email=data['email'], user_name=data['user_name'],
                start_date=data['start_date'], gender=data['gender'],
                name=data['name']
            )

            u.set_password(data['password'])
            u.save()

            e = Insurer.objects.create(user=u,
                                       insurer_start=data['insurer_start'],
                                       insurer_end=data['insurer_end'])

            s = Insurser_serializer(e)
            return Response(s.data, status=status.HTTP_200_OK)
