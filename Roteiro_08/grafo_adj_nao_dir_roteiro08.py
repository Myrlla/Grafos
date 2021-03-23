# -*- coding: utf-8 -*-
import math
from copy import deepcopy

class VerticeInvalidoException(Exception):
    pass

class ArestaInvalidaException(Exception):
    pass

class MatrizInvalidaException(Exception):
    pass


class ArestaNaoExistenteException(object):
    pass


class Grafo:

    QTDE_MAX_SEPARADOR = 1
    SEPARADOR_ARESTA = '-'
    __maior_vertice = 0

    def __init__(self, V=None, M=None):
        '''
        Constrói um objeto do tipo Grafo. Se nenhum parâmetro for passado, cria um Grafo vazio.
        Se houver alguma aresta ou algum vértice inválido, uma exceção é lançada.
        :param V: Uma lista dos vértices (ou nodos) do grafo.
        :param V: Uma matriz de adjacência que guarda as arestas do grafo. Cada entrada da matriz tem um inteiro que indica a quantidade de arestas que ligam aqueles vértices
        '''

        if V == None:
            V = list()
        if M == None:
            M = list()

        for v in V:
            if not(Grafo.verticeValido(v)):
                raise VerticeInvalidoException('O vértice ' + v + ' é inválido')
            if len(v) > self.__maior_vertice:
                self.__maior_vertice = len(v)

        self.N = list(V)

        if M == []:
            for k in range(len(V)):
                M.append(list())
                for l in range(len(V)):
                    if k>l:
                        M[k].append('-')
                    else:
                        M[k].append([])


        if len(M) != len(V):
            raise MatrizInvalidaException('A matriz passada como parâmetro não tem o tamanho correto')

        for c in M:
            if len(c) != len(V):
                raise MatrizInvalidaException('A matriz passada como parâmetro não tem o tamanho correto')

        for i in range(len(V)):
            for j in range(len(V)):
                '''
                Verifica se os índices passados como parâmetro representam um elemento da matriz abaixo da diagonal principal.
                Além disso, verifica se o referido elemento é um traço "-". Isso indica que a matriz é não direcionada e foi construída corretamente.
                '''
                if i>j and not(M[i][j] == '-'):
                    raise MatrizInvalidaException('A matriz não representa uma matriz não direcionada')


                aresta = V[i] + Grafo.SEPARADOR_ARESTA + V[j]
                if not(self.arestaValida(aresta)):
                    raise ArestaInvalidaException('A aresta ' + aresta + ' é inválida')

        self.M = list(M)

    def arestaValida(self, aresta=''):
        '''
        Verifica se uma aresta passada como parâmetro está dentro do padrão estabelecido.
        Uma aresta é representada por um string com o formato a-b, onde:
        a é um substring de aresta que é o nome de um vértice adjacente à aresta.
        - é um caractere separador. Uma aresta só pode ter um único caractere como esse.
        b é um substring de aresta que é o nome do outro vértice adjacente à aresta.
        Além disso, uma aresta só é válida se conectar dois vértices existentes no grafo.
        :param aresta: A aresta que se quer verificar se está no formato correto.
        :return: Um valor booleano que indica se a aresta está no formato correto.
        '''

        # Não pode haver mais de um caractere separador
        if aresta.count(Grafo.SEPARADOR_ARESTA) != Grafo.QTDE_MAX_SEPARADOR:
            return False

        # Índice do elemento separador
        i_traco = aresta.index(Grafo.SEPARADOR_ARESTA)

        # O caractere separador não pode ser o primeiro ou o último caractere da aresta
        if i_traco == 0 or aresta[-1] == Grafo.SEPARADOR_ARESTA:
            return False

        if not(self.existeVertice(aresta[:i_traco])) or not(self.existeVertice(aresta[i_traco+1:])):
            return False

        return True

    @classmethod
    def verticeValido(self, vertice: str):
        '''
        Verifica se um vértice passado como parâmetro está dentro do padrão estabelecido.
        Um vértice é um string qualquer que não pode ser vazio e nem conter o caractere separador.
        :param vertice: Um string que representa o vértice a ser analisado.
        :return: Um valor booleano que indica se o vértice está no formato correto.
        '''
        return vertice != '' and vertice.count(Grafo.SEPARADOR_ARESTA) == 0

    def existeVertice(self, vertice: str):
        '''
        Verifica se um vértice passado como parâmetro pertence ao grafo.
        :param vertice: O vértice que deve ser verificado.
        :return: Um valor booleano que indica se o vértice existe no grafo.
        '''
        return Grafo.verticeValido(vertice) and self.N.count(vertice) > 0

    def __primeiro_vertice_aresta(self, a: str):
        '''
        Dada uma aresta no formato X-Y, retorna o vértice X
        :param a: a aresta a ser analisada
        :return: O primeiro vértice da aresta
        '''
        return a[0:a.index(Grafo.SEPARADOR_ARESTA)]

    def __segundo_vertice_aresta(self, a: str):
        '''
        Dada uma aresta no formato X-Y, retorna o vértice Y
        :param a: A aresta a ser analisada
        :return: O segundo vértice da aresta
        '''
        return a[a.index(Grafo.SEPARADOR_ARESTA)+1:]

    def __indice_primeiro_vertice_aresta(self, a: str):
        '''
        Dada uma aresta no formato X-Y, retorna o índice do vértice X na lista de vértices
        :param a: A aresta a ser analisada
        :return: O índice do primeiro vértice da aresta na lista de vértices
        '''
        return self.N.index(self.__primeiro_vertice_aresta(a))

    def __indice_segundo_vertice_aresta(self, a: str):
        '''
        Dada uma aresta no formato X-Y, retorna o índice do vértice Y na lista de vértices
        :param a: A aresta a ser analisada
        :return: O índice do segundo vértice da aresta na lista de vértices
        '''
        return self.N.index(self.__segundo_vertice_aresta(a))

    def existeAresta(self, a: str):
        '''
        Verifica se uma aresta passada como parâmetro pertence ao grafo.
        :param aresta: A aresta a ser verificada
        :return: Um valor booleano que indica se a aresta existe no grafo.
        '''
        existe = False
        if Grafo.arestaValida(self, a):
            for i in range(len(self.M)):
                for j in range(len(self.M)):
                    if self.M[self.__indice_primeiro_vertice_aresta(a)][self.__indice_segundo_vertice_aresta(a)]:
                        existe = True

        return existe

    def adicionaVertice(self, v):
        '''
        Inclui um vértice no grafo se ele estiver no formato correto.
        :param v: O vértice a ser incluído no grafo.
        :raises VerticeInvalidoException se o vértice já existe ou se ele não estiver no formato válido.
        '''
        if v in self.N:
            raise VerticeInvalidoException('O vértice {} já existe'.format(v))

        if self.verticeValido(v):
            if len(v) > self.__maior_vertice:
                self.__maior_vertice = len(v)

            self.N.append(v) # Adiciona vértice na lista de vértices
            self.M.append([]) # Adiciona a linha

            for k in range(len(self.N)):
                if k != len(self.N) -1:
                    self.M[k].append([]) # adiciona os elementos da coluna do vértice
                    self.M[self.N.index(v)].append('-') # adiciona os elementos da linha do vértice
                else:
                    self.M[self.N.index(v)].append([])  # adiciona um zero no último elemento da linha
        else:
            raise VerticeInvalidoException('O vértice ' + v + ' é inválido')

    def adicionaAresta(self, a,peso):
        '''
        Adiciona uma aresta ao grafo no formato X-Y, onde X é o primeiro vértice e Y é o segundo vértice
        :param a: a aresta no formato correto
        :raise: lança uma exceção caso a aresta não estiver em um formato válido
        '''
        if self.arestaValida(a):
            i_a1 = self.__indice_primeiro_vertice_aresta(a)
            i_a2 = self.__indice_segundo_vertice_aresta(a)
            if i_a1 < i_a2:
                self.M[i_a1][i_a2].append(peso)
            else:
                self.M[i_a2][i_a1].append(peso)
        else:
            raise ArestaInvalidaException('A aresta {} é inválida'.format(a))

    def remove_aresta(self, a,peso):
        '''
        Remove uma aresta ao grafo no formato X-Y, onde X é o primeiro vértice e Y é o segundo vértice
        :param a: a aresta no formato correto
        :raise: lança uma exceção caso a aresta não estiver em um formato válido
        '''
        if self.arestaValida(a):
            if self.existeAresta(a):
                i_a1 = self.__indice_primeiro_vertice_aresta(a)
                i_a2 = self.__indice_segundo_vertice_aresta(a)
                if i_a1 < i_a2:
                    self.M[i_a1][i_a2].remove(peso)
                else:
                    self.M[i_a2][i_a1].remove(peso)
        else:
            raise ArestaInvalidaException('A aresta {} é inválida'.format(a))



    def vertices_nao_adjacentes(self):
        lista=[]
        for i in range(len(self.M)):
            for j in range(len(self.M[i])):
                if self.M[i][j] == 0 :
                    lista.append(self.N[i]+self.SEPARADOR_ARESTA+self.N[j])

        return lista

    def ha_laco(self):
        for i in range(len(self.M)):
            for j in range(len(self.M[i])):
                if self.M[i][j] != 0 and self.M[i][j] != self.SEPARADOR_ARESTA and self.N[i] == self.N[j]:
                    return True


    def ha_paralelas(self):
        for i in range(len(self.M)):
            for j in range(len(self.M[i])):
                if self.M[i][j]==2:
                    return True



    def grau(self,v):
        c=0
        n=0
        for i in range(len(self.M)):
            for j in range(len(self.M[i])):
                if self.M[i][j]!=self.SEPARADOR_ARESTA:
                    n=int(self.M[i][j])
                    if n>=1 and self.N[i]==v or self.N[j]==v:
                        c+=n
        return c


    def arestas_sobre_vertice(self,v):
        lista=[]
        n=0
        for i in range(len(self.M)):
            for j in range(len(self.M[i])):
                if self.M[i][j]!=self.SEPARADOR_ARESTA:
                    n=int(self.M[i][j])
                    if ( (n >= 1) and (self.N[i] == v or self.N[j] == v) ):
                        for c in range(n):
                            lista.append(self.N[i] + self.SEPARADOR_ARESTA + self.N[j])

        return lista



    def eh_completo(self):
        '''
        Analisa a matriz levando em consideracao apenas os elementos presentes acima
        da diagonal principal ao menos um deles seja 0 quer dizer que o grafo nao
        eh completo
        :return: Valor booleano que indica se o grafo eh completo ou nao
        '''
        matriz = self.M

        for i in range(len(matriz)):
            for j in range(len(matriz[i])):
                if i - j < 0:
                    if matriz[i][j] == 0:
                        return False
        return True






    def eh_conexo(self):
        vertices = self.N
        conexos = set()

        self.eh_conexo_aux(vertices[0], conexos)

        for i in vertices:
            if i not in conexos:
                return False
        return True

    def eh_conexo_aux(self, vertice='', conexos=set()):
        matriz = self.M
        vertices = self.N

        for i in range(len(matriz)):
            for j in range(len(matriz[i])):
                if i - j < 0 and len(matriz[i][j]) > 0:
                    if i == vertices.index(vertice) and vertices[j] not in conexos:
                        conexos.add(vertices[j])
                        self.eh_conexo_aux(vertices[j], conexos)

                    if j == vertices.index(vertice) and vertices[i] not in conexos:
                        conexos.add(vertices[i])

                        self.eh_conexo_aux(vertices[i], conexos)



    def quantidade_de_arestas(self):
        quantidade_de_arestas1 = 0
        for i in range(len(self.M)):
            for j in range(len(self.M[i])):
                if (self.M[i][j] == 1):
                    quantidade_de_arestas1 += 1

        return quantidade_de_arestas1


    def aresta_sobre_vertice_com_peso(self,v):
        copy = deepcopy(self.M)
        lista = []
        for i in range(len(copy)):
            for j in range(len(copy[i])):
                if copy[i][j] != self.SEPARADOR_ARESTA:

                    if len(copy[i][j])>=1 and (self.N[i]==v or self.N[j]==v):
                        aresta = self.N[i] + self.SEPARADOR_ARESTA + self.N[j]
                        if aresta not in lista:
                            lista.append(aresta)
        return lista

    def menor_peso_da_aresta(self):
        dic = {}
        copia = deepcopy(self.M)
        for i in range(len(self.M)):
            for j in range(len(self.M[i])):
                if (len(self.M[i][j]) != 0) and (self.M[i][j]!= self.SEPARADOR_ARESTA):
                    aresta = '{}{}{}'.format(self.N[i],self.SEPARADOR_ARESTA,self.N[j])
                    dic[aresta]=min(self.M[i][j])

        return dic



    def procura(self,v,lista=[]):
        v1=v
        print(v)
        print(lista)
        if len(lista)>0:
            for i in lista:
                print(i)
                if v1 not in i:
                    return True
                else:
                    return False
        return True





    '''
    - Roteiro 8 - Minimum Spanning Tree, Inicio -
    '''

    sets = {}

    def criar_floresta(self,v):
        self.sets[v]=[v]

    def procura(self,v):
        for i,x in self.sets.items():
            if v in x:
                return i
        return None


    def uniao(self,v1,v2):
        vertice1 = self.procura(v1)
        vertice2 = self.procura(v2)
        self.sets[vertice1]=self.sets[vertice1]+self.sets[vertice2]
        del self.sets[vertice2]


    def Kruskall_modificado(self):
        """
        Algoritmo original de Kruskal para encontrar a Árvore de Extensão Mínima (Minimum Spanning Tree) do Grafo.
        :return: Um Grafo/Árvore representando a Minimum Spanning Tree.
        """
        #Cria o Grafo/Árvore
        arvore_minima = Grafo ()

        for i in self.N:
            self.criar_floresta(i)

        arvore = []
        dicionarioArestasComPesos = self.menor_peso_da_aresta()
        arestas_menor_peso = self.menor_peso_da_aresta()
        arestas_menor_peso = arestas_menor_peso.values()
        vertices_não_presentes_na_arvore = self.N
        if self.eh_conexo():
            for a in arestas_menor_peso:
                for i in dicionarioArestasComPesos:
                    if dicionarioArestasComPesos[i]== a:
                        if self.procura(i[0]) != self.procura(i[2]):
                            v1=i[0]
                            v2=i[2]
                            arvore.append(i)
                            arvore.append(v1)
                            arvore.append(v2)
                            existe_vertice1 = arvore_minima.existeVertice(v1)
                            existe_vertice2 = arvore_minima.existeVertice(v2)
                            if not existe_vertice1:
                                arvore_minima.adicionaVertice(v1)
                            if not existe_vertice2:
                                arvore_minima.adicionaVertice(v2)
                            if not (existe_vertice1 and existe_vertice2) or (existe_vertice1 and existe_vertice2):
                                arvore_minima.adicionaAresta(i,a)
                            self.uniao(v1,v2)
            return arvore_minima


    def procurar_na_arvore(self,vertice,lista=[]):
        if vertice not in lista:
            return True
        else:
            return False



    def dicionario_peso_aresta(self):
        dic = {}
        copia = deepcopy(self.M)
        for i in range(len(self.M)):
            for j in range(len(self.M[i])):
                if (len(self.M[i][j]) != 0) and (self.M[i][j] != self.SEPARADOR_ARESTA):
                    aresta = '{}{}{}'.format(self.N[i], self.SEPARADOR_ARESTA, self.N[j])
                    dic[aresta] = self.M[i][j]

        return dic

    def vertices_adjacentes(self, v):
        lista_vertices_adjacentes = []
        posição = self.N.index(v)
        for i in range(len(self.M)):
            if i < posição:
                if self.M[i][posição]:
                    lista_vertices_adjacentes.append(self.N[i])
            elif i == posição:
                for j in range(posição, len(self.M[i])):
                    if self.M[i][j]:
                        lista_vertices_adjacentes.append(self.N[j])
            else:
                break
        return lista_vertices_adjacentes

    def criar_aresta(self,v1,v2):
        aresta = "{}{}{}".format(v1,self.SEPARADOR_ARESTA,v2)
        return aresta


    def PrimModificado(self):
        from math import inf
        vertices = deepcopy(self.N)
        arestas = []
        for i in range(len(self.M)):
            for j in range(len(self.M[i])):
                if (len(self.M[i][j]) != 0) and (self.M[i][j] != self.SEPARADOR_ARESTA):
                    aresta1 = '{}{}{}'.format(self.N[i], self.SEPARADOR_ARESTA, self.N[j])
                    arestas.append(aresta1)
        dic_peso = self.dicionario_peso_aresta()
        Jet = {}
        P = {}
        guarda_peso = inf
        guarda_aresta =''
        arvore = Grafo()
        for vertice in vertices:
            Jet[vertice] = inf
            P[vertice] = None

        for aresta in arestas:
            listap= dic_peso[aresta]
            peso = listap[0]
            if peso< guarda_peso:
                guarda_peso = peso
                guarda_aresta = aresta
                v1,v2 = aresta.split(self.SEPARADOR_ARESTA)
        Jet[v1] = 0
        lista_prioridade = deepcopy(self.N)
        while(len(lista_prioridade)!=0):
            menor_peso = inf
            vertice_menor_peso = ''
            for v in lista_prioridade:
                if isinstance(Jet[v],list)==True:#problema é aqui
                    jet = Jet[v][0]
                    if jet<menor_peso:
                        pesolista = Jet[v]
                        menor_peso = pesolista[0]
                        vertice_menor_peso= v
                else:
                    if Jet[v] < menor_peso:
                        menor_peso = Jet[v]
                        vertice_menor_peso = v
            x = vertice_menor_peso

            lista_prioridade.pop(lista_prioridade.index(vertice_menor_peso))
            lista_vertices_adjacente = self.vertices_adjacentes(x)
            for vertice_adjacente in lista_vertices_adjacente:
                aresta_y = x+"-"+vertice_adjacente
                if aresta_y not in arestas:
                    aresta_y = vertice_adjacente+'-'+x
                pesoy = dic_peso[aresta_y][0]
                jety = Jet[vertice_adjacente]
                if isinstance(jety,list)==True:
                    if vertice_adjacente in lista_prioridade and pesoy<jety[0]:
                        P[vertice_adjacente] = x
                        Jet[vertice_adjacente]= dic_peso[aresta_y]
                else:
                    if vertice_adjacente in lista_prioridade and pesoy<jety:
                        P[vertice_adjacente] = x
                        Jet[vertice_adjacente]= dic_peso[aresta_y]
        for v in vertices:
            arvore.adicionaVertice(v)
        lista_final = []
        for a,i in P.items():
            if i:
                lista_final.append(self.criar_aresta(i,a))
        dic_menor_peso = self.menor_peso_da_aresta()
        for i in lista_final:
            if i in dic_menor_peso:
                arvore.adicionaAresta(i,dic_menor_peso[i])

        return arvore
    def __str__(self):
        '''
        Fornece uma representação do tipo String do grafo.
        O String contém um sequência dos vértices separados por vírgula, seguido de uma sequência das arestas no formato padrão.
        :return: Uma string que representa o grafo
        '''

        # Dá o espaçamento correto de acordo com o tamanho do string do maior vértice
        espaco = ' '*(self.__maior_vertice)

        grafo_str = espaco + ' '

        for v in range(len(self.N)):
            grafo_str += self.N[v]
            if v < (len(self.N) - 1):  # Só coloca o espaço se não for o último vértice
                grafo_str += ' '

        grafo_str += '\n'

        for l in range(len(self.M)):
            grafo_str += self.N[l] + ' '
            for c in range(len(self.M)):
                if self.M[l][c] =='-':
                    grafo_str += '-' + ' '
                else:
                    grafo_str += str(len(self.M[l][c])) + ' ' #recebe o tamanho de self.M[l][c] pois se tiverem dois pesos, então haverá duas arestas, se não tiver nenhum, n tem aresta e o len==0
            grafo_str += '\n'

        return grafo_str































