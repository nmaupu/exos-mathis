# Plant identification tree — three implementations

This project implements the same small program in **three different programming languages**, each with a different style. The goal is to show how the same idea can be expressed in object-oriented, functional, and pure-functional ways.

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

Expected output for all three versions:
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

## Comparing the three styles

| Aspect              | Python (OO)              | Scheme (functional)            | Haskell (pure functional)       |
|---------------------|--------------------------|--------------------------------|---------------------------------|
| Data representation | Two classes              | Tagged lists                   | One algebraic data type         |
| How variants differ | Different classes        | Different tag symbols          | Different constructors          |
| Logic dispatch      | Method on the class      | `match` on the data shape      | Pattern matching on constructor |
| Type checking       | At runtime               | At runtime                     | At compile time                 |
| Mutation allowed    | Yes (but unused here)    | Avoided                        | Forbidden by default            |

### What to take away

- **The same problem can be modeled many ways.** OO ties data and behavior together inside a class. Functional separates data (tags or ADTs) from the functions that work on it.
- **Pattern matching** (`match` in Scheme, equation-based in Haskell) is often clearer than chains of `if`/`else`. It lets the *shape* of the data drive the logic.
- **Static typing** (Haskell) catches a whole class of bugs before you ever run the program — at the cost of having to be more precise upfront.
- **Recursion** appears in every version. It's the natural way to process tree-shaped data: handle a leaf directly, and combine the results of recursing on the children.

Each style has its strengths. Knowing more than one helps you pick the right tool — and, more importantly, it changes how you *think* about a problem.
