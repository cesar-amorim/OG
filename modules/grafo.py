from random import sample, randint
# import json
import ast
import itertools


class Vertice:
    def __init__(self, nome):
        self.nome = str(nome)
        self.visit = False
        self.adjcs = []

    @property
    def __str__(self):
        return self.nome


class Aresta:
    def __init__(self, nome):
        self.nome = str(nome)
        self.vert_ini = Vertice(nome[0])
        self.vert_des = Vertice(nome[1])
        self.visit = False
        self.explo = False
        self.desco = False


class Grafo:
    def __init__(self, qtd_vertices):
        self.qtd_vertices = qtd_vertices
        self.nome = "grafo_" + str(self.qtd_vertices)
        __vertice_list__ = list(range(1, int(qtd_vertices + 1)))
        self.vertices = []
        for vertice in __vertice_list__:
            self.vertices.append(Vertice(vertice))
        self.arestas = []
        self.lista_adjacencia = []
        self.matriz_adjacencia = []
        for lin in __vertice_list__:
            self.matriz_adjacencia.append(list(itertools.repeat(0, int(qtd_vertices))))
        self.lista_adjacencia = []

    def __iter__(self):
        yield self.nome
        yield from self.vertices
        yield from self.arestas

    def refresh_matriz_adj(self):
        for aresta in self.arestas:
            self.matriz_adjacencia[int(aresta[0] - 1)][int(aresta[1] - 1)] = 1
            self.matriz_adjacencia[int(aresta[1] - 1)][int(aresta[0] - 1)] = 1
        return None

    def gerate_arestas(self, vertices, qtd_arestas_max):
        if not vertices:
            vertices = self.vertices
            for vp in vertices:
                v_dest = sample(vertices, randint(0, qtd_arestas_max))
                for vd in v_dest:
                    while int(vp.nome) is vd:
                        desvio = vd
                        v_dest.remove(vd)
                        if len(v_dest) > 1:
                            vd = sample(v_dest, 1)[0]
                        else:
                            v_dest.insert(0, desvio)
                            break
                    if ([vd, int(vp.nome)] or [int(vp.nome), vd]) not in self.arestas:
                        self.arestas.append([int(vp.nome), vd])
                        self.refresh_matriz_adj()
        return len(self.arestas)

    def purge_arestas(self):
        if len(self.arestas) != 0:
            self.arestas.clear()
            for lin in self.vertices:
                self.matriz_adjacencia.append(list(itertools.repeat(0, int(self.qtd_vertices))))

    def insert_vertices(self, vertice):
        # inserir vertice da lista de vertices
        if type(vertice) is list:
            for v in vertice:
                self.vertices.append(Vertice(v))
                self.matriz_adjacencia.append(list(itertools.repeat(0, int(len(self.vertices)))))
        else:
            self.vertices.append(Vertice(vertice))
            self.matriz_adjacencia.append(list(itertools.repeat(0, int(len(self.vertices)))))

    def remove_vertices(self, vertice):
        # remover vertice da lista de vertices
        if type(vertice) is list:  # Se for uma lista de vertices
            for v in vertice:
                self.vertices.remove(v)
                # remover arestas que possuem esse vertice
                for a in self.arestas:
                    if vertice in a:
                        self.arestas.remove(a)
        else:   # Se vertice for somente um vertice
            self.vertices.remove(vertice)
        # remover arestas que possuem esse vertice
            for a in self.arestas:
                if vertice in a:
                    self.arestas.remove(a)
                    self.arestas.sort()

    def insert_aresta(self, aresta):
        if (aresta is list) and (len(aresta) == 2):  # Esperando uma aresta no formato [a, b], onde a e b são vertices
            for v in aresta:  # se ligar um vertice existente a um vertice não existente, cria novo vertice
                if v not in self.vertices:
                    self.insert_vertices(v)
            if aresta not in self.arestas:  # Verificar se já existe a aresta
                self.arestas.append(aresta)
                self.arestas.sort()
                # atualiza a matriz de adjacência
                self.matriz_adjacencia[aresta[0]][aresta[1]] = 1
                self.matriz_adjacencia[aresta[1]][aresta[0]] = 1
            else:
                raise ValueError("A aresta " + str(aresta) + "já existe neste grafo")
        else:
            raise TypeError("A aresta deve ser uma lista com apenas 2 valores\n informado: " + str(aresta))

    def remove_aresta(self, aresta):
        if (aresta is list) and (len(aresta) == 2):
            if aresta not in self.arestas:
                raise ValueError("A aresta " + str(aresta) + "não existe neste grafo")
            else:
                self.arestas.remove(aresta)
                # atualiza a matriz de adjacência
                self.matriz_adjacencia[aresta[0]][aresta[1]] = 0
                self.matriz_adjacencia[aresta[1]][aresta[0]] = 0
        else:
            raise TypeError("A aresta deve ser uma lista com apenas 2 valores\n informado: " + str(aresta))

    def vizinhos(self, vertice):
        vizinhos = []
        # verificar se existe arestas que contem o vertice
        if vertice in self.vertices:
            for aresta in self.arestas:
                for v in aresta:
                    if vertice in aresta:
                        if str(v) != str(vertice):
                            vizinhos.append(v)  # adicionar o outro vertice da aresta a lista
        else:
            raise ValueError("Vertice não encontrado no grafo: " + str(vertice))
        # retornar a lista de vizinhos
        vizinhos.sort()
        return vizinhos


def ler_de_arquivo(arq):
    cont = open(arq, 'r').read()
    dic = ast.literal_eval(cont)
    grf = Grafo(0)
    grf.nome = dic['nome']
    grf.vertices = dic['vertices']
    grf.arestas = dic['arestas']
    return grf


def transforma_em_mda(g):
    return []


def salvar_em_arquivo(grafo, arq):
    pass


# def gerar_grafo_randomico(qtd_vertices):
#     nome = ("grafo_" + str(qtd_vertices))
#     vertices = []
#     arestas = []
#     qtd_vertices = int(qtd_vertices)
#     for v in range(1, (qtd_vertices + 1)):
#         vertices.append(v)
#     for vp in vertices:
#         qtd_arestas = randint(1, round((qtd_vertices - 1)/2) + 1)
#         v_destinos = sample(vertices, qtd_arestas)
#         for vd in v_destinos:
#             while vp is vd:
#                 desvio = vd
#                 v_destinos.remove(vd)
#                 if len(v_destinos) > 1:
#                     vd = sample(v_destinos, 1)[0]
#                 else:
#                     v_destinos.insert(0, desvio)
#                     break
#             if [vd, vp] not in arestas:
#                 arestas.append([vp, vd])
#     return {"nome": nome, "vertices": vertices, "arestas": arestas}


# def ler_grafo_de(arq):
#     if not isinstance(arq, _io.TextIOWrapper):
#         raise TypeError("arq deve ser um arquivo")
#     else:
#         g = json.load(arq)
#     return g


# class Grafo(dict):
#     # def _get_grafo(self):
#     #     return self.__grafo
#     #
#     # def _set_grafo(self, value):
#     #     if not isinstance(value, dict):
#     #         raise TypeError("g deve ser um Dicionário")
#     #     self.__grafo = value
#
#     def _get_nome(self):
#         return self.nome
#
#     def _set_nome(self, valor):
#         if not isinstance(valor, str):
#             raise TypeError("O valor deve ser uma string")
#
#     nome = property(_get_nome, _set_nome)
#
#     def _get_vertices(self):
#         return self.vertices
#
#     def _set_vertices(self, valor):
#         if not isinstance(valor, list):
#             raise TypeError("O valor deve ser uma lista")
#
#     vertices = property(_get_vertices, _set_vertices)
#
#     # grafo = property(_get_grafo, _set_grafo)




# def adiciona_vertice_em(arq, v=int):
#     g = {}
#     g.update(ler_grafo_de(arq))
#     vertices = g['vertices']
#     vertices.append[v]
#     return dict(grafo=g)
#
#
# def remove_vertice_em(arq, v=int):
#     g = {}
#     g.update(ler_grafo_de(arq))
#     list(g['vertices']).remove(v)
#     for e in list(g['arestas']):
#         list(e).remove(v)
#         if len(list(e)) < 2:
#             list(e).clear()
#     return dict(grafo=g)
