from django.shortcuts import render
from .models import Projeto, Conteudo
from django.contrib.auth.decorators import login_required
import requests


@login_required
def projects_list(request):

    def getToken(client_id, client_secret):
        req = {'client_id': client_id, 'client_secret': client_secret, 'grant_type': 'client_credentials','scope': 'data:read'}
        resp = requests.post('https://developer.api.autodesk.com/authentication/v1/authenticate', req).json()
        return resp['access_token']

    token = getToken("Dm1AJ95famLKnf4MUOGpwO7zJIcBF4J7", "V050fdb1761e4460")

    def getRespJson(url, token):
        headers = {'Authorization': 'Bearer ' + token}
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        if resp.status_code == 200:
            return resp.json()
        else:
            return resp.status_code

    def getHubId(jason):
        return jason['data'][0]['id']

    resposta_hub = getRespJson("https://developer.api.autodesk.com/project/v1/hubs", token)

    hubId = getHubId(resposta_hub)

    resposta_pjt = getRespJson("https://developer.api.autodesk.com/project/v1/hubs/" + hubId + "/projects", token)

    Projeto.objects.all().delete()

    for element in resposta_pjt['data']:
        if element['type'] == 'projects':
            pjt = Projeto()
            pjt.nome = element['attributes']['name']
            pjt.identity = element['id']
            pjt.hubId = hubId
            pjt.save()
        else:
            pass

    projetos = Projeto.objects.all()
    return render(request, 'projects.html', {'projetos': projetos})


@login_required
def topfolders(request, projeto):

    def getToken(client_id, client_secret):
        req = {'client_id': client_id, 'client_secret': client_secret, 'grant_type': 'client_credentials','scope': 'data:read'}
        resp = requests.post('https://developer.api.autodesk.com/authentication/v1/authenticate', req).json()
        return resp['access_token']

    token = getToken("Dm1AJ95famLKnf4MUOGpwO7zJIcBF4J7", "V050fdb1761e4460")

    def getRespJson(url, token):
        headers = {'Authorization': 'Bearer ' + token}
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        if resp.status_code == 200:
            return resp.json()
        else:
            return resp.status_code

    pojeto = Projeto.objects.get(nome=projeto)

    resposta_pasta = getRespJson("https://developer.api.autodesk.com/project/v1/hubs/" + pojeto.hubId + "/projects/" + pojeto.identity + "/topFolders", token)

    Conteudo.objects.all().delete()

    for topfolder in resposta_pasta['data']:
        if topfolder['type'] == 'folders':
            cont = Conteudo()
            cont.nome = topfolder['attributes']['name']
            cont.identity = topfolder['id']
            cont.pjtId = pojeto.identity
            cont.save()
        else:
            pass

    pastas = Conteudo.objects.all()

    return render(request, 'topfolders.html', {'pastas': pastas})


@login_required
def folders_list(request, folder):

    def getToken(client_id, client_secret):
        req = {'client_id': client_id, 'client_secret': client_secret, 'grant_type': 'client_credentials','scope': 'data:read'}
        resp = requests.post('https://developer.api.autodesk.com/authentication/v1/authenticate', req).json()
        return resp['access_token']

    token = getToken("Dm1AJ95famLKnf4MUOGpwO7zJIcBF4J7", "V050fdb1761e4460")

    def getRespJson(url, token):
        headers = {'Authorization': 'Bearer ' + token}
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        if resp.status_code == 200:
            return resp.json()
        else:
            return resp.status_code

    conte = Conteudo.objects.get(nome=folder)

    resposta_obj = getRespJson("https://developer.api.autodesk.com/data/v1/projects/" + conte.pjtId + "/folders/" + conte.identity + "/contents", token)

    Conteudo.objects.all().delete()

    for content in resposta_obj['data']:
        if content['type'] == 'folders':
            contenido = Conteudo()
            contenido.nome = content['attributes']['name']
            contenido.identity = content['id']
            contenido.pjtId = conte.identity
            contenido.save()
        else:
            pass

    folders = Conteudo.objects.all()

    return render(request, 'folders.html', {'folders': folders})

@login_required
def upload(request):
    return render(request, 'upload.html')
