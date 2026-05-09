data Arbre = Feuille [String]
           | Noeud String Arbre Arbre

nb :: Arbre -> Int
nb (Feuille vs)      = length vs
nb (Noeud _ oui non) = nb oui + nb non

listeQuestion :: Arbre -> [String]
listeQuestion (Feuille _)        = []
listeQuestion (Noeud q oui non)  = q : listeQuestion oui ++ listeQuestion non

arbre :: Arbre
arbre =
  Noeud "simple"
    (Feuille [])
    (Noeud "alternee"
       (Noeud "bord dente"
          (Feuille ["sorbier"])
          (Feuille ["robinier", "noyer"]))
       (Feuille []))

main :: IO ()
main = do
  print (nb arbre)
  mapM_ putStrLn (listeQuestion arbre)
