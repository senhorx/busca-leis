import pandas as pd
from Crawler import BuscaInformacoes

def ajustaURL(valor):
    result = valor.split(" ")
    return result[1]

def retornaLista(lista):
    del(lista[0])
    del(lista[1])
    return list(lista)

df = pd.read_excel("processo198.xlsx")

leis = retornaLista(df['Unnamed: 1'])
artigos = retornaLista(df['Unnamed: 2'])
paragrafos = retornaLista(df['Unnamed: 3'])
incisos = retornaLista(df['Unnamed: 4'])
alineas = retornaLista(df['Unnamed: 5'])

for x in range(len(leis)):
    v2 = ""
    v3 = ""
    v4 = ""
    v5 = ""
    v1 = ajustaURL(leis[x])
    if str(artigos[x]) != "nan":
        v2 = artigos[x]
    if str(paragrafos[x]) != "nan":
        v3 = paragrafos[x]
    if str(incisos[x]) != "nan":
        v4 = incisos[x]
    if str(alineas[x]) != "nan":
        v5 = alineas[x]
    BuscaInformacoes(v1,v2,v3,v4,v5)
    print("******************")




