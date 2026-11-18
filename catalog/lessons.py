"""Cours integres. Blocs : p (paragraphe), ul (liste), code, tip (astuce), viz (visualiseur
interactif, voir web/lessons.js). Les reponses des quiz restent cote serveur."""

LESSONS = []


def lesson(id, icon, title, summary, blocks, quiz, related=()):
    LESSONS.append({"id": id, "icon": icon, "title": title, "summary": summary, "blocks": blocks,
                    "quiz": quiz, "related": list(related)})


def q(question, choices, answer, explain):
    return {"q": question, "choices": choices, "answer": answer, "explain": explain}


lesson("ascii", "🔤", "Les caractères et la table ASCII",
       "Un `char` est un nombre. Comprendre ça rend `isalpha`, `toupper`… évidents.",
       [{"t": "p", "x": "En C, un caractère est simplement un **nombre** : `'A'` vaut 65, `'a'` vaut 97, `'0'` vaut 48. La table ASCII associe un nombre (0 à 127) à chaque caractère."},
        {"t": "ul", "x": ["Majuscules : 65 (`'A'`) à 90 (`'Z'`). Minuscules : 97 (`'a'`) à 122 (`'z'`). Chiffres : 48 à 57.",
                          "`'a' - 'A'` vaut **32** : c'est pour ça que `toupper` fait `c - 32` et `tolower` fait `c + 32`.",
                          "Les caractères **imprimables** vont de 32 (l'espace) à 126 (`'~'`). 127 (DEL) ne l'est pas.",
                          "Les lettres sont **contiguës** : on teste « est-ce une lettre ? » avec deux comparaisons."]},
        {"t": "p", "x": "Essaie toi-même : tape un caractère ci-dessous et regarde ce que renvoient les fonctions de ta libft."},
        {"t": "viz", "x": "ascii"},
        {"t": "tip", "x": "Les fonctions `is*` prennent un `int` (pas un `char`) comme la vraie libc. Depuis le sujet v19.3, elles doivent renvoyer exactement **1** pour vrai et **0** pour faux (la vraie libc peut renvoyer une autre valeur non nulle, pas ta libft)."}],
       [q("Quel est le code ASCII de 'A' ?", ["48", "65", "97", "32"], 1, "'A' = 65, 'a' = 97, '0' = 48, l'espace = 32."),
        q("Que vaut 'a' - 'A' ?", ["1", "26", "32", "48"], 2, "Les minuscules sont 32 positions après les majuscules."),
        q("ft_isprint(127) renvoie…", ["1", "0", "ça dépend de l'ordinateur"], 1, "127 (DEL) n'est pas imprimable : l'intervalle est 32 à 126.")],
       ["ft_isalpha", "ft_isdigit", "ft_isalnum", "ft_isascii", "ft_isprint", "ft_toupper", "ft_tolower"])

lesson("strings", "🧵", "Les chaînes de caractères et le '\\0'",
       "Une chaîne C est un tableau terminé par un octet nul. Tout part de là.",
       [{"t": "p", "x": "Une chaîne C n'a pas de longueur enregistrée : elle se termine par un octet de valeur 0, écrit `'\\0'`. Pour savoir où elle s'arrête, on parcourt jusqu'à le trouver."},
        {"t": "code", "x": "char s[] = \"hello\";   /* 6 octets : h e l l o \\0 */"},
        {"t": "ul", "x": ["`ft_strlen(\"hello\")` vaut **5** : le `'\\0'` n'est pas compté.",
                          "Stocker `n` caractères demande **`n + 1`** octets : d'où le `malloc(len + 1)` partout.",
                          "Une chaîne que tu construis **doit** se terminer par `'\\0'`, sinon les autres fonctions lisent n'importe quoi.",
                          "Le `'\\0'` stoppe les fonctions `str*`, mais pas les fonctions `mem*` (elles comptent des octets)."]},
        {"t": "p", "x": "Regarde l'indice `i` avancer jusqu'au `'\\0'`, comme dans `ft_strlen`, `ft_strchr` ou `ft_strrchr`."},
        {"t": "viz", "x": "strstep"}],
       [q("Que vaut strlen(\"ab\\0cd\") ?", ["2", "5", "4", "3"], 0, "strlen s'arrête au premier '\\0' : seuls \"ab\" sont comptés."),
        q("Combien d'octets faut-il pour stocker la chaîne \"hello\" ?", ["5", "6", "4", "7"], 1, "5 caractères + le '\\0' final = 6 octets."),
        q("Pour dupliquer une chaîne de longueur n avec malloc, on alloue…", ["n", "n + 1", "n - 1", "2 * n"], 1, "n caractères + 1 pour le '\\0'.")],
       ["ft_strlen", "ft_strchr", "ft_strrchr", "ft_strdup"])

lesson("types", "🧱", "const, size_t et unsigned char",
       "Trois mots que tu verras dans chaque prototype de la libft.",
       [{"t": "ul", "x": ["**`const char *s`** : « je promets de ne pas modifier ce que `s` pointe ». Les fonctions qui ne font que lire (`strlen`, `strchr`…) prennent du `const`.",
                          "**`size_t`** : le type **non signé** des tailles. Piège : `size_t i = 0; i - 1` ne donne pas -1 mais un nombre gigantesque. Ne fais jamais `while (i >= 0)` avec un `size_t`.",
                          "**`unsigned char`** : un octet de 0 à 255. Un `char` peut être signé (-128 à 127), donc `0xFF` vaut -1. Pour comparer ou copier des **octets** (`memcmp`, `strncmp`, `memcpy`…), on caste en `unsigned char`."]},
        {"t": "code", "x": "int\tft_memcmp(const void *s1, const void *s2, size_t n)\n{\n\tconst unsigned char\t*a;\n\tconst unsigned char\t*b;\n\tsize_t\t\t\t\ti;\n\n\ta = (const unsigned char *)s1;\n\tb = (const unsigned char *)s2;\n\t..."},
        {"t": "tip", "x": "Pour parcourir à l'envers avec un `size_t` : `while (n > 0) { n--; d[n] = s[n]; }` (c'est exactement ce que fait `ft_memmove`)."}],
       [q("Que vaut (size_t)0 - 1 ?", ["-1", "un très grand nombre", "0", "une erreur de compilation"], 1, "size_t est non signé : 0 - 1 repasse à la valeur maximale."),
        q("const char *s signifie…", ["on ne modifie pas *s via s", "s ne peut pas changer de valeur", "la chaîne est forcément en mémoire morte", "rien de particulier"], 0, "const protège les caractères pointés ; pour protéger le pointeur lui-même ce serait char *const s."),
        q("Pourquoi caster en unsigned char dans ft_memcmp ?", ["pour comparer des octets de 0 à 255", "pour aller plus vite", "parce que char n'existe pas", "pour éviter malloc"], 0, "Avec un char signé, 0xFF serait négatif et le résultat de la comparaison faux.")],
       ["ft_strlen", "ft_memcmp", "ft_strncmp", "ft_memmove"])

lesson("pointers", "👉", "Pointeurs, tableaux et void *",
       "Ce qu'un pointeur fait vraiment quand tu écris p + 1 ou p[i].",
       [{"t": "ul", "x": ["Un pointeur contient une **adresse**. `p[i]` est exactement `*(p + i)`.",
                          "`p + 1` avance de **la taille du type pointé** : 1 octet pour `unsigned char *`, 4 pour `int *`.",
                          "`void *` est un pointeur « sans type » : on ne peut pas faire `ptr[i]` dessus. On le **caste** d'abord : `unsigned char *p = (unsigned char *)ptr;`.",
                          "Un `char **` est un tableau de chaînes (comme le retour de `ft_split`) : `tab[i]` est une chaîne, `tab[i][j]` un caractère.",
                          "`ft_strchr` renvoie un **pointeur dans la chaîne d'origine** (pas une copie) : `ft_strchr(\"hello\", 'l')` pointe sur le premier `l` (indice 2)."]},
        {"t": "code", "x": "unsigned char\t*p;\n\np = (unsigned char *)s;   /* s est un void * */\np[2] = 'x';               /* modifie le 3e octet */"}],
       [q("Peut-on écrire ptr[i] avec ptr de type void * ?", ["oui", "non : il faut caster d'abord", "oui, mais seulement si const"], 1, "void * n'a pas de taille de type : le compilateur ne sait pas de combien avancer."),
        q("Si p est un unsigned char *, p + 1 avance de…", ["1 octet", "4 octets", "8 octets"], 0, "Un pointeur avance de la taille du type pointé : 1 octet pour unsigned char."),
        q("ft_strchr(\"hello\", 'l') renvoie un pointeur sur…", ["le 1er 'l' (indice 2)", "le 2e 'l' (indice 3)", "le 'h'", "NULL"], 0, "strchr cherche la première occurrence (strrchr, la dernière).")],
       ["ft_memset", "ft_memcpy", "ft_memchr", "ft_strchr"])

lesson("memmove", "🔀", "Copier la mémoire : memcpy vs memmove",
       "Pourquoi memmove existe, et le sens de copie à choisir.",
       [{"t": "p", "x": "`memcpy` suppose que les zones source et destination **ne se chevauchent pas**. `memmove` marche **même si elles se chevauchent**."},
        {"t": "ul", "x": ["Si `dest < src` : copie de **gauche à droite**.",
                          "Si `dest > src` : copie de **droite à gauche** (sinon on écrase des octets source avant de les avoir lus).",
                          "Dans les deux cas : `n = 0` ne change rien et on renvoie `dest`."]},
        {"t": "p", "x": "Essaie : décale le texte de 2 vers la droite avec une copie naïve (avant), puis dans le bon sens."},
        {"t": "viz", "x": "memmove"}],
       [q("memmove(buf + 2, buf, 4) sur \"abcdef\" donne…", ["ababcd", "ababab", "abcdef", "ababcf"], 0, "Il faut copier de droite à gauche : on obtient \"ababcd\". Une copie naïve donnerait \"ababab\"."),
        q("Quand dest > src et que les zones se chevauchent, on copie…", ["de gauche à droite", "de droite à gauche", "peu importe"], 1, "En partant de la fin, on ne lit jamais un octet déjà écrasé."),
        q("ft_memmove(a, a, 5) doit…", ["planter", "ne rien changer", "mettre a à zéro"], 1, "Même adresse : la copie ne change rien.")],
       ["ft_memcpy", "ft_memmove"])

lesson("search", "🔎", "Chercher et comparer",
       "strchr, strrchr, memchr, strncmp, memcmp, strnstr : ce qu'ils renvoient exactement.",
       [{"t": "ul", "x": ["`ft_strchr(s, c)` : pointeur sur la **première** occurrence, `NULL` sinon. Si `c == '\\0'` : pointeur sur le `'\\0'` final (pas `NULL`).",
                          "`ft_strrchr` : pareil mais la **dernière** occurrence.",
                          "`ft_memchr(s, c, n)` : cherche dans `n` octets et **ne s'arrête pas au `'\\0'`**.",
                          "`ft_strncmp` / `ft_memcmp` : renvoient la **différence** du premier octet différent (`unsigned char`), ou 0. `strncmp` s'arrête au `'\\0'`, `memcmp` non.",
                          "`ft_strnstr(big, little, len)` : cherche `little` dans les `len` premiers caractères de `big`. `little` vide → renvoie `big`. Condition clé : `i + j < len`."]},
        {"t": "tip", "x": "La moulinette teste surtout les **cas limites** : chaîne vide, `n = 0`, caractère `'\\0'`, `len` plus petit que la chaîne, `len` plus grand que la chaîne."}],
       [q("ft_strchr(\"abc\", '\\0') renvoie…", ["NULL", "un pointeur sur le '\\0' final", "un pointeur sur 'a'"], 1, "On doit pouvoir trouver le '\\0' de fin, comme la vraie strchr."),
        q("ft_strncmp(\"abc\", \"abd\", 2) renvoie…", ["un nombre négatif", "0", "un nombre positif"], 1, "On ne compare que \"ab\" et \"ab\" : égal, donc 0."),
        q("ft_memchr s'arrête-t-elle au '\\0' ?", ["oui, comme strchr", "non, elle regarde n octets", "seulement si n est grand"], 1, "mem* travaille sur des octets, pas sur des chaînes.")],
       ["ft_strchr", "ft_strrchr", "ft_memchr", "ft_strncmp", "ft_memcmp", "ft_strnstr"])

lesson("lcpy", "✂️", "strlcpy et strlcat : tronquer proprement",
       "Les deux fonctions les plus piégeuses de la partie 1, expliquées avec des valeurs.",
       [{"t": "ul", "x": ["`ft_strlcpy(dst, src, size)` copie au plus `size - 1` caractères, termine par `'\\0'` (si `size > 0`) et renvoie **`strlen(src)`**.",
                          "Si le retour est **≥ `size`**, la chaîne a été tronquée.",
                          "`ft_strlcat(dst, src, size)` ajoute `src` à `dst` sans dépasser `size` octets au total. Retour = `min(size, strlen(dst)) + strlen(src)`.",
                          "Si `size <= strlen(dst)` : on n'écrit **rien** et on renvoie `size + strlen(src)`."]},
        {"t": "code", "x": "char d[4];\nft_strlcpy(d, \"hello\", 4);   /* d = \"hel\"  retour 5 */\n\nchar e[10] = \"ab\";\nft_strlcat(e, \"cdef\", 5);   /* e = \"abcd\" retour 6 */"},
        {"t": "tip", "x": "Dans les deux fonctions, le **retour** est la longueur que la chaîne **aurait voulu avoir** : c'est ainsi qu'on détecte la troncature."}],
       [q("ft_strlcpy(d, \"hello\", 4) renvoie…", ["3", "4", "5", "6"], 2, "Toujours strlen(src) : 5. Comme 5 >= 4, la copie a été tronquée (d = \"hel\")."),
        q("Avec d = \"ab\", ft_strlcat(d, \"cdef\", 5) donne…", ["d = \"abcd\", retour 6", "d = \"abcde\", retour 5", "d = \"abcdef\", retour 6", "d = \"ab\", retour 2"], 0, "Au plus 4 caractères + '\\0' : \"abcd\". Retour = 2 + 4 = 6."),
        q("Si size <= strlen(dst) dans strlcat…", ["on écrit quand même un '\\0'", "on n'écrit rien", "on renvoie 0"], 1, "On ne touche pas à dst et on renvoie size + strlen(src).")],
       ["ft_strlcpy", "ft_strlcat"])

lesson("malloc", "🧠", "malloc, free et les fuites mémoire",
       "Allouer, tester, libérer : les règles qui évitent 90 % des erreurs à la correction.",
       [{"t": "ul", "x": ["`malloc(n)` réserve `n` octets et renvoie un pointeur, ou **`NULL` si ça échoue** : toujours tester.",
                          "Tout bloc alloué doit être libéré par `free` exactement **une fois**. Un bloc jamais libéré = **fuite**. Libéré deux fois = plantage.",
                          "Qui libère ? **L'appelant**, pour ce qu'une fonction lui renvoie (`ft_strdup`, `ft_substr`, `ft_split`, `ft_itoa`…).",
                          "Si tu fais plusieurs allocations et que la 3e échoue, il faut **libérer les 2 premières** avant de renvoyer `NULL` (c'est le piège de `ft_split`).",
                          "`ft_calloc(nmemb, size)` : `nmemb * size` peut **déborder** `size_t` → renvoie `NULL` dans ce cas."]},
        {"t": "code", "x": "char\t*r;\n\nr = malloc(len + 1);\nif (!r)\n\treturn (NULL);"},
        {"t": "tip", "x": "Le trainer surveille ton `malloc` : il détecte les fuites **et** simule un `malloc` qui échoue pour vérifier que tu nettoies correctement."}],
       [q("Que fait malloc quand il n'y a plus de mémoire ?", ["il plante", "il renvoie NULL", "il renvoie un pointeur sur 0 octet"], 1, "Il renvoie NULL : c'est à toi de le tester."),
        q("ft_split(\"a b c\", ' ') fait combien de malloc ?", ["3", "4", "1", "6"], 1, "1 pour le tableau + 3 pour les mots = 4 (donc 4 free pour tout libérer)."),
        q("Si le 3e malloc d'un ft_split échoue, il faut…", ["renvoyer NULL directement", "libérer les 2 premiers mots et le tableau, puis renvoyer NULL", "ignorer l'erreur"], 1, "Sinon les blocs déjà alloués sont perdus : fuite mémoire.")],
       ["ft_calloc", "ft_strdup", "ft_substr", "ft_strjoin", "ft_split", "ft_itoa"])

lesson("split", "🪓", "ft_split pas à pas",
       "Compter les mots, allouer, remplir, nettoyer : la méthode qui marche.",
       [{"t": "ol", "x": ["**Compter les mots** (`count_words`) : un mot commence quand on passe d'un séparateur à autre chose.",
                           "**Allouer le tableau** : `(mots + 1)` cases de `char *` (le `+ 1` est pour le `NULL` final).",
                           "**Pour chaque mot** : sauter les séparateurs, mesurer le mot, l'allouer et le copier (`alloc_word`).",
                           "**Terminer** par `tab[i] = NULL`. Si une allocation échoue : `free_all` puis `NULL`."]},
        {"t": "p", "x": "Tape une chaîne et un séparateur, et regarde comment elle est découpée."},
        {"t": "viz", "x": "split"},
        {"t": "tip", "x": "Norme : 25 lignes max par fonction. Découper en `count_words`, `alloc_word`, `free_all`, `fill_tab` rend le code lisible ET conforme."}],
       [q("count_words(\"--a-b--c-\", '-') vaut…", ["2", "3", "4", "5"], 1, "Les mots sont a, b et c : 3."),
        q("Combien de cases faut-il allouer pour le tableau de 3 mots ?", ["3", "4", "2", "6"], 1, "3 mots + 1 case pour le NULL final."),
        q("ft_split(\"\", ' ') renvoie…", ["NULL", "un tableau contenant seulement NULL", "un tableau avec une chaîne vide"], 1, "Un tableau alloué de 1 case, qui vaut NULL : aucun mot.")],
       ["ft_split"])

lesson("fd", "🖨️", "write et les descripteurs de fichier",
       "Comment ft_putstr_fd écrit réellement à l'écran (ou ailleurs).",
       [{"t": "ul", "x": ["Un **descripteur de fichier** (`fd`) est un nombre qui désigne « où écrire » : 0 = clavier, **1 = écran**, 2 = écran des erreurs.",
                          "`write(fd, adresse, nombre_d_octets)` écrit des octets. C'est la seule fonction autorisée pour les `put*_fd`.",
                          "`ft_putchar_fd(c, fd)` : `write(fd, &c, 1)` (on passe l'**adresse** de `c`).",
                          "`ft_putstr_fd(s, fd)` : `write(fd, s, ft_strlen(s))`. `ft_putendl_fd` ajoute un `'\\n'`.",
                          "`ft_putnbr_fd` : récursive. Écrit d'abord les chiffres de gauche : `ft_putnbr_fd(n / 10, fd)`, puis `n % 10`. Piège : `INT_MIN`."]},
        {"t": "code", "x": "void\tft_putnbr_fd(int n, int fd)\n{\n\tlong long\tnb;\n\n\tnb = n;\n\tif (nb < 0)\n\t{\n\t\tft_putchar_fd('-', fd);\n\t\tnb = -nb;\n\t}\n\t..."},
        {"t": "tip", "x": "`-INT_MIN` ne rentre pas dans un `int` : on copie `n` dans un `long long` **avant** de prendre l'opposé (c'est le bug que ton `ft_itoa` et ton `ft_putnbr_fd` avaient sous Windows)."}],
       [q("Quel descripteur correspond à l'écran (sortie standard) ?", ["0", "1", "2", "3"], 1, "0 = entrée, 1 = sortie standard, 2 = sortie d'erreur."),
        q("ft_putendl_fd(\"abc\", 1) écrit combien d'octets ?", ["3", "4", "5"], 1, "\"abc\" + le retour à la ligne = 4 octets."),
        q("Pourquoi ft_putnbr_fd utilise un long long ?", ["pour aller plus vite", "pour supporter INT_MIN", "c'est obligatoire pour write"], 1, "-(-2147483648) dépasse INT_MAX : il faut un type plus grand pour l'opposé.")],
       ["ft_putchar_fd", "ft_putstr_fd", "ft_putendl_fd", "ft_putnbr_fd"])

lesson("funcptr", "🎯", "Les pointeurs de fonction (strmapi / striteri)",
       "Passer une fonction en paramètre : la syntaxe et la différence entre les deux fonctions.",
       [{"t": "p", "x": "`char (*f)(unsigned int, char)` se lit : « `f` est un pointeur vers une fonction qui prend un `unsigned int` et un `char`, et renvoie un `char` ». On l'appelle comme une fonction : `f(i, s[i])`."},
        {"t": "ul", "x": ["**`ft_strmapi`** crée une **nouvelle** chaîne (`malloc`) : `res[i] = f(i, s[i])`. `s` n'est pas modifiée.",
                          "**`ft_striteri`** modifie `s` **sur place** : `f(i, &s[i])`. Aucun `malloc`, pas de retour.",
                          "Dans `striteri`, `f` reçoit l'**adresse** du caractère (`char *`) pour pouvoir le changer."]},
        {"t": "code", "x": "static char\tadd_i(unsigned int i, char c)\n{\n\treturn (c + i);\n}\n/* ft_strmapi(\"abc\", add_i) donne \"ace\" */"}],
       [q("Quelle fonction modifie la chaîne d'origine ?", ["ft_strmapi", "ft_striteri", "les deux"], 1, "striteri travaille sur place avec char *. strmapi renvoie une nouvelle chaîne."),
        q("Que reçoit f dans ft_striteri ?", ["l'indice et le caractère", "l'indice et l'adresse du caractère", "seulement l'indice"], 1, "(unsigned int, char *) : l'adresse permet de modifier le caractère."),
        q("ft_strmapi(\"\", f) doit renvoyer…", ["NULL", "une chaîne vide allouée", "la chaîne d'origine"], 1, "Une nouvelle chaîne vide (allouée) : seul le '\\0' est écrit.")],
       ["ft_strmapi", "ft_striteri"])

lesson("lists", "🔗", "Les listes chaînées (partie 3)",
       "Des noeuds reliés par des pointeurs : t_list, la tête, et pourquoi on passe un t_list **.",
       [{"t": "p", "x": "Une **liste chaînée** est une suite de **noeuds** dispersés en mémoire. Chaque noeud contient une donnée (`content`) et l'adresse du noeud suivant (`next`). Le dernier a `next == NULL`."},
        {"t": "code", "x": "typedef struct s_list\n{\n\tvoid\t\t\t*content;\n\tstruct s_list\t*next;\n}\t\t\t\tt_list;"},
        {"t": "ul", "x": ["`content` est un **`void *`** : la liste peut contenir n'importe quoi (une chaîne, un `int`, une structure…). Elle ne **copie** pas la donnée : elle garde juste son adresse.",
                          "On ne connaît que la **tête** (le premier noeud). Pour atteindre le dernier, il faut parcourir : `while (lst->next) lst = lst->next;`.",
                          "Une liste vide, c'est simplement un pointeur de tête égal à **`NULL`**. Chaque fonction doit gérer ce cas.",
                          "**Pourquoi `t_list **lst` ?** Pour `ft_lstadd_front` et `ft_lstclear`, la **tête change**. Une fonction ne peut modifier que ce qu'on lui passe par adresse : on passe donc l'adresse du pointeur de tête.",
                          "`ft_lstsize` renvoie un **`unsigned int`** (c'est écrit dans le sujet), pas un `int`."]},
        {"t": "p", "x": "Manipule une liste ci-dessous : regarde la tête changer, la mémoire allouée, et ce qu'il faut libérer."},
        {"t": "viz", "x": "list"},
        {"t": "ul", "x": ["**Libérer** : un noeud = **deux** choses à libérer, le contenu (avec `del`) puis le noeud (avec `free`). Dans `ft_lstclear`, retiens `next` **avant** de libérer le noeud.",
                          "**`ft_lstmap`** crée une **nouvelle** liste. Si un `malloc` échoue en route : libère le contenu que `f` vient de produire (`del`), puis les noeuds déjà créés (`ft_lstclear`), puis renvoie `NULL`."]},
        {"t": "tip", "x": "Dessine toujours la liste sur papier avant de coder : des cases, des flèches `next`, et ce que devient `*lst` à chaque ligne. 90 % des bugs de liste se voient sur le dessin."}],
       [q("Pourquoi ft_lstadd_front prend-il un t_list ** ?", ["pour aller plus vite", "parce que la tête de liste change", "parce que t_list * est interdit", "pour pouvoir modifier content"], 1, "Il faut modifier le pointeur de tête de l'appelant : on en passe donc l'adresse."),
        q("Dans ft_lstclear, que faut-il faire avant de libérer un noeud ?", ["rien", "retenir son next", "mettre son content à NULL", "appeler ft_lstsize"], 1, "Après free(noeud), noeud->next n'existe plus : il faut avoir sauvegardé le suivant avant."),
        q("ft_lstdelone libère…", ["tous les noeuds de la liste", "le content (via del) et le noeud, mais pas les suivants", "seulement le noeud", "seulement le content"], 1, "Un seul noeud : son contenu avec del, puis le noeud avec free. Les suivants restent intacts."),
        q("Quel est le type de retour de ft_lstsize dans le sujet ?", ["int", "size_t", "unsigned int", "long"], 2, "Le sujet v19.3 demande `unsigned int ft_lstsize(t_list *lst)`.")],
       ["ft_lstnew", "ft_lstadd_front", "ft_lstsize", "ft_lstlast", "ft_lstadd_back", "ft_lstdelone", "ft_lstclear", "ft_lstiter", "ft_lstmap"])

lesson("norm","📏", "La norme de 42 en 10 règles",
       "Les erreurs de norminette les plus fréquentes, à connaître par cœur.",
       [{"t": "ol", "x": ["**25 lignes** maximum par fonction (sans compter les accolades).",
                           "**5 fonctions** maximum par fichier, **4 paramètres** maximum par fonction.",
                           "Indentation avec des **tabulations** (jamais des espaces).",
                           "**80 colonnes** maximum par ligne.",
                           "Toutes les **variables déclarées en haut** de la fonction, **alignées** par tabulation, puis une ligne vide.",
                           "**Interdits** : `for`, `do…while`, `switch`, `goto`, l'opérateur ternaire `?:`.",
                           "`return (valeur);` avec **parenthèses**.",
                           "Une seule instruction par ligne, pas d'espace avant `;` (`i++;` et pas `i ++ ;`).",
                           "**En-tête 42** au début de chaque fichier ; **retour à la ligne** à la fin.",
                           "Fonctions d'aide : `static` (sinon elles polluent la libft)."]},
        {"t": "tip", "x": "Un exercice n'est validé dans le trainer que si la **norme est OK** : c'est aussi le cas à l'école pour la libft."}],
       [q("Combien de lignes maximum par fonction ?", ["20", "25", "30", "42"], 1, "25 lignes (sans les accolades)."),
        q("Lequel de ces mots-clés est interdit ?", ["while", "if", "for", "return"], 2, "`for` est interdit : on utilise `while`."),
        q("Où déclare-t-on les variables ?", ["n'importe où", "en haut de la fonction", "dans le main seulement"], 1, "En haut de la fonction, alignées par tabulation, suivies d'une ligne vide.")],
       [])

LESSONS_BY_ID = {l["id"]: l for l in LESSONS}
