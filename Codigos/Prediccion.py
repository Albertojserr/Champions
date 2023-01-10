import pandas as pd
from normalizar import NormalizarPalabra


class Prediccion:

    def __init__(self):
        self.listaEquipos = pd.read_csv ('docs/equipo.csv')
        print(self.listaEquipos.head())
        self.equipos=self.listaEquipos['Equipo']
        print(type(self.equipos))
        self.equipos=list(self.equipos)
        self.años=["2020-21","2019-20","2018-19","2017-18","2015-16","2014-15","2013-14","2012-13","2011-12","2010-11","2009-10","2008-09"
        ,"2007-08","2006-07","2005-06","2004-05","2003-04","2002-03","2001-02","2000-01"]
        self.Champions={}
        for año in self.años:
            self.Champions[f'{año}']=pd.read_csv(f'Datos/Champions/resultados{año}.csv')

        self.golesLocal={}
        self.golesVisitante={}

        for equipo in self.equipos:
            self.golesLocal[equipo]=0
            self.golesVisitante[equipo]=0

        for año in self.años:
            for i in range(len(self.Champions[año])):
                if str(self.Champions[año].iloc[i]['Local']) in self.equipos:
                    self.golesLocal[self.Champions[año].iloc[i]['Local']]+=int(self.Champions[año].iloc[i]['GolesLocal'])
                if self.Champions[año].iloc[i]['Visitante'] in self.equipos:
                    self.golesVisitante[self.Champions[año].iloc[i]['Visitante']]+=int(self.Champions[año].iloc[i]['GolesVisitante'])
            print(f'año {año} terminado')

        print(self.golesLocal)

    def Ligas(self):
        self.golesLigaLocal={}
        self.golesLigaVisitante={}
        for equipo in self.equipos:
            self.golesLigaLocal[equipo]=0
            self.golesLigaVisitante[equipo]=0
            self.pais=str(self.listaEquipos['Pais'][self.listaEquipos['Equipo']==equipo].iloc[0])
            if self.pais.lower()=='paises bajos':
                self.pais='Holanda'
            self.pais=NormalizarPalabra(self.pais)
            self.datos=pd.read_csv(f'Datos/Ligas/{self.pais}2021-22.csv')
            if self.pais!='moldavia':
                for i in range(len(self.datos)):
                    if str(self.datos.iloc[i]['Local'])==str(equipo):
                        print(equipo)
                        self.golesLigaLocal[equipo]+=int(self.datos.iloc[i]['GolesLocal'])
                    if str(self.datos.iloc[i]['Visitante'])==str(equipo):
                        self.golesLigaVisitante[equipo]+=int(self.datos.iloc[i]['GolesVisitante'])
            else:
                self.golesLigaLocal[equipo]+=int(self.datos.iloc[0]['goles A favor'])/2
                self.golesLigaVisitante[equipo]+=int(self.datos.iloc[0]['goles A favor'])/2


        #print(golesLigaVisitante)
        #print(golesLigaLocal)

    def convertir(self):
        df1 = pd.DataFrame([[key, self.golesLigaVisitante[key]] for key in self.golesLigaVisitante.keys()], columns=['Equipo', 'goles'])
        df1.to_csv('golesLigaVisitante.csv', index=False)
        df2 = pd.DataFrame([[key, self.golesLigaLocal[key]] for key in self.golesLigaLocal.keys()], columns=['Equipo', 'goles'])
        df2.to_csv('golesLigaLocal.csv', index=False)
        print(df1)
        print(df2)


if __name__ == '__main__':
    pred=Prediccion()
    pred.Ligas()
    pred.convertir()

