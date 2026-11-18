"""Cours approfondis : complete les cours de lessons.py (blocs ajoutes a la suite, questions de quiz
en plus) et ajoute de nouveaux cours. Nouveaux types de blocs : h (titre de section), warn (piege),
try (mini-exercice avec correction repliee), recap (a retenir)."""
from .lessons import LESSONS, LESSONS_BY_ID, lesson, q


def H(x):
    return {"t": "h", "x": x}


def P(x):
    return {"t": "p", "x": x}


def UL(*x):
    return {"t": "ul", "x": list(x)}


def OL(*x):
    return {"t": "ol", "x": list(x)}


def CODE(x):
    return {"t": "code", "x": x}


def TIP(x):
    return {"t": "tip", "x": x}


def WARN(x):
    return {"t": "warn", "x": x}


def TRY(question, answer):
    return {"t": "try", "q": question, "a": answer}


def RECAP(*x):
    return {"t": "recap", "x": list(x)}


def more(lid, blocks, quiz, level=None, minutes=None):
    L = LESSONS_BY_ID[lid]
    L["blocks"].extend(blocks)
    L["quiz"].extend(quiz)
    if level:
        L["level"] = level
    if minutes:
        L["time"] = minutes


# --------------------------------------------------------------------------- cours existants, approfondis
more("ascii", [
    H("Le raisonnement derrière les fonctions is*"),
    P("Chaque fonction `is*` est un **test d'intervalle** sur le code ASCII. Pas besoin de connaître les nombres par cœur : "
      "on écrit les caractères (`'0'`, `'A'`, `'z'`) et le compilateur met les nombres."),
    UL("`ft_isdigit` : un seul intervalle, de `'0'` à `'9'`.",
       "`ft_isalpha` : **deux** intervalles reliés par un « ou » (majuscules **ou** minuscules).",
       "`ft_isalnum` : lettre **ou** chiffre. Tu peux simplement réutiliser tes deux fonctions précédentes.",
       "`ft_isascii` : de 0 à 127. `ft_isprint` : de 32 à 126.",
       "`ft_toupper` / `ft_tolower` : on ne change **que** les lettres concernées, tout le reste est renvoyé tel quel."),
    WARN(r"N'écris jamais `c >= 'A' && c <= 'z'` pour « est une lettre » : entre `'Z'` (90) et `'a'` (97) il y a aussi "
         r"`[ \ ] ^ _` et l'accent grave. Il faut **deux** intervalles séparés."),
    TRY("Que renvoient `ft_toupper('z')`, `ft_toupper('Z')` et `ft_toupper('5')` ?",
        "`'Z'`, `'Z'` et `'5'`. Seules les minuscules changent (on enlève 32), le reste est renvoyé inchangé."),
    TRY("Que doit renvoyer `ft_isalpha('a')` : `1`, ou n'importe quel nombre non nul ?",
        "**Exactement 1** (sujet v19.3). Et `ft_isalpha('5')` doit renvoyer exactement **0**."),
    RECAP("Un `char` est un nombre : `'A'` = 65, `'a'` = 97, `'0'` = 48.",
          "`is*` = un ou deux tests d'intervalle ; elles renvoient **1 ou 0**.",
          "`toupper` / `tolower` : ±32, uniquement sur les lettres."),
], [
    q("Quelle condition teste correctement « c est une lettre » ?",
      ["c >= 'A' && c <= 'z'", "(c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z')", "c >= 'a' || c <= 'Z'", "c > 64"], 1,
      "Il faut deux intervalles : les majuscules ou les minuscules. Le premier choix accepterait aussi `[`, `_`, etc."),
    q("ft_toupper('5') renvoie…", ["'5'", "'%'", "0", "NULL"], 0, "Ce n'est pas une lettre : la valeur est renvoyée telle quelle."),
], level="Débutant", minutes=8)

more("strings", [
    H("Parcourir une chaîne : les deux motifs"),
    P("Presque toutes les fonctions `str*` suivent l'un de ces deux schémas. Choisis celui qui te paraît le plus lisible :"),
    CODE("/* avec un indice */\ni = 0;\nwhile (s[i])\n\ti++;\n\n/* avec le pointeur lui-meme */\nwhile (*s)\n\ts++;"),
    P("Avec l'indice, tu peux toujours revenir en arrière (`s[i - 1]`) ; avec le pointeur, tu perds le début de la chaîne. "
      "Pour `ft_strlen`, `ft_strchr` ou `ft_strrchr`, l'indice est presque toujours le plus simple."),
    WARN("Les littéraux comme `\"hello\"` sont en **lecture seule**. `char *p = \"hello\"; p[0] = 'H';` plante (segfault). "
         "Pour une chaîne modifiable, utilise un tableau : `char s[] = \"hello\";`."),
    TRY("Que vaut `sizeof(s)` pour `char s[] = \"abc\";` ? Et `ft_strlen(s)` ?",
        "`sizeof(s)` vaut **4** (3 lettres + le `'\\0'`), `ft_strlen(s)` vaut **3**."),
    RECAP("Une chaîne = des caractères + un `'\\0'` final.",
          "Une chaîne de `n` caractères occupe `n + 1` octets.",
          "Un littéral entre guillemets ne se modifie pas."),
], [
    q("Que vaut sizeof(s) pour char s[] = \"abc\"; ?", ["3", "4", "5", "ça dépend"], 1, "3 lettres + le '\\0' final = 4 octets."),
    q("char *p = \"abc\"; p[0] = 'x'; …", ["marche très bien", "comportement indéfini (souvent un segfault)", "ne compile pas"], 1,
      "Un littéral est en mémoire en lecture seule : l'écrire est une erreur à l'exécution."),
], level="Débutant", minutes=8)

more("types", [
    H("Les pièges de signe, avec des chiffres"),
    CODE("size_t\ti;\n\ni = 5;\nwhile (i >= 0)   /* TOUJOURS vrai : size_t n'est jamais negatif ! */\n\ti--;\n\n/* version correcte */\nwhile (i > 0)\n{\n\ti--;\n\t/* travailler sur t[i] */\n}"),
    UL("`(unsigned char)300` vaut **44** : on garde le reste de la division par 256.",
       "`(unsigned char)-1` vaut **255**. Et `(size_t)-1` est le plus grand nombre possible.",
       "Compare toujours deux nombres **de même signe**, sinon le compilateur convertit à ta place (et `-Wextra` te le dira)."),
    TRY("`ft_strncmp(\"a\", \"\\xc3\", 1)` : le résultat est-il négatif ou positif ?",
        "**Négatif** : on compare des `unsigned char` (97 et 195), donc `97 - 195 < 0`. Avec un `char` signé, `0xC3` vaudrait -61 et le résultat serait faux."),
    RECAP("`size_t` n'est jamais négatif : attention aux boucles qui descendent.",
          "Pour comparer/copier des octets : `unsigned char`.",
          "`const` = « je ne modifie pas ce que je pointe »."),
], [
    q("Que vaut (unsigned char)300 ?", ["300", "44", "-212", "255"], 1, "300 - 256 = 44 : on garde le reste modulo 256."),
    q("while (i >= 0) avec i de type size_t…", ["s'arrête quand i vaut 0", "ne s'arrête jamais", "ne compile pas"], 1, "Un size_t est toujours >= 0 : la condition est toujours vraie."),
], level="Débutant", minutes=8)

more("pointers", [
    H("Pointeur de pointeur : char **"),
    P("`ft_split` renvoie un `char **` : un tableau dont **chaque case est une chaîne**. Lis les types de droite à gauche :"),
    CODE("char\t**tab;          /* tab : pointeur vers des char * */\n\ntab[0]      /* un char *  : la 1re chaine */\ntab[0][1]   /* un char    : le 2e caractere de la 1re chaine */\n\ni = 0;\nwhile (tab[i])     /* le tableau se termine par NULL */\n\ti++;"),
    WARN("`*p + 1` et `*(p + 1)` ne sont **pas** la même chose : le premier lit la valeur pointée puis ajoute 1, le second lit la case suivante."),
    TRY("Avec `int t[3] = {10, 20, 30}; int *p = t;`, que valent `*(p + 2)` et `p[1]` ?",
        "`*(p + 2)` = **30** (c'est `t[2]`), `p[1]` = **20**."),
    RECAP("`p[i]` = `*(p + i)` ; `p + 1` avance d'un élément, pas d'un octet.",
          "`void *` : toujours caster avant de lire ou d'écrire.",
          "`char **` : un tableau de chaînes, terminé par `NULL` pour `ft_split`."),
], [
    q("Avec int t[3] = {10, 20, 30}; int *p = t; que vaut *(p + 2) ?", ["10", "20", "30", "une adresse"], 2, "*(p + 2) est la 3e case : 30."),
    q("Dans ft_split, comment sait-on où le char ** se termine ?", ["avec un '\\0'", "avec un pointeur NULL dans la dernière case", "avec la taille stockée au début"], 1,
      "Le tableau se termine par NULL (c'est pour ça qu'on alloue mots + 1 cases)."),
], level="Débutant", minutes=10)

more("memmove", [
    H("Pourquoi ça casse : l'exemple trace à la main"),
    P("On veut copier `\"abcd\"` (4 octets) **2 cases plus loin** dans `buf = \"abcdef\"`, c'est-à-dire `memmove(buf + 2, buf, 4)`. "
      "Les zones se chevauchent. Voici la copie **gauche → droite** (la mauvaise) :"),
    OL("`buf[2] = buf[0]` : `\"abadef\"`.",
       "`buf[3] = buf[1]` : `\"ababef\"`.",
       "`buf[4] = buf[2]` : on lit `'a'` (déjà écrasé, ce devait être `'c'`) : `\"ababaf\"`.",
       "`buf[5] = buf[3]` : `\"ababab\"`. **Résultat faux.**"),
    P("En copiant de **droite à gauche** (de `i = 3` à `0`), on lit chaque octet avant de l'écraser : on obtient bien `\"ababcd\"`."),
    WARN("Une seule règle à retenir : si `dest > src`, on part de la **fin**. Sinon, du début. Et si `dest == src` ou `n == 0`, il n'y a rien à faire."),
    TRY("Que donne `memmove(buf, buf + 2, 4)` sur `\"abcdef\"`, et dans quel sens copie-t-on ?",
        "`\"cdefef\"`, en copiant de **gauche à droite** (`dest < src`)."),
    RECAP("`memcpy` : jamais de chevauchement. `memmove` : accepte le chevauchement.",
          "`dest > src` → de la fin vers le début ; sinon du début vers la fin."),
], [
    q("memmove(buf, buf + 2, 4) sur \"abcdef\" donne…", ["cdefef", "ababcd", "abcdef", "cdcdef"], 0, "dest < src : copie de gauche à droite, on obtient \"cdefef\"."),
    q("memcpy sur deux zones qui se chevauchent…", ["marche toujours", "est un comportement indéfini", "renvoie NULL"], 1, "C'est exactement la raison d'être de memmove."),
], level="Intermédiaire", minutes=10)

more("search", [
    H("Ce que renvoie une comparaison"),
    P("`ft_strncmp` et `ft_memcmp` ne renvoient pas seulement « -1, 0 ou 1 » : elles renvoient la **différence** entre les deux premiers octets différents, "
      "vus comme `unsigned char`. Ce qui compte : **négatif**, **nul** ou **positif**."),
    CODE("ft_strncmp(\"abc\", \"abd\", 3);  /* 'c' - 'd' = -1  (negatif) */\nft_strncmp(\"abc\", \"abd\", 2);  /* \"ab\" == \"ab\"   -> 0 */\nft_strncmp(\"\", \"a\", 5);        /* 0 - 'a'         (negatif) */"),
    WARN("Dans `ft_strnstr`, la condition de boucle est `i + j < len` (et pas seulement `big[i]`). Sinon tu dépasses `len`."),
    TRY("`ft_strnstr(\"hello\", \"llo\", 4)` renvoie quoi ? Et `ft_strnstr(\"hello\", \"\", 0)` ?",
        "Le premier renvoie **NULL** : « llo » finit à l'indice 5, au-delà de `len = 4`. Le second renvoie **`\"hello\"`** : `little` vide → on renvoie `big`."),
    RECAP("`strchr`/`strrchr` : pointeur dans la chaîne d'origine ou `NULL` ; le `'\\0'` est trouvable.",
          "`mem*` ignorent le `'\\0'`, `str*` s'y arrêtent.",
          "Cas limites : chaîne vide, `n = 0`, `len` trop petit ou trop grand."),
], [
    q("ft_strnstr(\"hello\", \"llo\", 4) renvoie…", ["un pointeur sur \"llo\"", "NULL", "\"hello\"", "0"], 1, "Il faut 5 caractères pour trouver \"llo\" en position 2 : len = 4 est trop court."),
    q("ft_strnstr(\"abc\", \"\", 0) renvoie…", ["NULL", "big (\"abc\")", "un pointeur sur le '\\0'"], 1, "Si little est vide, on renvoie big."),
], level="Intermédiaire", minutes=10)

more("lcpy", [
    H("Pourquoi renvoyer la longueur « voulue » ?"),
    P("Parce que l'appelant peut **détecter la troncature** sans rien recalculer :"),
    CODE("char\tbuf[8];\n\nif (ft_strlcpy(buf, src, sizeof(buf)) >= sizeof(buf))\n\t/* src ne tenait pas : buf contient une version tronquee */"),
    WARN("`size` est la taille **totale du buffer destination** (le `'\\0'` compris), pas « le nombre de caractères à copier »."),
    TRY("`ft_strlcpy(d, \"ab\", 0)` : que renvoie-t-elle, et que contient `d` ?",
        "Elle renvoie **2** (`strlen(src)`) et **n'écrit rien** dans `d` (`size == 0`)."),
    TRY("`d = \"abc\"` : que renvoie `ft_strlcat(d, \"xy\", 3)` ?",
        "`size (3) <= strlen(d) (3)` : on n'écrit rien et on renvoie `size + strlen(src) = 3 + 2 = 5`."),
    RECAP("`strlcpy` renvoie `strlen(src)`. `strlcat` renvoie `min(size, strlen(dst)) + strlen(src)`.",
          "Retour ≥ `size` ⇒ troncature."),
], [
    q("ft_strlcpy(d, \"ab\", 0) renvoie…", ["0", "2", "1", "-1"], 1, "Toujours strlen(src) = 2, et rien n'est écrit dans d."),
    q("ft_strlcat(d, \"xy\", 3) avec d = \"abc\" renvoie…", ["2", "3", "5", "6"], 2, "size <= strlen(dst) : on renvoie size + strlen(src) = 3 + 2 = 5."),
], level="Intermédiaire", minutes=10)

more("malloc", [
    H("Le schéma d'une fonction qui alloue"),
    P("Presque toutes tes fonctions de la partie 2 (`ft_substr`, `ft_strjoin`, `ft_strtrim`, `ft_itoa`, `ft_strmapi`…) suivent le même plan :"),
    OL("**Calculer** la taille nécessaire (longueurs, nombre de chiffres…).",
       "**Allouer** `taille + 1` octets.",
       "**Tester** : `if (!res) return (NULL);`",
       "**Remplir**, puis écrire le `'\\0'` final.",
       "**Renvoyer** le pointeur (c'est l'appelant qui fera le `free`)."),
    CODE("char\t*res;\n\nres = malloc(len + 1);\nif (!res)\n\treturn (NULL);\n/* ... remplir res[0] a res[len - 1] ... */\nres[len] = '\\0';\nreturn (res);"),
    WARN("Les 4 oublis qui font échouer à la correction : le `+ 1`, le test de `NULL`, le `'\\0'` final, et le `free` des allocations déjà faites quand une suivante échoue."),
    TRY("Combien d'octets faut-il pour `ft_strjoin(\"ab\", \"cde\")` ?", "`2 + 3 + 1 = 6` octets : les deux longueurs plus le `'\\0'`."),
    TRY("`ft_substr(\"hello\", 10, 3)` : que doit renvoyer la fonction ?",
        "Une **chaîne vide allouée** (`start` dépasse la fin) : un `malloc(1)` contenant `'\\0'`, pas `NULL`."),
    RECAP("`malloc` peut échouer : toujours tester.", "Chaque `malloc` = un `free` (par l'appelant).",
          "Erreur au milieu : libérer ce qui est déjà alloué."),
], [
    q("Combien d'octets pour ft_strjoin(\"ab\", \"cde\") ?", ["5", "6", "7", "4"], 1, "2 + 3 caractères + 1 pour le '\\0' = 6."),
    q("Selon le sujet v19.3, ft_calloc(0, 4) doit renvoyer…", ["NULL", "un pointeur non NULL", "-1"], 1, "Le sujet demande un pointeur valide (non NULL) même pour une taille nulle."),
], level="Intermédiaire", minutes=12)

more("split", [
    H("Les cas qui piègent"),
    UL("Plusieurs séparateurs de suite : `\"a,,b\"` avec `','` donne **2 mots** (`\"a\"`, `\"b\"`), jamais de chaîne vide.",
       "Séparateur au début ou à la fin : ignoré.",
       "Aucun séparateur : un seul mot (la chaîne entière).",
       "Chaîne vide ou uniquement des séparateurs : tableau **`{NULL}`** (alloué), pas `NULL`."),
    WARN("Quand l'allocation du mot numéro `i` échoue, il faut libérer les mots `0` à `i - 1`, **puis** le tableau, puis renvoyer `NULL`. "
         "Écris une fonction `free_all(tab, i)` : c'est aussi ce qui garde ton code sous 25 lignes."),
    TRY("Que renvoie `ft_split(\"hello\", 'z')` ?", "Un tableau de **2 cases** : `{\"hello\", NULL}`."),
    TRY("Combien de `malloc` pour `ft_split(\"a b c\", ' ')` ?", "**4** : un pour le tableau et un par mot."),
    RECAP("Compter → allouer le tableau (`mots + 1`) → remplir mot par mot → `NULL` final.",
          "Échec d'un malloc : tout libérer, renvoyer `NULL`."),
], [
    q("ft_split(\"a,,b\", ',') renvoie combien de mots ?", ["2", "3", "4"], 0, "Les séparateurs consécutifs ne créent pas de mots vides : \"a\" et \"b\"."),
    q("ft_split(\"hello\", 'z') renvoie…", ["NULL", "{\"hello\", NULL}", "{\"hello\"}"], 1, "Un mot (la chaîne entière) suivi du NULL final."),
], level="Avancé", minutes=15)

more("fd", [
    H("write : l'adresse et la valeur de retour"),
    CODE("char\tc;\n\nc = 'A';\nwrite(1, &c, 1);   /* OUI : on passe l'ADRESSE de c */\nwrite(1, c, 1);    /* NON : c est un nombre (65), pas une adresse */"),
    UL("`write` renvoie le nombre d'octets écrits, ou **-1** en cas d'erreur (fd invalide, par exemple).",
       "Pour la libft, tu n'as pas besoin de tester ce retour.",
       "`write(2, ...)` écrit sur la **sortie d'erreur** : pratique pour tes messages de debug sans polluer la sortie normale."),
    TRY("Déroule `ft_putnbr_fd(42, 1)` (version récursive) : dans quel ordre écrit-on les caractères ?",
        "`ft_putnbr_fd(42)` appelle d'abord `ft_putnbr_fd(4)` (qui écrit `'4'`), **puis** écrit `'2'` : on obtient `\"42\"`. Le chiffre le plus à gauche est écrit en premier grâce à la récursion."),
    RECAP("`write(fd, adresse, nombre_d_octets)` : toujours une adresse.", "fd 1 = écran, 2 = erreurs.",
          "`ft_putnbr_fd` : récursion + `long long` pour `INT_MIN`."),
], [
    q("Que doit-on passer à write comme 2e argument ?", ["le caractère lui-même", "l'adresse des octets à écrire", "la longueur"], 1, "write attend un pointeur vers les octets : write(fd, &c, 1)."),
    q("Dans ft_putnbr_fd(42, 1), quel caractère est écrit en premier ?", ["'2'", "'4'", "'\\n'"], 1, "On écrit d'abord ft_putnbr_fd(4), donc '4', puis '2'."),
], level="Intermédiaire", minutes=8)

more("funcptr", [
    H("Lire la syntaxe sans paniquer"),
    UL("`char (*f)(unsigned int, char)` : **`f` est un pointeur vers une fonction** (les parenthèses autour de `*f` sont indispensables).",
       "`char *f(unsigned int, char)` : sans ces parenthèses, c'est la déclaration d'une **fonction** qui renvoie un `char *`. Autre chose !",
       "On appelle `f(i, s[i])` exactement comme une fonction normale ; pas besoin d'écrire `(*f)(...)`."),
    WARN("Dans `ft_striteri`, `f` reçoit `&s[i]` (un `char *`) : pour modifier le caractère, la fonction écrit `*c = ...`."),
    TRY("`f(i, c)` renvoie `c - 32`. Que donne `ft_strmapi(\"abc\", f)` ?", "**`\"ABC\"`** (une nouvelle chaîne allouée ; l'originale n'est pas modifiée)."),
    TRY("`f(i, c)` fait `*c = i + '0'`. Que devient `\"xyz\"` après `ft_striteri(s, f)` ?", "**`\"012\"`** : la chaîne est modifiée sur place."),
    RECAP("`strmapi` → nouvelle chaîne ; `striteri` → modification sur place.", "Les parenthèses de `(*f)` font le pointeur de fonction."),
], [
    q("Quelle déclaration est un pointeur de fonction ?", ["char *f(unsigned int, char)", "char (*f)(unsigned int, char)", "char f*(unsigned int, char)"], 1, "Les parenthèses autour de *f font de f un pointeur vers une fonction."),
    q("ft_striteri(s, f) avec f qui écrit *c = i + '0' sur \"xyz\" donne…", ["\"xyz\"", "\"012\"", "\"123\"", "NULL"], 1, "i vaut 0, 1, 2 : les caractères deviennent '0', '1', '2'."),
], level="Avancé", minutes=10)

more("lists", [
    H("Pas à pas : ajouter à la fin"),
    P("Le raisonnement pour `ft_lstadd_back(t_list **lst, t_list *new)`, avant d'écrire une ligne de code :"),
    OL("Si la liste est **vide** (`*lst == NULL`), le nouveau noeud **devient** la tête : `*lst = new`.",
       "Sinon, on cherche le **dernier** noeud (c'est le travail de `ft_lstlast`).",
       "On relie : `dernier->next = new`.",
       "`new->next` doit déjà valoir `NULL` : c'est `ft_lstnew` qui s'en charge."),
    CODE("avant :   *lst -> [a] -> [b] -> NULL        new -> [c] -> NULL\napres :   *lst -> [a] -> [b] -> [c] -> NULL"),
    WARN("Le cas **liste vide** est celui qu'on oublie le plus. Teste toujours ta fonction sur une liste vide avant de la croire correcte."),
    TRY("On part de `[a]` et on fait `ft_lstadd_front(&l, b)` puis `ft_lstadd_front(&l, c)`. Dans quel ordre est la liste ?",
        "**`c → b → a`** : chaque ajout en tête devient le premier noeud."),
    TRY("Que renvoie `ft_lstlast(NULL)` et que vaut `ft_lstsize(NULL)` ?", "`NULL` et **0**."),
    RECAP("Liste vide = pointeur `NULL`. Tête qui change ⇒ `t_list **`.",
          "`lstdelone` : `del(content)` puis `free(noeud)`. `lstclear` : retenir `next` avant de libérer.",
          "`lstmap` : nouvelle liste ; en cas d'échec, tout nettoyer et renvoyer `NULL`."),
], [
    q("Après ft_lstadd_front(&l, b) puis ft_lstadd_front(&l, c) sur [a], l'ordre est…", ["a, b, c", "c, b, a", "b, c, a"], 1, "Chaque noeud ajouté devient la nouvelle tête : c → b → a."),
    q("ft_lstadd_back sur une liste vide (*lst == NULL) doit…", ["ne rien faire", "mettre new comme tête (*lst = new)", "planter"], 1, "Le nouveau noeud devient le premier et le seul."),
], level="Avancé", minutes=18)

more("norm", [
    H("Réussir la norme sans stress"),
    P("La méthode qui marche : lancer `norminette` **à chaque fonction terminée**, pas à la fin de tout le projet. Les messages les plus courants :"),
    UL("`TOO_MANY_LINES` : plus de 25 lignes → découpe en fonctions `static`.",
       "`TOO_MANY_VARS_FUNC` : plus de **5 variables** dans la fonction.",
       "`DECL_ASSIGN_LINE` : tu as écrit `int i = 0;` → déclare d'abord, assigne ensuite sur une autre ligne.",
       "`MISALIGNED_VAR_DECL` / `MISALIGNED_FUNC_DECL` : les noms ne sont pas alignés par tabulation.",
       "`LINE_TOO_LONG` : plus de 80 colonnes (une tabulation compte 4).",
       "`INVALID_HEADER` : l'en-tête 42 est absent ou modifié."),
    TRY("Pourquoi `int\ti = 0;` en début de fonction est-il refusé ?",
        "Une déclaration et une affectation sur la **même ligne** sont interdites pour les variables locales (`DECL_ASSIGN_LINE`) : écris `int\ti;` en haut puis `i = 0;` plus bas."),
    RECAP("25 lignes, 5 variables, 4 paramètres, 5 fonctions par fichier, 80 colonnes.",
          "Pas de `for`, de ternaire, de `switch`. Tabulations, en-tête 42, `static` pour les aides."),
], [
    q("Combien de variables maximum dans une fonction ?", ["3", "4", "5", "10"], 2, "5 variables locales maximum."),
    q("int i = 0; au début d'une fonction est refusé car…", ["on ne peut pas initialiser un int", "déclaration et affectation sur la même ligne", "i est un mauvais nom"], 1, "La norme impose de déclarer, puis d'assigner sur une autre ligne."),
], level="Débutant", minutes=8)


# --------------------------------------------------------------------------- nouveaux cours
lesson("compile", "⚙️", "Compiler, flags et Makefile",
       "Du fichier .c à libft.a : ce que fait vraiment cc, et comment écrire un Makefile propre.",
       [P("Quand tu lances `cc`, quatre étapes s'enchaînent : le **préprocesseur** (traite `#include` et `#define`), le **compilateur** (C → code machine, fichier `.o`), "
          "l'**assembleur** et l'**éditeur de liens** (assemble les `.o` en un programme). Pour la libft, on s'arrête aux `.o` puis on les range dans une archive."),
        H("Les flags obligatoires"),
        UL("`-Wall -Wextra` : active les avertissements (variable non utilisée, comparaison signé/non signé…).",
           "`-Werror` : transforme chaque avertissement en **erreur**. Pas de warning toléré.",
           "`-c` : compile **sans lier** : produit un `.o`. C'est ce qu'on veut pour chaque fichier de la libft (il n'y a pas de `main`)."),
        CODE("cc -Wall -Wextra -Werror -c ft_strlen.c        # produit ft_strlen.o\nar rcs libft.a ft_strlen.o ft_atoi.o ...        # range les .o dans l'archive\ncc -Wall -Wextra -Werror main.c -L. -lft -o test   # utilise libft.a"),
        H("Le Makefile minimal"),
        CODE("NAME\t= libft.a\nCC\t= cc\nCFLAGS\t= -Wall -Wextra -Werror\nSRCS\t= ft_atoi.c ft_strlen.c\nOBJS\t= $(SRCS:.c=.o)\n\nall: $(NAME)\n\n$(NAME): $(OBJS)\n\tar rcs $(NAME) $(OBJS)\n\n%.o: %.c libft.h\n\t$(CC) $(CFLAGS) -c $< -o $@\n\nclean:\n\trm -f $(OBJS)\n\nfclean: clean\n\trm -f $(NAME)\n\nre: fclean all\n\n.PHONY: all clean fclean re"),
        UL("Une règle s'écrit `cible: dépendances` puis la commande **précédée d'une tabulation** (pas d'espaces !).",
           "`make` ne recompile que ce qui a changé : lancer `make` deux fois de suite doit répondre « rien à faire ». Un Makefile qui **relink** à chaque fois est refusé.",
           "`.PHONY` dit à make que `all`, `clean`… sont des actions et non des fichiers."),
        WARN("`%.o: %.c libft.h` : sans `libft.h` dans les dépendances, modifier le header ne recompile rien. Et **aucun `main`** dans les fichiers de la libft : il entrerait en conflit avec le tien."),
        H("Le header"),
        CODE("#ifndef LIBFT_H\n# define LIBFT_H\n# include <stddef.h>\n\nsize_t\tft_strlen(const char *s);\n\n#endif"),
        P("Le garde `#ifndef … #endif` évite qu'un fichier incluant deux fois le header redéfinisse tout. Chaque fonction publique de la libft a son prototype ici."),
        TRY("`undefined reference to ft_xxx` à l'édition de liens : quelles sont les deux causes les plus fréquentes ?",
            "Le fichier `ft_xxx.c` n'est **pas dans `SRCS`** du Makefile (donc pas dans `libft.a`), ou `-lft` est placé **avant** `main.c` dans la commande."),
        RECAP("`-Wall -Wextra -Werror` toujours.", "`-c` fabrique des `.o`, `ar rcs` fabrique `libft.a`.",
              "Makefile : `all`, `clean`, `fclean`, `re`, `.PHONY`, pas de relink.")],
       [q("Que fait le flag -Werror ?", ["il active tous les warnings", "il transforme les warnings en erreurs", "il supprime les erreurs"], 1, "Un warning devient une erreur : la compilation échoue."),
        q("Que fait cc -c ft_strlen.c ?", ["crée un exécutable", "crée ft_strlen.o sans lier", "exécute le fichier"], 1, "-c compile sans faire l'édition de liens : on obtient un .o."),
        q("Dans un Makefile, une commande doit être précédée…", ["de 4 espaces", "d'une tabulation", "d'un @"], 1, "Make exige une vraie tabulation."),
        q("make lancé deux fois de suite doit…", ["tout recompiler", "dire qu'il n'y a rien à faire", "supprimer libft.a"], 1, "Sinon c'est du relink, interdit par le sujet."),
        q("Pourquoi le garde #ifndef LIBFT_H dans le header ?", ["pour accélérer le programme", "éviter les définitions en double", "c'est facultatif et inutile"], 1, "Un header inclus deux fois sans garde redéfinirait les types.")],
       ["ft_strlen"])

lesson("memory", "🧱", "La mémoire : pile, tas et adresses",
       "Où vivent tes variables, ce que devient un pointeur après un return, et les 4 erreurs mémoire classiques.",
       [P("Un programme C dispose surtout de deux zones de mémoire :"),
        UL("**La pile** (*stack*) : les variables locales et les paramètres. Elle est gérée **automatiquement** : tout disparaît à la sortie de la fonction.",
           "**Le tas** (*heap*) : la mémoire obtenue avec `malloc`. Elle reste jusqu'au `free`. C'est **toi** qui gères sa durée de vie."),
        CODE("char\t*bad(void)\n{\n\tchar\tbuf[10];\n\n\tbuf[0] = 'a';\n\tbuf[1] = '\\0';\n\treturn (buf);   /* ERREUR : buf est sur la pile, il disparait au return */\n}"),
        P("Ici, `buf` n'existe plus quand l'appelant récupère l'adresse : c'est un **pointeur pendant** (*dangling*). Avec `-Wall -Werror`, ce code ne compile même pas. "
          "Pour renvoyer une chaîne, on l'alloue avec `malloc` : c'est pourquoi `ft_strdup`, `ft_substr`, `ft_itoa`… allouent."),
        H("Les 4 erreurs classiques"),
        OL("**Fuite** : un `malloc` sans `free`. Le programme grossit pour rien.",
           "**Double free** : libérer deux fois le même bloc. Plantage ou corruption.",
           "**Use after free** : lire ou écrire un bloc déjà libéré.",
           "**Débordement** (*overflow*) : écrire au-delà de la taille allouée (le `+ 1` oublié du `'\\0'` !)."),
        CODE("int\t*p;\n\np = malloc(sizeof(*p) * 4);   /* 4 int : taille calculee depuis le type */\nif (!p)\n\treturn (NULL);\n..\nfree(p);\np = NULL;                    /* bonne habitude : plus de pointeur pendant */"),
        WARN("`sizeof` d'un **pointeur** vaut la taille du pointeur (8 octets en 64 bits), pas celle des données pointées. `sizeof(char *)` ≠ longueur d'une chaîne : utilise `ft_strlen`."),
        TRY("Pourquoi `ft_strdup` peut-elle renvoyer sa copie alors qu'une fonction qui renvoie un tableau local ne le peut pas ?",
            "La copie de `ft_strdup` est sur le **tas** (`malloc`) : elle survit à la fonction. Un tableau local est sur la **pile** et disparaît au `return`."),
        RECAP("Pile : automatique, disparaît au `return`. Tas : `malloc`/`free`, ta responsabilité.",
              "Fuite, double free, use after free, débordement : les 4 erreurs à traquer.")],
       [q("Où vit une variable locale (char buf[10]) ?", ["sur le tas", "sur la pile", "dans le fichier .c"], 1, "Les variables locales sont sur la pile et disparaissent avec la fonction."),
        q("Pourquoi renvoyer l'adresse d'un tableau local est une erreur ?", ["le tableau est trop petit", "il n'existe plus après le return", "un tableau ne peut pas être renvoyé"], 1, "La pile est libérée à la sortie de la fonction : l'adresse devient invalide."),
        q("Un malloc jamais libéré est…", ["un double free", "une fuite mémoire", "un débordement"], 1, "C'est une fuite : la mémoire reste prise jusqu'à la fin du programme."),
        q("sizeof(char *) sur un système 64 bits vaut…", ["1", "4", "8", "la longueur de la chaîne"], 2, "Un pointeur fait 8 octets en 64 bits, quelle que soit la chaîne pointée."),
        q("Écrire 11 octets dans un malloc(10) est…", ["autorisé", "un débordement de tampon", "un double free"], 1, "On écrit au-delà du bloc : c'est un débordement.")],
       ["ft_calloc", "ft_strdup"])

lesson("conv", "🔢", "atoi et itoa : convertir texte et nombres",
       "Le raisonnement chiffre par chiffre, et le piège de INT_MIN.",
       [H("ft_atoi : du texte vers le nombre"),
        P("L'idée : lire les caractères de gauche à droite et construire le nombre en **décalant d'un chiffre** à chaque fois."),
        OL("**Sauter les espaces** au début (` `, `\\t`, `\\n`, `\\v`, `\\f`, `\\r`).",
           "**Lire un signe** : un seul `+` ou `-` (noter le signe).",
           "**Boucler sur les chiffres** : `res = res * 10 + (c - '0')`.",
           "S'arrêter au **premier caractère qui n'est pas un chiffre**, puis appliquer le signe."),
        CODE("\"  -42abc\"\n  res = 0\n  '4' : res = 0 * 10 + 4  =  4\n  '2' : res = 4 * 10 + 2  = 42\n  'a' : stop       -> signe '-'  -> -42"),
        P("`c - '0'` transforme le **caractère** `'7'` (55) en **nombre** 7 : les chiffres sont contigus dans la table ASCII."),
        H("ft_itoa : du nombre vers le texte"),
        OL("**Compter les chiffres** (et ajouter 1 pour le `-` si négatif).",
           "**Allouer** `len + 1` octets.",
           "**Remplir à partir de la droite** : `s[--len] = n % 10 + '0'; n = n / 10;`.",
           "Cas particulier : **0** doit donner `\"0\"` (une boucle `while (n)` ne tournerait pas)."),
        WARN("`INT_MIN` (-2147483648) n'a **pas d'opposé** dans un `int` : `-n` déborde. Copie `n` dans un **`long long`** avant de prendre la valeur absolue. "
             "(`long` fait 32 bits sous Windows, 64 sur Linux : `long long` marche partout.)"),
        TRY("Combien de caractères pour `ft_itoa(-105)` ? Et pour `ft_itoa(0)` ?",
            "`-105` : **4** caractères (3 chiffres + le `-`), donc 5 octets avec le `'\\0'`. `0` : **1** caractère, `\"0\"`."),
        RECAP("atoi : `res * 10 + (c - '0')`, avec espaces et signe au début.",
              "itoa : compter, allouer, remplir de droite à gauche ; attention à `0` et à `INT_MIN`.")],
       [q("Que vaut '7' - '0' ?", ["55", "7", "48", "'7'"], 1, "Les chiffres sont contigus : '7' - '0' vaut 7."),
        q("ft_atoi(\"  -42abc\") renvoie…", ["-42", "42", "0", "-42abc"], 0, "Espaces sautés, signe '-', chiffres 4 et 2, arrêt sur 'a' : -42."),
        q("Combien d'octets pour ft_itoa(-105) ?", ["3", "4", "5", "6"], 2, "'-', '1', '0', '5' + '\\0' = 5 octets."),
        q("Pourquoi itoa utilise-t-il un long long pour n ?", ["pour aller plus vite", "pour pouvoir calculer -INT_MIN", "parce que write l'exige"], 1, "Dans un int, -INT_MIN déborde ; un long long le contient."),
        q("ft_itoa(0) doit renvoyer…", ["une chaîne vide", "\"0\"", "NULL"], 1, "Le cas 0 est particulier : il faut produire le caractère '0'.")],
       ["ft_atoi", "ft_itoa"])

lesson("recursion", "🔁", "La récursivité (putnbr, itoa)",
       "Une fonction qui s'appelle elle-même : le cas d'arrêt, la pile d'appels, et l'ordre qui change tout.",
       [P("Une fonction est **récursive** quand elle s'appelle elle-même sur un problème **plus petit**. Elle a toujours deux parties :"),
        UL("Le **cas de base** : le cas le plus simple, qu'on résout directement (et qui **arrête** la récursion).",
           "Le **cas récursif** : on réduit le problème et on s'appelle."),
        CODE("int\tft_fact(int n)\n{\n\tif (n <= 1)\n\t\treturn (1);            /* cas de base */\n\treturn (n * ft_fact(n - 1));   /* cas recursif */\n}\n/* ft_fact(3) = 3 * ft_fact(2) = 3 * 2 * ft_fact(1) = 3 * 2 * 1 = 6 */"),
        H("L'ordre des instructions change le résultat"),
        P("Pour afficher un nombre chiffre par chiffre, **l'ordre** entre l'appel récursif et l'écriture est essentiel :"),
        CODE("void\tft_putnbr_fd(int n, int fd)   /* n >= 0 pour simplifier */\n{\n\tif (n > 9)\n\t\tft_putnbr_fd(n / 10, fd);   /* d'abord les chiffres de gauche */\n\tft_putchar_fd(n % 10 + '0', fd);   /* puis le dernier chiffre */\n}\n/* 42 : appelle putnbr(4) -> ecrit '4' ; puis ecrit '2'  => \"42\" */"),
        P("Si tu écris le chiffre **avant** l'appel récursif, tu affiches le nombre **à l'envers** (`\"24\"`)."),
        WARN("Sans cas de base (ou si le problème ne rétrécit pas), la fonction s'appelle à l'infini : **débordement de pile** (*stack overflow*), et le programme plante."),
        TRY("`ft_putnbr_fd(-42, 1)` : par quoi faut-il commencer avant la récursion ?",
            "Écrire le **`'-'`** une seule fois et passer à la valeur positive (en pensant à `INT_MIN`, voir le cours « atoi et itoa »). La récursion ne s'occupe que des chiffres."),
        RECAP("Récursion = cas de base + appel sur un problème plus petit.",
              "Ordre appel/écriture : avant = à l'envers, après = dans le bon ordre.",
              "Tout algorithme récursif peut aussi s'écrire avec une boucle.")],
       [q("Que se passe-t-il sans cas de base ?", ["rien", "appels à l'infini et débordement de pile", "la fonction renvoie 0"], 1, "Chaque appel en crée un autre : la pile se remplit et le programme plante."),
        q("ft_fact(4) vaut…", ["10", "16", "24", "4"], 2, "4 * 3 * 2 * 1 = 24."),
        q("Dans ft_putnbr_fd récursive, pour écrire dans le bon ordre il faut…", ["écrire le chiffre puis appeler", "appeler (n / 10) puis écrire le chiffre", "appeler deux fois"], 1, "D'abord les chiffres de gauche (appel récursif), ensuite n % 10."),
        q("Avec ft_putnbr_fd(5, fd), l'appel récursif…", ["a lieu une fois", "n'a pas lieu (5 <= 9)", "boucle à l'infini"], 1, "Le test n > 9 est faux : on écrit directement '5'."),
        q("Une récursion peut aussi s'écrire…", ["impossible autrement", "avec une boucle while", "uniquement avec for"], 1, "Les deux sont équivalents : la boucle évite la pile d'appels.")],
       ["ft_putnbr_fd", "ft_itoa"])

lesson("debug", "🐞", "Déboguer : segfault, printf, gdb et fuites",
       "Que faire quand ça plante : une méthode et les outils qui comptent.",
       [P("Un **segfault** (*segmentation fault*) = ton programme a touché une mémoire interdite. Les causes habituelles, dans l'ordre :"),
        OL("Déréférencer **`NULL`** (ou un pointeur non initialisé) : `*p` alors que `p == NULL`.",
           "Lire/écrire **hors des bornes** d'un tableau ou d'une chaîne (`s[len + 1]`).",
           "Une chaîne **sans `'\\0'`** : un `while (s[i])` qui ne s'arrête jamais.",
           "**Modifier un littéral** (`char *p = \"abc\"; p[0] = 'x';`).",
           "Utiliser un bloc **déjà libéré** (`free` puis lecture)."),
        H("La méthode"),
        OL("**Reproduire** avec le plus petit exemple possible (un `main` de 5 lignes).",
           "**Observer** : afficher les valeurs suspectes avec `write(2, ...)` ou `printf` (sur la sortie d'erreur, pour ne pas polluer la sortie).",
           "**Réduire** : couper le code en deux (mettre en commentaire) pour savoir dans quelle moitié se trouve le bug.",
           "**Dessiner** la mémoire sur papier (indices, adresses, `next`) : la plupart des bugs se voient."),
        H("Les outils"),
        UL("`cc -g` : ajoute les infos de debug (numéros de lignes). **gdb** : `gdb ./a.out` puis `run`, `bt` (où a-t-il planté ?), `break ft_split`, `next`, `print i`.",
           "`-fsanitize=address -g` : sous Linux/macOS, le programme s'arrête avec un message clair sur le débordement ou le use-after-free.",
           "**valgrind** (Linux) : `valgrind --leak-check=full ./a.out` liste chaque fuite. Sous macOS : `leaks --atExit -- ./a.out`.",
           "**Dans le trainer** : « crash » = segfault, « timeout » = boucle infinie (souvent un `'\\0'` oublié), « fuite » = un `malloc` sans `free` (le trainer surveille tes `malloc`)."),
        WARN("Ne « corrige » pas un segfault en ajoutant des `if` au hasard : trouve **d'abord** la cause (quelle ligne, quelle valeur), puis corrige."),
        TRY("Ton `ft_strlen` tourne sans jamais finir sur `\"hello\"` : quelle est la cause la plus probable ?",
            "La condition de boucle ne détecte jamais le `'\\0'` (par exemple `while (s[i] != 0 && ...)` mal écrit, ou un `i` qui ne s'incrémente pas) : le trainer affichera un **timeout**."),
        RECAP("Segfault = `NULL`, hors bornes, `'\\0'` manquant, littéral modifié, use-after-free.",
              "Méthode : reproduire, observer, réduire, dessiner.", "Outils : `-g` + gdb, `-fsanitize=address`, valgrind.")],
       [q("Quelle commande gdb indique où le programme a planté ?", ["run", "bt", "next", "print"], 1, "bt (backtrace) affiche la pile d'appels au moment du plantage."),
        q("Lequel de ces cas provoque typiquement un segfault ?", ["lire *p avec p == NULL", "appeler ft_strlen(\"\")", "utiliser size_t"], 0, "Déréférencer NULL accède à une adresse interdite."),
        q("Pourquoi afficher les messages de debug sur la sortie d'erreur (fd 2) ?", ["c'est plus rapide", "ça ne pollue pas la sortie normale", "write(1) est interdit"], 1, "La sortie normale reste propre pour comparer les résultats."),
        q("Quel flag ajoute les informations de debug à la compilation ?", ["-O3", "-g", "-c"], 1, "-g permet à gdb d'afficher les lignes et les noms de variables."),
        q("Un timeout dans le trainer évoque d'abord…", ["une boucle infinie", "une fuite mémoire", "une faute de norme"], 0, "Le programme ne finit jamais : souvent un '\\0' non détecté ou un indice jamais incrémenté.")],
       [])

# --------------------------------------------------------------------------- parcours : ordre, niveaux, durees
ORDER = ["compile", "memory", "ascii", "strings", "types", "pointers", "search", "memmove", "lcpy", "malloc",
         "conv", "split", "recursion", "fd", "funcptr", "lists", "norm", "debug"]
_META = {"compile": ("Débutant", 10), "memory": ("Débutant", 12), "conv": ("Intermédiaire", 12),
         "recursion": ("Intermédiaire", 12), "debug": ("Intermédiaire", 12)}
LESSONS_BY_ID.update({l["id"]: l for l in LESSONS})     # lesson() n'enregistre que dans LESSONS
for _id, (_lv, _min) in _META.items():
    LESSONS_BY_ID[_id]["level"] = _lv
    LESSONS_BY_ID[_id]["time"] = _min
LESSONS.sort(key=lambda l: ORDER.index(l["id"]) if l["id"] in ORDER else len(ORDER))
LESSONS_BY_ID.clear()
LESSONS_BY_ID.update({l["id"]: l for l in LESSONS})
