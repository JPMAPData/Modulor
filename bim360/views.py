from django.shortcuts import render, redirect, get_object_or_404
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

    projetos_list = []

    for element in resposta_pjt['data']:
        if element['type'] == 'projects':
            pjt = Projeto()
            pjt.nome = element['attributes']['name']
            pjt.ident = element['id']
            pjt.hubId = hubId
            projetos_list.append(pjt)
        else:
            pass

    projetos = projetos_list
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

    resposta_pasta = getRespJson("https://developer.api.autodesk.com/project/v1/hubs/" + projeto.hubId + "/projects/" + projeto.ident + "/topFolders", token)

    pastas = []

    for topfolder in resposta_pasta['data']:
        if topfolder['type'] == 'folders':
            cont = Conteudo()
            cont.nome = topfolder['attributes']['name']
            cont.ident = topfolder['id']
            cont.pjtId = projeto.ident
            pastas.append(cont)
        else:
            pass

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

    resposta_obj = getRespJson("https://developer.api.autodesk.com/data/v1/projects/" + folder.pjtId + "/folders/" + folder.ident + "/contents", token)

    folders = []

    for content in resposta_obj['data']:
        if content['type'] == 'folders':
            contenido = Conteudo()
            contenido.nome = content['attributes']['name']
            contenido.ident = content['id']
            contenido.pjtId = folder.pjtId
            folders.append(contenido)

    return render(request, 'folders.html', {'folders': folders})

