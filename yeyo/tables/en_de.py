import csv
import random
coordenadas1={}
coordenadas2={}
valores1={}
valores2={}
encode=""
decode=""

#tupla de ruidos
tuplofus = ("B:14:CD10","1W90:6G:5X80","58LV72:8PO:QM95","82R86:S8:7D908","559>8J:3a:1ma156","58lo64:5S2H:0P1762")

#Anexo de palabra
palabra = str(input("Escriba la palabra: "))
num = len(palabra)


#Generar tablas
with open('tables\default1.csv', newline='',encoding='utf-8-sig') as tabla1:
    lector= csv.reader(tabla1,delimiter=';')
    for i,fila in enumerate(lector):
        for j,valor in enumerate(fila):
            coordenadas1[f"1.{i}.{j}"] = valor
            valores1[valor]=f"1.{i}.{j}"
            
with open('tables\default2.csv',newline='',encoding='utf-8-sig') as tabla2:
    lector=csv.reader(tabla2,delimiter=';')
    for i,fila in enumerate(lector):
        for j,valor in enumerate(fila):
            coordenadas2[f"2.{i}.{j}"]=valor
            valores2[valor]=f"2.{i}.{j}"
            
#INICIO DEL ENCODER
def encoderletters(letter):
    coordenada = valores1.get(letter)
    if coordenada:
        return coordenada
    else:
        return encodersymbols(letter)
def encodersymbols(numeric):
    return valores2.get(numeric)
        
def messagecifrado(cadena):
    resultado=""
    #listas para ruidos extras
    listaux =[]
    ruidox2 = []
    aux=""
    for character in cadena:
        symbol=encoderletters(character)
        """
        Para agregar ruidos a los principales, se debe manejar cada caracter de forma separada
        para luego usar una frase y su numero de longitud que aumentara a cada numero tratado 
        como int independiente para luego juntos y crear la nueva cadena cifrada con ruidos
        """
        listaux = symbol.split(".") #cada caracter se guarda y separa de forma independiente
        ruidox2 = list(map(int,listaux)) #se convertien en int para luego aplicar el aumento
        # se aplica el aumento a cada elemento
        for i in range(len(ruidox2)):
            ruidox2[i]+=num
        #se convierten en str y se juntas para crear el caracter cifrado con ruido    
        aux = ".".join(map(str, ruidox2))
        ghost=random.choice(tuplofus) 
        resultado+=f"{ghost}-{aux}-" #se guardan todos los elementos con los ruidos
    return resultado
#FIN DEL ENCODER

#INICIO DEL DECODER
def decoderLetters(letter):
    for clave,valor in coordenadas1.items():
        if clave == letter:
            return valor
    return decodersymbols(letter)

def decodersymbols(symbol):
        for clave,valor in coordenadas2.items():
            if clave == symbol:
                return valor
          
def MessageDecifrado(cadena):
    resultado=""
    listsymbols=cadena.split("-")
    listsymbols.pop()
    limpia=[] #limpia de ruido 
    listaux=[]
    remove_ruido = [] # eliminacion de aumento en valores reales
    cad_aux=""

    #Remover los ruido
    for i in listsymbols:
        if i not in tuplofus:
            limpia.append(i)

    #decodificar el mensaje + eliminacion de alteracion de valores reales    
    for elements in limpia:
        cad_aux = elements
        listaux = cad_aux.split(".")
        remove_ruido = list(map(int,listaux))
        
        for i in range(len(remove_ruido)):
            remove_ruido[i]-=num
        aux = ".".join(map(str,remove_ruido))
        

        symbolD=decoderLetters(aux)
        resultado+=f"{symbolD}"
    return resultado
#FIN DEL DECODER