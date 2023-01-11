import pandas as pd
import sys
sys.path.append('../')
años=["2020-21","2019-20","2018-19","2017-18","2015-16","2014-15","2013-14","2012-13","2011-12","2010-11","2009-10","2008-09"
    ,"2007-08","2006-07","2005-06","2004-05","2003-04","2002-03","2001-02","2000-01"]
listaEquipos = pd.read_csv ('docs/equipo.csv')
print(listaEquipos.head())
equipos=listaEquipos['Equipo']
print(type(equipos))
equipos=list(equipos)
print(type(equipos))
print(equipos)
for año in años:
    data=pd.read_csv(f'Datos/resultados{año}.csv')
    dic={}
    for nombre in data.Local.unique():
        lista=str(nombre).lower().split()
        if 'inter' in lista:
            dic[nombre]='Internazionale'
        for equipo in equipos:
            if str(equipo).lower() in lista:
                dic[nombre]=str(equipo)
        if 'manchester' in lista:
            if 'united' in lista:
                dic[nombre]='Man. United'
            elif 'city' in lista:
                dic[nombre]='Man. City'
        elif 'lille' in lista:
            dic[nombre]='LOSC'
        elif 'parís' in lista:
            dic[nombre]='Paris'
        elif 'sporting' in lista:
            if 'portugal' in lista:
                dic[nombre]='Sporting CP'
        elif 'donetsk' in lista:
            dic[nombre]='Shakhtar Donetsk'
        elif 'real' in lista:
            if 'madrid' in lista:
                dic[nombre]='Real Madrid'
        elif 'young' in lista:
            dic[nombre]='Young Boys'
        elif 'oporto' in lista:
            dic[nombre]='Porto'
        elif 'beşiktaş' in lista:
            dic[nombre]='Besiktas'

    for nombre in dic:
        data["Local"]=data["Local"].replace(nombre,dic[nombre])

    dic={}
    for nombre in data.Visitante.unique():
        lista=str(nombre).lower().split()
        if 'inter' in lista:
            dic[nombre]='Internazionale'
        for equipo in equipos:
            if str(equipo).lower() in lista:
                dic[nombre]=str(equipo)
        if 'manchester' in lista:
            if 'united' in lista:
                dic[nombre]='Man. United'
            elif 'city' in lista:
                dic[nombre]='Man. City'
        elif 'lille' in lista:
            dic[nombre]='LOSC'
        elif 'parís' in lista:
            dic[nombre]='Paris'
        elif 'sporting' in lista:
            if 'portugal' in lista:
                dic[nombre]='Sporting CP'
        elif 'donetsk' in lista:
            dic[nombre]='Shakhtar Donetsk'
        elif 'real' in lista:
            if 'madrid' in lista:
                dic[nombre]='Real Madrid'
        elif 'young' in lista:
            dic[nombre]='Young Boys'
        elif 'oporto' in lista:
            dic[nombre]='Porto'
        elif 'beşiktaş' in lista:
            dic[nombre]='Besiktas'
    for nombre in dic:
        data["Visitante"]=data["Visitante"].replace(nombre,dic[nombre])
    data.to_csv(f'Datos/resultados{año}.csv',index=False)


def NormalizarPalabra(palabra:str):
    palabra=palabra.lower()
    palabra=palabra.replace("á","a")
    palabra=palabra.replace("é","e")
    palabra=palabra.replace("í","i")
    palabra=palabra.replace("ó","o")
    palabra=palabra.replace("ö","o")
    palabra=palabra.replace("ú","u")
    palabra=palabra.replace("ü","u")
    palabra=palabra.replace("ç","c")
    return palabra