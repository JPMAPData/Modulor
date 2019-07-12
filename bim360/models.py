from django.db import models

# Create your models here.

class Projeto(models.Model):

    def __init__(self):
        self.nome = ""
        self.ident = ""
        self.hubId = ""

class Conteudo(models.Model):

    def __init__(self):
        self.nome = ""
        self.ident = ""
        self.pjtId = ""
