from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from django.contrib import auth
from rest_framework_jwt.settings import api_settings


class UserLogIn(APIView):

    def post(self, request):
        try:
            data = JSONParser().parse(request)
            user = auth.authenticate(request, email=data['email'], password=data['password'])
            if user is not None:
                auth.login(request, user)
                return Response({'username': data["user_name"],
                                 'token': api_settings.JWT_ENCODE_HANDLER(api_settings.JWT_PAYLOAD_HANDLER(user))})

        except Exception:
            return Response({'id': 404, 'massage': "the username or code incorrect"})