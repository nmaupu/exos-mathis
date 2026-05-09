package main

import "fmt"

type Arbre interface {
	EstResultat() bool
	Nb() int
	ListeQuestion() []string
}

type Noeud struct {
	Question string
	SiOui    Arbre
	SiNon    Arbre
}

func (n Noeud) EstResultat() bool {
	return false
}

func (n Noeud) Nb() int {
	return n.SiOui.Nb() + n.SiNon.Nb()
}

func (n Noeud) ListeQuestion() []string {
	return append([]string{n.Question},
		append(n.SiOui.ListeQuestion(), n.SiNon.ListeQuestion()...)...)
}

type Feuille struct {
	Vegetaux []string
}

func (f Feuille) EstResultat() bool {
	return true
}

func (f Feuille) Nb() int {
	return len(f.Vegetaux)
}

func (f Feuille) ListeQuestion() []string {
	return []string{}
}

func main() {
	arbre := Noeud{
		Question: "simple",
		SiOui:    Feuille{Vegetaux: []string{}},
		SiNon: Noeud{
			Question: "alternee",
			SiOui: Noeud{
				Question: "bord dente",
				SiOui:    Feuille{Vegetaux: []string{"sorbier"}},
				SiNon:    Feuille{Vegetaux: []string{"robinier", "noyer"}},
			},
			SiNon: Feuille{Vegetaux: []string{}},
		},
	}

	fmt.Println(arbre.Nb())
	for _, q := range arbre.ListeQuestion() {
		fmt.Println(q)
	}
}
