import datetime
from django.db import models
from django.contrib.auth.models import User

"""
class Profile(models.Model):
    name = models.CharField(max_length=200)
    id = models.AutoField(primary_key=True)
    age = models.IntegerField()
    area_de_interesse = models.CharField(max_length=200)
    descricao = models.CharField(max_length=10000)
    profissao = models.CharField(max_length=200)
    empresa = models.CharField(max_length=200)
    gender = models.BooleanField(default=True)
    status = models.BooleanField(default=False)
    def __str__(self):
        return self.name +" "+ self.id
"""


class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    age = models.IntegerField()
    area_de_interesse = models.CharField(max_length=200)
    descricao = models.CharField(max_length=10000)
    profissao = models.CharField(max_length=200)
    empresa = models.CharField(max_length=200)
    gender = models.BooleanField(default=True)
    status = models.BooleanField(default=False)
    morada = models.CharField(max_length=250)


class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name_text = models.CharField(max_length=200)
    empresa = models.CharField(max_length=200)
    descricao = models.CharField(max_length=200)
    responsavel = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    users = models.CharField(max_length=250, null=True)
    aprovado = models.BooleanField(null=True)
    complete = models.BooleanField(null=True)

    def __str__(self):
        return self.name_text



class Project_Avaliacao(models.Model):
    id = models.AutoField(primary_key=True)
    admin_ID = models.ForeignKey(Profile, on_delete=models.CASCADE)
    project_ID = models.ForeignKey(Project, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.id + " " + self.admin_ID + " " + self.project_ID + " " + self.approved
