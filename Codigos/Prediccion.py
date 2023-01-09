import pandas as pd
from normalizar import NormalizarPalabra
listaEquipos = pd.read_csv ('docs/equipo.csv')
print(listaEquipos.head())
equipos=listaEquipos['Equipo']
print(type(equipos))
equipos=list(equipos)
años=["2020-21","2019-20","2018-19","2017-18","2015-16","2014-15","2013-14","2012-13","2011-12","2010-11","2009-10","2008-09"
    ,"2007-08","2006-07","2005-06","2004-05","2003-04","2002-03","2001-02","2000-01"]
Champions={}
for año in años:
    Champions[f'{año}']=pd.read_csv(f'Datos/Champions/resultados{año}.csv')

golesLocal={}
golesVisitante={}

for equipo in equipos:
    golesLocal[equipo]=0
    golesVisitante[equipo]=0

for año in años:
    for i in range(len(Champions[año])):
        if str(Champions[año].iloc[i]['Local']) in equipos:
            golesLocal[Champions[año].iloc[i]['Local']]+=int(Champions[año].iloc[i]['GolesLocal'])
        if Champions[año].iloc[i]['Visitante'] in equipos:
            golesVisitante[Champions[año].iloc[i]['Visitante']]+=int(Champions[año].iloc[i]['GolesVisitante'])
    print(f'año {año} terminado')

print(golesLocal)
def Ligas():
    golesLigaLocal={}
    golesLigaVisitante={}
    for equipo in equipos:
        golesLigaLocal[equipo]=0
        golesLigaVisitante[equipo]=0
        pais=str(listaEquipos['Pais'][listaEquipos['Equipo']==equipo].iloc[0])
        if pais.lower()=='paises bajos':
            pais='Holanda'
        pais=NormalizarPalabra(pais)
        datos=pd.read_csv(f'Datos/Ligas/{pais}2021-22.csv')
        if pais!='moldavia':
            for i in range(len(datos)):
                if str(datos.iloc[i]['Local'])==str(equipo):
                    print(equipo)
                    golesLigaLocal[equipo]+=int(datos.iloc[i]['GolesLocal'])
                if str(datos.iloc[i]['Visitante'])==str(equipo):
                    golesLigaVisitante[equipo]+=int(datos.iloc[i]['GolesVisitante'])
        else:
            golesLigaLocal[equipo]+=int(datos.iloc[0]['goles A favor'])/2
            golesLigaVisitante[equipo]+=int(datos.iloc[0]['goles A favor'])/2


    print(golesLigaVisitante)

#Ligas()