from io import *
import random


class Nodo():
    def __init__(self,valor_h):
        self.__h=valor_h
        self.__vecinos=[]

    def heuristica(self):
        return self.__h

    def addNodo(self,nd):
        self.__vecinos.append(nd)

    def getNodos(self):
        return list(self.__vecinos)

class Astar():
    def __init__(self,nodos,aristas,inicio,fin):
        self:__nodosGr=dict(nodos)
        self.__aristas=dict(aristas)
        self.__raiz=inicio
        self.__tope=fin
        self.__setNodos={inicio}

    def busqueda(self,inicio,camino,sumaCamino):#busqueda a estrella
        #retorna (camino,costo del camino,si el camino llega al nodo objetivo)
        ndActual=self.__nodosGr[inicio]
        vecinos=ndActual.getNodos()
        mapa_c={}
        lista_c=[]
        for v in vecinos:
            if(v in self.__setNodos): continue
            h_v=self.__nodosGr[v].heuristica()
            sum=sumaCamino+self.__aristas[(inicio,v)] #sum=suma del camino hasta el vertice v
            sum_h=sum+h_v #sum_t=suma del camino hasta el vertice v + heuristica de v
            lista_c.append(sum_h)
            mapa_c[sum_h]=(v,sum)
            self.__setNodos.add(v)
        ret=None
        if(len(lista_c)==0): #return (camino,sumaCamino+,False)
            suma_t=sumaCamino+ndActual.heuristica()
            ret=(camino,suma_t,False)
            return ret
        lista_c.sort()
        for c in lista_c:
            vertice=mapa_c[c]
            camino_nuevo=camino+" -> "+vertice[0]
            if(vertice[0]==self.__tope):
                ret=(camino_nuevo,c,True)
                break
            ret=self.busqueda(vertice[0],camino_nuevo,vertice[1])
            if(ret[2]): break
        return ret

class DFS():
    def __init__(self,nodos,aristas,inicio,fin):
        self.__nodos=dict(nodos)
        self.__aristas=dict(aristas)
        self.__raiz=inicio
        self.__tope=fin
        self.__setNodos={inicio}
    
    def busqueda(self,inicio,camino,sumaCamino):#busqueda en profundidad (sucesor aleatorio)
        ndActual=self.__nodos[inicio]
        vecinos=ndActual.getNodos()
        ret=(camino,sumaCamino,False)
        while(len(vecinos)>0):
            v=random.choice(vecinos)
            while((v in self.__setNodos) and len(vecinos)>0):
                vecinos.remove(v)
                if(len(vecinos)>0) v=random.choice(vecinos)
            if(len(vecinos)==0) break
            vecinos.remove(v)
            caminoNuevo=camino+" -> "+v
            sumaNueva=sumaCamino+self.__aristas[(inicio,v)]
            if(v==self.__tope):
                ret=(caminoNuevo,sumaNueva,True)
                break
            ret=busqueda(v,caminoNuevo,sumaNueva)
            if(ret[2]): break
        return ret
            
def getNodo(linea):
    partes=linea.split()
    return partes[1][0]

def bcu(nodos,aristas,inicio,fin): #busqueda de costo uniforme
    camino=inicio
    q=[(inicio,inicio,0)] #cola
    #la cola recibe parametros de la forma: (nodo,camino hasta el nodo,costo del camino hasta el nodo)
    set_nodos={inicio}
    ndActual=None
    while(len(q)>0):
        ndActual=q.pop(0)
        if(ndActual[0]==fin): break
        vecinos=nodos[ndActual[0]].getNodos()
        mapaNodos={}
        listaValores=[]
        for v in vecinos:
            a=(ndActual[0],v)
            valor_a=aristas[a]
            mapaNodos[valor_a]=v
            listaValores.append(valor_a)
        listaValores.sort()
        for lv in listaValores:
            v=mapaNodos[lv]
            if(v in set_nodos): continue
            camino=ndActual[1]+" -> "+v
            #a=(ndActual[0],v)
            costoCamino=ndActual[2]+lv
            nuevoNd=(v,camino,costoCamino)
            q.append(nuevoNd)
            set_nodos.add(v)
    return ndActual

def greedy(nodos,aristas,inicio,fin):#busqueda greedy
    camino=inicio
    costoCamino=0
    ndActual=(inicio,nodos[inicio])
    h_fin=nodos[fin].heuristica()
    while(ndActual[0]!=fin):
        vecinos=ndActual[1].getNodos()
        h_min=None
        for v in vecinos:
            h=nodos[v].heuristica()
            if(h_min==None or h<h_min):
                costoCamino+=aristas[(ndActual[0],v)]
                ndActual=(v,nodos[v])
                h_min=h
        camino+=" -> "+ndActual[0]
    ret=(camino,costoCamino+h_fin)
    return ret

def main():
    ia_input=open("ia_input.txt","r")
    lineas=ia_input.readlines()
    ia_input.close()
    nodos={}
    inicio=getNodo(lineas[0])
    fin=getNodo(lineas[1])
    pos=0
    for i in range(2,len(lineas)):
        partes=lineas[i].split()
        if len(partes)>2:
            pos=i
            break
        nodos[partes[0]]=Nodo(int(partes[1]))
    aristas={}
    for i in range(pos,len(lineas)):
        partes=lineas[i].split(", ")
        a=(partes[0],partes[1])
        aristas[a]=int(partes[2])
        nd=nodos[partes[0]]
        nd.addNodo(partes[1])
    a_estrella=Astar(nodos,aristas,inicio,fin)
    profundidad=DFS(nodos,aristas,inicio,fin)
    res_dfs=profundidad.busqueda(inicio,inicio,0)
    res_bcu=bcu(nodos,aristas,inicio,fin)
    res_greedy=greedy(nodos,aristas,inicio,fin)
    res_astar=a_estrella.busqueda(inicio,inicio,0)

    print("Busqueda en profundidad (eligiendo un sucesor al azar):")
    print(f"Camino: {res_dfs[0]}")
    print(f"Costo: {res_dfs[1]}")
    print("------------------------------------")

    print("Busqueda con costo uniforme:")
    print(f"Camino: {res_bcu[1]}")
    print(f"Costo: {res_bcu[2]}")
    print("------------------------------------")

    print("Busqueda greedy:")
    print(f"Camino: {res_greedy[0]}")
    print(f"Costo: {res_greedy[1]}")
    print("------------------------------------")

    print("Busqueda a estrella:")
    print(f"Camino: {res_astar[0]}")
    print(f"Costo: {res_astar[1]}")
    print("------------------------------------")

    print("funciona :D")

main()