from django.db import models

# Create your models here.

class Projeto(models.Model):
    nome = ""
    ident = ""
    items = []

class Conteudo(models.Model):
    tipos = ['Pasta', 'Arquivo']
    tipo = ""
    nome = ""
    ident = ""
    items = []
    def set_tipo(self, ind):
        self.tipo = self.tipos[ind]


