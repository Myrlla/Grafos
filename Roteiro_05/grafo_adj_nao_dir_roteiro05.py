# -*- coding: utf-8 -*-

class VerticeInvalidoException(Exception):
    pass

class ArestaInvalidaException(Exception):
    pass

class MatrizInvalidaException(Exception):
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
                        M[k].append(0)


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
                    self.M[k].append(0) # adiciona os elementos da coluna do vértice
                    self.M[self.N.index(v)].append('-') # adiciona os elementos da linha do vértice
                else:
                    self.M[self.N.index(v)].append(0)  # adiciona um zero no último elemento da linha
        else:
            raise VerticeInvalidoException('O vértice ' + v + ' é inválido')

    def adicionaAresta(self, a):
        '''
        Adiciona uma aresta ao grafo no formato X-Y, onde X é o primeiro vértice e Y é o segundo vértice
        :param a: a aresta no formato correto
        :raise: lança uma exceção caso a aresta não estiver em um formato válido
        '''
        if self.arestaValida(a):
            i_a1 = self.__indice_primeiro_vertice_aresta(a)
            i_a2 = self.__indice_segundo_vertice_aresta(a)
            if i_a1 < i_a2:
                self.M[i_a1][i_a2] += 1
            else:
                self.M[i_a2][i_a1] += 1
        else:
            raise ArestaInvalidaException('A aresta {} é inválida'.format(a))

    def remove_aresta(self, a):
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
                    self.M[i_a1][i_a2] -= 1
                else:
                    self.M[i_a2][i_a1] -= 1
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


    def ciclo_hamiltoniano(self):
        v=self.N[0]
        lista=[]
        self.ciclo_hamiltoniano_recursiva(v,lista)
        u=lista[-1]
        lista_vv=self.arestas_sobre_vertice(u)
        for i in lista_vv:
            v1,v2= i.split(self.SEPARADOR_ARESTA)
            if v1 or v2 == lista[0]:
                lista.append(i)
                lista.append(lista[0])

                for i in self.N:
                    if i not in lista:
                        return False
                return lista



    def ciclo_hamiltoniano_recursiva(self,v,lista=[]):
        lista_v=[]
        lista.append(v)
        lista_v=self.arestas_sobre_vertice(v)



        for i in lista_v:
            if i not in lista:
                v1,v2=i.split(self.SEPARADOR_ARESTA)
                if v1!=v and v1 not in lista:
                    lista.append(i)
                    self.ciclo_hamiltoniano_recursiva(v1,lista)
                elif v2!= v and v2 not in lista:
                    lista.append(i)
                    self.ciclo_hamiltoniano_recursiva(v2,lista)

                else:
                    break

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
                if i - j < 0 and matriz[i][j] > 0:
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

    def caminho_eureliano(self):
        conexo = self.eh_conexo()
        if conexo == True:
            vertices_impares = 0
            guarda_vertice_impar = []
            caminho_eureliano = []
            vertice_aleatorio = []
            for i in range(len(self.M)):
                for j in range(len(self.M[i])):
                    if self.M[i][j] != self.SEPARADOR_ARESTA:
                        vertice_aleatorio.append(self.N[i])
                        vertice = self.N[i]
                        lista_aresta_sobre_vertice = self.arestas_sobre_vertice(vertice)
                        if len(lista_aresta_sobre_vertice) == 1:
                            vertices_impares += 1
                            guarda_vertice_impar.append(vertice)
            if vertices_impares == 0:
                resposta = self.caminho_eureliano_sem_vertice_impar(caminho_eureliano, vertice_aleatorio[0])
                return resposta
            if vertices_impares == (len(self.N) + 1):
                vertice1 = guarda_vertice_impar[0]
                vertice2 = guarda_vertice_impar[1]
                resposta = self.caminho_eureliano_rec_com_vertice_impar(caminho_eureliano, vertice1, vertice2)
                return resposta
        return False

    def caminho_eureliano_sem_vertice_impar(self, lista, vertice):
        lista.append(vertice)
        lista_arestas = self.arestas_sobre_vertice(vertice)
        for a in lista_arestas:
            if a not in lista:
                v1 = a[0]
                v2 = a[2]
                if (v1 not in lista):
                    if a not in lista:
                        lista.append(a)
                        self.caminho_eureliano_sem_vertice_impar(lista, v1)
                if (v2 not in lista):
                    if a not in lista:
                        lista.append(a)
                        self.caminho_eureliano_sem_vertice_impar(lista, v2)

        if len(lista) == 0:
            return False
        else:
            vertice_inicial = self.N[0]
            lista_arestas_vertice_inicial = self.arestas_sobre_vertice(vertice_inicial)
            for i in range(len(self.M)):
                for j in range(len(self.M[i])):
                    vertice_inicial = self.N[i]

            for i in lista_arestas_vertice_inicial:
                aresta_final = i

            lista.append(aresta_final)
            return lista

    def caminho_eureliano_rec_com_vertice_impar(self, lista, vertice1, vertice2):
        lista.append(vertice1)
        lista_arestas = self.arestas_sobre_vertice(vertice1)
        for a in lista_arestas:
            if a not in lista:
                v1 = a[0]
                v2 = a[2]
                if (v1 not in lista) and (v2 not in lista):
                    if v1 != vertice1 and (v1 not in lista):
                        if v1 != vertice2:
                            lista.append(a)
                            self.caminho_eureliano_rec_com_vertice_impar(lista, v1, vertice2)
                        elif v1 == vertice2 and len(self.N) == (a + 1):
                            lista.append(vertice2)
                    elif v2 != vertice1 and (v2 not in lista):
                        if v2 != vertice2:
                            lista.append(a)
                            self.caminho_eureliano_rec_com_vertice_impar(lista, v2, vertice2)
                        elif v2 == vertice2 and len(self.N) == (a + 1):
                            lista.append(vertice2)

        if len(lista) < 3:
            return False

        return lista



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
                grafo_str += str(self.M[l][c]) + ' '
            grafo_str += '\n'

        return grafo_str































