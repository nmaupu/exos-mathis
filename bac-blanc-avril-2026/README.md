# Plant identification tree — four implementations

This project implements the same small program in **four different programming languages**, each with a different style. The goal is to show how the same idea can be expressed in object-oriented, functional, pure-functional, and interface-based ways.

## What the program does

The program represents a **decision tree** to identify trees by their leaves. At each node, you ask a yes/no question (like "are the leaves alternate?"). Following the answers leads you to a leaf of the tree containing a list of possible plant species.

The tree we build looks like this:

```
                       "simple?"
                      /         \
                    YES          NO
                    /             \
              (no plants)      "alternate?"
                              /            \
                            YES             NO
                            /                \
                    "toothed edge?"      (no plants)
                    /            \
                  YES             NO
                  /                \
            [sorbier]      [robinier, noyer]
```

The program does two things:
1. **Counts** the total number of plants stored in the leaves (`nb`).
2. **Lists** all the questions in the tree (`liste_question`).

Expected output for all four versions:
```
3
simple
alternee
bord dente
```

---

## 1. Python — object-oriented style (`main.py`)

Python is a popular general-purpose language. Here we use **classes**, which is the typical way to model "things with behavior" in object-oriented programming.

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

### Key ideas

- **Two classes**: `Noeud` (a question node) and `Feuille` (a leaf with plants).
- **Each class has its own version of `nb()` and `liste_question()`.** When you call `something.nb()`, Python looks at *which class* the object belongs to and runs the matching method. This is called **polymorphism**.
- **Recursion**: `Noeud.nb()` calls `nb()` on its two children. The recursion stops at `Feuille`, which doesn't recurse — it just returns the length of its plant list.

### Running it

```bash
python3 main.py
```

---

## 2. Guile Scheme — functional style with pattern matching (`main.scm`)

Scheme is a dialect of **Lisp**, one of the oldest programming languages. Guile is a particular implementation of Scheme. Code is written using lots of parentheses: `(function arg1 arg2)` instead of `function(arg1, arg2)`.

In functional programming, we don't usually have classes. Instead, we use **plain data** (here, lists tagged with a symbol) and **functions that operate on that data**.

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

### Key ideas

- **No classes.** A tree is just a list. A leaf looks like `('feuille ("sorbier"))` and a node looks like `('noeud "simple" left right)`. The first element (`'feuille` or `'noeud`) is a *tag* that says what kind of thing the list represents.
- **Pattern matching** with `match` lets us inspect the shape of the data. `(('feuille vs) ...)` reads as: "if `arbre` is a list starting with `'feuille`, give the second element the name `vs` and run this branch." It's like a `switch`/`if` on steroids — it both *checks* the shape and *extracts* the parts in one step.
- **The underscore `_`** means "I don't care about this value" — useful when a piece of data is irrelevant for that branch.
- **`append-map`** applies a function to each item of a list and concatenates the results. Here it recursively collects questions from both children.
- **No mutation, no `self`.** The functions take the tree as input and return a new value. This is the heart of functional programming.

### Running it

```bash
guile main.scm
```

---

## 3. Haskell — pure functional style with algebraic data types (`Main.hs`)

Haskell is a **statically-typed, purely functional** language. Two important consequences:

- **Statically typed**: every expression has a type the compiler checks *before* running the program. If you try to use a number as a string, the program won't even compile.
- **Purely functional**: functions can't have side effects (no modifying variables, no surprise printing). Everything is a value transformed into another value.

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

### Key ideas

- **Algebraic data type (ADT)**: the line `data Arbre = Feuille [String] | Noeud String Arbre Arbre` defines a new type called `Arbre` that can be **either** a `Feuille` (containing a list of strings) **or** a `Noeud` (containing a string and two sub-trees). The `|` reads as "or". This is similar to Scheme's tagged lists, but the compiler now *guarantees* you can't accidentally build something else.
- **Type signatures**: `nb :: Arbre -> Int` reads as "`nb` is a function that takes an `Arbre` and returns an `Int`". The compiler verifies this.
- **Pattern matching by constructor**: each function is defined by writing one equation per case (`Feuille` and `Noeud`). The compiler will warn you if you forget a case — a great safety net.
- **Recursion** is the only way to walk through the tree (no loops in pure Haskell).
- **The colon `:`** in `q : listeQuestion oui ++ ...` means "prepend `q` to the list" (just like `cons` in Scheme).

### Running it

Two options. **Interpreted** (no build artifacts):
```bash
runghc Main.hs
```

**Compiled** (produces a fast binary):
```bash
ghc Main.hs
./Main
```

Compiling creates `Main`, `Main.hi`, and `Main.o`. To clean up: `rm Main Main.hi Main.o`.

---

## 4. Go — interface-based style (`main.go`)

Go is a **statically-typed, compiled** language designed at Google. It does not have classes the way Python does, but it has **structs** (groups of fields) and **interfaces** (sets of method signatures). This combination is Go's way of doing polymorphism.

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

### Key ideas

- **The `Arbre` interface** lists the three methods every tree node must provide: `EstResultat`, `Nb`, and `ListeQuestion`. It says *what* you can do with an `Arbre`, but not *how* — that's left to each concrete type.
- **Two structs**, `Noeud` and `Feuille`, each carrying their own data. They both **satisfy the `Arbre` interface** simply because they implement the three required methods. Unlike Java or C#, you don't write `implements Arbre` anywhere — Go figures it out automatically. This is called **structural typing**.
- **`EstResultat` is the perfect example** of the requested split: `Noeud.EstResultat()` returns `false`, `Feuille.EstResultat()` returns `true`. Same method name, different behavior depending on the concrete type.
- **The `SiOui` and `SiNon` fields are typed `Arbre`** (the interface), so a `Noeud` can hold either kind of child. At runtime, when you call `n.SiOui.Nb()`, Go looks at what's actually stored there (a `Noeud` or a `Feuille`) and runs the matching method. This is **dynamic dispatch through an interface**.
- **Method receivers** like `func (n Noeud) Nb() int` mean "this is a method on the `Noeud` type, where `n` plays the same role as `self` in Python or `this` in Java".
- **The `...` in `append(..., slice...)`** is the *spread operator*: it tells `append` to add each element of the slice individually instead of the slice as a whole.

### Running it

```bash
go run main.go
```

Or compile to a binary:

```bash
go build -o exo
./exo
```

---

## Comparing the four styles

| Aspect              | Python (OO)              | Scheme (functional)            | Haskell (pure functional)       | Go (interface)                  |
|---------------------|--------------------------|--------------------------------|---------------------------------|---------------------------------|
| Data representation | Two classes              | Tagged lists                   | One algebraic data type         | Two structs + interface         |
| How variants differ | Different classes        | Different tag symbols          | Different constructors          | Different structs               |
| Logic dispatch      | Method on the class      | `match` on the data shape      | Pattern matching on constructor | Method via interface            |
| Type checking       | At runtime               | At runtime                     | At compile time                 | At compile time                 |
| Mutation allowed    | Yes (but unused here)    | Avoided                        | Forbidden by default            | Yes (but unused here)           |
| Variants are open   | Yes (any new class)      | Yes (any new tag)              | No (closed: must edit the ADT)  | Yes (any new struct)            |

The last row matters: with Haskell's algebraic data type, all the variants are listed in one place, and the compiler forces you to handle every case. With classes (Python), tagged lists (Scheme), or interfaces (Go), anyone can add a new variant later — more flexible, but the compiler can no longer warn you if you forget to handle it somewhere.

### What to take away

- **The same problem can be modeled many ways.** OO ties data and behavior together inside a class. Functional separates data (tags or ADTs) from the functions that work on it. Go's interfaces sit in between: structs hold the data, methods provide the behavior, and the interface is just a contract.
- **Pattern matching** (`match` in Scheme, equation-based in Haskell) is often clearer than chains of `if`/`else`. It lets the *shape* of the data drive the logic.
- **Polymorphism** shows up under different names: method dispatch (Python), pattern matching (Scheme/Haskell), interface satisfaction (Go). The underlying idea is the same — *the same call name does different things depending on the kind of value*.
- **Static typing** (Haskell, Go) catches a whole class of bugs before you ever run the program — at the cost of having to be more precise upfront.
- **Recursion** appears in every version. It's the natural way to process tree-shaped data: handle a leaf directly, and combine the results of recursing on the children.

Each style has its strengths. Knowing more than one helps you pick the right tool — and, more importantly, it changes how you *think* about a problem.
