import requests
from bs4 import BeautifulSoup

def AjustaUrl(url):
    result = url.rsplit('/', 1)[-1]
    return url.replace(result,"")

def SeparaTitulo(valor):
    result = valor.split(",")
    result = result[3]
    result = result.replace("<h1>","")
    result = result.replace("</h1>","")
    result = result.replace("]","")
    return result

def RetornaComponentes(content):
    lista = []
    result = content.split('<div class="texto">')
    result = result[1].split('<div class="rodapeTexto">')
    result = result[0]
    result = result.split('<center>')
    if(len(result)>1):
        del(result[0])
    for x in range(len(result)):
        result[x] = result[x].replace("</center>"," ")
        result[x] = result[x].replace("</div>"," ")
        result[x] = result[x].replace("</div>"," ")
        result[x] = result[x].replace("</html>"," ")
        lista.append(result[x].split("<br/>"))

    for x in range(len(lista)):
        for y in range(len(lista[x])):
            lista[x][y] = lista[x][y].replace('\xa0'," ")
            lista[x][y] = lista[x][y].replace('<b>'," ")
            lista[x][y] = lista[x][y].replace('</b>'," ")
            lista[x][y] = lista[x][y].replace('\n'," ")
            lista[x][y] = lista[x][y].replace('<p>'," ")
            lista[x][y] = lista[x][y].replace('</p>'," ")
    return lista

def FormataAlinea(valor):
    result = valor.split("</tr>")
    for x in range(len(result)):
        valor = result[x].split("<i>")
        if len(valor)>1:
            result[x] = valor[1].replace("</i>","")
            result[x] = result[x].replace("<td>","")
            result[x] = result[x].replace("</td>","")
            result[x] = result[x].replace(";","")
    return result

def BuscaInfo(valor,info):
    return info.lower() in valor.lower()

def DefineArtigo(valor):
    valor = valor.replace(" ","")
    valor = valor.replace("Art","")
    if int(valor)<10:
        return "Art. {}º".format(valor)
    else:
        return "Art. {}.".format(valor)

def DefineProxArtigo(valor):
    valor = valor.replace(" ","")
    valor = valor.replace("Art","")
    valor = int(valor)
    valor += 1
    if int(valor)<10:
        return "Art. {}º".format(valor)
    else:
        return "Art. {}.".format(valor)

def DefineParagrafo(valor):
    return "§ {}".format(valor)

def DefineProxParagrafo(valor):
    return "§ {}".format(int(valor)+1)

def DefineAlinea(valor):
    return "{})".format(valor)

def BuscaArtigo(lista,info):
    for value in lista:
        for result in value:
            if BuscaInfo(result, info):
                print(result)
                return value
    return "Não encontrado"

def BuscaParagrafo(lista,ant,prox,info):
    anterior = False
    proximo = False
    for result in lista:
        if BuscaInfo(result,ant):
            anterior = True
        if BuscaInfo(result, prox):
            proximo = True
        if BuscaInfo(result, info):
            return result
    return "Não encontrado"

def BuscaInciso(lista,antA,proxA,antP,proxP,info):
    anterior = False
    proximo = False
    anteriorP = False
    proximoP = False
    for result in lista:
        if BuscaInfo(result,antA):
            anterior = True
        if BuscaInfo(result, proxA):
            proximo = True
        if antP != "" and proxP != "":
            if BuscaInfo(result,antP):
                anteriorP = True
            if BuscaInfo(result,proxP):
                proximoP = True
            if BuscaInfo(result, info) and anterior==True and proximo==False and anteriorP==True and proximoP==False:
                return result
        else:
            if BuscaInfo(result, info) and anterior==True and proximo==False:
                return result
    return "Não encontrado"

def BuscaAlinea(lista,antA,proxA,antP,proxP,inci,info):
    anterior = False
    proximo = False
    anteriorP = False
    proximoP = False
    inciso = False
    for result in lista:
        if BuscaInfo(result,antA):
            anterior = True
        if BuscaInfo(result, proxA):
            proximo = True
        if antP != "" and proxP != "":
            if BuscaInfo(result,antP):
                anteriorP = True
            if BuscaInfo(result,proxP):
                proximoP = True
            if anterior==True and proximo==False and anteriorP==True and proximoP==False:
                if BuscaInfo(result, inci):
                    inciso = True
                if BuscaInfo(result, info) and inciso==True:
                    valor = FormataAlinea(result)
                    for v in valor:
                        if BuscaInfo(v, info):
                            return v
        else:
            if anterior==True and proximo==False:
                if BuscaInfo(result, inci):
                    inciso = True
                if BuscaInfo(result, info) and inciso==True:
                    valor = FormataAlinea(result)
                    for v in valor:
                        if BuscaInfo(v,info):
                            return v
    return "Não encontrado"
def BuscaInformacoes(lei,art,para,inci,ali):
    url = "https://www.lexml.gov.br/busca/search?keyword={};f1-tipoDocumento=Legisla%C3%A7%C3%A3o::Lei".format(lei)
    r = requests.get(url)
    bf = BeautifulSoup(r.text,"html.parser")
    div = bf.find("div",{'id':'main_1'})
    tr = div.find_all("tr")
    link = tr[2].find("a")['href']

    r = requests.get("https://www.lexml.gov.br{}".format(link))
    bf = BeautifulSoup(r.text,"html.parser")
    links = bf.find_all("a",{'class':'noprint'})
    url = links[1]['href']

    r = requests.get(url)
    bf = BeautifulSoup(r.text,"html.parser")
    titulo = bf.find_all("h1")
    titulo = SeparaTitulo(str(titulo))
    print("Lei {}: {}".format(lei,titulo))

    sessao = bf.find_all("div",{"class":"sessao"})
    link = sessao[0].find("a")

    url = AjustaUrl(url)+link['href']
    r = requests.get(url)
    bf = BeautifulSoup(r.text,"html.parser")
    textos = str(bf)
    legislacao = RetornaComponentes(textos)

    v1 = str(art)
    v2 = str(para)
    v3 = str(inci)
    v4 = str(ali)

    art = DefineArtigo(v1)
    para = DefineParagrafo(v2)
    ali = DefineAlinea(v4)
    artigo = BuscaArtigo(legislacao,art)
    if v2 != "":
        paragrafo = BuscaParagrafo(artigo,art,DefineProxArtigo("Art 4"),para)
        print(paragrafo)
        if v3 != "":
            inciso = BuscaInciso(artigo,art,DefineProxArtigo(v1),para,DefineProxParagrafo(v1),v3)
            print("Inciso "+inciso)
            if v4 != "":
                alinea = BuscaAlinea(artigo,art,DefineProxArtigo("Art 29"),para,DefineProxParagrafo(v1),v3,ali)
                print("Alinea "+alinea)
    else:
        if v3 != "":
            inciso = BuscaInciso(artigo, art, DefineProxArtigo(v1), "", "", v3)
            print("Inciso "+inciso)
            if v4 != "":
                alinea = BuscaAlinea(artigo, art, DefineProxArtigo("Art 29"), "", "", v3, ali)
                print("Alinea "+alinea)

