"""Approfondissements : parties 2 (fonctions en plus) et 3 (listes chaînées)."""
from .func_deep import deep

MALLOC_FAIL = ("`malloc` renvoie `NULL` quand il ne peut pas réserver la mémoire. Si on ne teste pas, la première écriture dans ce pointeur fait planter le programme "
               "(segfault). On renvoie `NULL` à l'appelant, qui doit lui aussi le gérer.")

# ---------------------------------------------------------------- substr
deep("ft_substr", 3,
     "`unsigned int start` : position de départ (0 = premier caractère). `size_t len` : nombre maximum de caractères voulus. Le résultat est une **nouvelle** chaîne : l'appelant doit la libérer.")
deep("ft_substr", 5, "`substr` : la nouvelle chaîne ; `i` : compteur de copie ; `s_len` : longueur de `s`. Les trois sont déclarés en haut (règle de la norme).")
deep("ft_substr", 9, "Si `s` est `NULL`, `ft_strlen(s)` planterait. On renvoie `NULL` avant de s'en servir. `!s` veut dire `s == NULL`.")
deep("ft_substr", 11, "On a besoin de la longueur de `s` pour deux choses : savoir si `start` est valide, et ne pas copier plus que ce qui existe.")
deep("ft_substr", 12,
     "Si `start >= s_len`, il n'y a **aucun** caractère à partir de `start`. Le sujet attend alors une chaîne **vide** (un seul octet `'\\0'`) et pas `NULL` : `NULL` voudrait dire « erreur ». "
     "`ft_strdup(\"\")` fait exactement ça : alloue 1 octet contenant `'\\0'`.")
deep("ft_substr", 14,
     "`s_len - start` est le nombre de caractères disponibles après `start`. Il est positif ici, car on a vérifié `start < s_len` juste avant (sinon la soustraction de deux nombres non signés donnerait un énorme nombre). "
     "Si on demande plus (`len` trop grand), on réduit `len` : on ne copie jamais plus que ce qui existe.")
deep("ft_substr", 16,
     "`len + 1` : les `len` caractères plus le `'\\0'`. `sizeof(char)` vaut toujours 1, c'est juste une habitude d'écriture. " + MALLOC_FAIL)
deep("ft_substr", 19,
     "On copie `s[start + i]` dans `substr[i]`. Le décalage `start + i` est la clé : `i` repart de 0 dans la nouvelle chaîne, mais on lit plus loin dans `s`. "
     "Le test `s[start + i]` (deuxième condition) est une sécurité : on s'arrête si on rencontre le `'\\0'` de `s`.")
deep("ft_substr", 25, "La copie ne met pas de `'\\0'` : on le pose nous-mêmes à l'indice `i` (= `len` ici), sinon la chaîne ne serait pas terminée.")
deep("ft_substr", 26, "On renvoie la nouvelle chaîne (à libérer par l'appelant avec `free`).")

# ---------------------------------------------------------------- strjoin
deep("ft_strjoin", 3, "`char const *s1` est identique à `const char *s1` : l'ordre de `const` et `char` n'a pas d'importance, c'est la même chose.")
deep("ft_strjoin", 5, "`str` : le résultat ; `len1` et `len2` : les longueurs des deux chaînes, pour calculer la taille et pour copier.")
deep("ft_strjoin", 9, "Si l'une des deux chaînes est `NULL`, on ne peut pas mesurer ni copier : `NULL`. `!s1 || !s2` = « s1 est NULL ou s2 est NULL ».")
deep("ft_strjoin", 11, "On mesure une fois chaque chaîne (pas besoin de la mesurer ensuite).")
deep("ft_strjoin", 13,
     "Taille = `len1` + `len2` + 1. Le `+ 1` est pour le **seul** `'\\0'` final du résultat. " + MALLOC_FAIL)
deep("ft_strjoin", 14, "Test de `malloc` : voir plus haut.")
deep("ft_strjoin", 16,
     "On copie les `len1` caractères de `s1` au début de `str`, **sans** son `'\\0'` : s'il était copié, il couperait la chaîne avant `s2`.")
deep("ft_strjoin", 17,
     "`str + len1` est l'adresse de la case juste après la copie de `s1` (arithmétique de pointeurs : on avance de `len1` octets). On y copie `s2` avec ses `len2 + 1` octets : "
     "les caractères **et** son `'\\0'`, qui termine ainsi tout le résultat.")
deep("ft_strjoin", 18, "On renvoie la nouvelle chaîne. Les deux chaînes d'origine ne sont jamais modifiées.")

# ---------------------------------------------------------------- strtrim
deep("ft_strtrim", 3,
     "`set` n'est pas un texte à chercher en entier : c'est un **ensemble de caractères**. `ft_strtrim(\"abxba\", \"ab\")` retire `a` et `b` en début **et** en fin, donne `\"x\"`.")
deep("ft_strtrim", 5,
     "On ne copie pas caractère par caractère : on cherche deux indices, `start` (premier caractère à garder) et `end` (juste **après** le dernier à garder), puis on extrait avec `ft_substr`.")
deep("ft_strtrim", 9, "Si `s1` ou `set` est `NULL`, rien n'est possible : `NULL`.")
deep("ft_strtrim", 11,
     "`ft_strchr(set, s1[start])` renvoie un pointeur (non nul) si le caractère est dans `set`, `NULL` sinon. Un pointeur non nul est « vrai » dans un `if`/`while` : "
     "la boucle avance `start` tant que le caractère est à retirer. `s1[start]` d'abord : on s'arrête à la fin de la chaîne.",
     "Pourquoi `s1[start] &&` en premier ? Arrivé au `'\\0'` final de `s1`, `ft_strchr(set, '\\0')` renvoie un pointeur **non nul** (il trouve le `'\\0'` de `set`). "
     "Sans ce test, la boucle croirait que le `'\\0'` est « à retirer » et continuerait au-delà de la fin de `s1`.")
deep("ft_strtrim", 14, "`end` démarre juste après le dernier caractère (sur le `'\\0'`) : c'est la borne « exclue » qui sert à `ft_substr`.")
deep("ft_strtrim", 15,
     "On recule `end` tant que le caractère **juste avant** (`s1[end - 1]`) est à retirer. On lit `end - 1` et pas `end` : `s1[end]` est le `'\\0'`. "
     "`end > start` empêche de passer sous `start` : si toute la chaîne est à retirer, `end` s'arrête sur `start` et le résultat est vide. Ça évite aussi `s1[-1]`.")
deep("ft_strtrim", 17,
     "`end - start` est le nombre de caractères conservés (l'intervalle `[start, end[`). `ft_substr` alloue et copie. Elle gère aussi le résultat vide (renvoie `\"\"`). "
     "On a donc la même gestion d'erreur d'allocation sans la réécrire.")

# ---------------------------------------------------------------- split
deep("ft_split", 3,
     "**`char **`** = un pointeur vers des pointeurs vers des `char` = un tableau de chaînes. Schéma pour `\"a bc\"` :\n"
     "tab ──> [ ptr0 ][ ptr1 ][ NULL ]\n"
     "           │        │\n"
     "           ▼        ▼\n"
     "          \"a\"      \"bc\"\n"
     "Le dernier pointeur est `NULL` : c'est la façon de dire « fin du tableau » (pas de champ « taille »).",
     "`count_words` est `static` : visible seulement dans ce fichier. Le sujet autorise ces fonctions d'aide, nécessaires pour tenir dans 25 lignes par fonction.",
     "Machine à deux états avec `in_word` : « suis-je dans un mot ? ». Un caractère différent de `c` quand on n'est **pas** dans un mot = début d'un nouveau mot : `count++`. "
     "Un séparateur (`c`) remet `in_word` à 0. Plusieurs séparateurs d'affilée ne créent donc pas de mots vides.\n"
     "\"aa  b\" : a(début, 1) a(déjà dans le mot) ' '(sortie) ' ' b(début, 2)  -> 2 mots")
deep("ft_split", 24,
     "Copie un mot de `len` caractères : `malloc(len + 1)` (le `+ 1` est le `'\\0'`), vérification, boucle de copie, puis `word[i] = '\\0'`. Comme `ft_substr`, mais sans `start`.")
deep("ft_split", 42,
     "**Pourquoi libérer en cas d'échec ?** Si le 3e `malloc` échoue, les 2 mots déjà alloués et le tableau seraient perdus (ni l'appelant ni nous n'aurions encore leur adresse) : c'est une **fuite**. "
     "`free_all` libère les mots de `i - 1` à 0, puis le tableau lui-même (`free(tab)`) et renvoie `NULL`.",
     "Comme `i` est un `int`, `while (i > 0) { i--; free(tab[i]); }` libère exactement les indices `i - 1, ..., 0`.")
deep("ft_split", 53,
     "`fill_tab` remplit `tab` mot par mot. Elle renvoie 1 (succès) ou 0 (échec, tout est libéré). Pourquoi pas directement dans `ft_split` ? Pour respecter 25 lignes.")
deep("ft_split", 58, "`i` : numéro du mot en cours (indice dans `tab`). `len` : longueur du mot en cours.")
deep("ft_split", 61,
     "On saute les séparateurs en début de mot. `*s && *s == c` : jamais de lecture après la fin (le `'\\0'` stoppe la boucle). Avancer `s` modifie la copie locale du pointeur seulement.")
deep("ft_split", 63,
     "S'il reste des caractères après les séparateurs, c'est un mot. On mesure `len` : le nombre de caractères avant le prochain séparateur ou le `'\\0'`. `s[len]` est lu sans avancer `s`.")
deep("ft_split", 68,
     "`alloc_word(s, len)` copie le mot. Si elle échoue (`NULL`), on nettoie : `free_all(tab, i)` libère les `i` mots **déjà** réussis (le mot courant n'existe pas) et le tableau. "
     "On renvoie 0 pour dire à `ft_split` que tout est déjà libéré.")
deep("ft_split", 74, "Mot réussi : `i++` passe à la case suivante. `s += len` saute le mot qu'on vient de copier ; la boucle externe reprend sur le séparateur suivant.")
deep("ft_split", 78,
     "`tab[i] = NULL` : le terminateur. À ce stade `i` vaut exactement le nombre de mots, et le tableau a bien `count_words + 1` cases : la case `i` existe.")
deep("ft_split", 82, "`char **` en retour : un tableau de chaînes. À libérer par l'appelant : chaque mot avec `free`, puis `free` du tableau.")
deep("ft_split", 84, "Si `s` est `NULL`, `NULL`. Sinon on prépare `tab`.")
deep("ft_split", 88,
     "`sizeof(char *)` est la taille d'un **pointeur** (8 octets sur 64 bits), car chaque case du tableau est un pointeur vers un mot. "
     "On réserve `count_words + 1` cases : une par mot plus la case finale `NULL`. Oublier le `+ 1` ferait déborder à l'écriture du `NULL`.")
deep("ft_split", 91,
     "Si `fill_tab` renvoie 0, il a déjà tout libéré (mots + tableau) : il ne faut **surtout pas** refaire `free(tab)` (double free). On renvoie simplement `NULL`.")

# ---------------------------------------------------------------- itoa
deep("ft_itoa", 3,
     "`ft_nbrlen` compte les caractères nécessaires. Elle prend un `long long` pour que `-n` fonctionne même pour `INT_MIN` (voir plus bas).",
     "`if (n <= 0)` : pour `0` ou un négatif, on compte déjà **1 caractère** (le `'0'` ou le `'-'`). Pour un négatif, `n = -n` le rend positif pour compter ses chiffres. "
     "Pour `0`, `-0` vaut 0 : la boucle ne tourne pas, et le `1` compté est bien le `'0'`.",
     "`while (n > 0) { n /= 10; len++; }` : chaque division par 10 enlève un chiffre. `1234 -> 123 -> 12 -> 1 -> 0` : 4 tours = 4 chiffres. "
     "(La division entière jette le reste.)")
deep("ft_itoa", 21, "Un `int` en entrée, une chaîne allouée en sortie (à libérer par l'appelant).")
deep("ft_itoa", 23,
     "**Pourquoi un `long long` ?** Un `int` va de -2 147 483 648 à 2 147 483 647. L'opposé de `INT_MIN` serait +2 147 483 648, qui **ne tient pas** dans un `int` : débordement. "
     "Un `long long` (64 bits) peut le contenir. Sans cela, `ft_itoa(-2147483648)` échouerait.")
deep("ft_itoa", 27, "`nb = n` : conversion automatique `int` -> `long long` (sans perte). Puis on calcule la longueur à allouer.")
deep("ft_itoa", 29, "`len + 1` : les caractères du nombre (signe compris) plus le `'\\0'`. " + MALLOC_FAIL)
deep("ft_itoa", 32,
     "On pose le `'\\0'` à la fin tout de suite : `res[len]` est la dernière case (indice `len`, car les caractères occupent `0` à `len - 1`). "
     "On remplira ensuite de droite à gauche, vers le début.")
deep("ft_itoa", 33,
     "Si `nb < 0` : le signe `'-'` va dans la **première** case, puis on travaille sur la valeur positive. Les chiffres iront de la case `1` à la fin. `res[0] = '-'`.")
deep("ft_itoa", 38,
     "Le cas `0` : la boucle `while (nb > 0)` ne tourne pas du tout. On écrit donc `'0'` à la main dans `res[0]`. La longueur calculée est 1, la case 1 contient déjà le `'\\0'`.")
deep("ft_itoa", 40,
     "**Remplissage de droite à gauche.** On obtient les chiffres dans l'ordre inverse : `nb % 10` est le **dernier** chiffre. `--len` recule d'une case **avant** d'écrire (préfixe), "
     "donc on remplit `len - 1`, `len - 2`, etc. `nb % 10` est un nombre de 0 à 9 ; `+ '0'` le transforme en caractère (`7 + 48 = 55` = `'7'`). "
     "`nb /= 10` jette le dernier chiffre.\n"
     "nb=105 : 105 % 10 = 5 -> '5' ; nb=10\n"
     "         10 % 10 = 0 -> '0' ; nb=1\n"
     "          1 % 10 = 1 -> '1' ; nb=0   (on remplit de droite à gauche : \"105\")")
deep("ft_itoa", 45, "On renvoie la chaîne. Le `'-'` éventuel est déjà en `res[0]`.")

# ---------------------------------------------------------------- strmapi / striteri
deep("ft_strmapi", 3,
     "`char (*f)(unsigned int, char)` se lit : « `f` est un **pointeur vers une fonction** qui prend un `unsigned int` et un `char`, et renvoie un `char` ». "
     "Les parenthèses autour de `*f` sont indispensables : sans elles, ce serait une fonction qui renvoie un `char *`. "
     "On l'appelle comme une fonction normale : `f(i, s[i])`.")
deep("ft_strmapi", 5, "`i` est un `unsigned int`, le type exact attendu par `f` pour son premier paramètre (et non `size_t`).")
deep("ft_strmapi", 8, "Une fonction `NULL` ne peut pas être appelée (plantage). On vérifie `s` **et** `f` avant tout.")
deep("ft_strmapi", 10, "Même taille que `s` plus le `'\\0'`. " + MALLOC_FAIL)
deep("ft_strmapi", 13, "Départ à 0.")
deep("ft_strmapi", 14,
     "`res[i] = f(i, s[i])` : on applique `f` à la position et au caractère, et on range le résultat dans la **nouvelle** chaîne. `s` n'est jamais modifiée : "
     "c'est la différence avec `ft_striteri`. L'indice vient avant le caractère, dans cet ordre.")
deep("ft_strmapi", 19, "La boucle s'arrête avant le `'\\0'` de `s` : on pose le nôtre à la fin de `res`, sinon elle ne serait pas terminée.")
deep("ft_strmapi", 20, "On renvoie la nouvelle chaîne (à libérer par l'appelant).")

deep("ft_striteri", 3,
     "`void (*f)(unsigned int, char *)` : pointeur vers une fonction qui reçoit l'indice et l'**adresse** d'un caractère (`char *`), et ne renvoie rien. "
     "Comme `f` reçoit l'adresse, elle peut modifier le caractère dans la chaîne d'origine : `*c = ...`.")
deep("ft_striteri", 5, "Un `unsigned int` : c'est le type du premier paramètre de `f`.")
deep("ft_striteri", 7, "`return ;` sans valeur : la fonction est `void`. Avec `NULL` on ne ferait rien d'utile, donc on sort tout de suite.")
deep("ft_striteri", 9, "Départ à l'indice 0.")
deep("ft_striteri", 10,
     "`&s[i]` est l'**adresse** du caractère numéro `i` (équivalent à `s + i`). Passer `s[i]` donnerait une copie : `f` pourrait la changer sans effet sur la chaîne. "
     "Passer `&s[i]` lui permet de modifier l'original. C'est le mécanisme de base pour modifier une variable dans une autre fonction.")

# ---------------------------------------------------------------- put*_fd
deep("ft_putchar_fd", 3,
     "`fd` (file descriptor) est un numéro qui désigne « où écrire » : 0 = entrée standard, **1 = sortie standard (l'écran)**, 2 = sortie d'erreur. Un fichier ouvert avec `open` reçoit aussi un numéro.")
deep("ft_putchar_fd", 5,
     "`write(fd, &c, 1)` : écrire **1 octet** depuis l'adresse `&c`. `write` attend une **adresse** (un pointeur), pas la valeur : `&c` est l'adresse de la variable `c`. "
     "`write(fd, c, 1)` ne compilerait pas, ou planterait en prenant `c` pour une adresse. `write` est un appel système : il demande directement au système d'écrire.")
deep("ft_putstr_fd", 3, "Écrit toute la chaîne d'un coup. `fd` : où écrire (1 = écran).")
deep("ft_putstr_fd", 5, "Si `s` est `NULL`, `ft_strlen(s)` planterait : on ne fait rien. `return ;` sort d'une fonction `void`.")
deep("ft_putstr_fd", 7,
     "`write(fd, s, ft_strlen(s))` : `s` est déjà une adresse, et `ft_strlen` donne le nombre d'octets, `'\\0'` exclu. "
     "Un seul appel `write` est plus rapide qu'un appel par caractère : chaque appel système a un coût.")
deep("ft_putendl_fd", 3, "Comme `ft_putstr_fd`, plus un retour à la ligne (`endl` = end of line).")
deep("ft_putendl_fd", 5, "Si `s` est `NULL`, on ne fait rien du tout (pas même le `\\n`).")
deep("ft_putendl_fd", 7, "La chaîne d'abord, sans son `'\\0'`.")
deep("ft_putendl_fd", 8,
     "`\"\\n\"` est une chaîne de 1 caractère (le retour à la ligne) : on écrit 1 octet depuis son adresse. On écrit exactement **un** `\\n`.")

deep("ft_putnbr_fd", 3, "Un `int` en entrée, rien en sortie : tout part sur `fd`.")
deep("ft_putnbr_fd", 5, "`long long` pour pouvoir prendre l'opposé de `INT_MIN` sans débordement (voir `ft_itoa`).")
deep("ft_putnbr_fd", 7, "On copie `n` dans `nb` (conversion sans perte `int` -> `long long`).")
deep("ft_putnbr_fd", 8,
     "Si négatif : on écrit `'-'` **une seule fois**, puis `nb = -nb` pour continuer avec un nombre positif. Après cette ligne, `nb` est toujours >= 0, donc plus de signe à gérer dans les appels récursifs.")
deep("ft_putnbr_fd", 13,
     "**Récursion.** Pour écrire 123, il faut écrire d'abord 12 puis 3. `nb / 10` retire le dernier chiffre. L'appel récursif écrit tous les chiffres de gauche **avant** que la ligne suivante n'écrive le dernier.\n"
     "putnbr(123) -> putnbr(12) -> putnbr(1) -> écrit '1'\n"
     "                           <- écrit '2' (12 % 10)\n"
     "                <- écrit '3' (123 % 10)",
     "La condition d'arrêt `nb >= 10` est essentielle : sans elle, la récursion ne se terminerait jamais.")
deep("ft_putnbr_fd", 15,
     "`nb % 10` donne le dernier chiffre (0 à 9) ; `+ '0'` le convertit en caractère (`3 + 48 = 51 = '3'`). `ft_putchar_fd` reçoit un `char` : la valeur passe sans perte car elle est entre 48 et 57.")

# ---------------------------------------------------------------- listes
deep("ft_lstnew", 3,
     "Une liste chaînée est une suite de **noeuds** reliés par des pointeurs :\n"
     "[content|next] ──> [content|next] ──> [content|next] ──> NULL\n"
     "Chaque noeud a un `content` (la donnée, de type `void *` pour accepter n'importe quoi) et un `next` (le noeud suivant, ou `NULL` pour le dernier). "
     "Contrairement à un tableau, on peut insérer sans tout décaler, mais on ne peut pas accéder directement au n-ième élément.")
deep("ft_lstnew", 5, "`node` : le pointeur vers le noeud qu'on va créer.")
deep("ft_lstnew", 7,
     "`sizeof(t_list)` = la taille d'**un noeud** (deux pointeurs : 16 octets sur 64 bits). Attention : `sizeof(t_list *)` serait la taille d'un seul pointeur (8) : trop petit, débordement à l'écriture de `next`. " + MALLOC_FAIL)
deep("ft_lstnew", 10,
     "`node->content` est la forme courte de `(*node).content` : « le champ `content` de la structure pointée par `node` ». "
     "On range **l'adresse** de la donnée : on ne copie pas son contenu. Le noeud et la donnée restent deux choses séparées.")
deep("ft_lstnew", 11, "Un noeud tout neuf n'a pas de suivant : `NULL`. Si on oubliait cette ligne, `next` contiendrait une valeur quelconque (le `malloc` ne met rien à zéro), et le parcours planterait.")
deep("ft_lstnew", 12, "On renvoie le noeud : à libérer avec `ft_lstdelone`.")

deep("ft_lstadd_front", 3,
     "**Pourquoi `t_list **lst` (deux étoiles) ?** Le pointeur de tête, par exemple `t_list *liste;`, est une variable de l'appelant. Si on passait `liste` par valeur, la fonction recevrait une **copie** et ne pourrait pas changer la tête de l'appelant. "
     "En passant son **adresse** (`&liste`), la fonction peut écrire dans la vraie variable via `*lst`.\n"
     "appelant :  liste ──> [a] ──> [b]\n"
     "lst = &liste  ─────>  liste  (on peut modifier `liste` en écrivant `*lst = ...`)")
deep("ft_lstadd_front", 5, "Si `lst` (pas de liste) ou `new` (rien à ajouter) est `NULL`, on ne fait rien. `lst == NULL` est différent de `*lst == NULL` (qui est simplement une liste vide, valide).")
deep("ft_lstadd_front", 7,
     "`new->next = *lst` : le nouveau noeud pointe vers l'**ancienne tête** (`*lst`). Si la liste était vide, `*lst` vaut `NULL` et `new->next` aussi : correct.")
deep("ft_lstadd_front", 8,
     "`*lst = new` : la tête de l'appelant devient `new`. **L'ordre des deux lignes compte** : si on faisait `*lst = new` d'abord, on perdrait l'adresse de l'ancienne tête avant de la relier.")

deep("ft_lstsize", 3, "`unsigned int` : un nombre de noeuds n'est jamais négatif. Le sujet v19.3 impose ce type de retour.")
deep("ft_lstsize", 5, "`n` : le compteur, du même type que le retour.")
deep("ft_lstsize", 7, "Une liste vide (`NULL`) doit renvoyer 0 : on part de 0 et la boucle ne tourne pas.")
deep("ft_lstsize", 8,
     "`lst` est un paramètre : une **copie locale** du pointeur. On peut donc l'avancer (`lst = lst->next`) sans abîmer la liste de l'appelant. "
     "`lst->next` : le noeud suivant, ou `NULL` pour le dernier, ce qui arrête la boucle.")
deep("ft_lstsize", 13, "Renvoie le nombre de noeuds parcourus.")

deep("ft_lstlast", 3, "Renvoie un pointeur vers le dernier noeud (pas son contenu), ou `NULL` si la liste est vide.")
deep("ft_lstlast", 5, "Liste vide : on renvoie `NULL` tout de suite. Sans ça, `lst->next` lirait un champ d'un pointeur `NULL` : plantage.")
deep("ft_lstlast", 7,
     "On avance tant que le noeud **a un suivant** (`lst->next` non nul). On s'arrête donc **sur** le dernier noeud (celui dont `next` vaut `NULL`), pas après lui. "
     "Avec `while (lst)`, on irait jusqu'à `NULL` et on ne pourrait plus renvoyer le dernier noeud.")
deep("ft_lstlast", 9, "On renvoie le dernier noeud (pas une copie : l'appelant peut le modifier).")

deep("ft_lstadd_back", 3, "`**` encore : si la liste est vide, la tête de l'appelant doit changer (elle devient `new`). Voir `ft_lstadd_front` pour le détail.")
deep("ft_lstadd_back", 5, "Rien à faire si pas de liste ou rien à ajouter.")
deep("ft_lstadd_back", 7,
     "Liste vide (`*lst == NULL`) : il n'y a pas de dernier noeud auquel s'accrocher. `new` devient la tête, via `*lst = new`.")
deep("ft_lstadd_back", 9,
     "Sinon on trouve le dernier noeud avec `ft_lstlast(*lst)` (on passe `*lst`, la tête, pas `lst`) et on le relie : `->next = new`. "
     "On réutilise ainsi `ft_lstlast`. `new->next` doit déjà valoir `NULL` (c'est le cas si `new` vient de `ft_lstnew`).")

deep("ft_lstdelone", 3,
     "**`void (*del)(void *)`** = pointeur vers une fonction qui reçoit un `void *` et ne renvoie rien. Pourquoi ? `ft_lstdelone` ne sait pas **comment** libérer le contenu : "
     "c'est peut-être une chaîne (`free`), une structure complexe (une fonction à soi), ou rien du tout. L'appelant fournit la fonction qui sait faire.")
deep("ft_lstdelone", 5, "`lst` `NULL` : rien à libérer. `return ;` dans une fonction `void`.")
deep("ft_lstdelone", 7,
     "`if (del)` : on teste que la fonction existe avant de l'appeler (appeler un pointeur de fonction `NULL` fait planter). `del(lst->content)` libère le **contenu**.")
deep("ft_lstdelone", 9,
     "`free(lst)` libère le **noeud**. L'ordre est important : si on libérait le noeud d'abord, `lst->content` ne serait plus accessible (la mémoire est rendue), "
     "et on perdrait l'adresse du contenu : fuite, ou lecture d'une zone libérée. On ne touche **pas** à `lst->next` : le noeud suivant reste valide.")

deep("ft_lstclear", 3, "`t_list **lst` : à la fin, la tête de l'appelant doit valoir `NULL` (liste vide). Il faut donc pouvoir modifier la variable de l'appelant, d'où le `**`.")
deep("ft_lstclear", 5, "`next` garde le noeud suivant **avant** de libérer le noeud courant : après un `free`, on n'a plus le droit de lire dedans.")
deep("ft_lstclear", 7, "`lst` `NULL` (pas même un pointeur de tête) : rien à faire.")
deep("ft_lstclear", 9,
     "Boucle tant que la tête n'est pas `NULL`, en trois étapes **dans cet ordre** :\n"
     "1) next = (*lst)->next   (on retient la suite)\n"
     "2) ft_lstdelone(*lst)    (on libère le contenu puis le noeud)\n"
     "3) *lst = next           (la tête avance)",
     "`(*lst)->next` : les parenthèses sont obligatoires. `->` s'applique d'abord à ce qui est à sa gauche : sans parenthèses, `*lst->next` signifierait `*(lst->next)`, "
     "ce qui n'a pas de sens ici. `*lst` est la tête, `(*lst)->next` son suivant.",
     "Lire un noeud après l'avoir libéré (use after free) est un bug sérieux. C'est pour ça qu'on sauvegarde `next` d'abord. "
     "À la fin de la boucle, `*lst` vaut `NULL` : la liste de l'appelant est bien vide.")

deep("ft_lstiter", 3, "`void (*f)(void *)` : fonction qui reçoit le **contenu** (pas le noeud). `lst` n'est pas un `**` : on ne modifie pas la tête.")
deep("ft_lstiter", 5,
     "Parcours classique : `f(lst->content)` puis `lst = lst->next`. Sans cette dernière ligne, la boucle ne finit jamais (boucle infinie). Liste vide : la boucle ne tourne pas.")

deep("ft_lstmap", 3,
     "Deux pointeurs de fonction : `f` transforme un contenu en un **nouveau** contenu ; `del` sait libérer un contenu si quelque chose se passe mal. "
     "`ft_lstmap` ne modifie pas la liste d'origine : elle en construit une autre.")
deep("ft_lstmap", 5, "`new_list` : la tête de la nouvelle liste. `node` : le noeud en cours de création. `content` : le contenu produit par `f`.")
deep("ft_lstmap", 9, "La nouvelle liste est vide (`NULL`) au départ : `ft_lstadd_back` sait gérer ce cas.")
deep("ft_lstmap", 10, "On parcourt la liste d'origine, un noeud à la fois.")
deep("ft_lstmap", 12, "`f(lst->content)` produit un contenu : souvent alloué avec `malloc`. C'est maintenant à nous d'en prendre soin.")
deep("ft_lstmap", 13, "`ft_lstnew(content)` crée un noeud pour le contenir. Cette allocation peut elle aussi échouer.")
deep("ft_lstmap", 14,
     "**Gestion d'erreur sans fuite.** Si `ft_lstnew` échoue, on a un `content` qui n'appartient à aucun noeud : `del(content)` le libère. "
     "Puis `ft_lstclear(&new_list, del)` libère les noeuds **déjà créés** (et leurs contenus). Enfin on renvoie `NULL`. Oublier `del(content)` ferait fuiter le dernier contenu produit.",
     "`&new_list` : l'adresse de la tête, car `ft_lstclear` prend un `t_list **` et doit la remettre à `NULL`.")
deep("ft_lstmap", 20,
     "`ft_lstadd_back(&new_list, node)` : on accroche à la fin. On passe `&new_list` car la première fois, la tête change (de `NULL` à `node`). "
     "`lst = lst->next` avance dans la liste d'origine.")
deep("ft_lstmap", 23, "On renvoie la nouvelle liste. L'originale n'a pas bougé.")
