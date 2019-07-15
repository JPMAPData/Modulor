from django.db import models


class Projeto(models.Model):

    nome = models.CharField(max_length=300, default="")
    identity = models.CharField(max_length=300, default="")
    hubId = models.CharField(max_length=300, default="")


class Conteudo(models.Model):

    nome = models.CharField(max_length=300, default="")
    identity = models.CharField(max_length=300, default="")
    pjtId = models.CharField(max_length=300, default="")
