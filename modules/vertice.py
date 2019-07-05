class Vertice:
    def __init__(self, nome):
        self.nome = str(nome)
        self.visit = False
        self.adjcs = []

    # def __str__(self):
    #     return "«{0}» em:{1}".format(self.nome, id(self))
