from random import sample, randint
from vertice import Vertice
from aresta import Aresta
import ast
import itertools
# import json


class Grafo:
    def __init__(self, qtd_vertices):
        self.qtd_vertices = qtd_vertices
        self.nome = "grafo_" + str(self.qtd_vertices)
        __vertice_list__ = list(range(1, int(qtd_vertices + 1)))
        self.vertices = []
        for vertice in __vertice_list__:
            self.vertices.append(Vertice(vertice))
        self.arestas = set()
        self.matriz_adjacencia = []
        for k in range(0, qtd_vertices):
            self.matriz_adjacencia.append(list(itertools.repeat(0, int(qtd_vertices))))
        self.lista_adjacencia = []

    def __iter__(self):
        yield self.nome
        yield from self.vertices
        yield from self.arestas

    def add_matriz_adj(self, vertc):
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

    def del_matriz_adj(self, vertc):
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
        aresta = set()
        if not vertices:
            vertices = self.vertices
        for v_part in vertices:
            v_destino = sample(vertices, randint(0, qtd_arestas_max))
            aresta.add(v_part)
            for v_dest in v_destino:
                aresta.add(v_dest)
                if len(aresta) == 2:
                    a = Aresta(aresta)
                    self.arestas.add(a)
                else:
                    pass
                #     while v_part is v_dest:
                #         desvio = v_dest
                #         v_destino.remove(v_dest)
                #         if len(v_destino) > 1:
                #             v_dest = sample(v_destino, 1)[0]
                #         else:
                #             v_destino.insert(0, desvio)
                #             break
                if v_dest.nome != v_part.nome:
                    # if not(any((v_dest, v_part) in a for a in self.arestas) and any((v_part, v_dest) in a for a in self.arestas)):
                    #     self.arestas.add(Aresta([v_part, v_dest]))
                    self.add_matriz_adj(v_part)
                    self.add_matriz_adj(v_dest)
            aresta.clear()
        if all(type(x) is Vertice for x in vertices):
            for v in vertices:
                self.lista_adjacencia.append(self.vizinhos(v))
        else:
            TypeError("Um nao-vertice foi informado em {0}".format(vertices))
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
                        for a in self.arestas:
                            if vv in (a.vert_ini, a.vert_des):
                                self.arestas.remove(a)
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
                    # self.arestas.sort()
                    self.del_matriz_adj(vert)

    def insert_aresta(self, aresta):
        if aresta is Aresta:  # Esperando uma aresta do TIPO Aresta
            for v in aresta.lista_vertices:  # se ligar um vertice existente a um não existente, cria novo vertice
                if v not in self.vertices:
                    self.insert_vertices(v)
            if aresta not in self.arestas:  # Verificar se já existe a aresta
                self.arestas.add(aresta)
                # self.arestas.sort()
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
            grf.arestas.add(Aresta(lista))   # para gerar uma aresta com esses 2 vertices
            lista.clear()  # limpa a lista parcial para recomeçar
        else:
            grf.arestas.add(Aresta(a))  # caso não ache o vertice em vértices, registra como uma lista de vertices, não uma resta
    for x in range(0, grf.qtd_vertices):  # reeinicia a matriz de adjacencia vazia com os vértices inseridos anteriormente
        grf.matriz_adjacencia.append(list(itertools.repeat(0, grf.qtd_vertices)))
    for v in grf.vertices:
        grf.add_matriz_adj(v)  # popular matriz de adjacencia vazia com os vértices inseridos anteriormente
        grf.lista_adjacencia.append(grf.vizinhos(v))  # popular lista de adjacências
    return grf


# def salvar_em_arquivo(grafo, arq):
#     pass
