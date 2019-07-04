from random import sample, randint
# import json
import ast
import itertools


class Vertice:
    def __init__(self, nome):
        self.nome = str(nome)
        self.visit = False
        self.adjcs = []

    def __str__(self):
        return "«{0}» em:{1}".format(self.nome, id(self))


class Aresta:
    def __init__(self, nome):
        if type(nome) is list and len(nome) == 2:
            if type(nome[0]) is Vertice:
                self.vert_ini = nome[0]
            else:
                self.vert_ini = Vertice(nome[0])
            if type(nome[1]) is Vertice:
                self.vert_des = nome[1]
            else:
                self.vert_des = Vertice(nome[1])
        else:
            self.nome = str(nome)
            self.vert_ini = Vertice(nome[0])
            self.vert_des = Vertice(nome[1])
        self.nome = "{0}{1}".format(self.vert_ini.nome, self.vert_des.nome)
        self.lista_vertices = (self.vert_ini, self.vert_des)
        self.visit = False
        self.explo = False
        self.desco = False

    def __iter__(self):
        yield self.nome
        yield self.lista_vertices
        yield self.vert_ini
        yield self.vert_des

    def __str__(self):
        return "[({0}): em: {1}]".format(self.nome, id(self))


class Grafo:
    def __init__(self, qtd_vertices):
        self.qtd_vertices = qtd_vertices
        self.nome = "grafo_" + str(self.qtd_vertices)
        __vertice_list__ = list(range(1, int(qtd_vertices + 1)))
        self.vertices = []
        for vertice in __vertice_list__:
            self.vertices.append(Vertice(vertice))
        self.arestas = []
        self.matriz_adjacencia = []
        for lin in __vertice_list__:
            self.matriz_adjacencia.append(list(itertools.repeat(0, int(qtd_vertices))))
        self.lista_adjacencia = []

    def __iter__(self):
        yield self.nome
        yield from self.vertices
        yield from self.arestas

    def add_matriz_adj(self, vertc):  # TODO: atualizar para o TIPO vertice
        for aresta in self.arestas:
            if type(vertc) is Vertice and vertc in aresta:
                self.matriz_adjacencia[int(aresta.lista_vertices[0].nome) - 1][int(aresta.lista_vertices[1].nome) - 1] = 1
                self.matriz_adjacencia[int(aresta.lista_vertices[1].nome) - 1][int(aresta.lista_vertices[0].nome) - 1] = 1
            else:
                if type(vertc) is not Vertice:
                    raise TypeError("%s nao e um Vertice" % str(type(vertc)))
                if vertc not in aresta:
                    pass  # raise ValueError("Vertice inexistente: {0}", vertc.nome)
        return None

    def del_matriz_adj(self, vertc):  # TODO: atualizar para o TIPO vertice
        for aresta in self.arestas:
            if type(vertc) is Vertice and vertc in aresta:
                if vertc is aresta:
                    self.matriz_adjacencia[int(aresta[0].nome) - 1][int(aresta[1].nome) - 1] = 1
                    self.matriz_adjacencia[int(aresta[1].nome) - 1][int(aresta[0].nome) - 1] = 1
            else:
                if type(vertc) is not Vertice:
                    raise TypeError(" %s nao e um Vertice" % str(vertc))
                if vertc not in aresta:
                    raise ValueError("Vertice inexistente: %s" % vertc.nome)
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
                    if ([vd, vp] or [vp, vd]) not in self.arestas:
                        self.arestas.append(Aresta([vp, vd]))
                        self.add_matriz_adj(vp)
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
                for c in self.matriz_adjacencia:
                    c.append(0)
                self.matriz_adjacencia.append(list(itertools.repeat(0, int(len(self.vertices)))))
        else:
            self.vertices.append(Vertice(vertice))
            for c in self.matriz_adjacencia:
                c.append(0)
            self.matriz_adjacencia.append(list(itertools.repeat(0, int(len(self.vertices)))))

    def remove_vertices(self, vert):
        # remover vertice da lista de vertices
        if type(vert) is list:  # Se for uma lista de vertices
            for v in vert:
                if vert is Vertice:
                    for vv in self.vertices:
                        if vv.nome == str(v):
                            self.vertices.remove(vv)
                        # remover arestas que possuem esse vertice
                        for a in self.arestas:  # TODO: mudar aresta para o TIPO Aresta
                            if vv in (a.vert_ini, a.vert_des):
                                self.arestas.remove(a)  # TODO: atualizar a matriz de adjacencias
                                self.del_matriz_adj(vv)
                else:
                    raise TypeError("O valor informado deve der um Vertice.\n Informado: " + str(type(vert)))
        else:   # Se vertice for somente um Vertice
            if vert is Vertice:
                self.vertices.remove(vert)
                self.del_matriz_adj(vert)
            else:
                raise TypeError("O valor informado deve der um Vertice.\n Informado: " + str(type(vert)))
            for a in self.arestas:  # remover arestas que possuem esse vertice
                if vert in a:
                    self.arestas.remove(a)
                    self.arestas.sort()
                    self.del_matriz_adj(vert)

    def insert_aresta(self, aresta):
        if aresta is Aresta:  # Esperando uma aresta do TIPO Aresta
            for v in aresta.lista_vertices:  # se ligar um vertice existente a um não existente, cria novo vertice
                if v not in self.vertices:
                    self.insert_vertices(v)
            if aresta not in self.arestas:  # Verificar se já existe a aresta
                self.arestas.append(aresta)
                self.arestas.sort()
                self.add_matriz_adj(aresta.vert_ini)  # atualiza a matriz de adjacência
                self.add_matriz_adj(aresta.vert_des)
            else:
                raise ValueError("A aresta " + str(aresta) + "já existe neste grafo")
        else:
            raise TypeError("A aresta deve de tipo Aresta\n informado: " + type(aresta))

    def remove_aresta(self, aresta):
        if aresta is Aresta:
            if aresta not in self.arestas:
                raise ValueError("A aresta " + aresta.nome + "não existe neste grafo")
            else:
                self.arestas.remove(aresta)
                self.del_matriz_adj(aresta.vert_ini)  # atualiza a matriz de adjacência
                self.del_matriz_adj(aresta.vert_des)
        else:
            raise TypeError("A aresta deve do tipo Aresta\n informado: " + str(aresta))

    def vizinhos(self, vertice):
        if type(vertice) is Vertice:
            vizinhos = []
            if vertice in self.vertices:  # verificar se existe arestas que contem o vertice
                for aresta in self.arestas:
                    for v in aresta.lista_vertices:
                        if vertice in aresta.lista_vertices \
                                and v.nome != vertice.nome \
                                and int(v.nome) not in vizinhos:
                            vizinhos.append(int(v.nome))  # adicionar o outro vertice da aresta a lista
            else:
                raise ValueError("Vertice não encontrado no grafo: " + vertice.nome)
        else:
            TypeError("Valor informado não é um vertice")
            return None
        vizinhos.sort()
        return vizinhos  # retornar a lista de vizinhos


def ler_de_arquivo(arq):
    cont = open(arq, 'r').read()
    dic = ast.literal_eval(cont)
    grf = Grafo(0)  # Cria um Grafo vazio
    grf.nome = dic['nome']  # Extrai o nome do arquivo e inclui direto no grafo vazio
    lista = []
    # grf.vertices = dic['vertices']
    for v in dic['vertices']:
        grf.vertices.append(Vertice(v))  # Cria um Vertice para cada vertice extraido do arquivo e inclui em vertices
    grf.qtd_vertices = int(len(grf.vertices))  # atualiza o Numero de vertices
    # grf.arestas = dic['arestas']
    for a in dic['arestas']:                    # para cada aresta do arquivo...
        if type(a) is list and len(a) == 2:     # verifica se é válida (uma lista com 2 elementos)...
            for v in a:                         # e para cada elemento dessa lista de 2...
                for vertc in grf.vertices:      # verifica se corresponde a um vertice obtidos...
                    if str(v) == vertc.nome:    # através do nome...
                        lista.append(vertc)     # e junta a uma lista parcial...
            grf.arestas.append(Aresta(lista))   # para gerar uma aresta com esses 2 vertices
            lista.clear()  # limpa a lista parcial para recomeçar
        else:
            grf.arestas.append(Aresta(a))  # caso não ache o vertice em vértices, registra como uma lista de vertices, não uma resta
    for x in range(0, grf.qtd_vertices):  # reeinicia a matriz de adjacencia vazia com os vértices inseridos anteriormente
        grf.matriz_adjacencia.append(list(itertools.repeat(0, grf.qtd_vertices)))
    for v in grf.vertices:
        grf.add_matriz_adj(v)  # popular matriz de adjacencia vazia com os vértices inseridos anteriormente
        grf.lista_adjacencia.append(grf.vizinhos(v))  # popular lista de adjacências
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
