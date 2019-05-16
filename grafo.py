from random import sample, randint
import json


class Grafo:
    def __init__(self, qtd_vertices):
        self.qtd_vertices = qtd_vertices
        self.nome = "grafo_" + str(self.qtd_vertices)
        self.vertices = list(range(1, int(qtd_vertices + 1)))
        self.arestas = []

    def gerate_arestas(self, vertices, qtd_arestas):
        if not vertices:
            vertices = self.vertices
            for vp in vertices:
                v_dest = sample(vertices, qtd_arestas)
                for vd in v_dest:
                    while vp is vd:
                        desvio = vd
                        v_dest.remove(vd)
                        if len(v_dest) > 1:
                            vd = sample(v_dest, 1)[0]
                        else:
                            v_dest.insert(0, desvio)
                            break
                    if [vd, vp] not in self.arestas:
                        self.arestas.append([vp, vd])
        return len(self.arestas)

    def insert_vertice(self):
        # inserir vertice da lista de vertices
        pass

    def remove_vertice(self):
        # remover vertice da lista de vertices
        # remover arestas que possuem esse vertice
        pass

    def insert_aresta(self):
        # verificar existencia, caso não exista:
        #    # inserir aresta da lista de arestas
        pass

    def remove_aresta(self):
        # verificar existencia, caso exista:
        #   # remover aresta da lista de arestas
        pass

    def vizinhos(self, vertice):
        # verificar se existe arestas que contem o vertice
        # adicionar o outro vertice da aresta a lista
        # retornar a lista de vizinhos
        pass


def ler_de_arquivo(arq):
    pass


def salvar_em_arquivo(grafo, arq):
    pass


def gerar_grafo_randomico(qtd_vertices):
    nome = ("grafo_" + str(qtd_vertices))
    vertices = []
    arestas = []
    qtd_vertices = int(qtd_vertices)
    for v in range(1, (qtd_vertices + 1)):
        vertices.append(v)
    for vp in vertices:
        qtd_arestas = randint(1, round((qtd_vertices - 1)/2) + 1)
        v_destinos = sample(vertices, qtd_arestas)
        for vd in v_destinos:
            while vp is vd:
                desvio = vd
                v_destinos.remove(vd)
                if len(v_destinos) > 1:
                    vd = sample(v_destinos, 1)[0]
                else:
                    v_destinos.insert(0, desvio)
                    break
            if [vd, vp] not in arestas:
                arestas.append([vp, vd])
    return {"nome": nome, "vertices": vertices, "arestas": arestas}


def ler_grafo_de(arq):
    if not isinstance(arq, _io.TextIOWrapper):
        raise TypeError("arq deve ser um arquivo")
    else:
        g = json.load(arq)
    return g


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


def transforma_em_mda(g):
    return []


def adiciona_vertice_em(arq, v=int):
    g = {}
    g.update(ler_grafo_de(arq))
    vertices = g['vertices']
    vertices.append[v]
    return dict(grafo=g)


def remove_vertice_em(arq, v=int):
    g = {}
    g.update(ler_grafo_de(arq))
    list(g['vertices']).remove(v)
    for e in list(g['arestas']):
        list(e).remove(v)
        if len(list(e)) < 2:
            list(e).clear()
    return dict(grafo=g)
