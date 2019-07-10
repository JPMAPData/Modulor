from django.shortcuts import render, redirect, get_object_or_404
from .models import Projeto, Conteudo
import requests
# Create your views here.

def folders_list(request):
    def getToken(client_id, client_secret):
        req = {'client_id': client_id, 'client_secret': client_secret, 'grant_type': 'client_credentials','scope': 'data:read'}
        resp = requests.post('https://developer.api.autodesk.com/authentication/v1/authenticate', req).json()
        return resp['access_token']

    token = getToken("Dm1AJ95famLKnf4MUOGpwO7zJIcBF4J7", "vAyaauIpMr4qhy6O")

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
            pjt = Projeto(nome=element['attributes']['name'], ident=element['id'])
            projetos_list.append(pjt)
        else:
            pass

    def subpastas(projeto, pasta):
        resposta_obj = getRespJson("https://developer.api.autodesk.com/data/v1/projects/" + projeto.ident + "/folders/" + pasta.ident + "/contents", token)
        for content in resposta_obj['data']:
            if content['type'] == 'folders':
                contenido = Conteudo(nome=content['attributes']['name'], ident=content['id'])
                contenido.set_tipo(0)
                pasta.items.append(contenido)
                subpastas(projeto, contenido)
            else:
                contenido = Conteudo(content['attributes']['displayName'], content['id'])
                contenido.set_tipo(1)
                pasta.items.append(contenido)

    for pjt in projetos_list:
        resposta_pasta = getRespJson("https://developer.api.autodesk.com/project/v1/hubs/" + hubId + "/projects/" + pjt.ident + "/topFolders", token)
        for topfolder in resposta_pasta['data']:
            if topfolder['type'] == 'folders':
                cont = Conteudo(nome=topfolder['attributes']['name'], ident=topfolder['id'])
                cont.set_tipo(0)
                pjt.items.append(cont)
                subpastas(pjt, cont)
            else:
                cont = Conteudo(nome=topfolder['attributes']['name'], ident=topfolder['id'])
                cont.set_tipo(1)
                pjt.items.append(cont)

    projetos = Projeto.objects.all()
    return render(request, 'pastas.html', {'projetos': projetos})
