#!/usr/bin/env guile
!#

(use-modules (ice-9 match)
             (srfi srfi-1))

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

(define arbre
  (noeud "simple"
         (feuille '())
         (noeud "alternee"
                (noeud "bord dente"
                       (feuille '("sorbier"))
                       (feuille '("robinier" "noyer")))
                (feuille '()))))

(display (nb arbre)) (newline)
(for-each (lambda (q) (display q) (newline))
          (liste-question arbre))
