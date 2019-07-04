from vertice import Vertice


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
