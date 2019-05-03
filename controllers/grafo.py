from random import *
import json


def gerar_grafo_randomico(qtd_vertices):
    nome = ("grafo_" + str(qtd_vertices))
    vertices = []
    arestas = []
    qtd_vertices = int(qtd_vertices)
    vertices.append(range(1, (qtd_vertices + 1)))
    for vp in vertices:
        qtd_arestas = randint(1, (qtd_vertices + 1))
        v_destinos = sample(vertices, qtd_arestas)
        for vd in v_destinos:
            if vp is vd:
                v_desvios = v_destinos.remove(vd)
                vd = sample(v_desvios, 1)
            arestas.append([vp, vd])

    return dict(grafo=gerar_grafo_randomico)


def ler_grafo_de(arq):
    g = json.loads(arq)
    return g


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
