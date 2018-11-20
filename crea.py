## author: Martín Cepeda, 2017

import requests
from bs4 import BeautifulSoup

def results(palabra,a): #palabra es String, a es Int, retorna 0 si se escribieron los resultados, 1 si hay que afinar la búsqueda o 2 si no hay resultados
    print("Buscando "+palabra+" en "+str(a))
    write_log(a)
    direccion = "http://corpus.rae.es/cgi-bin/crpsrvEx.dll?MfcISAPICommand=buscar&tradQuery=1&destino=0&texto="+palabra+"&autor=&titulo=&ano1="+str(a)+"&ano2="+str(a)+"&medio=1000&pais=1000&tema=1000"
    page = requests.get(direccion)
    soup = BeautifulSoup(page.content, 'html.parser')
    i = soup.prettify().find(" casos en")  # lugar del código donde está la cantidad de resultados
    fid = str(soup.find("input",{"name":"FID"})["value"])  # ID de la búsqueda
    n = 0
    try:
        n = int(soup.prettify()[i-5:i].strip("><"))
        print(n)
        if n > 999:
            return 1
    except ValueError:
        print(n)
        return 2
    p = n//25 +1 # cantidad de páginas de resultados
    for i in range(p):
        print(str(round((i+1)/p*100,1))+"%")
        direccion = "http://corpus.rae.es/cgi-bin/crpsrvEx.dll?visualizar?tipo1=4&tipo2=0&iniItem="+str(i*25)+"&ordenar1=0&ordenar2=0&FID="+fid+"&desc={B}+{I}+"+palabra+"{|I},+en+{I}"+str(a)+"-"+str(a)+"{|I},+en+todos+los+medios,+en+{I}CREA+{|I}+{|B}{BR}&marcas=0"
        page = requests.get(direccion)
        soup = BeautifulSoup(page.content, 'html.parser')
        contenido = soup.find("tt").text    #tabla de resultados
        filtrado = contenido.replace(contenido[:contenido.find("\n")],"")[:-2] # borra primera línea de encabezado en la tabla de resultados, quita el salto de línea de la última fila
        write_results(palabra,a,filtrado)
    return 0

def write_results(palabra,a,text):
    name = palabra
    for i in '/<>:"|?*':
        if i in palabra:
            name = name.replace(i,"-cs-")       
    arc = open("CREA_"+name+"_"+str(a)+".txt","a")
    arc.write(text)
    arc.close()
    
def write_log(t):
    file = open("log.txt","w")
    p,s = 0,0
    if len(prefix)!=0:
        p=1
    if len(suffix)!=0:
        s=1
    file.write(" ".join([str(p),str(s),query,prefix,suffix,str(t)]))
    file.close()
    
def read_log():
    global query, prefix, suffix, start
    file = open("log.txt","r")
    datos = file.read().strip().split()
    file.close()
    lp = int(datos[0])
    ls = int(datos[1])
    query = datos[2]
    if lp==1 and ls==1:
        prefix = datos[3]
        suffix = datos[4]
    elif lp==1 and ls==0:
        prefix = datos[3]
        suffix=""
    elif lp==0 and ls==1:
        prefix = ""
        suffix = datos[3]
    else:
        prefix=""
        suffix=""
    start = int(datos[3+ls+lp])
    
###############################################################################

query = "anti-"             # PALABRA A BUSCAR
prefix = ""                # Prefijo
suffix = "*"               # Sufijo

continuar = False          # CONTINUAR BÚSQUEDA ANTERIOR?

start = 2003           # Año de inicio de la búsqueda 
stop = 2003               # Año de término de la búsqueda

###############################################################################

if continuar:
    read_log()
tiempo = range(start,stop)  # Rango de tiempo
letras = "abcdefghijklmñopqrstuvwxyz"

for t in tiempo:
    actual = query
    if results(prefix+actual+suffix,t)==1:
        for i in letras:
            if results(prefix+actual+i+suffix,t)==1:
                for j in letras:
                    results(prefix+actual+i+j+suffix,t)
