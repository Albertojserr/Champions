import pandas as pd
import sys
sys.path.append('../')

class Normalizar:

    def __init__(self):
        self.años=["2020-21","2019-20","2018-19","2017-18","2015-16","2014-15","2013-14","2012-13","2011-12","2010-11","2009-10","2008-09"
            ,"2007-08","2006-07","2005-06","2004-05","2003-04","2002-03","2001-02","2000-01"]
        self.listaEquipos = pd.read_csv ('docs/equipo.csv')
        print(self.listaEquipos.head())
        self.equipos=self.listaEquipos['Equipo']
        print(type(self.equipos))
        self.equipos=list(self.equipos)
        print(type(self.equipos))
        print(self.equipos)

    def prepararDatos(self):
        for año in self.años:
            self.data=pd.read_csv(f'Datos/Champions/resultados{año}.csv')
            self.df1=pd.unique(self.data['Local'])
            self.df2=pd.unique(self.data['Visitante'])
            self.df3=list(self.df1) + list(self.df2)

    def nombrarEquiposUnicos(self):
        self.listaUnicos=[]
        self.equiposUnicos=set(self.df3)

        for equipo in self.equiposUnicos:
            self.listaUnicos.append(equipo)

        return self.listaUnicos


    def normalizarDatos(self):

        self.dic={}
        for nombre in self.listaUnicos:
            self.lista=str(nombre).lower().split()
            if 'inter' in self.lista:
                self.dic[nombre]='Internazionale'
            for equipo in self.equipos:
                if str(equipo).lower() in self.lista:
                    self.dic[nombre]=str(equipo)
            if 'manchester' in self.lista:
                if 'united' in self.ista:
                    self.dic[nombre]='Man. United'
                elif 'city' in self.lista:
                    self.dic[nombre]='Man. City'
            elif 'lille' in self.lista:
                self.dic[nombre]='LOSC'
            elif 'parís' in self.lista:
                self.dic[nombre]='Paris'
            elif 'sporting' in self.lista:
                if 'portugal' in self.lista:
                    self.dic[nombre]='Sporting CP'
            elif 'donetsk' in self.lista:
                self.dic[nombre]='Shakhtar Donetsk'
            elif 'real' in self.lista:
                if 'madrid' in self.lista:
                    self.dic[nombre]='Real Madrid'
            elif 'young' in self.lista:
                self.dic[nombre]='Young Boys'
            elif 'oporto' in self.lista:
                self.dic[nombre]='Porto'
            elif 'beşiktaş' in self.lista:
                self.dic[nombre]='Besiktas'

        for nombre in self.dic:
            self.data["Local"]=self.data["Local"].replace(nombre,self.dic[nombre])
            self.data["Visitante"]=self.data["Visitante"].replace(nombre,self.dic[nombre])

    def GuardarDatos(self):
        for año in self.años:
            self.data.to_csv(f'Datos/resultados{año}.csv',index=False)
    '''
    def NormalizarPalabra(self,palabra):
        palabra=palabra.lower()
        replacements= (
            ("á","a"),
            ("é","e"),
            ("í","i"),
            ("ó","o"),
            ("ö","o"),
            ("ú","u"),
            ("ü","u"),
            ("ç","c")
        )
        for self.equiposUnicos in replacements:
            palabra=palabra.replace(*self.equiposUnicos)


        #palabra=palabra.replace("á","a")
        #palabra=palabra.replace("é","e")
        #palabra=palabra.replace("í","i")
        #palabra=palabra.replace("ó","o")
        #palabra=palabra.replace("ö","o")
        #palabra=palabra.replace("ú","u")
        #palabra=palabra.replace("ü","u")
        #palabra=palabra.replace("ç","c")
        return palabra

        '''

    @staticmethod
    def ejecutar():
        normalizar=Normalizar()
        normalizar.prepararDatos()
        normalizar.nombrarEquiposUnicos()
        normalizar.normalizarDatos()
        normalizar.GuardarDatos()

def NormalizarPalabra(palabra):
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


if __name__ == '__main__':
    Normalizar.ejecutar()