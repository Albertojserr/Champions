import pandas as pd
import sys
sys.path.append('../')


#Normalizamos los datos para tener todos sin tildes y por tanto poder hacer posteriormente un análisis mejor.
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


#La clase Normalizar se encarga de normalizar los datos de los equipos, es decir, de cambiar los nombres de los equipos
#para tener los nombres correctos y que coincidan con los nombres de la base de datos de los equipos.
class Normalizar:

    def __init__(self):
        self.años=["2020-21","2019-20","2018-19","2017-18","2015-16","2014-15","2013-14","2012-13","2011-12","2010-11","2009-10","2008-09"
            ,"2007-08","2006-07","2005-06","2004-05","2003-04","2002-03","2001-02","2000-01"] #Estos son los años que tenemos en la base de datos (localizados en la carpeta Datos/Champions)
        self.listaEquipos = pd.read_csv ('docs/equipo.csv') #Leemos el csv con los nombres de los equipos
        print(self.listaEquipos.head()) #Mostramos los datos del csv
        self.equipos=self.listaEquipos['Equipo'] #Cogemos los nombres de los equipos
        print(type(self.equipos)) #Mostramos el tipo de datos
        self.equipos=list(self.equipos) #Convertimos el tipo de datos a lista
        print(type(self.equipos)) #Mostramos el tipo de datos
        print(self.equipos) #Mostramos los nombres de los equipos

    def prepararDatos(self):
        for año in self.años:
            self.data=pd.read_csv(f'Datos/Champions/resultados{año}.csv')
            self.df1=pd.unique(self.data['Local']) #cogemos los nombres de los equipos locales sin incluir repetidos
            self.df2=pd.unique(self.data['Visitante']) #cogemos los nombres de los equipos visitantes sin incluir repetidos (realmente son los mismos que los locales)
            self.df3=list(self.df1) + list(self.df2) #juntamos los dos arrays anteriores (pero ahora estarán repetidos los nombres de los equipos)

    def nombrarEquiposUnicos(self):
        self.listaUnicos=[]
        self.equiposUnicos=set(self.df3) #Eliminamos los repetidos

        for equipo in self.equiposUnicos:
            self.listaUnicos.append(equipo) #Hacemos una nueva lista con los elementos sin repetir.

        return self.listaUnicos #Devolvemos la lista de equipos sin repetir que la utilizaremos para normalizar los datos.


    def normalizarDatos(self):
        self.dic={} #Creamos un diccionario para guardar los nombres normalizados
        for nombre in self.listaUnicos: #Recorremos la lista de equipos sin repetir
            self.lista=str(nombre).lower().split()
            if 'inter' in self.lista:
                self.dic[nombre]='Internazionale' #Aquí ya hemos actualizado el nombre con el que queremos tenerlo y
                #lo guardamos en el diccionario. El nombre del equipo que queremos cambiar es la clave y el nombre que queremos que tenga es el valor.
                #Haremos lo mismo con todos los equipos. Ponemos primero inter ya que si lo encuentra puede que lo encuentre con milan y el programa se iría al AC Milan en vez del Inter de Milan.
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

    #Guardamos los datos en el csv correspondiente a cada año.
    def GuardarDatos(self):
        for año in self.años:
            self.data.to_csv(f'Datos/resultados{año}.csv',index=False)


    def Ligas(self): #El método de ligas es como el de champions solo que solo se usará para la predicción del resultaod con la red neuronal.
        self.golesLigaLocal={}
        self.golesLigaVisitante={}
        for equipo in self.equipos:
            self.golesLigaLocal[equipo]=[0,0,0]
            self.golesLigaVisitante[equipo]=[0,0,0]
            self.pais=str(self.listaEquipos['Pais'][self.listaEquipos['Equipo']==equipo].iloc[0])
            if self.pais.lower()=='paises bajos':
                self.pais='Holanda'
            self.pais=NormalizarPalabra(self.pais)
            self.datos=pd.read_csv(f'Datos/Ligas/{self.pais}2021-22.csv')
            if self.pais!='moldavia':
                for i in range(len(self.datos)):
                    if str(self.datos.iloc[i]['Local'])==str(equipo):
                        print(equipo)
                        self.golesLigaLocal[equipo][0]+=int(self.datos.iloc[i]['GolesLocal'])
                        self.golesLigaLocal[equipo][1]+=int(self.datos.iloc[i]['GolesVisitante'])
                        self.golesLigaLocal[equipo][2]+=1
                    if str(self.datos.iloc[i]['Visitante'])==str(equipo):
                        self.golesLigaVisitante[equipo][0]+=int(self.datos.iloc[i]['GolesVisitante'])
                        self.golesLigaVisitante[equipo][1]+=int(self.datos.iloc[i]['GolesLocal'])
                        self.golesLigaVisitante[equipo][2]+=1
            else:
                self.golesLigaLocal[equipo][0]+=int(self.datos.iloc[0]['goles A favor'])/2
                self.golesLigaLocal[equipo][1]+=int(self.datos.iloc[0]['goles En contra'])/2
                self.golesLigaLocal[equipo][2]+=int(self.datos.iloc[0]['partidos'])/2
                self.golesLigaVisitante[equipo][0]+=int(self.datos.iloc[0]['goles A favor'])/2
                self.golesLigaVisitante[equipo][1]+=int(self.datos.iloc[0]['goles En contra'])/2
                self.golesLigaVisitante[equipo][2]+=int(self.datos.iloc[0]['partidos'])/2
        for key in self.golesLigaLocal:
            if self.golesLigaLocal[key][2]!=0:
                self.golesLigaLocal[key][0]=float(self.golesLigaLocal[key][0]/self.golesLigaLocal[key][2])
                self.golesLigaLocal[key][1]=float(self.golesLigaLocal[key][1]/self.golesLigaLocal[key][2])
            else:
                self.golesLigaLocal[key]=[0,0,0]
        for key in self.golesLigaVisitante:
            if self.golesLigaVisitante[key][2]!=0:
                self.golesLigaVisitante[key][0]=float(self.golesLigaVisitante[key][0]/self.golesLigaVisitante[key][2])
                self.golesLigaVisitante[key][1]=float(self.golesLigaVisitante[key][1]/self.golesLigaVisitante[key][2])
            else:
                self.golesLigaVisitante[key]=[0,0,0]


    def convertirLiga(self):
        df1= pd.DataFrame([[key, self.golesLigaLocal[key][0],self.golesLigaLocal[key][1]] for key in self.golesLigaLocal.keys()], columns=['Equipo','golesLocal','golesRecibidosLocal'])
        df1.to_csv('golesLigaLocal.csv', index=False)
        df2 = pd.DataFrame([[key, self.golesLigaVisitante[key][0], self.golesLigaVisitante[key][1]] for key in self.golesLigaVisitante.keys()], columns=['EquipoVisitante', 'golesVisitante','golesRecibidosVisitante'])
        df2.to_csv('golesLigaVisitante.csv', index=False)
        df3 = pd.concat([df1, df2], axis=1)
        df3=df3.drop(['EquipoVisitante'],axis=1)
        df3.to_csv('golesLiga.csv', index=False)
        print(df3)


    #Hacemos la función ejecutar() para que quede más organizado y podamos usarla en el main.
    @staticmethod
    def ejecutar():
        normalizar=Normalizar()
        normalizar.prepararDatos()
        normalizar.nombrarEquiposUnicos()
        normalizar.normalizarDatos()
        normalizar.GuardarDatos()
        #normalizar.Ligas()
        #normalizar.convertirLiga()



#Ejecutamos el programa
if __name__ == '__main__':
    Normalizar.ejecutar()