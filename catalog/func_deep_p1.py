"""Approfondissements : partie 1 (fonctions de la libc)."""
from .func_deep import deep

INT_WHY = ("Pourquoi `int c` et pas `char c` ? Dans la vraie libc, ces fonctions acceptent un `int` qui vaut soit un "
           "caractère (0 à 255), soit `EOF` (qui vaut -1). Un `char` ne peut pas représenter à la fois 0 à 255 et -1 "
           "sans ambiguïté (selon la machine, `char` est signé ou non). C'est aussi pour ça que les tests passent -1.")
RET_WHY = ("Le sujet v19.3 demande de renvoyer exactement **1** ou **0**. La vraie `isalpha` renvoie « n'importe quel "
           "nombre non nul », mais ici on veut des valeurs précises, d'où l'écriture explicite du `return (1)`.")

# ---------------------------------------------------------------- is*
deep("ft_isalpha", 3, INT_WHY)
deep("ft_isalpha", 5,
     "`'A'` n'est pas un « texte » : en C, un caractère entre apostrophes est un **nombre** (son code ASCII, 65 pour `'A'`). "
     "Écrire `c >= 'A'` ou `c >= 65` est exactement la même chose ; la première forme se lit mieux.",
     "`&&` veut dire « et » : les deux conditions doivent être vraies. `||` veut dire « ou » : une seule suffit. "
     "Les parenthèses séparent les deux intervalles pour qu'on les lise d'un coup d'œil.",
     "`||` est **court-circuité** : si le premier intervalle est vrai, le deuxième n'est même pas évalué (le résultat est déjà connu).",
     "Pourquoi deux intervalles ? Dans la table ASCII, les majuscules (65 à 90) et les minuscules (97 à 122) ne sont pas collées : "
     "entre elles il y a `[`, `]`, `^`, `_` et l'accent grave. Un seul intervalle `'A'` à `'z'` les accepterait à tort.")
deep("ft_isalpha", 6, RET_WHY)

deep("ft_isdigit", 3, INT_WHY)
deep("ft_isdigit", 5,
     "Un seul intervalle suffit car le standard C **garantit** que les chiffres `'0'` à `'9'` se suivent (sur toutes les machines). "
     "Ce n'est pas garanti pour les lettres, mais ça l'est pour les chiffres.",
     "Attention à la différence : `'0'` est le caractère (code 48), `0` est le nombre zéro (le caractère nul). `ft_isdigit(0)` doit donc renvoyer 0.")
deep("ft_isdigit", 6, RET_WHY)

deep("ft_isalnum", 3, INT_WHY)
deep("ft_isalnum", 5,
     "On **réutilise** `ft_isalpha` et `ft_isdigit` au lieu de recopier les intervalles : moins de code, moins de risque d'erreur, "
     "et si on corrige l'une des deux, `ft_isalnum` est corrigée gratuitement. C'est un principe de base : ne pas répéter.",
     "Grâce au court-circuit de `||`, si `c` est une lettre, `ft_isdigit` n'est jamais appelée.",
     "Une fonction appelle l'autre : à l'édition de liens, `ft_isalpha.o` et `ft_isdigit.o` doivent donc être dans `libft.a` (ils y sont via le Makefile).")

deep("ft_isascii", 3, INT_WHY)
deep("ft_isascii", 5,
     "ASCII = les 128 premiers codes (0 à 127). Comme `c` est un `int`, il peut valoir 200, 1000 ou -5 : il faut donc **deux** bornes. "
     "`c >= 0` élimine les négatifs, `c <= 127` élimine tout ce qui dépasse.",
     "Les codes 128 à 255 existent (ce sont des octets valides, par exemple les lettres accentuées en Latin-1) mais ne font pas partie de l'ASCII.")
deep("ft_isascii", 6, RET_WHY)

deep("ft_isprint", 3, INT_WHY)
deep("ft_isprint", 5,
     "Imprimable = qui laisse une trace visible à l'écran, **espace compris**. L'espace est le code 32, `'~'` est le code 126.",
     "Avant 32 : caractères de contrôle (0 = nul, 9 = tabulation, 10 = retour à la ligne…). Après 126 : le code 127 (DEL) qui ne s'affiche pas.")
deep("ft_isprint", 6, RET_WHY)

# ---------------------------------------------------------------- toupper / tolower
deep("ft_toupper", 3,
     "Elle renvoie un `int` (pas un `char`) pour la même raison que `is*` : compatibilité avec la vraie libc, qui accepte aussi `EOF`.")
deep("ft_toupper", 5,
     "Le test est indispensable : retirer 32 à un caractère qui n'est pas une minuscule le casserait (par exemple `'A' - 32` = 33, soit `'!'`).")
deep("ft_toupper", 6,
     "Pourquoi 32 ? En binaire, `'A'` = 0100 0001 (65) et `'a'` = 0110 0001 (97) : la seule différence est le bit de valeur 32. "
     "Écrire `c - 32` ou `c - ('a' - 'A')` donne le même résultat ; la deuxième forme explique d'où vient le 32.")
deep("ft_tolower", 5,
     "Même principe que `ft_toupper`, dans l'autre sens : on ne touche qu'aux **majuscules** (65 à 90), tout le reste revient tel quel.")
deep("ft_tolower", 6,
     "`'A'` (65) + 32 = `'a'` (97). C'est le même écart de 32 que pour `ft_toupper`, parcouru à l'envers.")

# ---------------------------------------------------------------- strlen
deep("ft_strlen", 3,
     "`const char *s` : le `const` s'applique aux **caractères pointés** : il promet « je ne modifierai pas la chaîne ». "
     "Le compilateur refusera donc toute écriture du genre `s[0] = 'x'` dans la fonction. Ça permet aussi de lui passer un littéral (`\"abc\"`) sans warning.",
     "`size_t` est le type fait pour représenter une **taille** ou un nombre d'éléments : non signé (une longueur n'est jamais négative) "
     "et assez grand pour toute zone mémoire (64 bits sur un PC actuel). Un `int` serait limité à environ 2 milliards.")
deep("ft_strlen", 5,
     "On déclare `i` en `size_t` car c'est la valeur qu'on va renvoyer : même type, pas de conversion, pas de warning de signe.")
deep("ft_strlen", 8,
     "Une chaîne C est une suite d'octets terminée par un octet **nul** (`'\\0'`, de valeur 0). Elle ne connaît pas sa longueur : "
     "il faut la parcourir jusqu'au `'\\0'`.",
     "`s[i]` veut dire `*(s + i)` : on part de l'adresse `s` et on avance de `i` caractères. Comme un `char` fait 1 octet, avancer de `i` caractères = avancer de `i` octets. "
     "`while (s[i])` est la forme courte de `while (s[i] != '\\0')` : un caractère nul vaut 0, donc « faux », et la boucle s'arrête.")
deep("ft_strlen", 10,
     "On ne compte pas le `'\\0'` : `i` s'est arrêté dessus, donc `i` est exactement le nombre de caractères **avant** lui.")

# ---------------------------------------------------------------- memset / bzero
deep("ft_memset", 3,
     "`void *` = « adresse de quelque chose, sans dire de quoi ». C'est voulu : `memset` doit marcher sur un tableau de `char`, d'`int`, "
     "sur une structure… Elle ne regarde que des octets.",
     "`int c` : héritage historique de la libc. On n'utilisera que l'**octet de poids faible** de cette valeur (voir plus bas).")
deep("ft_memset", 5,
     "**Pourquoi un `unsigned char *` ?** Avec un `void *`, on ne peut ni écrire `s[i]` ni `*s` : le compilateur ne sait pas quelle taille a « un élément », "
     "donc de combien avancer. Il faut choisir un type dont l'élément fait **exactement 1 octet** pour avancer octet par octet.",
     "`unsigned char` est parfait pour ça : sa taille est 1 octet par définition en C, et il est **non signé** (valeurs 0 à 255, "
     "pas de surprise avec un octet comme `0xFF` qui deviendrait -1 en `char` signé).",
     "`i` est un `size_t` parce que `n` en est un : comparer un `int` à un `size_t` (`i < n`) déclenche un warning de signe, "
     "qui devient une erreur avec `-Wextra -Werror`.")
deep("ft_memset", 8,
     "**C'est la ligne que tout le monde se demande.** `s` est un `void *` : le compilateur voit une adresse mais ne sait pas lire ce qu'il y a derrière. "
     "Le cast `(unsigned char *)s` ne change **ni l'adresse, ni la mémoire** : il change seulement la façon dont le compilateur la regarde, "
     "comme si on mettait des lunettes « chaque case = 1 octet ».",
     "Exemple avec la zone d'un tableau `int tab[2]` (2 × 4 octets) :\n"
     "vue en int * :           tab[0]        tab[1]\n"
     "                       [ 4 octets ]  [ 4 octets ]\n"
     "vue en unsigned char * : [0][1][2][3]  [4][5][6][7]  <- ptr[i] = 1 octet à chaque pas",
     "Honnêteté : en C, un `void *` se convertit tout seul en `unsigned char *`, donc ce cast est ici facultatif. On l'écrit pour montrer l'intention. "
     "Il devient **obligatoire** quand on enlève un `const` (par exemple de `const void *` vers `unsigned char *`).")
deep("ft_memset", 9,
     "`i` compte le nombre d'octets **déjà écrits**. On l'utilise comme indice : `ptr[i]` est l'octet numéro `i` de la zone. "
     "On initialise à 0 sur une ligne séparée car la norme interdit `size_t i = 0;`.")
deep("ft_memset", 10,
     "`while (i < n)` : on écrit exactement `n` octets, de l'indice 0 à `n - 1`. Avec `<=` on écrirait un octet de trop (débordement de zone).",
     "`(unsigned char)c` : `c` est un `int` (souvent 4 octets) mais on n'écrit qu'**un octet**. Le cast garde les 8 bits de poids faible : "
     "`c = 256` donne 0, `c = 0x141` donne `0x41` (`'A'`). C'est le comportement de la vraie `memset`.",
     "Piège classique : `memset` remplit **octet par octet**. `memset(tab_int, 1, sizeof(tab_int))` ne met pas des `1` dans le tableau mais des `0x01010101` "
     "(16 843 009) dans chaque `int`. Elle ne sert vraiment qu'à mettre à 0 ou à remplir des `char`.")
deep("ft_memset", 15,
     "Le prototype promet de renvoyer la zone d'origine, pour pouvoir enchaîner les appels (`ft_memset(buf, 0, n)` utilisable comme une valeur). "
     "`ptr` pointe sur la même adresse mais a un autre type : on renvoie `s`, tel qu'on l'a reçu.")

deep("ft_bzero", 3,
     "`void` : aucun retour. C'est la différence avec `memset` : `bzero` est une fonction ancienne (BSD) qui ne renvoie rien.")
deep("ft_bzero", 5,
     "Exactement la même logique que `ft_memset` : `void *` n'est pas indexable, on passe par un `unsigned char *` (1 octet par élément). "
     "Voir le cours `ft_memset` pour le détail du cast.")
deep("ft_bzero", 8,
     "Le cast `(unsigned char *)s` n'envoie aucune donnée : il dit juste au compilateur de lire la zone `s` comme une suite d'octets, pour pouvoir écrire `ptr[i]`.")
deep("ft_bzero", 10,
     "Ici on écrit **la valeur 0** (octet de valeur nulle), pas le caractère `'0'` (code 48). Mettre une zone à 0 est très courant : "
     "ça met des pointeurs à `NULL`, des nombres à 0 et des chaînes à « vide ». C'est ce que `ft_calloc` utilise.")

# ---------------------------------------------------------------- memcpy
deep("ft_memcpy", 3,
     "Les deux `void *` permettent de copier n'importe quel type de données. `const void *src` : la source est **en lecture seule**, "
     "la fonction promet de ne pas la modifier. Le retour (`dest`) permet d'écrire `ft_memcpy(a, b, n)` comme une valeur.")
deep("ft_memcpy", 5,
     "`unsigned char *d` : pointeur pour **écrire** octet par octet. `const unsigned char *s` : pointeur pour **lire**, avec `const` pour garder la promesse faite par le prototype. "
     "Dans `const unsigned char *s`, le `const` porte sur l'octet pointé (on ne peut pas faire `s[i] = ...`), mais le pointeur `s` lui-même peut changer.",
     "Les noms `d` et `s` ne sont pas ceux des paramètres (`dest`, `src`) : on garde les paramètres intacts pour renvoyer `dest` à la fin.")
deep("ft_memcpy", 9,
     "Si `dest` **et** `src` sont `NULL`, il n'y a rien à copier : on renvoie `NULL` plutôt que de planter. "
     "La vraie `memcpy` ne protège pas (comportement indéfini). Si un seul des deux est `NULL` et que `n > 0`, ça plantera comme la vraie.")
deep("ft_memcpy", 11,
     "Les casts sont obligatoires pour `s` : on passe de `const void *` à `const unsigned char *` en **gardant** le `const`. "
     "Pour `d`, on passe de `void *` à `unsigned char *`. Dans les deux cas, la mémoire n'est pas touchée : seul le « type de lecture » change.")
deep("ft_memcpy", 14,
     "La boucle copie un octet à la fois, de gauche à droite : `d[i] = s[i]` pour `i` de 0 à `n - 1`. La vraie `memcpy` copie par blocs de 8 octets pour aller vite ; "
     "ici, la version octet par octet est plus simple et suffit.",
     "Pourquoi les zones ne doivent pas se chevaucher ? Si `d` est juste après `s` dans la même zone, en copiant de gauche à droite on **écrase des octets "
     "source avant de les avoir lus**. Exemple avec `memcpy(buf + 1, buf, 3)` sur `\"abcd\"` :\n"
     "i=0 : buf[1] = buf[0] = 'a'  -> \"aacd\"\n"
     "i=1 : buf[2] = buf[1] = 'a'  -> \"aaad\"  (on recopie le 'a' qu'on vient d'écrire, pas le 'b' d'origine)\n"
     "i=2 : buf[3] = buf[2] = 'a'  -> \"aaaa\"",
     "C'est exactement le problème que résout `ft_memmove`.")
deep("ft_memcpy", 19,
     "On renvoie `dest` (le pointeur reçu), pas `d` : ils pointent sur la même adresse, mais `dest` a le type `void *` que le prototype promet.")

# ---------------------------------------------------------------- memmove
deep("ft_memmove", 3,
     "`static` devant une fonction signifie : « cette fonction n'est visible que dans ce fichier ». Aucun autre `.c` ne peut l'appeler, "
     "et elle n'entre pas en conflit avec un autre nom. C'est le bon outil pour une fonction d'aide.",
     "Pourquoi une aide ? La norme limite une fonction à **25 lignes**. En séparant la copie (qui a deux sens) de la fonction principale (cast + vérification), tout reste sous la limite.")
deep("ft_memmove", 5, "Un seul compteur `size_t`, du même type que `n`.")
deep("ft_memmove", 7,
     "`d < s` compare deux **adresses** : « la destination est-elle avant la source en mémoire ? ». Le sens de copie en dépend, pour ne jamais écraser un octet pas encore lu.",
     "Cas 1 : destination **avant** la source (`d < s`). On copie de gauche à droite : chaque octet source est lu avant que la zone d'écriture l'atteigne.\n"
     "src :  . a b c d .\n"
     "dst :  a b c d . .    (d = s - 1) : on lit s[0], on l'écrit en d[0], etc. -> OK")
deep("ft_memmove", 16,
     "Cas 2 : destination **après** la source (`d > s`). Si on copiait de gauche à droite, on écraserait la fin de la source avant de la lire. On copie donc de **droite à gauche**.\n"
     "src :  a b c d . .\n"
     "dst :  . . a b c d    (d = s + 2) : on commence par le dernier octet -> OK",
     "Piège du `size_t` : un `size_t` ne peut pas être négatif. Une boucle `i = n - 1; while (i >= 0)` ne se termine **jamais** (quand `i` vaut 0 et qu'on fait `i--`, il repasse au plus grand nombre possible). "
     "Voilà pourquoi on part de `i = n`, on teste `i > 0`, et on fait `i--` **avant** de copier : `i` prend les valeurs `n - 1, ..., 0` puis la boucle s'arrête quand `i` vaut 0.")
deep("ft_memmove", 27, "Même signature que `ft_memcpy` : `const void *src` parce qu'on ne modifie pas la source.")
deep("ft_memmove", 29,
     "Mêmes pointeurs d'octets que pour `ft_memcpy`. Le `const` de `s` est conservé : la fonction ne modifie jamais la source.")
deep("ft_memmove", 32,
     "`!dest && !src` est la forme courte de `dest == NULL && src == NULL`. Le `!` veut dire « n'est pas » : un pointeur `NULL` vaut 0, donc `!p` est vrai si `p` est `NULL`.")
deep("ft_memmove", 34,
     "On convertit puis on délègue le vrai travail à l'aide `ft_do_memmove`. Les casts ne changent rien en mémoire : ils indiquent « lis ces zones octet par octet ».")
deep("ft_memmove", 37, "On renvoie `dest` : le prototype promet l'adresse de départ de la destination.")

# ---------------------------------------------------------------- strlcpy
deep("ft_strlcpy", 3,
     "Pourquoi `strlcpy` existe : `strncpy` ne garantit pas le `'\\0'` final et écrit des zéros inutiles. `strlcpy` **termine toujours** la chaîne (si `size > 0`) et ne déborde jamais.",
     "`size` = la taille **totale du buffer** de destination, `'\\0'` compris (pas le nombre de caractères à copier).")
deep("ft_strlcpy", 5, "`i` est un `size_t` car on le compare à `size - 1` qui en est un.")
deep("ft_strlcpy", 8,
     "Pourquoi traiter `size == 0` à part ? Plus bas on écrit `size - 1`. Avec `size = 0`, `size - 1` ne vaut pas -1 mais **le plus grand `size_t` possible** "
     "(le nombre est non signé : il « boucle »). La boucle croirait avoir des milliards de cases libres et écrirait n'importe où. "
     "Avec `size == 0`, il n'y a de toute façon pas la place pour un `'\\0'` : on n'écrit rien.")
deep("ft_strlcpy", 10,
     "Deux conditions : `src[i] != '\\0'` (il reste des caractères à copier) **et** `i < size - 1` (il reste de la place, avec une case gardée pour le `'\\0'`). "
     "Dès que l'une est fausse, on s'arrête.",
     "L'ordre est sûr : on ne lit `src[i]` que tant que `i` est valide pour `src`, et on n'écrit `dest[i]` que si `i < size - 1`, donc dans le buffer.")
deep("ft_strlcpy", 15,
     "Après la boucle, `i` est soit la longueur de `src` (tout copié), soit `size - 1` (tronqué). Dans les deux cas, `dest[i]` est dans le buffer (car `size >= 1`) : "
     "on y pose le `'\\0'`. La chaîne est donc **toujours terminée**.")
deep("ft_strlcpy", 16,
     "On renvoie la longueur de `src` (pas ce qu'on a copié) : c'est la taille que la copie « aurait voulu » avoir. "
     "L'appelant détecte la troncature avec `if (ft_strlcpy(dst, src, size) >= size)`.")

# ---------------------------------------------------------------- strlcat
deep("ft_strlcat", 3,
     "`size` = la taille **totale** du buffer de `dest` (pas la place restante). Comme `strlcpy`, `strlcat` garantit un `'\\0'` final si le buffer est assez grand pour contenir `dest`.")
deep("ft_strlcat", 5, "`dest_len` : longueur actuelle de `dest` ; `src_len` : celle de `src` ; `i` : l'indice dans `src`. Trois `size_t` car ce sont des tailles.")
deep("ft_strlcat", 9,
     "On ne peut pas faire `ft_strlen(dest)` : si `dest` n'est pas terminé dans ses `size` octets, `strlen` lirait au-delà du buffer. "
     "On mesure donc à la main en ajoutant `dest_len < size` **avant** de lire `dest[dest_len]`. Grâce au court-circuit de `&&`, "
     "si `dest_len` atteint `size`, on ne lit pas `dest[size]` (hors du buffer).")
deep("ft_strlcat", 12, "On a besoin de `src_len` pour la valeur de retour, même quand on ne copie rien.")
deep("ft_strlcat", 13,
     "Si `size <= dest_len`, `dest` remplit déjà tout le buffer (ou plus) : aucune place pour ajouter quoi que ce soit, même pas un `'\\0'`. "
     "On ne touche à rien et on renvoie `size + src_len` : la longueur qu'aurait le résultat si le buffer avait été assez grand.")
deep("ft_strlcat", 15,
     "`i` repart de 0 dans `src`. L'écriture se fait en `dest[dest_len + i]` : on écrit **à la suite** de `dest`.",
     "Condition `dest_len + i < size - 1` : la position d'écriture doit rester avant la dernière case (réservée au `'\\0'`). "
     "Ici `size - 1` est sûr, car on a vérifié plus haut que `size > dest_len >= 0`, donc `size >= 1` : pas de « boucle » du `size_t` vers le plus grand nombre.")
deep("ft_strlcat", 21,
     "`dest_len + i` est la première case libre après ce qu'on a copié. On y pose le `'\\0'`. Cette case est toujours dans le buffer.")
deep("ft_strlcat", 22,
     "Retour = `dest_len + src_len` : la longueur du résultat **idéal**. Si cette valeur est `>= size`, la concaténation a été tronquée.")

# ---------------------------------------------------------------- strchr / strrchr
deep("ft_strchr", 3,
     "Le paramètre est `const char *` (on ne modifie pas la chaîne) mais on renvoie un `char *` : c'est un « trou » connu de la vraie libc. "
     "On renvoie un pointeur **dans** la chaîne d'origine, pas une copie : `ft_strchr(s, 'l') - s` donne l'indice du caractère trouvé.",
     "`int c` comme dans la vraie libc, mais c'est bien un caractère : on le convertit en `char` avant de comparer.")
deep("ft_strchr", 5,
     "`while (*s)` : `*s` est le caractère pointé par `s`. La boucle tourne tant que ce n'est pas `'\\0'`. "
     "On avance `s` lui-même (`s++`, plus bas) : `s` est une copie locale du pointeur, l'appelant ne voit pas la différence.",
     "`(char)c` : `c` est un `int`, `*s` un `char`. La norme dit que la fonction cherche `c` converti en `char`. "
     "Sans ce cast, un `c` comme 321 (= 'A' + 256) ne serait jamais égal à un `char`, alors que la vraie fonction le trouverait.")
deep("ft_strchr", 9,
     "`s++` avance le pointeur d'une case (1 octet pour un `char`). On passe au caractère suivant.")
deep("ft_strchr", 11,
     "On sort de la boucle quand `*s == '\\0'`, donc `s` pointe sur le `'\\0'` final. Cette boucle ne teste jamais ce caractère : "
     "il faut donc traiter à part le cas où on cherche `'\\0'`. La vraie `strchr(\"abc\", '\\0')` renvoie bien un pointeur sur le `'\\0'`.")
deep("ft_strchr", 13, "Aucune correspondance : `NULL`. Ne pas confondre avec le cas `'\\0'` ci-dessus, qui renvoie un vrai pointeur.")

deep("ft_strrchr", 3, "Même prototype que `ft_strchr` : `const char *` en entrée, `char *` en sortie (pointeur dans la chaîne d'origine).")
deep("ft_strrchr", 5,
     "`last_occurrence` garde en mémoire la **dernière** adresse où on a vu `c`. Le `const` porte sur les caractères pointés : on ne les modifie jamais.")
deep("ft_strrchr", 7, "`NULL` au départ : tant qu'on n'a rien trouvé, c'est la réponse correcte.")
deep("ft_strrchr", 8,
     "Différence avec `ft_strchr` : on ne s'arrête **pas** à la première occurrence. On parcourt toute la chaîne et on écrase `last_occurrence` à chaque fois "
     "qu'on retrouve `c`. À la fin, elle contient la dernière.",
     "(On pourrait aussi partir de la fin avec `ft_strlen`, mais la version « on mémorise » est plus simple et n'a pas de problème de `size_t`.)")
deep("ft_strrchr", 14,
     "Comme pour `ft_strchr`, la boucle ne regarde pas le `'\\0'` final. Si on cherche `'\\0'`, la dernière occurrence est ce `'\\0'` (et c'est aussi la seule) : "
     "`s` y pointe après la boucle.")
deep("ft_strrchr", 16,
     "On renvoie la dernière position mémorisée, ou `NULL` si on n'a jamais trouvé `c`. Le cast `(char *)` retire le `const` pour correspondre au prototype.")

# ---------------------------------------------------------------- strncmp / memchr / memcmp
deep("ft_strncmp", 3,
     "Valeur de retour : **0** si les chaînes sont égales sur `n` caractères, **négative** si `s1` vient avant `s2`, **positive** sinon. "
     "Seul le **signe** compte pour l'appelant ; la valeur exacte (la différence de deux caractères) n'est qu'un détail.")
deep("ft_strncmp", 5, "`i` est un `size_t` car on le compare à `n`.")
deep("ft_strncmp", 8,
     "Trois conditions combinées : `i < n` (limite), et `s1[i] || s2[i]` (« au moins une des deux chaînes n'est pas finie »). "
     "On s'arrête dès que **les deux** sont finies (`'\\0'`).",
     "Si une seule chaîne est finie, par exemple `\"ab\"` contre `\"abc\"`, on entre dans la boucle à `i = 2` : `'\\0'` contre `'c'` sont différents, et la ligne suivante renvoie la différence (négative).")
deep("ft_strncmp", 10,
     "**Pourquoi `unsigned char` ?** Un `char` peut être signé : les octets 128 à 255 (lettres accentuées en UTF-8, par exemple) deviendraient négatifs et se classeraient **avant** les lettres ASCII. "
     "La vraie `strncmp` compare comme des `unsigned char` (0 à 255). On caste donc chaque caractère avant de comparer et de soustraire.",
     "La soustraction se fait en `int` : les `unsigned char` sont d'abord convertis en `int` (promotion), donc `3 - 5` donne bien `-2` et pas 254.")
deep("ft_strncmp", 12, "Caractères identiques : on regarde le suivant.")
deep("ft_strncmp", 14,
     "On arrive ici si on a épuisé `n` caractères ou si les deux chaînes se sont terminées au même endroit sans différence : **0**. Avec `n = 0`, on arrive ici tout de suite.")

deep("ft_memchr", 3,
     "`const void *s` : zone en lecture seule, de type quelconque. On renvoie un `void *` car le résultat peut pointer dans n'importe quelle donnée.")
deep("ft_memchr", 5,
     "`ptr` est le pointeur de lecture : `const unsigned char *` pour lire des octets (0 à 255) sans pouvoir les modifier. `ch` est l'octet cherché.")
deep("ft_memchr", 8,
     "`c` est un `int`. On le convertit **une fois** en `unsigned char` : seul son octet de poids faible est cherché, comme dans la vraie `memchr`. "
     "On évite ainsi de refaire la conversion à chaque tour de boucle.")
deep("ft_memchr", 9, "On regarde la zone `s` comme une suite d'octets en lecture seule.")
deep("ft_memchr", 10,
     "`while (n--)` : le test utilise la valeur de `n` **avant** de la décrémenter. Si `n` vaut 3, la condition est vraie 3 fois (3, 2, 1) puis fausse (0). "
     "C'est donc une boucle qui tourne exactement `n` fois. Avec `n = 0`, elle ne tourne pas.",
     "`*ptr == ch` : `*ptr` est l'octet pointé par `ptr`. `ptr++` avance d'un octet. Contrairement à `ft_strchr`, on ne s'arrête **jamais** au `'\\0'` : seul `n` compte.",
     "Le cast `(void *)ptr` retire le `const` : le prototype renvoie un `void *` non `const`.")
deep("ft_memchr", 16, "Aucun des `n` octets ne correspond : `NULL`.")

deep("ft_memcmp", 3,
     "Comme `ft_strncmp`, mais sur des **octets bruts** (pas de `'\\0'` spécial). Valeur de retour : 0, négative ou positive.")
deep("ft_memcmp", 5,
     "Deux pointeurs `const unsigned char *`. `unsigned` est essentiel : avec des `char` signés, l'octet `0xFF` vaudrait -1 et un octet `0x80` serait « plus petit » que `0x7F`, "
     "ce qui est faux pour un `memcmp`.")
deep("ft_memcmp", 9, "On convertit les deux zones en `const unsigned char *` (on garde le `const`), puis `i` à 0.")
deep("ft_memcmp", 12,
     "Si deux octets diffèrent, on renvoie leur différence. Les `unsigned char` sont promus en `int` avant la soustraction : `3 - 5 = -2` (et pas 254). "
     "La boucle ne s'arrête pas au `'\\0'` : `memcmp` compare toujours `n` octets, sauf différence trouvée avant.")
deep("ft_memcmp", 18, "Les `n` octets sont tous égaux : **0**. Avec `n = 0`, c'est le résultat immédiat.")

# ---------------------------------------------------------------- strnstr
deep("ft_strnstr", 3,
     "Vocabulaire : `haystack` (botte de foin) = où on cherche ; `needle` (aiguille) = ce qu'on cherche ; `len` = on ne regarde que les `len` premiers caractères de `haystack`. "
     "Retour : un pointeur dans `haystack` (pas une copie) ou `NULL`.")
deep("ft_strnstr", 5, "`i` : position de départ de la tentative dans `haystack`. `j` : combien de caractères de `needle` ont déjà correspondu à cette position.")
deep("ft_strnstr", 8,
     "Une aiguille vide est « trouvée » au tout début : `strstr(\"abc\", \"\")` renvoie `\"abc\"`. Il faut le gérer avant la boucle, sinon on ne renverrait jamais rien. "
     "`*needle == '\\0'` est le premier caractère de `needle`.")
deep("ft_strnstr", 10, "On teste chaque position de départ possible, de gauche à droite.")
deep("ft_strnstr", 11,
     "`haystack[i] && i < len` : tant qu'on n'est ni à la fin de `haystack` ni au-delà de `len`. On teste `haystack[i]` en premier : `haystack[i]` doit être valide avant d'être lu.")
deep("ft_strnstr", 13, "Chaque nouvelle tentative recommence au début de `needle` (`j = 0`).")
deep("ft_strnstr", 14,
     "Boucle interne : on compare `haystack[i + j]` et `needle[j]` tant qu'ils sont égaux. Les conditions sont dans un ordre utile : "
     "`haystack[i + j]` et `needle[j]` non nuls (on ne dépasse pas les chaînes), puis égalité, puis `(i + j) < len` (on ne regarde jamais au-delà de `len`).",
     "La condition `(i + j) < len` est la clé : sans elle, `ft_strnstr(\"hello\", \"llo\", 4)` trouverait `llo` alors que le dernier `o` est à l'indice 4, donc hors des 4 premiers caractères.")
deep("ft_strnstr", 17,
     "Pourquoi tester `needle[j] == '\\0'` ? La boucle interne s'arrête soit sur une différence, soit parce qu'elle a fini `needle`. Si `needle[j]` est `'\\0'`, "
     "tous les caractères de `needle` ont correspondu : c'est trouvé.",
     "`haystack + i` est de l'**arithmétique de pointeurs** : l'adresse de `haystack`, avancée de `i` caractères. C'est le pointeur sur le début de la correspondance. "
     "Le cast `(char *)` retire le `const`.")
deep("ft_strnstr", 19, "Pas de correspondance à cette position : on essaie la suivante.")
deep("ft_strnstr", 21, "Toutes les positions sont essayées sans succès : `NULL`.")

# ---------------------------------------------------------------- atoi
deep("ft_atoi", 3, "`const char *str` : la chaîne est lue seulement. Le retour est un `int` ; si le nombre ne tient pas dans un `int`, le comportement n'est pas défini (comme la vraie `atoi`).")
deep("ft_atoi", 5,
     "Trois variables : `i` (indice), `sign` (+1 ou -1), `result` (le nombre qu'on construit). On sépare le signe du résultat pour l'appliquer **à la fin**.")
deep("ft_atoi", 9,
     "Les trois sont initialisées sur des lignes séparées : la norme interdit l'initialisation dans la déclaration (`int i = 0;`).")
deep("ft_atoi", 12,
     "Les « espaces blancs » acceptés par `atoi` sont : l'espace (code 32) et les codes 9 à 13 : tabulation `\\t` (9), `\\n` (10), `\\v` (11), `\\f` (12), `\\r` (13). "
     "On les saute tant qu'on en trouve. La boucle s'arrête au premier caractère qui n'en est pas un.")
deep("ft_atoi", 14,
     "Un seul signe est accepté. S'il y a `'-'`, `sign` devient -1 ; pour `'+'`, `sign` reste à 1. Dans les deux cas, `i++` passe au caractère suivant le signe. "
     "Ainsi `\"+-5\"` donne 0 : après `'+'`, le `'-'` n'est pas un chiffre.")
deep("ft_atoi", 20,
     "**Comment on construit un nombre chiffre par chiffre.** Pour `\"42\"` : on part de 0. Pour `'4'` : `0 * 10 + 4 = 4`. Pour `'2'` : `4 * 10 + 2 = 42`. "
     "Multiplier par 10 « décale » les chiffres déjà lus d'un cran vers la gauche.",
     "`str[i] - '0'` transforme un **caractère** en **chiffre**. `'4'` vaut 52 dans la table ASCII, `'0'` vaut 48 : `52 - 48 = 4`. "
     "Ça marche car les chiffres se suivent dans la table (voir `ft_isdigit`).")
deep("ft_atoi", 25,
     "On applique le signe en une fois, à la fin. Un nombre négatif est construit en positif puis multiplié par -1. "
     "(Limite : `-2147483648` n'est pas représentable en positif dans un `int` ; c'est un cas à comportement indéfini que `atoi` ne traite pas.)")

# ---------------------------------------------------------------- calloc / strdup
deep("ft_calloc", 3,
     "`calloc(count, size)` = « `count` éléments de `size` octets chacun, **tous mis à zéro** ». C'est `malloc` + remise à zéro, avec une protection en plus.")
deep("ft_calloc", 5, "`void *` : on ne sait pas encore ce qu'on va stocker dedans ; l'appelant le convertira (en C, automatiquement).")
deep("ft_calloc", 7,
     "**Pourquoi cette protection ?** `count * size` est un produit de deux `size_t` : si le résultat dépasse le maximum d'un `size_t`, "
     "il « boucle » et donne une valeur toute petite. Par exemple avec des `size_t` de 64 bits : `(2^63) * 2` = 0. `malloc(0)` réussirait, "
     "et le programme croirait avoir une zone énorme : écriture hors zone assurée.",
     "Pour tester sans déborder, on **divise** au lieu de multiplier : « `size` est trop grand si `size > SIZE_MAX / count` ». Une division ne déborde pas. "
     "`SIZE_MAX` est la plus grande valeur d'un `size_t` (défini dans `<stdint.h>`, inclus par `libft.h`).",
     "`count != 0` d'abord : on ne divise jamais par zéro (le `&&` court-circuite).")
deep("ft_calloc", 9,
     "On alloue `count * size` octets. On sait que le produit ne déborde pas. Si `count` ou `size` vaut 0, `malloc(0)` renvoie sur la plupart des systèmes un pointeur valide : "
     "le sujet v19.3 demande justement un pointeur non `NULL` dans ce cas.")
deep("ft_calloc", 10,
     "`malloc` renvoie `NULL` quand il n'y a plus de mémoire. Il faut **toujours** tester : écrire dans un pointeur `NULL` fait planter le programme. On renvoie `NULL` à l'appelant, qui doit le gérer à son tour.")
deep("ft_calloc", 12,
     "`malloc` ne remet rien à zéro : la mémoire contient des valeurs quelconques. `ft_bzero` met les `count * size` octets à 0 : c'est la seule différence avec `malloc`.")
deep("ft_calloc", 13, "On renvoie la zone. C'est à l'appelant de la libérer avec `free`.")

deep("ft_strdup", 3,
     "`strdup` = « string duplicate » : une copie indépendante d'une chaîne, dans de la mémoire allouée par `malloc`. L'appelant doit la libérer (`free`).")
deep("ft_strdup", 5, "`dest` : la copie ; `len` : la longueur de la source.")
deep("ft_strdup", 8, "On mesure la source une fois, pour réserver la bonne taille et pour copier.")
deep("ft_strdup", 9,
     "`len + 1` : les `len` caractères **plus un octet pour le `'\\0'`**. Oublier ce `+ 1` est l'erreur classique : le `'\\0'` serait écrit un octet **après** la fin de la zone.")
deep("ft_strdup", 10, "Toujours tester `malloc`. En cas d'échec on renvoie `NULL` au lieu de copier dans une zone inexistante.")
deep("ft_strdup", 12,
     "On copie `len + 1` octets : les caractères **et** le `'\\0'` en une seule fois, avec `ft_memcpy`. Pas besoin de boucle ni de poser le `'\\0'` à la main.")
deep("ft_strdup", 13, "On renvoie la copie. Modifier la copie ne touche pas l'original.")

# ---------------------------------------------------------------- complements (lignes courtes)
_ELSE0 = "Sinon : exactement **0**. Il n'y a pas besoin de tester la condition inverse : si on arrive au `else`, la condition du `if` était fausse."
deep("ft_isalpha", 7, _ELSE0)
deep("ft_isdigit", 7, _ELSE0)
deep("ft_isalnum", 6, "Si `ft_isalpha(c)` **ou** `ft_isdigit(c)` renvoie une valeur non nulle, la condition est vraie : on renvoie exactement **1**.")
deep("ft_isalnum", 7, _ELSE0)
deep("ft_isascii", 7, _ELSE0)
deep("ft_isprint", 7, _ELSE0)
deep("ft_toupper", 7, "Tout ce qui n'est pas une minuscule (majuscule, chiffre, espace, accent…) est renvoyé **sans changement** : c'est ce que fait la vraie `toupper`.")
deep("ft_tolower", 3, "Même prototype que `ft_toupper` : un `int` en entrée et en sortie, pour accepter aussi `EOF` (-1) comme la vraie libc.")
deep("ft_tolower", 7, "Tout ce qui n'est pas une majuscule est renvoyé **sans changement**.")
deep("ft_strlen", 7,
     "On part de l'indice 0 : le premier caractère. On l'écrit sur une ligne à part car la norme interdit `size_t i = 0;` dans la déclaration.")
deep("ft_memcpy", 13, "`i` compte les octets déjà copiés. Initialisation séparée de la déclaration (règle de la norme).")
deep("ft_strlcpy", 7, "Initialisation de `i` séparée de la déclaration (règle de la norme).")
deep("ft_strncmp", 7, "Initialisation de `i` séparée de la déclaration (règle de la norme).")
