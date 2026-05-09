class Noeud:
    def __init__(self, question, sioui, sinon):
        self.question = question
        self.sioui = sioui
        self.sinon = sinon

    def est_resultat(self):
        return False

    def nb(self):
        return self.sioui.nb() + self.sinon.nb()

    def liste_question(self):
       return [self.question] + self.sioui.liste_question() + self.sinon.liste_question()

class Feuille:
    def __init__(self, vegetaux):
        self.vegetaux = vegetaux

    def est_resultat(self):
        return True

    def nb(self):
        return len(self.vegetaux)

    def liste_question(self):
       return []


if __name__ == '__main__':
    n_bord_dente = Noeud("bord dente", Feuille(["sorbier"]), Feuille(["robinier", "noyer"]))
    n_alternee = Noeud("alternee", n_bord_dente, Feuille([]))
    a = Noeud("simple", Feuille([]), n_alternee)

    print(a.nb())
    ret = a.liste_question()
    for elt in ret:
        print(elt)
