from django.contrib.auth.models import User
from PortalVoluntariadoIPS import serializers

from .models import Profile, Project, Project_Avaliacao


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'age', 'area_de_interesse', 'descricao', 'profissao', 'empresa', 'gender', 'status']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ['id', 'user']