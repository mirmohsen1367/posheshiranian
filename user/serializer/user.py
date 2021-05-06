from rest_framework import serializers
from user.models import EvaluationExpert, CUser, Insurer
from customer.models import Company
from rest_framework.validators import UniqueValidator

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CUser
        fields = (
            'email',
            'user_name',
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