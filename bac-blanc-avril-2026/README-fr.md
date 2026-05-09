# Arbre d'identification de plantes — quatre implémentations

Ce projet implémente le même petit programme dans **quatre langages de programmation différents**, chacun avec un style différent. L'objectif est de montrer comment une même idée peut s'exprimer en orienté objet, en fonctionnel, en fonctionnel pur, et à base d'interfaces.

## Ce que fait le programme

Le programme représente un **arbre de décision** pour identifier des arbres à partir de leurs feuilles. À chaque nœud, on pose une question oui/non (par exemple « les feuilles sont-elles alternées ? »). En suivant les réponses, on arrive à une feuille de l'arbre qui contient une liste d'espèces possibles.

L'arbre que l'on construit ressemble à ceci :

```
                       "simple ?"
                      /          \
                    OUI           NON
                    /              \
              (aucune plante)    "alternée ?"
                                /            \
                              OUI             NON
                              /                \
                     "bord denté ?"       (aucune plante)
                     /            \
                   OUI             NON
                   /                \
            [sorbier]      [robinier, noyer]
```

Le programme fait deux choses :
1. **Compte** le nombre total de plantes stockées dans les feuilles (`nb`).
2. **Liste** toutes les questions de l'arbre (`liste_question`).

Sortie attendue pour les quatre versions :
```
3
simple
alternee
bord dente
```

---

## 1. Python — style orienté objet (`main.py`)

Python est un langage généraliste très répandu. Ici on utilise des **classes**, qui sont la manière classique de modéliser des « choses qui ont un comportement » en programmation orientée objet.

```python
class Noeud:
    def __init__(self, question, sioui, sinon):
        self.question = question
        self.sioui = sioui
        self.sinon = sinon

    def nb(self):
        return self.sioui.nb() + self.sinon.nb()

    def liste_question(self):
       return [self.question] + self.sioui.liste_question() + self.sinon.liste_question()

class Feuille:
    def __init__(self, vegetaux):
        self.vegetaux = vegetaux

    def nb(self):
        return len(self.vegetaux)

    def liste_question(self):
       return []
```

### Idées clés

- **Deux classes** : `Noeud` (un nœud avec une question) et `Feuille` (une feuille avec des plantes).
- **Chaque classe a sa propre version de `nb()` et `liste_question()`.** Quand on appelle `quelquechose.nb()`, Python regarde *à quelle classe* appartient l'objet et exécute la méthode correspondante. Ça s'appelle le **polymorphisme**.
- **Récursion** : `Noeud.nb()` appelle `nb()` sur ses deux enfants. La récursion s'arrête sur `Feuille`, qui ne récurse pas — elle retourne simplement la longueur de sa liste de plantes.

### Pourquoi l'OO de Python est « approximatif » comparé aux vrais langages OO

Python *ressemble* à un langage orienté objet, mais comparé à Java, C#, ou même Go, son support de l'OO est étonnamment informel. Trois faiblesses concrètes apparaissent dans cet exemple même :

#### 1. Pas de vraies interfaces — le polymorphisme repose sur le « duck typing »

En Java ou en Go, on déclarerait une interface comme `Arbre` listant les méthodes que tout arbre doit fournir, et le compilateur refuserait de construire le programme si `Noeud` ou `Feuille` en oubliait une. En Python, **rien** ne joue ce rôle. La ligne

```python
return self.sioui.nb() + self.sinon.nb()
```

fonctionne uniquement parce que `self.sioui` *se trouve avoir* une méthode appelée `nb`. C'est ce qu'on appelle le **duck typing** : « si ça marche comme un canard et que ça cancane comme un canard, alors c'est un canard ». Les inconvénients :

- **Rien ne vous empêche de passer la mauvaise chose.** `Noeud("?", "hello", 42)` est accepté à la construction. Le crash arrive plus tard, au fond de la récursion, quand Python essaie `"hello".nb()` et échoue avec `AttributeError`.
- **Pas de contrat commun.** Si vous décidez demain que tout arbre doit avoir une méthode `description()`, il n'y a aucun endroit où déclarer cette exigence. Vous devez penser à l'ajouter aux deux classes — et espérer ne pas en avoir oublié une autre quelque part.
- **Les outils ne peuvent que deviner.** Les éditeurs et les linters n'ont pas de contrat formel à vérifier. Ils utilisent des heuristiques et passent souvent à côté d'erreurs qu'un vrai compilateur attraperait instantanément.

Python *propose* `abc.ABC` et `typing.Protocol` pour simuler des interfaces, mais c'est **optionnel** et la plupart des vérifications se font quand même à l'exécution, quand le programme tourne déjà. Comparez avec Go, où l'interface `Arbre` est vérifiée à la compilation, avant même que le programme démarre.

#### 2. La lourdeur de `self`

Regardez à quelle fréquence `self` apparaît dans le code Python :

```python
def __init__(self, question, sioui, sinon):
    self.question = question
    self.sioui = sioui
    self.sinon = sinon
```

Cinq `self` en trois lignes. En Java ou C#, ce serait simplement :

```java
this.question = question;  // ou même juste : question = question (avec le shadowing de champ)
```

et `this` est implicite quand on appelle ses propres méthodes. En Go, le récepteur est nommé une seule fois en haut de chaque méthode et c'est tout. Python vous oblige à :

- passer `self` comme **premier paramètre** de *chaque* méthode (oui, vous l'écrivez à chaque fois),
- préfixer **chaque** accès à un champ et **chaque** appel de méthode par `self.`.

Pour une petite classe, c'est gérable, mais dans du code plus volumineux, ça ajoute du bruit visuel qui masque la logique. Beaucoup voient `self` comme un détail d'implémentation qui fuit : c'est la manière dont Python transforme `obj.methode(args)` en `Classe.methode(obj, args)` en interne.

#### 3. Les champs privés n'existent pas vraiment

En Java, C#, ou C++, on peut marquer un champ `private` et le compilateur **interdit** à quiconque hors de la classe de le lire ou de le modifier. C'est l'**encapsulation**, l'un des piliers de l'OO. Python n'a rien d'équivalent :

- Un underscore en préfixe (`self._question`) est **purement une convention** — un poli « s'il vous plaît, n'y touchez pas ». L'interpréteur ne vous arrête pas. N'importe qui peut écrire `mon_noeud._question = "haha"` et ça marchera.
- Un double underscore (`self.__question`) déclenche le **name mangling** : Python renomme l'attribut en `_NomDeClasse__question`. Ça rend l'accès accidentel depuis une classe fille plus difficile, mais ce n'est pas une protection — c'est de l'obscurcissement. Vous pouvez toujours écrire `mon_noeud._Noeud__question` pour le lire ou le modifier librement.

Donc dans notre exemple, même si on voulait rendre `question`, `sioui`, et `sinon` immuables et internes à `Noeud`, **on ne peut pas**. N'importe qui peut atteindre l'objet de l'extérieur et recâbler l'arbre. En Java ou en Go, ces champs pourraient être réellement cachés derrière un constructeur et des accesseurs en lecture seule, et le compilateur ferait respecter ça.

#### Résumé

L'OO de Python ressemble plus à une **boîte à outils de conventions** qu'à un système strict. C'est flexible et rapide à écrire, mais on échange ça contre des garanties :

| Caractéristique         | Java / C# / Go            | Python                            |
|-------------------------|---------------------------|-----------------------------------|
| Contrat d'interface     | Imposé par le compilateur | Aucun (ou opt-in, à l'exécution)  |
| `this` / récepteur      | Implicite                 | `self` explicite partout          |
| Champs privés           | Imposés par le compilateur| Convention seulement              |
| Détection de mauvais type| À la compilation         | À l'exécution, quand ça plante    |

Ce n'est pas vraiment un défaut — c'est un choix de conception assumé (« on fait confiance au programmeur »). Mais c'est la raison pour laquelle beaucoup disent que Python n'est *pas* un langage fortement orienté objet, simplement un langage qui *supporte* les objets.

### Pour l'exécuter

```bash
python3 main.py
```

---

## 2. Guile Scheme — style fonctionnel avec filtrage de motifs (`main.scm`)

Scheme est un dialecte de **Lisp**, l'un des plus vieux langages de programmation. Guile est une implémentation particulière de Scheme. Le code s'écrit avec beaucoup de parenthèses : `(fonction arg1 arg2)` au lieu de `fonction(arg1, arg2)`.

En programmation fonctionnelle, on n'utilise généralement pas de classes. À la place, on utilise des **données simples** (ici, des listes étiquetées avec un symbole) et des **fonctions qui opèrent sur ces données**.

```scheme
(define (noeud question sioui sinon) `(noeud ,question ,sioui ,sinon))
(define (feuille vegetaux)            `(feuille ,vegetaux))

(define (nb arbre)
  (match arbre
    (('feuille vs)            (length vs))
    (('noeud _ sioui sinon)   (+ (nb sioui) (nb sinon)))))

(define (liste-question arbre)
  (match arbre
    (('feuille _)             '())
    (('noeud q sioui sinon)   (cons q (append-map liste-question
                                                  (list sioui sinon))))))
```

### Idées clés

- **Pas de classes.** Un arbre n'est qu'une liste. Une feuille ressemble à `('feuille ("sorbier"))` et un nœud ressemble à `('noeud "simple" gauche droite)`. Le premier élément (`'feuille` ou `'noeud`) est une *étiquette* qui dit de quel genre de chose il s'agit.
- **Le filtrage de motifs** avec `match` permet d'inspecter la forme des données. `(('feuille vs) ...)` se lit : « si `arbre` est une liste qui commence par `'feuille`, donne au deuxième élément le nom `vs` et exécute cette branche ». C'est comme un `switch`/`if` sous stéroïdes — il *vérifie* la forme et *extrait* les morceaux en une seule étape.
- **L'underscore `_`** signifie « cette valeur ne m'intéresse pas » — utile quand un morceau de donnée n'est pas pertinent dans une branche.
- **`append-map`** applique une fonction à chaque élément d'une liste et concatène les résultats. Ici il collecte récursivement les questions des deux enfants.
- **Pas de mutation, pas de `self`.** Les fonctions prennent l'arbre en entrée et retournent une nouvelle valeur. C'est le cœur de la programmation fonctionnelle.

### Pour l'exécuter

```bash
guile main.scm
```

---

## 3. Haskell — style fonctionnel pur avec types algébriques (`Main.hs`)

Haskell est un langage **typé statiquement et purement fonctionnel**. Deux conséquences importantes :

- **Typé statiquement** : chaque expression a un type que le compilateur vérifie *avant* l'exécution du programme. Si vous essayez d'utiliser un nombre comme une chaîne, le programme ne compilera même pas.
- **Purement fonctionnel** : les fonctions ne peuvent pas avoir d'effets de bord (pas de modification de variables, pas d'affichage surprise). Tout est une valeur transformée en une autre valeur.

```haskell
data Arbre = Feuille [String]
           | Noeud String Arbre Arbre

nb :: Arbre -> Int
nb (Feuille vs)      = length vs
nb (Noeud _ oui non) = nb oui + nb non

listeQuestion :: Arbre -> [String]
listeQuestion (Feuille _)        = []
listeQuestion (Noeud q oui non)  = q : listeQuestion oui ++ listeQuestion non
```

### Idées clés

- **Type algébrique (ADT)** : la ligne `data Arbre = Feuille [String] | Noeud String Arbre Arbre` définit un nouveau type appelé `Arbre` qui peut être **soit** une `Feuille` (contenant une liste de chaînes), **soit** un `Noeud` (contenant une chaîne et deux sous-arbres). Le `|` se lit « ou ». C'est similaire aux listes étiquetées de Scheme, mais le compilateur *garantit* maintenant que vous ne pouvez pas accidentellement construire autre chose.
- **Signatures de type** : `nb :: Arbre -> Int` se lit « `nb` est une fonction qui prend un `Arbre` et retourne un `Int` ». Le compilateur vérifie ça.
- **Filtrage de motifs par constructeur** : chaque fonction est définie en écrivant une équation par cas (`Feuille` et `Noeud`). Le compilateur vous avertira si vous oubliez un cas — un excellent filet de sécurité.
- **La récursion** est la seule manière de parcourir l'arbre (pas de boucles en Haskell pur).
- **Le deux-points `:`** dans `q : listeQuestion oui ++ ...` signifie « préfixer `q` à la liste » (comme `cons` en Scheme).

### Pour l'exécuter

Deux options. **Interprété** (sans artefacts de compilation) :
```bash
runghc Main.hs
```

**Compilé** (produit un binaire rapide) :
```bash
ghc Main.hs
./Main
```

La compilation crée `Main`, `Main.hi`, et `Main.o`. Pour faire le ménage : `rm Main Main.hi Main.o`.

---

## 4. Go — style à base d'interfaces (`main.go`)

Go est un langage **typé statiquement et compilé** conçu chez Google. Il n'a pas de classes comme Python, mais il a des **structs** (groupes de champs) et des **interfaces** (ensembles de signatures de méthodes). Cette combinaison est la manière dont Go fait du polymorphisme.

```go
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

func (n Noeud) EstResultat() bool { return false }
func (n Noeud) Nb() int           { return n.SiOui.Nb() + n.SiNon.Nb() }
func (n Noeud) ListeQuestion() []string {
    return append([]string{n.Question},
        append(n.SiOui.ListeQuestion(), n.SiNon.ListeQuestion()...)...)
}

type Feuille struct {
    Vegetaux []string
}

func (f Feuille) EstResultat() bool      { return true }
func (f Feuille) Nb() int                { return len(f.Vegetaux) }
func (f Feuille) ListeQuestion() []string { return []string{} }
```

### Idées clés

- **L'interface `Arbre`** liste les trois méthodes que tout nœud d'arbre doit fournir : `EstResultat`, `Nb`, et `ListeQuestion`. Elle dit *quoi* on peut faire avec un `Arbre`, mais pas *comment* — c'est laissé à chaque type concret.
- **Deux structs**, `Noeud` et `Feuille`, qui portent chacun leurs propres données. Les deux **satisfont l'interface `Arbre`** simplement parce qu'ils implémentent les trois méthodes requises. Contrairement à Java ou C#, on n'écrit `implements Arbre` nulle part — Go le déduit automatiquement. C'est ce qu'on appelle le **typage structurel**.
- **`EstResultat` est l'exemple parfait** de la séparation demandée : `Noeud.EstResultat()` retourne `false`, `Feuille.EstResultat()` retourne `true`. Même nom de méthode, comportement différent selon le type concret.
- **Les champs `SiOui` et `SiNon` sont typés `Arbre`** (l'interface), donc un `Noeud` peut contenir n'importe quel type d'enfant. À l'exécution, quand on appelle `n.SiOui.Nb()`, Go regarde ce qui est réellement stocké là (un `Noeud` ou une `Feuille`) et exécute la méthode correspondante. C'est la **dispatch dynamique via une interface**.
- **Les récepteurs de méthode** comme `func (n Noeud) Nb() int` signifient « ceci est une méthode sur le type `Noeud`, où `n` joue le même rôle que `self` en Python ou `this` en Java ».
- **Le `...` dans `append(..., slice...)`** est l'opérateur de *spread* : il dit à `append` d'ajouter chaque élément du slice individuellement plutôt que le slice entier.

### Pour l'exécuter

```bash
go run main.go
```

Ou compiler en binaire :

```bash
go build -o exo
./exo
```

---

## Comparaison des quatre styles

| Aspect                  | Python (OO)              | Scheme (fonctionnel)         | Haskell (fonctionnel pur)        | Go (interface)                  |
|-------------------------|--------------------------|------------------------------|----------------------------------|---------------------------------|
| Représentation des données | Deux classes          | Listes étiquetées            | Un type algébrique               | Deux structs + interface        |
| Comment les variantes diffèrent | Classes différentes | Symboles d'étiquette        | Constructeurs différents         | Structs différents              |
| Dispatch logique        | Méthode de la classe     | `match` sur la forme         | Filtrage par constructeur        | Méthode via l'interface         |
| Vérification des types  | À l'exécution            | À l'exécution                | À la compilation                 | À la compilation                |
| Mutation autorisée      | Oui (mais inutilisée ici)| Évitée                       | Interdite par défaut             | Oui (mais inutilisée ici)       |
| Variantes ouvertes      | Oui (toute nouvelle classe) | Oui (toute nouvelle étiquette) | Non (fermé : il faut éditer l'ADT) | Oui (tout nouveau struct)    |

La dernière ligne est importante : avec le type algébrique de Haskell, toutes les variantes sont listées en un seul endroit, et le compilateur force à traiter chaque cas. Avec les classes (Python), les listes étiquetées (Scheme), ou les interfaces (Go), n'importe qui peut ajouter une nouvelle variante plus tard — plus flexible, mais le compilateur ne peut plus prévenir si on oublie de la traiter quelque part.

### À retenir

- **Le même problème peut se modéliser de plusieurs manières.** L'OO lie données et comportement à l'intérieur d'une classe. Le fonctionnel sépare les données (étiquettes ou ADT) des fonctions qui les manipulent. Les interfaces de Go sont entre les deux : les structs portent les données, les méthodes fournissent le comportement, et l'interface n'est qu'un contrat.
- **Le filtrage de motifs** (`match` en Scheme, équations en Haskell) est souvent plus clair que des chaînes de `if`/`else`. Il laisse la *forme* des données piloter la logique.
- **Le polymorphisme** apparaît sous différents noms : dispatch de méthode (Python), filtrage de motifs (Scheme/Haskell), satisfaction d'interface (Go). L'idée sous-jacente est la même — *le même nom d'appel fait des choses différentes selon le type de la valeur*.
- **Le typage statique** (Haskell, Go) attrape toute une classe de bugs avant même que le programme ne tourne — au prix de devoir être plus précis dès le départ.
- **La récursion** apparaît dans toutes les versions. C'est la manière naturelle de traiter des données en forme d'arbre : traiter une feuille directement, et combiner les résultats de la récursion sur les enfants.

Chaque style a ses forces. En connaître plusieurs aide à choisir le bon outil — et, plus important, ça change votre manière de *penser* un problème.
