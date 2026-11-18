"""Cours « fonction par fonction » : chaque fonction de la libft est decortiquee ligne par ligne.
Le code affiche est celui de runtime/ref/<fonction>.c (sans l'en-tete 42) ; les numeros de lignes
des explications (a, b, texte) sont ceux de ce code. tools/e2e.py verifie qu'ils restent valides."""
import os

REF_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "runtime", "ref")
FUNCS = []
HEADER_LINES = 12


def fn(id, role, walk, cases=(), trace=None, pitfalls=(), why=()):
    FUNCS.append({"id": id, "role": role, "walk": [list(w) for w in walk], "cases": list(cases),
                  "trace": trace, "pitfalls": list(pitfalls), "why": list(why)})


def code_lines(fid):
    with open(os.path.join(REF_DIR, fid + ".c"), encoding="utf-8") as f:
        return f.read().split("\n")[HEADER_LINES:]


# ============================================================ PARTIE 1 : libc
fn("ft_isalpha", "Renvoie 1 si `c` est une lettre (majuscule ou minuscule), 0 sinon.",
   [(3, 3, "`int c` et pas `char c` : comme la vraie libc, la fonction reçoit un `int` (un caractère converti). Elle renvoie un `int` : **1** ou **0** (sujet v19.3)."),
    (5, 5, "La condition a **deux intervalles** reliés par `||` : majuscules (`'A'` 65 à `'Z'` 90) **ou** minuscules (`'a'` 97 à `'z'` 122). Chaque intervalle est un `&&` : `c` doit être **à la fois** ≥ au début et ≤ à la fin."),
    (6, 6, "C'est une lettre : on renvoie exactement **1**."),
    (7, 8, "Sinon on renvoie exactement **0**. (Les parenthèses de `return (...)` sont exigées par la norme.)")],
   cases=["`ft_isalpha('a')` → 1 ; `ft_isalpha('Z')` → 1", "`ft_isalpha('5')` → 0 ; `ft_isalpha('[')` → 0 (le `[` est entre `'Z'` et `'a'`)", "`ft_isalpha(0)` et `ft_isalpha(-1)` → 0"],
   pitfalls=["Écrire un seul intervalle `'A'` à `'z'` : il accepterait `[ \\ ] ^ _` et l'accent grave.", "Renvoyer `c` ou un autre nombre non nul au lieu de **1** : refusé depuis le sujet v19.3."])

fn("ft_isdigit", "Renvoie 1 si `c` est un chiffre (`'0'` à `'9'`), 0 sinon.",
   [(3, 3, "Même prototype que les autres `is*` : un `int` en entrée, un `int` (1 ou 0) en sortie."),
    (5, 5, "Un **seul** intervalle : de `'0'` (48) à `'9'` (57). Les chiffres sont contigus dans la table ASCII, donc deux comparaisons suffisent."),
    (6, 6, "Dans l'intervalle : **1**."), (7, 8, "Hors de l'intervalle : **0**.")],
   cases=["`ft_isdigit('0')` → 1, `ft_isdigit('9')` → 1", "`ft_isdigit('a')` → 0, `ft_isdigit(' ')` → 0", "`ft_isdigit(0)` (le caractère nul) → 0, pas 1 : `0` n'est pas `'0'`."],
   pitfalls=["Confondre le nombre `0` et le caractère `'0'` (qui vaut 48).", "Écrire `c > '0'` : le `'0'` lui-même serait refusé."])

fn("ft_isalnum", "Renvoie 1 si `c` est une lettre **ou** un chiffre, 0 sinon.",
   [(3, 3, "Même prototype que les autres `is*`."),
    (5, 5, "On **réutilise** `ft_isalpha` et `ft_isdigit` (elles sont dans la même libft) avec un `||` : lettre **ou** chiffre. Pas besoin de réécrire les intervalles."),
    (6, 6, "Si l'un des deux est vrai : **1**."), (7, 8, "Sinon **0**.")],
   cases=["`ft_isalnum('a')` → 1, `ft_isalnum('7')` → 1", "`ft_isalnum('_')` → 0, `ft_isalnum(' ')` → 0"],
   pitfalls=["Si `ft_isalpha` ou `ft_isdigit` est fausse, `ft_isalnum` l'est aussi : teste-les d'abord.", "Dans le Makefile, ces deux fichiers doivent être présents dans `libft.a`, sinon erreur de liaison."],
   why=["Pourquoi un `if/else` plutôt que `return (ft_isalpha(c) || ft_isdigit(c));` ? Les deux marchent ; le `if/else` renvoie explicitement 1 ou 0. En C, `||` donne déjà 1 ou 0, donc la version courte serait aussi conforme."])

fn("ft_isascii", "Renvoie 1 si `c` est un code ASCII valide (0 à 127), 0 sinon.",
   [(3, 3, "Un `int` en entrée : c'est utile ici, car un `int` peut valoir plus de 127 ou être négatif."),
    (5, 5, "Intervalle de **0 à 127** (inclus). Le test `c >= 0` rejette les valeurs négatives, `c <= 127` rejette les valeurs étendues (128 à 255 et au-delà)."),
    (6, 6, "ASCII : **1**."), (7, 8, "Sinon **0**.")],
   cases=["`ft_isascii(0)` → 1, `ft_isascii(127)` → 1", "`ft_isascii(128)` → 0, `ft_isascii(-1)` → 0"],
   pitfalls=["Oublier `c >= 0` : `-1` serait accepté.", "Se tromper de borne (`< 127` refuserait le caractère 127)."])

fn("ft_isprint", "Renvoie 1 si `c` est un caractère imprimable (de l'espace `' '` à `'~'`), 0 sinon.",
   [(3, 3, "Même prototype que les autres `is*`."),
    (5, 5, "Imprimable = de **32** (l'espace) à **126** (`'~'`). Les codes 0 à 31 sont des caractères de contrôle (retour à la ligne, tabulation…) et 127 (DEL) ne s'affiche pas."),
    (6, 6, "Imprimable : **1**."), (7, 8, "Sinon **0**.")],
   cases=["`ft_isprint(' ')` → 1, `ft_isprint('~')` → 1", "`ft_isprint('\\n')` → 0, `ft_isprint(127)` → 0", "`ft_isprint(31)` → 0, `ft_isprint(32)` → 1"],
   pitfalls=["Oublier que l'espace (32) est imprimable.", "Inclure 127 dans l'intervalle."])

fn("ft_toupper", "Transforme une minuscule en majuscule ; renvoie tout autre caractère inchangé.",
   [(3, 3, "Reçoit un `int` et renvoie un `int` (le caractère converti), comme `toupper` de la libc."),
    (5, 5, "Seules les **minuscules** (`'a'` 97 à `'z'` 122) sont transformées. Tout le reste (majuscules, chiffres, ponctuation) ne bouge pas."),
    (6, 6, "On retire **32** : `'a' - 32 = 'A'`. C'est la distance fixe entre minuscules et majuscules dans la table ASCII."),
    (7, 8, "Sinon on renvoie `c` tel quel.")],
   cases=["`ft_toupper('a')` → `'A'`, `ft_toupper('z')` → `'Z'`", "`ft_toupper('A')` → `'A'` (déjà majuscule), `ft_toupper('5')` → `'5'`"],
   pitfalls=["Soustraire 32 à n'importe quel caractère : `'A' - 32` donnerait un caractère de contrôle.", "Écrire `'a' - 'A'` à la place de `32` marche aussi et se lit mieux."])

fn("ft_tolower", "Transforme une majuscule en minuscule ; renvoie tout autre caractère inchangé.",
   [(3, 3, "Même prototype que `ft_toupper`."),
    (5, 5, "Seules les **majuscules** (`'A'` 65 à `'Z'` 90) sont concernées."),
    (6, 6, "On ajoute **32** : `'A' + 32 = 'a'`."),
    (7, 8, "Sinon on renvoie `c` inchangé.")],
   cases=["`ft_tolower('A')` → `'a'`", "`ft_tolower('a')` → `'a'`, `ft_tolower('5')` → `'5'`"],
   pitfalls=["Ajouter 32 à un caractère qui n'est pas une majuscule (`'a' + 32` = `'\\x81'`…)."])

fn("ft_strlen", "Renvoie le nombre de caractères d'une chaîne, sans compter le `'\\0'` final.",
   [(3, 3, "`const char *s` : on ne modifie pas la chaîne. Retourne un **`size_t`** (type des tailles, jamais négatif)."),
    (5, 5, "`i` est aussi un `size_t` : il va compter les caractères et sera renvoyé tel quel."),
    (7, 7, "On commence à l'indice 0 (premier caractère)."),
    (8, 9, "`while (s[i])` : tant que le caractère n'est pas `'\\0'` (qui vaut 0, donc faux), on avance. **C'est la boucle de base de toutes les fonctions `str*`.**"),
    (10, 10, "À la sortie, `i` est l'indice du `'\\0'`, donc le nombre de caractères avant lui.")],
   cases=["`ft_strlen(\"\")` → 0 (le `'\\0'` est tout de suite à l'indice 0)", "`ft_strlen(\"abc\")` → 3", "`ft_strlen(\"ab\\0cd\")` → 2 (on s'arrête au premier `'\\0'`)"],
   trace="s = \"abc\"\ni=0 : s[0]='a' (vrai) -> i=1\ni=1 : s[1]='b' (vrai) -> i=2\ni=2 : s[2]='c' (vrai) -> i=3\ni=3 : s[3]='\\0' (faux) -> sortie, return 3",
   pitfalls=["Renvoyer un `int` : `size_t` est le type attendu par le sujet.", "Appeler `ft_strlen(NULL)` plante : comme la vraie `strlen`, ce n'est pas géré."])

fn("ft_memset", "Remplit les `n` premiers octets d'une zone mémoire avec la valeur d'un octet.",
   [(3, 3, "`void *s` : un pointeur « sans type », car `memset` marche sur n'importe quelle zone. `int c` : la valeur à écrire. Retourne la zone de départ (`void *`)."),
    (5, 6, "Un `void *` ne peut pas s'indexer (`s[i]` n'a pas de sens sans taille de type). On prend donc un **`unsigned char *`** : un pointeur sur des **octets**. `i` compte les octets écrits."),
    (8, 8, "Le cast `(unsigned char *)s` dit « traite cette zone comme une suite d'octets »."),
    (9, 9, "Départ à 0."),
    (10, 14, "On écrit `n` octets : `ptr[i] = (unsigned char)c` (seul l'octet de poids faible de `c` compte, comme dans la vraie `memset`)."),
    (15, 15, "On renvoie le pointeur de **départ** (`s`) tel qu'il a été reçu.")],
   cases=["`n = 0` : rien n'est écrit, la fonction renvoie `s`.", "`ft_memset(buf, 'x', 3)` sur `buf` : les 3 premiers octets deviennent `'x'`.", "`c = 256` → l'octet écrit vaut 0 (le cast garde 8 bits)."],
   pitfalls=["Utiliser `<= n` : un octet de trop est écrit (débordement).", "Oublier le cast `(unsigned char)c` ou renvoyer `ptr` (déjà avancé ou casté) au lieu de `s`."])

fn("ft_bzero", "Met à zéro les `n` premiers octets d'une zone mémoire.",
   [(3, 3, "Ne renvoie rien (`void`) : elle agit directement sur la zone `s`."),
    (5, 6, "Comme pour `ft_memset` : un `unsigned char *` pour travailler octet par octet, et un compteur `size_t`."),
    (8, 9, "Cast de `s` en pointeur d'octets, puis `i` à 0."),
    (10, 14, "Pour chaque octet, `ptr[i] = 0` : la valeur **nulle** (pas le caractère `'0'` qui vaut 48).")],
   cases=["`n = 0` : rien ne change.", "`ft_bzero(buf, 4)` : `buf[0]` à `buf[3]` valent 0, les suivants ne bougent pas."],
   pitfalls=["Écrire `'0'` au lieu de `0`.", "`bzero` est équivalente à `ft_memset(s, 0, n)` : tu peux d'ailleurs l'écrire ainsi."])

fn("ft_memcpy", "Copie `n` octets de `src` vers `dest` (les zones ne doivent pas se chevaucher).",
   [(3, 3, "`dest` est modifiable (`void *`), `src` est en lecture seule (`const void *`). Renvoie `dest`."),
    (5, 7, "Deux pointeurs d'octets : `d` pour écrire (pas de `const`), `s` pour lire (**`const`** pour respecter la promesse de ne pas modifier la source), et le compteur `i`."),
    (9, 10, "Si **les deux** pointeurs sont `NULL`, on renvoie `NULL` sans rien copier (la vraie `memcpy` est indéfinie ici ; ce cas évite un plantage)."),
    (11, 12, "Casts des `void *` vers des pointeurs d'octets."),
    (13, 13, "Départ à 0."),
    (14, 18, "On copie octet par octet, **de gauche à droite** : `d[i] = s[i]`."),
    (19, 19, "On renvoie `dest` (le pointeur d'origine, pas `d`).")],
   cases=["`n = 0` : aucune copie, renvoie `dest`.", "Zones qui se chevauchent : comportement **indéfini** (c'est le rôle de `ft_memmove`).", "Contrairement à `strcpy`, **le `'\\0'` n'est pas copié automatiquement** : seulement les `n` octets demandés."],
   trace="src = \"abc\", n = 3\ni=0 : d[0] = 'a'\ni=1 : d[1] = 'b'\ni=2 : d[2] = 'c'   -> 3 octets copies",
   pitfalls=["Copier à l'envers par erreur (ce n'est utile que pour `memmove`).", "Retourner `d` ou `s` au lieu de `dest`."])

fn("ft_memmove", "Copie `n` octets de `src` vers `dest` **même si les zones se chevauchent**.",
   [(3, 3, "Fonction d'aide `static` (visible seulement dans ce fichier) : elle fait la copie dans le bon sens. Elle sert à tenir dans les 25 lignes de la norme."),
    (5, 5, "Un compteur `size_t`."),
    (7, 15, "Si `d < s` (la destination est **avant** la source) : copie de **gauche à droite**, comme `memcpy`. On lit chaque octet avant que l'écriture ne puisse l'écraser."),
    (16, 24, "Sinon (`d >= s`) : copie de **droite à gauche**. `i` part de `n` et on décrémente **avant** de copier (`i--` puis `d[i] = s[i]`) : ainsi `i` va de `n - 1` à `0` et ne devient jamais négatif (important avec un `size_t`)."),
    (27, 27, "La vraie fonction : mêmes paramètres que `memcpy`."),
    (29, 30, "Pointeurs d'octets, comme pour `memcpy`."),
    (32, 33, "Cas particulier : si `dest` **et** `src` sont `NULL`, on renvoie `NULL` sans rien faire."),
    (34, 36, "Casts puis appel de l'aide qui choisit le sens."),
    (37, 37, "On renvoie `dest`.")],
   cases=["`dest == src` : la copie ne change rien.", "`n = 0` : rien à faire.", "Chevauchement avec `dest > src` : on copie de la fin vers le début."],
   trace="buf = \"abcdef\" ; ft_memmove(buf + 2, buf, 4)\nd = buf+2 est APRES s = buf  -> copie de droite a gauche :\ni=3 : d[3]=s[3] -> buf[5] = 'd'  \"abcded\"\ni=2 : d[2]=s[2] -> buf[4] = 'c'  \"abcdcd\"\ni=1 : d[1]=s[1] -> buf[3] = 'b'  \"abcbcd\"\ni=0 : d[0]=s[0] -> buf[2] = 'a'  \"ababcd\"  (correct)",
   pitfalls=["Toujours copier de gauche à droite : faux quand `dest > src`.", "Faire `i = n - 1; while (i >= 0)` avec un `size_t` : boucle infinie, `i` ne peut pas être négatif."])

fn("ft_strlcpy", "Copie `src` dans `dest` sans dépasser `size` octets (le `'\\0'` compris) et renvoie la longueur de `src`.",
   [(3, 3, "`size` est la taille **totale** du buffer `dest`. Retourne un `size_t` : la longueur que la copie « aurait voulu » avoir."),
    (5, 5, "Un compteur `i` pour avancer dans `src` et `dest`."),
    (7, 7, "Départ à 0."),
    (8, 9, "Si `size == 0`, on n'a même pas la place pour un `'\\0'` : on n'écrit **rien** et on renvoie `ft_strlen(src)`."),
    (10, 14, "On copie tant qu'il reste des caractères dans `src` **et** qu'on n'a pas rempli `size - 1` cases (on garde une place pour le `'\\0'`)."),
    (15, 15, "On termine toujours `dest` par `'\\0'` (ici `size >= 1`, donc il y a de la place)."),
    (16, 16, "On renvoie la longueur **complète** de `src`. Si ce retour est ≥ `size`, la copie a été tronquée.")],
   cases=["`ft_strlcpy(d, \"hello\", 4)` : `d = \"hel\"`, retour **5**.", "`ft_strlcpy(d, \"ab\", 10)` : `d = \"ab\"`, retour **2**.", "`size = 0` : `dest` n'est pas touché, retour `strlen(src)`."],
   trace="d[4], src = \"hello\", size = 4\ni=0..2 : copie 'h','e','l' (i < size-1 = 3)\ni=3 : stop (3 < 3 est faux)\nd[3] = '\\0'  -> d = \"hel\"\nretour strlen(src) = 5   (5 >= 4 : tronque)",
   pitfalls=["Copier `size` caractères au lieu de `size - 1` : plus de place pour le `'\\0'`.", "Renvoyer le nombre de caractères **copiés** au lieu de `strlen(src)`."])

fn("ft_strlcat", "Ajoute `src` à la fin de `dest` sans que `dest` dépasse `size` octets au total ; renvoie la longueur qu'aurait eue le résultat.",
   [(3, 3, "`size` est la taille **totale** du buffer `dest`, `'\\0'` compris."),
    (5, 7, "`dest_len` : longueur de `dest` ; `src_len` : longueur de `src` ; `i` : position dans `src`."),
    (9, 11, "On mesure `dest` **sans dépasser `size`** : si `dest` n'a pas de `'\\0'` dans ses `size` premiers octets, on s'arrête à `size` (on ne lit jamais au-delà du buffer)."),
    (12, 12, "Longueur de `src`, nécessaire pour la valeur de retour."),
    (13, 14, "Si `size <= dest_len`, il n'y a **aucune place** : on n'écrit rien et on renvoie `size + src_len`."),
    (15, 20, "On copie `src` à la suite de `dest` tant qu'il reste de la place : `dest_len + i < size - 1` garde une case pour le `'\\0'`."),
    (21, 21, "On termine par `'\\0'`."),
    (22, 22, "Retour : `dest_len + src_len` = la longueur du résultat **idéal**. Si ≥ `size`, il y a eu troncature.")],
   cases=["`d = \"ab\"` (buffer de 10), `ft_strlcat(d, \"cdef\", 5)` : `d = \"abcd\"`, retour **6**.", "`d = \"abc\"`, `size = 3` : rien n'est écrit, retour `3 + strlen(src)`."],
   trace="d = \"ab\", src = \"cdef\", size = 5\ndest_len = 2, src_len = 4 ; size(5) > 2 : on copie\ni=0 : 2+0 < 4 ok -> d[2]='c'\ni=1 : 2+1 < 4 ok -> d[3]='d'\ni=2 : 2+2 < 4 faux -> stop\nd[4] = '\\0' -> d = \"abcd\"  ; retour 2 + 4 = 6",
   pitfalls=["Lire `dest` sans limite (`ft_strlen(dest)`) quand `dest` n'est pas terminé dans `size` octets.", "Oublier le cas `size <= dest_len`."])

fn("ft_strchr", "Renvoie un pointeur sur la **première** occurrence de `c` dans `s`, ou `NULL`.",
   [(3, 3, "`const char *s` en entrée, mais on renvoie un `char *` (pointeur **dans** la chaîne d'origine, pas une copie). `int c` : le caractère cherché."),
    (5, 8, "On parcourt la chaîne avec le pointeur `s` lui-même. On compare avec `(char)c` : `c` est un `int`, il faut le ramener à un `char`. Si trouvé : on renvoie `s` (adresse du caractère). Le cast `(char *)` retire le `const` : c'est nécessaire car le prototype renvoie un `char *`."),
    (9, 9, "Sinon on avance d'une case."),
    (11, 12, "Après la boucle, `s` pointe sur le `'\\0'` final. Si on cherchait justement `'\\0'`, on renvoie ce pointeur (la vraie `strchr` le permet)."),
    (13, 13, "Rien trouvé : `NULL`.")],
   cases=["`ft_strchr(\"hello\", 'l')` → pointeur sur l'indice 2 (le 1er `l`).", "`ft_strchr(\"hello\", 'z')` → `NULL`.", "`ft_strchr(\"hello\", '\\0')` → pointeur sur le `'\\0'` final (indice 5), **pas** `NULL`.", "`ft_strchr(\"\", 'a')` → `NULL`."],
   pitfalls=["Oublier le cas `c == '\\0'`.", "Renvoyer l'**indice** au lieu d'un pointeur.", "Comparer `*s` à `c` sans le cast `(char)`."])

fn("ft_strrchr", "Renvoie un pointeur sur la **dernière** occurrence de `c` dans `s`, ou `NULL`.",
   [(3, 3, "Même prototype que `ft_strchr`."),
    (5, 5, "`last_occurrence` mémorise la dernière position trouvée. `const char *` car on pointe dans une chaîne qu'on ne modifie pas."),
    (7, 7, "Au départ, rien trouvé : `NULL`."),
    (8, 13, "On parcourt **toute** la chaîne. À chaque fois que `*s == (char)c`, on met à jour `last_occurrence` : la dernière mise à jour est donc la dernière occurrence."),
    (14, 15, "Cas `c == '\\0'` : la dernière « occurrence » est le `'\\0'` final, sur lequel `s` pointe maintenant."),
    (16, 16, "Sinon on renvoie la dernière position mémorisée (ou `NULL` si jamais trouvé). Cast `(char *)` pour retirer le `const`.")],
   cases=["`ft_strrchr(\"hello\", 'l')` → pointeur sur l'indice 3 (le 2e `l`).", "`ft_strrchr(\"hello\", 'z')` → `NULL`.", "`ft_strrchr(\"hello\", '\\0')` → pointeur sur le `'\\0'` final."],
   pitfalls=["S'arrêter à la première occurrence (c'est `ft_strchr`).", "Oublier le cas `'\\0'`."])

fn("ft_strncmp", "Compare au plus `n` caractères de deux chaînes ; renvoie la différence du premier octet différent.",
   [(3, 3, "Retourne un `int` : négatif si `s1 < s2`, 0 si égales (sur `n` caractères), positif sinon."),
    (5, 5, "Un compteur `i` (type `size_t`, comme `n`)."),
    (7, 7, "Départ à 0."),
    (8, 8, "On continue tant que `i < n` **et** qu'au moins une des chaînes n'est pas finie (`s1[i] || s2[i]`). Ainsi on s'arrête au `'\\0'` : `strncmp` travaille sur des chaînes."),
    (10, 11, "Dès que deux caractères diffèrent, on renvoie leur **différence**. On caste en **`unsigned char`** : les octets au-dessus de 127 doivent compter comme des nombres positifs (comme dans la vraie libc)."),
    (12, 12, "Les caractères sont égaux : on passe au suivant."),
    (14, 14, "Si on arrive ici : égalité sur `n` caractères (ou jusqu'au `'\\0'` commun) : **0**.")],
   cases=["`ft_strncmp(\"abc\", \"abd\", 3)` → négatif (`'c' - 'd' = -1`).", "`ft_strncmp(\"abc\", \"abd\", 2)` → 0 (on compare seulement `\"ab\"`).", "`n = 0` → 0.", "`ft_strncmp(\"a\", \"\", 5)` → positif (`'a' - '\\0'`)."],
   pitfalls=["Oublier le cast en `unsigned char`.", "Continuer après le `'\\0'` (`memcmp` le fait, pas `strncmp`).", "Utiliser `<= n` : un caractère de trop."])

fn("ft_memchr", "Cherche un octet dans les `n` premiers octets d'une zone ; renvoie un pointeur ou `NULL`.",
   [(3, 3, "`const void *s` : zone en lecture seule. Renvoie un `void *` (pointeur sur l'octet trouvé)."),
    (5, 6, "`ptr` pour lire octet par octet (`const unsigned char *`), `ch` pour l'octet cherché."),
    (8, 8, "On convertit `c` (un `int`) en `unsigned char` une bonne fois pour toutes."),
    (9, 9, "Cast de la zone en pointeur d'octets."),
    (10, 15, "`while (n--)` : la boucle tourne **exactement `n` fois** (la valeur de `n` avant la décrémentation est testée). Si l'octet courant vaut `ch`, on renvoie son adresse (cast `(void *)` pour retirer le `const`), sinon on avance."),
    (16, 16, "Rien trouvé : `NULL`.")],
   cases=["`n = 0` → `NULL` sans rien lire.", "Contrairement à `strchr`, **ne s'arrête pas au `'\\0'`** : elle regarde `n` octets quoi qu'ils valent.", "`ft_memchr(\"abc\\0def\", 'e', 7)` trouve le `e` après le `'\\0'`."],
   pitfalls=["S'arrêter au `'\\0'` (ce sont les `str*` qui le font).", "Lire plus de `n` octets."])

fn("ft_memcmp", "Compare `n` octets de deux zones ; renvoie la différence du premier octet différent.",
   [(3, 3, "Deux zones en lecture seule. Retourne un `int` (négatif, 0 ou positif)."),
    (5, 7, "Deux pointeurs d'octets **non signés** (`unsigned char`), pour que les valeurs soient comparées de 0 à 255."),
    (9, 11, "Casts et départ à 0."),
    (12, 17, "Pour chaque position, si les octets diffèrent, on renvoie leur **différence** (`ptr1[i] - ptr2[i]`). Sinon on avance."),
    (18, 18, "Les `n` octets sont identiques : **0**.")],
   cases=["`n = 0` → 0.", "Ne s'arrête **pas** au `'\\0'` : `ft_memcmp(\"a\\0b\", \"a\\0c\", 3)` est négatif.", "`ft_memcmp(\"abc\", \"abd\", 3)` → négatif."],
   pitfalls=["Comparer des `char` signés : un octet `0xFF` vaudrait -1.", "Oublier que `memcmp` compare des octets bruts, pas des chaînes."])

fn("ft_strnstr", "Cherche la chaîne `needle` dans les `len` premiers caractères de `haystack`.",
   [(3, 3, "`haystack` = la botte de foin, `needle` = l'aiguille, `len` = nombre maximum de caractères de `haystack` examinés. Retourne un pointeur dans `haystack` ou `NULL`."),
    (5, 6, "`i` : où commence la tentative dans `haystack` ; `j` : combien de caractères de `needle` ont déjà correspondu."),
    (8, 9, "Si `needle` est vide, on renvoie directement `haystack` (comportement de `strstr`)."),
    (10, 10, "On commence à l'indice 0."),
    (11, 12, "Boucle externe : essayer chaque position de départ `i`, tant qu'on n'a pas dépassé la chaîne ni `len`."),
    (13, 13, "Pour chaque départ, on repart de `j = 0`."),
    (14, 16, "Boucle interne : on avance tant que les caractères **correspondent** et que `i + j < len` (on ne dépasse jamais `len`). Cette condition `i + j < len` est la clé de la fonction."),
    (17, 18, "Si on a parcouru tout `needle` (on est sur son `'\\0'`), c'est trouvé : on renvoie l'adresse du début de la correspondance."),
    (19, 19, "Sinon, on essaie le départ suivant."),
    (21, 21, "Aucune correspondance : `NULL`.")],
   cases=["`ft_strnstr(\"hello\", \"llo\", 5)` → pointeur sur l'indice 2.", "`ft_strnstr(\"hello\", \"llo\", 4)` → `NULL` (« llo » dépasserait `len`).", "`ft_strnstr(\"abc\", \"\", 0)` → `haystack`.", "`needle` plus long que `haystack` → `NULL`."],
   trace="haystack = \"hello\", needle = \"ll\", len = 5\ni=0 : 'h' != 'l'          -> j=0, needle[0] != 0 -> i=1\ni=1 : 'e' != 'l'          -> i=2\ni=2 : 'l'=='l' j=1, 'l'=='l' j=2, needle[2]=='\\0' -> trouve : haystack + 2",
   pitfalls=["Ne pas borner par `len` : on lit trop loin.", "Oublier le cas `needle` vide."])

fn("ft_atoi", "Convertit le début d'une chaîne en nombre `int`, comme `atoi`.",
   [(3, 3, "`const char *str` : on lit sans modifier. Retourne un `int`."),
    (5, 7, "`i` : position dans la chaîne ; `sign` : +1 ou -1 ; `result` : le nombre en cours de construction."),
    (9, 11, "Valeurs de départ : indice 0, signe positif, résultat 0. (La norme interdit d'initialiser à la déclaration, donc on le fait ici.)"),
    (12, 13, "**Sauter les espaces blancs** du début : l'espace `' '` et les codes 9 à 13 (`\\t \\n \\v \\f \\r`)."),
    (14, 19, "**Le signe** : un seul `+` ou `-` est accepté. Si c'est `'-'`, `sign` passe à -1. Dans les deux cas on avance d'une case (`i++`) pour passer le signe."),
    (20, 24, "**Les chiffres** : tant que le caractère est entre `'0'` et `'9'`, on décale le résultat d'un cran (`result * 10`) et on ajoute le chiffre (`str[i] - '0'` transforme le caractère `'7'` en nombre 7). La boucle s'arrête au premier caractère qui n'est pas un chiffre."),
    (25, 25, "On applique le signe à la fin.")],
   cases=["`ft_atoi(\"  -42abc\")` → -42.", "`ft_atoi(\"abc\")` → 0 (aucun chiffre).", "`ft_atoi(\"+5\")` → 5 ; `ft_atoi(\"+-5\")` → 0 (un seul signe).", "`ft_atoi(\"\")` → 0.", "Débordement (`\"99999999999\"`) : comportement indéfini, comme `atoi`."],
   trace="str = \"  -42abc\"\n2 espaces sautes -> i=2\nstr[2] = '-' : sign = -1, i=3\nstr[3] = '4' : result = 0*10 + 4 = 4\nstr[4] = '2' : result = 4*10 + 2 = 42\nstr[5] = 'a' : stop\nreturn 42 * -1 = -42",
   pitfalls=["Accepter plusieurs signes (`\"--5\"`).", "Oublier `- '0'` (on ajouterait 52 pour `'4'`).", "Ne pas sauter les caractères 9 à 13."])

fn("ft_calloc", "Alloue `count * size` octets **mis à zéro**.",
   [(3, 3, "Mêmes paramètres que `calloc` : `count` éléments de `size` octets. Renvoie un `void *` (ou `NULL` si échec)."),
    (5, 5, "Le pointeur vers la mémoire allouée."),
    (7, 8, "**Protection contre le débordement** : `count * size` peut dépasser le maximum d'un `size_t` et donner une petite valeur fausse. On teste avant avec une **division** (`size > SIZE_MAX / count`), qui, elle, ne déborde pas. `count != 0` évite la division par zéro."),
    (9, 9, "On alloue le nombre d'octets demandé."),
    (10, 11, "Toujours tester `malloc` : s'il échoue (`NULL`), on renvoie `NULL`."),
    (12, 12, "On met tous les octets à 0 avec `ft_bzero` (la différence avec `malloc`)."),
    (13, 13, "On renvoie la zone.")],
   cases=["`ft_calloc(3, 4)` → 12 octets à zéro.", "`ft_calloc(0, 4)` ou `ft_calloc(4, 0)` → un pointeur **non `NULL`** (sujet v19.3), car `malloc(0)` renvoie un pointeur valide sur ce système.", "`ft_calloc(SIZE_MAX, 2)` → `NULL` (débordement)."],
   pitfalls=["Faire `malloc(count * size)` sans tester le débordement.", "Oublier de mettre à zéro.", "Libérer deux fois : `free` une seule fois par l'appelant."])

fn("ft_strdup", "Renvoie une **copie** d'une chaîne, allouée avec `malloc`.",
   [(3, 3, "Reçoit une chaîne en lecture seule, renvoie un `char *` à libérer par l'appelant."),
    (5, 6, "`dest` : la nouvelle chaîne ; `len` : la longueur de la source."),
    (8, 8, "On mesure la source avec `ft_strlen`."),
    (9, 9, "`malloc(len + 1)` : les `len` caractères **plus le `'\\0'`**."),
    (10, 11, "Si `malloc` échoue : `NULL`."),
    (12, 12, "`ft_memcpy(dest, src, len + 1)` copie les caractères **et** le `'\\0'` final en une seule fois."),
    (13, 13, "On renvoie la copie : c'est à l'appelant de faire `free`.")],
   cases=["`ft_strdup(\"\")` → chaîne vide allouée (1 octet).", "Modifier la copie ne modifie pas l'original.", "Si `malloc` échoue : `NULL`."],
   pitfalls=["`malloc(len)` sans le `+ 1` : débordement d'un octet.", "Renvoyer `src` au lieu d'une copie.", "Oublier que le résultat doit être libéré."])

# ============================================================ PARTIE 2 : fonctions en plus
fn("ft_substr", "Extrait une sous-chaîne de `s` à partir de `start`, de longueur au plus `len`.",
   [(3, 3, "`start` est un `unsigned int`, `len` un `size_t`. Retourne une **nouvelle chaîne allouée**."),
    (5, 7, "`substr` : le résultat ; `i` : compteur de copie ; `s_len` : longueur de `s`."),
    (9, 10, "Si `s` est `NULL` : `NULL`."),
    (11, 11, "On calcule la longueur de `s`."),
    (12, 13, "Si `start` est **au-delà de la fin** (`start >= s_len`), il n'y a rien à extraire : on renvoie une **chaîne vide allouée** (`ft_strdup(\"\")`), pas `NULL`."),
    (14, 15, "On **réduit `len`** à ce qui reste après `start` (`s_len - start`) : on ne copie jamais plus que ce qui existe."),
    (16, 18, "`malloc(len + 1)` (le `+ 1` pour le `'\\0'`) et test de `NULL`."),
    (19, 24, "Copie de `len` caractères à partir de `s[start]`."),
    (25, 25, "Terminaison par `'\\0'`."),
    (26, 26, "On renvoie la sous-chaîne (à libérer par l'appelant).")],
   cases=["`ft_substr(\"hello\", 1, 3)` → `\"ell\"`.", "`ft_substr(\"hello\", 10, 3)` → `\"\"` (chaîne vide allouée).", "`ft_substr(\"hello\", 2, 100)` → `\"llo\"` (len réduit).", "`len = 0` → chaîne vide."],
   trace="s = \"hello\" (s_len = 5), start = 1, len = 3\nstart(1) < 5 -> ok ; len(3) <= 5-1 -> inchange\nmalloc(4)\ncopie s[1],s[2],s[3] = 'e','l','l'\nsubstr[3] = '\\0' -> \"ell\"",
   pitfalls=["Renvoyer `NULL` quand `start` dépasse la fin (le sujet attend une chaîne vide).", "Ne pas borner `len` : lecture au-delà de `s`.", "Oublier le `+ 1` du `malloc`."])

fn("ft_strjoin", "Concatène `s1` et `s2` dans une **nouvelle** chaîne allouée.",
   [(3, 3, "Deux chaînes en lecture seule, une chaîne allouée en sortie."),
    (5, 7, "`str` : le résultat ; `len1`, `len2` : les longueurs."),
    (9, 10, "Si l'une des chaînes est `NULL` : on renvoie `NULL`."),
    (11, 12, "On mesure les deux chaînes."),
    (13, 13, "`malloc(len1 + len2 + 1)` : les deux longueurs **plus le `'\\0'`**."),
    (14, 15, "Test de `NULL`."),
    (16, 16, "On copie `s1` (sans son `'\\0'`) au début de `str`."),
    (17, 17, "On copie `s2` juste après (`str + len1`), **avec son `'\\0'`** (`len2 + 1`) : c'est lui qui termine le résultat."),
    (18, 18, "On renvoie la nouvelle chaîne.")],
   cases=["`ft_strjoin(\"ab\", \"cde\")` → `\"abcde\"` (6 octets alloués).", "`ft_strjoin(\"\", \"\")` → `\"\"`.", "Les deux chaînes d'origine ne sont pas modifiées."],
   trace="s1 = \"ab\", s2 = \"cde\" : len1 = 2, len2 = 3, malloc(6)\nmemcpy(str, s1, 2)         -> \"ab\"\nmemcpy(str + 2, s2, 3 + 1) -> \"abcde\\0\"",
   pitfalls=["`malloc(len1 + len2)` : pas de place pour le `'\\0'`.", "Copier `s1` avec son `'\\0'` : il couperait la chaîne."])

fn("ft_strtrim", "Retire de **début et fin** de `s1` tous les caractères présents dans `set`.",
   [(3, 3, "`set` : l'ensemble des caractères à retirer. Renvoie une chaîne allouée."),
    (5, 7, "`trimmed` : résultat ; `start` : premier caractère conservé ; `end` : indice juste après le dernier caractère conservé."),
    (9, 10, "Si `s1` ou `set` est `NULL` : `NULL`."),
    (11, 13, "**Début** : on avance `start` tant que le caractère courant est dans `set` (`ft_strchr(set, s1[start])` n'est pas `NULL`)."),
    (14, 14, "`end` démarre à la **fin** de la chaîne."),
    (15, 16, "**Fin** : on recule `end` tant que le caractère **juste avant** est dans `set`, sans jamais passer sous `start` (`end > start`)."),
    (17, 18, "`ft_substr` extrait la partie conservée : de `start`, sur `end - start` caractères. Elle gère aussi le cas « tout a été retiré » (résultat vide).")],
   cases=["`ft_strtrim(\"  hi  \", \" \")` → `\"hi\"`.", "`ft_strtrim(\"xxhixx\", \"x\")` → `\"hi\"`.", "`ft_strtrim(\"xxx\", \"x\")` → `\"\"` (tout retiré).", "`ft_strtrim(\"abc\", \"\")` → `\"abc\"` (`set` vide)."],
   trace="s1 = \"  hi  \", set = \" \"\nstart : s1[0]=' ' dans set -> 1 ; s1[1]=' ' -> 2 ; s1[2]='h' stop  => start = 2\nend = 6 : s1[5]=' ' -> 5 ; s1[4]=' ' -> 4 ; s1[3]='i' stop => end = 4\nsubstr(s1, 2, 2) = \"hi\"",
   pitfalls=["Retirer aussi les caractères du **milieu** (on ne touche que début et fin).", "Oublier la condition `end > start` : `end` descendrait sous `start` sur une chaîne entièrement retirée."])

fn("ft_split", "Découpe `s` selon le séparateur `c` et renvoie un tableau de chaînes terminé par `NULL`.",
   [(3, 22, "**`count_words`** : compte les mots. `in_word` indique si on est déjà dans un mot. Quand on voit un caractère ≠ séparateur **et** qu'on n'était pas dans un mot, c'est le **début d'un mot** : `count++`. Un séparateur remet `in_word` à 0."),
    (24, 40, "**`alloc_word`** : alloue et copie **un** mot de `len` caractères : `malloc(len + 1)`, test de `NULL`, copie, puis `'\\0'` final (`word[i] = '\\0'`)."),
    (42, 51, "**`free_all`** : en cas d'échec, libère les `i` mots déjà alloués (de `i - 1` à 0), puis le tableau lui-même, et renvoie `NULL`. On libère donc **tout** ce qui est déjà alloué : aucune fuite."),
    (53, 56, "**`fill_tab`** remplit le tableau. `i` : numéro du mot courant ; `len` : longueur du mot courant."),
    (58, 59, "`i` repart à 0 ; la boucle externe tourne tant qu'il reste des caractères."),
    (61, 62, "On saute les séparateurs en tête (`while (*s && *s == c) s++`)."),
    (63, 67, "S'il reste des caractères, on **mesure le mot** : `len` avance jusqu'au prochain séparateur ou à la fin."),
    (68, 73, "On alloue le mot. Si ça échoue : `free_all(tab, i)` libère les `i` mots déjà faits et le tableau, puis `fill_tab` renvoie 0 (échec)."),
    (74, 75, "Mot réussi : on passe au suivant (`i++`) et on avance `s` de `len` pour sauter le mot."),
    (78, 79, "À la fin on écrit **`tab[i] = NULL`** (la case finale) et on renvoie 1 (succès)."),
    (82, 82, "La fonction principale : prototype avec `char **` en retour (tableau de chaînes)."),
    (84, 87, "`tab` : le tableau. Si `s` est `NULL` : `NULL`."),
    (88, 90, "On alloue le tableau : **`count_words + 1`** cases (le `+ 1` pour la case `NULL` finale)."),
    (91, 93, "On remplit. Si `fill_tab` échoue, il a déjà tout libéré : on renvoie `NULL`. Sinon on renvoie le tableau.")],
   cases=["`ft_split(\"a b c\", ' ')` → `{\"a\", \"b\", \"c\", NULL}`.", "`ft_split(\"  a  b \", ' ')` → `{\"a\", \"b\", NULL}` (séparateurs répétés ignorés).", "`ft_split(\"hello\", 'z')` → `{\"hello\", NULL}`.", "`ft_split(\"\", ' ')` → `{NULL}` (tableau alloué de 1 case).", "Un `malloc` qui échoue : tout est libéré, la fonction renvoie `NULL`."],
   trace="s = \"a bc\", c = ' '\ncount_words = 2  -> malloc(3 cases)\nfill_tab : saute rien, mot 'a' (len 1) -> tab[0] = \"a\"\n           saute ' ', mot 'bc' (len 2) -> tab[1] = \"bc\"\n           tab[2] = NULL",
   pitfalls=["Oublier le `+ 1` du tableau (pas de `NULL` final).", "Ne pas libérer les mots déjà alloués quand un `malloc` échoue.", "Créer des mots vides pour des séparateurs consécutifs."],
   why=["Pourquoi 5 petites fonctions ? La norme limite une fonction à 25 lignes : on découpe en fonctions `static` (invisibles hors du fichier), chacune avec **une** responsabilité."])

fn("ft_itoa", "Convertit un `int` en chaîne de caractères allouée.",
   [(3, 19, "**`ft_nbrlen`** compte les caractères nécessaires. `if (n <= 0)` : pour `0` ou un négatif, il faut **1 caractère de plus** (le chiffre `'0'` ou le signe `'-'`), puis on prend l'opposé. La boucle compte ensuite les chiffres en divisant par 10 (`n /= 10`)."),
    (21, 21, "La fonction principale : un `int` en entrée, une chaîne allouée en sortie."),
    (23, 25, "`nb` est un **`long long`** : pour pouvoir calculer l'opposé de `INT_MIN` (-2147483648) sans débordement. `len` : nombre de caractères. `res` : le résultat."),
    (27, 28, "On copie `n` dans `nb`, puis on calcule la longueur."),
    (29, 31, "`malloc(len + 1)` et test de `NULL`."),
    (32, 32, "On pose tout de suite le `'\\0'` final à l'indice `len`."),
    (33, 37, "Si le nombre est **négatif** : `'-'` en première case, puis on passe à la valeur positive."),
    (38, 39, "**Cas 0** : la boucle suivante ne tourne pas pour 0, donc on écrit `'0'` à la main."),
    (40, 44, "On remplit **de droite à gauche** : `--len` puis `res[len] = nb % 10 + '0'` (le dernier chiffre, converti en caractère), puis `nb /= 10` pour passer au chiffre suivant."),
    (45, 45, "On renvoie la chaîne.")],
   cases=["`ft_itoa(42)` → `\"42\"` ; `ft_itoa(-42)` → `\"-42\"`.", "`ft_itoa(0)` → `\"0\"`.", "`ft_itoa(-2147483648)` → `\"-2147483648\"` (cas `INT_MIN`).", "`ft_itoa(2147483647)` → `\"2147483647\"`."],
   trace="n = -105 : nbrlen = 4  (1 pour '-' + 3 chiffres), malloc(5)\nres[4] = '\\0' ; nb < 0 : res[0] = '-', nb = 105\n--len=3 : res[3] = 105 % 10 + '0' = '5' ; nb = 10\n--len=2 : res[2] = '0' ; nb = 1\n--len=1 : res[1] = '1' ; nb = 0  -> \"-105\"",
   pitfalls=["Oublier `INT_MIN` : `-n` déborde dans un `int` ; utiliser un `long long`.", "Oublier le cas `0`.", "Oublier le `'\\0'` ou un caractère pour le signe dans la taille."])

fn("ft_strmapi", "Crée une **nouvelle** chaîne en appliquant `f(indice, caractère)` à chaque caractère de `s`.",
   [(3, 3, "`char (*f)(unsigned int, char)` : un **pointeur de fonction** qui reçoit l'indice et le caractère, et renvoie un caractère."),
    (5, 6, "`res` : la nouvelle chaîne ; `i` : l'indice (un `unsigned int`, comme le veut `f`)."),
    (8, 9, "Si `s` ou `f` est `NULL` : `NULL`."),
    (10, 12, "On alloue `ft_strlen(s) + 1` octets et on teste `NULL`."),
    (13, 13, "Départ à l'indice 0."),
    (14, 18, "Pour chaque caractère : `res[i] = f(i, s[i])`. **On écrit dans `res`** : `s` reste intacte."),
    (19, 19, "Terminaison de la nouvelle chaîne par `'\\0'`."),
    (20, 20, "On renvoie `res` (à libérer par l'appelant).")],
   cases=["Avec `f` qui renvoie `c - 32` : `ft_strmapi(\"abc\", f)` → `\"ABC\"`.", "`ft_strmapi(\"\", f)` → chaîne vide allouée.", "`s` n'est pas modifiée."],
   pitfalls=["Modifier `s` (c'est le rôle de `ft_striteri`).", "Oublier le `'\\0'` final.", "Appeler `f(s[i], i)` : l'indice vient en premier."])

fn("ft_striteri", "Applique `f(indice, &caractère)` à chaque caractère de `s`, **sur place**.",
   [(3, 3, "`void (*f)(unsigned int, char *)` : la fonction reçoit l'indice et **l'adresse** du caractère, donc elle peut le modifier. `ft_striteri` ne renvoie rien."),
    (5, 5, "`i` : l'indice, de type `unsigned int` (celui de `f`)."),
    (7, 8, "Si `s` ou `f` est `NULL`, on ne fait rien."),
    (9, 9, "Départ à 0."),
    (10, 14, "Pour chaque caractère : `f(i, &s[i])`. L'adresse `&s[i]` permet à `f` de changer le caractère de la chaîne d'origine.")],
   cases=["Avec `f` qui fait `*c = i + '0'` : `\"xyz\"` devient `\"012\"`.", "Chaîne vide : `f` n'est jamais appelée.", "Aucun `malloc`, aucune valeur de retour."],
   pitfalls=["Passer `s[i]` au lieu de `&s[i]` : `f` ne pourrait pas modifier la chaîne.", "Confondre avec `ft_strmapi` (qui crée une nouvelle chaîne)."])

fn("ft_putchar_fd", "Écrit le caractère `c` sur le descripteur de fichier `fd`.",
   [(3, 3, "`char c` : le caractère. `int fd` : la destination (1 = écran, 2 = erreurs). Ne renvoie rien."),
    (5, 5, "`write(fd, &c, 1)` : on passe l'**adresse** de `c` (`&c`) et le nombre d'octets à écrire (1). Écrire `write(fd, c, 1)` serait faux : `c` est un nombre, pas une adresse.")],
   cases=["`ft_putchar_fd('A', 1)` affiche `A`.", "Un `fd` invalide : `write` échoue en silence (on ne gère pas ce cas)."],
   pitfalls=["Oublier le `&`.", "Écrire plus d'un octet."])

fn("ft_putstr_fd", "Écrit la chaîne `s` sur le descripteur `fd`.",
   [(3, 3, "`char *s` : la chaîne ; `fd` : la destination."),
    (5, 6, "Si `s` est `NULL`, on ne fait rien (évite un plantage)."),
    (7, 7, "`write(fd, s, ft_strlen(s))` : on écrit **tous les caractères d'un coup**, sans le `'\\0'` final.")],
   cases=["`ft_putstr_fd(\"abc\", 1)` écrit 3 octets.", "`ft_putstr_fd(\"\", 1)` n'écrit rien."],
   pitfalls=["Écrire le `'\\0'` (`ft_strlen(s) + 1`) : il apparaîtrait dans la sortie."])

fn("ft_putendl_fd", "Écrit la chaîne `s` suivie d'un retour à la ligne.",
   [(3, 3, "Mêmes paramètres que `ft_putstr_fd`."),
    (5, 6, "Si `s` est `NULL`, on ne fait rien."),
    (7, 7, "On écrit la chaîne (sans son `'\\0'`)."),
    (8, 8, "Puis **un** retour à la ligne `\"\\n\"`, avec `write(fd, \"\\n\", 1)`.")],
   cases=["`ft_putendl_fd(\"abc\", 1)` écrit `abc` puis `\\n` : 4 octets.", "`ft_putendl_fd(\"\", 1)` écrit seulement `\\n`."],
   pitfalls=["Oublier le `\\n`.", "Écrire deux retours à la ligne."])

fn("ft_putnbr_fd", "Écrit l'entier `n` sur le descripteur `fd` (en caractères).",
   [(3, 3, "Reçoit un `int`, écrit sur `fd`, ne renvoie rien."),
    (5, 5, "`nb` : un `long long`, pour supporter `INT_MIN` (voir le cours « atoi et itoa »)."),
    (7, 7, "On copie `n` dans `nb`."),
    (8, 12, "Nombre **négatif** : on écrit `'-'` **une seule fois**, puis on travaille sur la valeur positive."),
    (13, 14, "**Récursion** : si `nb >= 10`, on écrit **d'abord** tous les chiffres de gauche (`nb / 10`). C'est ce qui garantit le bon ordre."),
    (15, 15, "Puis on écrit le **dernier chiffre** : `nb % 10` (0 à 9) + `'0'` pour le transformer en caractère.")],
   cases=["`ft_putnbr_fd(42, 1)` écrit `42`.", "`ft_putnbr_fd(-42, 1)` écrit `-42`.", "`ft_putnbr_fd(0, 1)` écrit `0`.", "`ft_putnbr_fd(-2147483648, 1)` écrit `-2147483648`."],
   trace="ft_putnbr_fd(42) : nb = 42 >= 10 -> ft_putnbr_fd(4)\n   ft_putnbr_fd(4) : 4 < 10 -> ecrit '4'\nretour : ecrit 42 % 10 + '0' = '2'   -> \"42\"",
   pitfalls=["Écrire le dernier chiffre **avant** l'appel récursif : le nombre sortirait à l'envers.", "Oublier `INT_MIN`.", "Écrire plusieurs `'-'`."])

# ============================================================ PARTIE 3 : listes
fn("ft_lstnew", "Crée un nouveau noeud de liste contenant `content`, avec `next = NULL`.",
   [(3, 3, "Retourne un **`t_list *`** (pointeur sur le noeud). Reçoit un `void *` : n'importe quelle donnée, **non copiée**."),
    (5, 5, "`node` : le futur noeud."),
    (7, 9, "`malloc(sizeof(t_list))` réserve la place d'**un noeud**. Si ça échoue, `NULL`."),
    (10, 10, "On range l'adresse de la donnée (on **ne copie pas** le contenu)."),
    (11, 11, "Le noeud est seul : son `next` vaut `NULL`."),
    (12, 12, "On renvoie le noeud.")],
   cases=["`ft_lstnew(\"a\")` → noeud dont `content` pointe sur `\"a\"` et `next == NULL`.", "`ft_lstnew(NULL)` est valide : un noeud avec un contenu vide.", "Le noeud devra être libéré avec `ft_lstdelone`."],
   pitfalls=["Oublier d'initialiser `next` à `NULL`.", "Faire `malloc(sizeof(t_list *))` (la taille d'un pointeur, pas d'un noeud)."])

fn("ft_lstadd_front", "Ajoute le noeud `new` au **début** de la liste.",
   [(3, 3, "`t_list **lst` : l'**adresse** du pointeur de tête, car la tête va **changer**. Ne renvoie rien."),
    (5, 6, "Si `lst` ou `new` est `NULL`, on ne fait rien."),
    (7, 7, "Le nouveau noeud **pointe vers l'ancienne tête** (`*lst`). Si la liste était vide, `*lst` vaut `NULL` : `new->next` aussi, c'est correct."),
    (8, 8, "`*lst = new` : le nouveau noeud **devient la tête**. Cette ligne modifie le pointeur de l'appelant, d'où le `**`.")],
   cases=["Liste vide : `new` devient l'unique noeud.", "Liste `[b]` + `new = a` → `[a, b]`.", "Deux ajouts de suite : le dernier ajouté est en tête."],
   trace="avant :  *lst -> [b] -> NULL        new -> [a] -> NULL\nligne 7 : new->next = *lst   =>   [a] -> [b] -> NULL\nligne 8 : *lst = new         =>   *lst -> [a] -> [b] -> NULL",
   pitfalls=["Inverser les deux lignes : on perdrait l'ancienne tête.", "Passer un `t_list *` simple : la tête de l'appelant ne changerait pas."])

fn("ft_lstsize", "Compte les noeuds d'une liste.",
   [(3, 3, "Retourne un **`unsigned int`** (c'est écrit dans le sujet v19.3), pas un `int`."),
    (5, 5, "`n` : le compteur."),
    (7, 7, "Départ à 0 : une liste vide a 0 noeud."),
    (8, 12, "On parcourt : tant que `lst` n'est pas `NULL`, on compte (`n++`) puis on passe au noeud suivant (`lst = lst->next`). On modifie seulement la **copie locale** `lst`, pas la liste de l'appelant."),
    (13, 13, "On renvoie le nombre de noeuds.")],
   cases=["`ft_lstsize(NULL)` → 0.", "Liste `[a, b, c]` → 3."],
   trace="[a] -> [b] -> [c] -> NULL\nlst=a : n=1 ; lst=b : n=2 ; lst=c : n=3 ; lst=NULL : stop -> 3",
   pitfalls=["Renvoyer un `int` au lieu d'un `unsigned int`.", "Oublier de gérer la liste vide (la boucle le fait toute seule)."])

fn("ft_lstlast", "Renvoie le **dernier** noeud d'une liste.",
   [(3, 3, "Retourne un `t_list *` (le dernier noeud) ou `NULL`."),
    (5, 6, "Liste vide : `NULL` (sinon `lst->next` planterait)."),
    (7, 8, "On avance tant que le noeud **a un suivant** (`lst->next` non `NULL`). On s'arrête **sur** le dernier noeud, pas après lui."),
    (9, 9, "On renvoie ce dernier noeud.")],
   cases=["`ft_lstlast(NULL)` → `NULL`.", "Liste d'un noeud → ce noeud lui-même.", "`[a, b, c]` → `c`."],
   pitfalls=["Écrire `while (lst)` : on irait jusqu'à `NULL` et on renverrait `NULL`.", "Oublier le cas liste vide."])

fn("ft_lstadd_back", "Ajoute le noeud `new` à la **fin** de la liste.",
   [(3, 3, "`t_list **lst` : liste vide possible, la tête peut donc changer."),
    (5, 6, "Si `lst` ou `new` est `NULL`, on ne fait rien."),
    (7, 8, "**Liste vide** (`*lst == NULL`) : `new` devient la tête."),
    (9, 10, "Sinon : `ft_lstlast(*lst)` trouve le dernier noeud, et on le relie à `new` avec `->next = new`.")],
   cases=["Liste vide : `*lst = new`.", "`[a]` + `new = b` → `[a, b]`.", "`new->next` doit déjà valoir `NULL` (c'est `ft_lstnew` qui s'en charge)."],
   trace="avant :  *lst -> [a] -> [b] -> NULL      new -> [c] -> NULL\nft_lstlast(*lst) = [b]\n[b]->next = new   =>   *lst -> [a] -> [b] -> [c] -> NULL",
   pitfalls=["Oublier le cas liste vide.", "Appeler `ft_lstlast(lst)` (avec un `**`) au lieu de `ft_lstlast(*lst)`."])

fn("ft_lstdelone", "Libère **un seul** noeud : son contenu (avec `del`) puis le noeud.",
   [(3, 3, "`void (*del)(void *)` : une fonction **fournie par l'appelant** qui sait libérer le contenu."),
    (5, 6, "Si `lst` est `NULL`, rien à faire."),
    (7, 8, "On appelle `del(lst->content)` pour libérer le **contenu** (si `del` existe)."),
    (9, 9, "Puis `free(lst)` libère le **noeud** lui-même. L'ordre compte : on libère le contenu **avant** le noeud, sinon on perdrait l'adresse du contenu.")],
   cases=["Les noeuds suivants ne sont **pas** touchés.", "`del = free` fonctionne si le contenu a été alloué avec `malloc`."],
   pitfalls=["Libérer le noeud avant le contenu.", "Libérer aussi `lst->next` : c'est le travail de `ft_lstclear`."])

fn("ft_lstclear", "Libère **tous** les noeuds de la liste et met la tête à `NULL`.",
   [(3, 3, "`t_list **lst` : la tête sera remise à `NULL` pour l'appelant."),
    (5, 5, "`next` : **retient** le noeud suivant avant de libérer le courant."),
    (7, 8, "Si `lst` est `NULL`, rien à faire."),
    (9, 14, "Pour chaque noeud : **1)** on sauvegarde `(*lst)->next` ; **2)** `ft_lstdelone` libère contenu et noeud ; **3)** `*lst = next` passe au suivant. À la fin, `*lst` vaut `NULL` : la liste de l'appelant est vide.")],
   cases=["Liste vide : rien ne se passe.", "`[a, b, c]` : les 3 noeuds et leurs contenus sont libérés, `*lst == NULL`."],
   trace="*lst -> [a] -> [b] -> NULL\ntour 1 : next = [b] ; libere a ; *lst = [b]\ntour 2 : next = NULL ; libere b ; *lst = NULL\n-> liste vide",
   pitfalls=["Libérer le noeud **avant** de sauvegarder `next` : après le `free`, `next` n'existe plus (use after free).", "Oublier de remettre `*lst` à `NULL`."])

fn("ft_lstiter", "Applique `f` au **contenu** de chaque noeud, dans l'ordre.",
   [(3, 3, "`void (*f)(void *)` : fonction qui reçoit le contenu d'un noeud. La liste elle-même n'est pas modifiée (sauf si `f` change les contenus)."),
    (5, 9, "On parcourt la liste : pour chaque noeud, `f(lst->content)` puis on passe au suivant (`lst = lst->next`). Liste vide : la boucle ne tourne pas.")],
   cases=["`ft_lstiter(NULL, f)` : ne fait rien.", "`f` est appelée **une fois par noeud**, dans l'ordre."],
   pitfalls=["Appeler `f(lst)` au lieu de `f(lst->content)`.", "Oublier d'avancer (`lst = lst->next`) : boucle infinie."])

fn("ft_lstmap", "Crée une **nouvelle liste** dont chaque contenu est `f(contenu)` ; nettoie tout en cas d'échec.",
   [(3, 3, "Deux fonctions : `f` transforme un contenu en **nouveau** contenu, `del` sait le libérer. Renvoie la nouvelle liste (ou `NULL`)."),
    (5, 7, "`new_list` : la nouvelle liste (tête) ; `node` : le noeud en cours ; `content` : le contenu transformé."),
    (9, 9, "La nouvelle liste est vide au départ."),
    (10, 11, "Pour chaque noeud de la liste d'origine :"),
    (12, 12, "`f(lst->content)` produit un **nouveau contenu** (souvent alloué)."),
    (13, 13, "`ft_lstnew` crée le noeud qui le contiendra."),
    (14, 19, "**Si la création du noeud échoue** : on libère le contenu que `f` vient de produire (`del(content)`), puis toute la liste déjà construite (`ft_lstclear`), et on renvoie `NULL`. Rien ne fuit."),
    (20, 21, "Sinon, on ajoute le noeud **à la fin** de la nouvelle liste (`ft_lstadd_back`) et on passe au noeud suivant de l'original."),
    (23, 23, "On renvoie la nouvelle liste. L'originale n'a pas changé.")],
   cases=["Liste vide → `NULL`.", "`[1, 2, 3]` avec `f = double` → `[2, 4, 6]` (nouveaux noeuds).", "Un `malloc` qui échoue en route → `NULL`, sans fuite."],
   pitfalls=["Oublier `del(content)` quand `ft_lstnew` échoue : fuite du contenu produit par `f`.", "Modifier la liste d'origine."])

FUNCS_BY_ID = {f["id"]: f for f in FUNCS}

# Explications approfondies (« pourquoi on ecrit ca ») : 4e element de chaque ligne du walk
from . import func_deep  # noqa: E402
for _f in FUNCS:
    _d = func_deep.DEEP.get(_f["id"], {})
    for _w in _f["walk"]:
        _w[3:] = [_d.get(_w[0], [])]


def check(by_id_exercises):
    """Liste les problemes : fonction sans cours, numeros de lignes hors du fichier, lignes de code non expliquees."""
    bad = []
    for ex_id in by_id_exercises:
        if ex_id not in FUNCS_BY_ID:
            bad.append("pas de cours pour " + ex_id)
    for f in FUNCS:
        lines = code_lines(f["id"])
        while lines and lines[-1] == "":
            lines.pop()
        covered = set()
        starts = {w[0] for w in f["walk"]}
        for a_deep in func_deep.DEEP.get(f["id"], {}):
            if a_deep not in starts:
                bad.append("%s : approfondissement sur la ligne %d, qui ne debute aucune explication" % (f["id"], a_deep))
        for w in f["walk"]:
            a, b = w[0], w[1]
            if not (1 <= a <= b <= len(lines)):
                bad.append("%s : lignes %s-%s hors du fichier (%d lignes)" % (f["id"], a, b, len(lines)))
            covered.update(range(a, b + 1))
        for n, text in enumerate(lines, 1):
            if text.strip() and n not in covered and n > 2 and text.strip() not in ("{", "}"):
                bad.append("%s : ligne %d non expliquee : %s" % (f["id"], n, text.strip()))
    return bad
