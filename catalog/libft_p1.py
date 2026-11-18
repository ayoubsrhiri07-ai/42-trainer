"""Libft, partie 1 : fonctions de la libc a recoder."""
from ._util import ex

EXERCISES = []
add = EXERCISES.append

# ---------------------------------------------------------------- niveau 1
add(ex("int ft_isalpha(int c)", 1,
       "Teste si le caractere est une lettre.",
       ["Renvoie exactement 1 si `c` est une lettre (A-Z ou a-z), sinon exactement 0 (le sujet v19.3 impose 1 ou 0, pas une autre valeur).",
        "Le parametre est un `int`, comme dans la vraie libc."],
       [("ft_isalpha('a')", "1"), ("ft_isalpha('5')", "0")],
       r'''
void run(void)
{
	int c, good, bad;

	good = 1; bad = 1;
	for (c = 0; c < 256; c++)
	{
		int exp = (c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z');
		if (ft_isalpha(c) != exp)
		{
			if (exp) good = 0; else bad = 0;
		}
	}
	CHECK("toutes les lettres A-Z et a-z sont reconnues", good);
	CHECK("chiffres, ponctuation et caracteres >= 128 donnent 0", bad);
	CHECK("bornes : '@' et '[' valent 0", !ft_isalpha('@') && !ft_isalpha('['));
	CHECK("bornes : '`' et '{' valent 0", !ft_isalpha('`') && !ft_isalpha('{'));
}
''',
       hints=["Dans la table ASCII, les majuscules sont contigues, les minuscules aussi.",
              "Compare `c` avec 'A' et 'Z', puis avec 'a' et 'z'.",
              "`if ((c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z')) return (1);`"]))

add(ex("int ft_isdigit(int c)", 1,
       "Teste si le caractere est un chiffre.",
       ["Renvoie exactement 1 si `c` est un chiffre ('0' a '9'), sinon exactement 0 (le sujet v19.3 impose 1 ou 0, pas une autre valeur)."],
       [("ft_isdigit('7')", "1"), ("ft_isdigit('a')", "0")],
       r'''
void run(void)
{
	int c, good, bad;

	good = 1; bad = 1;
	for (c = 0; c < 256; c++)
	{
		int exp = (c >= '0' && c <= '9');
		if (ft_isdigit(c) != exp)
		{
			if (exp) good = 0; else bad = 0;
		}
	}
	CHECK("'0' a '9' sont reconnus", good);
	CHECK("tout le reste donne 0", bad);
	CHECK("bornes : '/' et ':' valent 0", !ft_isdigit('/') && !ft_isdigit(':'));
}
''',
       hints=["Les chiffres sont contigus dans la table ASCII.", "Compare avec '0' et '9'.",
              "`return (c >= '0' && c <= '9');` (attention a la norme : un `if`, pas de `?:`)."]))

add(ex("int ft_isalnum(int c)", 1,
       "Teste si le caractere est alphanumerique.",
       ["Renvoie exactement 1 si `c` est une lettre ou un chiffre, sinon exactement 0 (le sujet v19.3 impose 1 ou 0, pas une autre valeur).",
        "Tu as le droit de reutiliser `ft_isalpha` et `ft_isdigit`."],
       [("ft_isalnum('a')", "1"), ("ft_isalnum('_')", "0")],
       r'''
void run(void)
{
	int c, good, bad;

	good = 1; bad = 1;
	for (c = 0; c < 256; c++)
	{
		int exp = (c >= '0' && c <= '9') || (c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z');
		if (ft_isalnum(c) != exp)
		{
			if (exp) good = 0; else bad = 0;
		}
	}
	CHECK("lettres et chiffres reconnus", good);
	CHECK("tout le reste donne 0 ('_', espace, >= 128...)", bad);
}
''',
       hints=["Un caractere alphanumerique est une lettre OU un chiffre.",
              "Reutilise tes fonctions precedentes.", "`if (ft_isalpha(c) || ft_isdigit(c)) return (1);`"]))

add(ex("int ft_isascii(int c)", 1,
       "Teste si le caractere est dans la table ASCII.",
       ["Renvoie exactement 1 si `c` est entre 0 et 127 inclus, sinon exactement 0 (le sujet v19.3 impose 1 ou 0, pas une autre valeur)."],
       [("ft_isascii(65)", "1"), ("ft_isascii(128)", "0")],
       r'''
void run(void)
{
	int c, good, bad;

	good = 1; bad = 1;
	for (c = 0; c < 256; c++)
	{
		int exp = (c <= 127);
		if (ft_isascii(c) != exp)
		{
			if (exp) good = 0; else bad = 0;
		}
	}
	CHECK("0 a 127 sont ASCII", good);
	CHECK("128 a 255 ne sont pas ASCII", bad);
	CHECK("bornes : 127 oui, 128 non", ft_isascii(127) && !ft_isascii(128));
}
''',
       hints=["La table ASCII va de 0 a 127.", "Deux comparaisons suffisent.",
              "`if (c >= 0 && c <= 127) return (1);`"]))

add(ex("int ft_isprint(int c)", 1,
       "Teste si le caractere est imprimable.",
       ["Renvoie exactement 1 si `c` est imprimable (de l'espace `' '` = 32 a `'~'` = 126), sinon exactement 0 (le sujet v19.3 impose 1 ou 0, pas une autre valeur)."],
       [("ft_isprint(' ')", "1"), ("ft_isprint(127)", "0")],
       r'''
void run(void)
{
	int c, good, bad;

	good = 1; bad = 1;
	for (c = 0; c < 256; c++)
	{
		int exp = (c >= 32 && c <= 126);
		if (ft_isprint(c) != exp)
		{
			if (exp) good = 0; else bad = 0;
		}
	}
	CHECK("32 a 126 sont imprimables", good);
	CHECK("0-31, 127 et >= 128 ne le sont pas", bad);
	CHECK("bornes : 31 non, 32 oui, 126 oui, 127 non", !ft_isprint(31) && ft_isprint(32) && ft_isprint(126) && !ft_isprint(127));
}
''',
       hints=["Imprimable = de l'espace (32) au tilde (126).", "Deux bornes, un `&&`.",
              "`if (c >= 32 && c <= 126) return (1);`"]))

add(ex("int ft_toupper(int c)", 1,
       "Met un caractere en majuscule.",
       ["Si `c` est une minuscule, renvoie la majuscule correspondante, sinon renvoie `c` inchange."],
       [("ft_toupper('a')", "'A'"), ("ft_toupper('5')", "'5'")],
       r'''
void run(void)
{
	int c, good, bad;

	good = 1; bad = 1;
	for (c = 0; c < 256; c++)
	{
		int exp = (c >= 'a' && c <= 'z') ? c - 32 : c;
		if (ft_toupper(c) != exp)
		{
			if (c >= 'a' && c <= 'z') good = 0; else bad = 0;
		}
	}
	CHECK("a-z deviennent A-Z", good);
	CHECK("tout le reste est renvoye inchange", bad);
	CHECK("ft_toupper('A') reste 'A'", ft_toupper('A') == 'A');
}
''',
       hints=["La difference entre 'a' et 'A' dans la table ASCII est 32.",
              "Ne change que les minuscules.", "`if (c >= 'a' && c <= 'z') return (c - 32);`"]))

add(ex("int ft_tolower(int c)", 1,
       "Met un caractere en minuscule.",
       ["Si `c` est une majuscule, renvoie la minuscule correspondante, sinon renvoie `c` inchange."],
       [("ft_tolower('A')", "'a'"), ("ft_tolower('5')", "'5'")],
       r'''
void run(void)
{
	int c, good, bad;

	good = 1; bad = 1;
	for (c = 0; c < 256; c++)
	{
		int exp = (c >= 'A' && c <= 'Z') ? c + 32 : c;
		if (ft_tolower(c) != exp)
		{
			if (c >= 'A' && c <= 'Z') good = 0; else bad = 0;
		}
	}
	CHECK("A-Z deviennent a-z", good);
	CHECK("tout le reste est renvoye inchange", bad);
}
''',
       hints=["Inverse de toupper : on AJOUTE 32.", "Ne change que les majuscules.",
              "`if (c >= 'A' && c <= 'Z') return (c + 32);`"]))

add(ex("size_t ft_strlen(const char *s)", 1,
       "Calcule la longueur d'une chaine.",
       ["Renvoie le nombre de caracteres avant le `'\\0'` final (le `'\\0'` n'est pas compte).",
        "Le type de retour est `size_t`, pas `int`."],
       [("ft_strlen(\"hello\")", "5"), ("ft_strlen(\"\")", "0")],
       r'''
void run(void)
{
	char	big[2001];
	int		i;

	CHECK("ft_strlen(\"\") == 0", ft_strlen("") == 0);
	CHECK("ft_strlen(\"a\") == 1", ft_strlen("a") == 1);
	CHECK("ft_strlen(\"hello\") == 5", ft_strlen("hello") == 5);
	CHECK("s'arrete au premier '\\0' : \"ab\\0cd\" -> 2", ft_strlen("ab\0cd") == 2);
	CHECK("les espaces comptent : \"  a b \" -> 6", ft_strlen("  a b ") == 6);
	for (i = 0; i < 2000; i++)
		big[i] = 'x';
	big[2000] = '\0';
	CHECK("chaine de 2000 caracteres", ft_strlen(big) == 2000);
}
''',
       hints=["Parcours la chaine avec un indice jusqu'a trouver '\\0'.",
              "`while (s[i])` suffit comme condition.", "Retourne l'indice final : `return (i);` avec `size_t i`."]))

add(ex("void ft_bzero(void *s, size_t n)", 1,
       "Met `n` octets a zero.",
       ["Ecrit `n` octets de valeur 0 a partir de l'adresse `s`.", "Ne renvoie rien."],
       [("ft_bzero(buf, 3)", "les 3 premiers octets valent 0")],
       r'''
void run(void)
{
	unsigned char a[16], b[16];

	memset(a, 0xAA, 16); memset(b, 0xAA, 16);
	ft_bzero(a, 5); memset(b, 0, 5);
	CHECK("ft_bzero(buf, 5) met 5 octets a 0 et ne touche pas le reste", !memcmp(a, b, 16));
	memset(a, 0xAA, 16); memset(b, 0xAA, 16);
	ft_bzero(a, 0);
	CHECK("ft_bzero(buf, 0) ne change rien", !memcmp(a, b, 16));
	memset(a, 0xAA, 16); memset(b, 0xAA, 16);
	ft_bzero(a + 3, 4); memset(b + 3, 0, 4);
	CHECK("fonctionne au milieu d'un tampon", !memcmp(a, b, 16));
	memset(a, 0xAA, 16);
	ft_bzero(a, 16);
	{ int i, z = 1; for (i = 0; i < 16; i++) if (a[i]) z = 0; CHECK("remise a zero de 16 octets", z); }
}
''',
       hints=["Parcours `n` octets avec un `unsigned char *`.", "Un `void *` ne peut pas etre indexe : caste-le d'abord.",
              "`ptr[i] = 0;` dans une boucle `while (i < n)`."]))

add(ex("void *ft_memset(void *s, int c, size_t n)", 1,
       "Remplit `n` octets avec une valeur.",
       ["Ecrit `(unsigned char)c` dans les `n` premiers octets de `s` et renvoie `s`."],
       [("ft_memset(buf, 'x', 3)", "buf commence par xxx")],
       r'''
void run(void)
{
	unsigned char a[16], b[16];
	void *r;

	memset(a, 0xAA, 16); memset(b, 0xAA, 16);
	r = ft_memset(a + 2, 'x', 5); memset(b + 2, 'x', 5);
	CHECK("ft_memset(buf+2, 'x', 5) remplit 5 octets exactement", !memcmp(a, b, 16));
	CHECK("renvoie le pointeur recu", r == a + 2);
	memset(a, 0xAA, 16); memset(b, 0xAA, 16);
	ft_memset(a, 321, 4); memset(b, 321, 4);
	CHECK("la valeur est convertie en unsigned char (321 -> 65 'A')", !memcmp(a, b, 16));
	memset(a, 0xAA, 16); memset(b, 0xAA, 16);
	ft_memset(a, 0, 0);
	CHECK("n = 0 ne change rien", !memcmp(a, b, 16));
	memset(a, 0xAA, 16);
	ft_memset(a, 0xFF, 16);
	{ int i, z = 1; for (i = 0; i < 16; i++) if (a[i] != 0xFF) z = 0; CHECK("remplissage avec 0xFF", z); }
}
''',
       hints=["Comme bzero, mais avec la valeur `c`.", "Convertis `c` : `(unsigned char)c`.",
              "N'oublie pas de renvoyer `s` (le pointeur d'origine)."]))

# ---------------------------------------------------------------- niveau 2
add(ex("void *ft_memcpy(void *dest, const void *src, size_t n)", 2,
       "Copie `n` octets d'une zone memoire a une autre.",
       ["Copie `n` octets de `src` vers `dest` et renvoie `dest`.",
        "Les zones ne se chevauchent pas (c'est le travail de `memmove`)."],
       [("ft_memcpy(dst, \"abc\", 4)", "dst contient abc")],
       r'''
void run(void)
{
	unsigned char a[32], b[32], src[32];
	int i;
	void *r;

	for (i = 0; i < 32; i++)
		src[i] = (unsigned char)(i * 7 + 1);
	memset(a, 0xAA, 32); memset(b, 0xAA, 32);
	r = ft_memcpy(a + 1, src, 10); memcpy(b + 1, src, 10);
	CHECK("copie 10 octets, le reste est intact", !memcmp(a, b, 32));
	CHECK("renvoie dest", r == a + 1);
	memset(a, 0xAA, 32); memset(b, 0xAA, 32);
	ft_memcpy(a, src, 0);
	CHECK("n = 0 ne change rien", !memcmp(a, b, 32));
	src[3] = 0; src[4] = 0;
	memset(a, 0xAA, 32); memset(b, 0xAA, 32);
	ft_memcpy(a, src, 8); memcpy(b, src, 8);
	CHECK("copie aussi les octets nuls (ce n'est pas strcpy)", !memcmp(a, b, 32));
	{
		unsigned char big[1000], big2[1000];
		for (i = 0; i < 1000; i++) big[i] = (unsigned char)i;
		ft_memcpy(big2, big, 1000);
		CHECK("copie de 1000 octets", !memcmp(big, big2, 1000));
	}
}
''',
       hints=["Utilise deux `unsigned char *` : un pour dest, un pour src.", "Une boucle `while (i < n)`.",
              "`d[i] = s[i];` puis `return (dest);`"]))

add(ex("char *ft_strchr(const char *s, int c)", 2,
       "Cherche la premiere occurrence d'un caractere.",
       ["Renvoie un pointeur sur la premiere occurrence de `c` dans `s`, ou `NULL` si absent.",
        "Si `c` vaut `'\\0'`, renvoie un pointeur sur le `'\\0'` final de `s`.",
        "`c` est converti en `char`."],
       [("ft_strchr(\"hello\", 'l')", "pointe sur \"llo\""), ("ft_strchr(\"hello\", 'z')", "NULL")],
       r'''
void run(void)
{
	const char *s = "hello";

	CHECK("ft_strchr(\"hello\", 'l') -> s + 2", ft_strchr(s, 'l') == s + 2);
	CHECK("ft_strchr(\"hello\", 'h') -> s", ft_strchr(s, 'h') == s);
	CHECK("ft_strchr(\"hello\", 'o') -> s + 4", ft_strchr(s, 'o') == s + 4);
	CHECK("caractere absent -> NULL", ft_strchr(s, 'z') == NULL);
	CHECK("ft_strchr(\"hello\", '\\0') -> pointe sur le '\\0' final", ft_strchr(s, '\0') == s + 5);
	{
		const char *e = "";
		CHECK("chaine vide et '\\0' -> la chaine elle-meme", ft_strchr(e, '\0') == e);
	}
	CHECK("chaine vide et 'a' -> NULL", ft_strchr("", 'a') == NULL);
	CHECK("c est converti en char : 'l' + 256 trouve 'l'", ft_strchr(s, 'l' + 256) == s + 2);
}
''',
       hints=["Parcours `s` jusqu'au '\\0'. Compare chaque caractere a `(char)c`.",
              "Il faut renvoyer `(char *)s` (cast pour retirer le const).",
              "Apres la boucle, traite le cas `c == '\\0'` (renvoie la fin de la chaine)."]))

add(ex("char *ft_strrchr(const char *s, int c)", 2,
       "Cherche la derniere occurrence d'un caractere.",
       ["Comme `ft_strchr`, mais renvoie un pointeur sur la **derniere** occurrence.",
        "Si `c` vaut `'\\0'`, renvoie un pointeur sur le `'\\0'` final."],
       [("ft_strrchr(\"hello\", 'l')", "pointe sur \"lo\"")],
       r'''
void run(void)
{
	const char *s = "hello";

	CHECK("ft_strrchr(\"hello\", 'l') -> s + 3 (la derniere)", ft_strrchr(s, 'l') == s + 3);
	CHECK("ft_strrchr(\"hello\", 'h') -> s", ft_strrchr(s, 'h') == s);
	CHECK("caractere absent -> NULL", ft_strrchr(s, 'z') == NULL);
	CHECK("ft_strrchr(\"hello\", '\\0') -> s + 5", ft_strrchr(s, '\0') == s + 5);
	CHECK("ft_strrchr(\"\", 'a') -> NULL", ft_strrchr("", 'a') == NULL);
	{
		const char *p = "a/b/c";
		const char *q = "abc";
		CHECK("ft_strrchr(\"a/b/c\", '/') -> p + 3", ft_strrchr(p, '/') == p + 3);
		CHECK("une seule occurrence : \"abc\", 'b' -> q + 1", ft_strrchr(q, 'b') == q + 1);
	}
}
''',
       hints=["Parcours toute la chaine en retenant la derniere position trouvee.",
              "Initialise ton pointeur de resultat a NULL.", "Traite `c == '\\0'` apres la boucle."]))

add(ex("int ft_strncmp(const char *s1, const char *s2, size_t n)", 2,
       "Compare deux chaines sur `n` caracteres au maximum.",
       ["Renvoie 0 si egales, un nombre negatif si `s1 < s2`, positif si `s1 > s2`.",
        "La comparaison se fait en `unsigned char` et s'arrete au premier `'\\0'` ou apres `n` caracteres."],
       [("ft_strncmp(\"abc\", \"abd\", 2)", "0"), ("ft_strncmp(\"abc\", \"abd\", 3)", "negatif")],
       r'''
static int sgn(int x) { return ((x > 0) - (x < 0)); }

void run(void)
{
	const char *t[] = {"", "a", "abc", "abd", "abcd", "ab", "b", "\xff", "\x01", "A"};
	int	nt = 10, i, j, n, ok;

	ok = 1;
	for (i = 0; i < nt; i++)
		for (j = 0; j < nt; j++)
			for (n = 0; n <= 5; n++)
				if (sgn(ft_strncmp(t[i], t[j], n)) != sgn(strncmp(t[i], t[j], n)))
					ok = 0;
	CHECK("meme signe que strncmp sur 500 combinaisons", ok);
	CHECK("n = 0 -> 0", ft_strncmp("abc", "xyz", 0) == 0);
	CHECK("\"abc\" vs \"abd\" sur 2 caracteres -> 0", ft_strncmp("abc", "abd", 2) == 0);
	CHECK("\"abc\" vs \"abd\" sur 3 caracteres -> negatif", ft_strncmp("abc", "abd", 3) < 0);
	CHECK("comparaison en unsigned char : \"\\xff\" > \"\\x01\"", ft_strncmp("\xff", "\x01", 1) > 0);
	CHECK("s'arrete au '\\0' : \"ab\\0c\" vs \"ab\\0d\" -> 0", ft_strncmp("ab\0c", "ab\0d", 4) == 0);
	CHECK("chaine plus courte : \"ab\" vs \"abc\" -> negatif", ft_strncmp("ab", "abc", 3) < 0);
	CHECK("valeur de retour = difference des octets (\"b\" - \"a\" = 1)", ft_strncmp("b", "a", 1) == 1);
}
''',
       hints=["Boucle tant que `i < n` et qu'au moins une des deux chaines n'est pas finie.",
              "Caste en `unsigned char` AVANT de comparer/soustraire.",
              "Au premier octet different : `return ((unsigned char)s1[i] - (unsigned char)s2[i]);`"]))

add(ex("void *ft_memchr(const void *s, int c, size_t n)", 2,
       "Cherche un octet dans une zone memoire.",
       ["Renvoie un pointeur sur la premiere occurrence de l'octet `(unsigned char)c` parmi les `n` premiers octets, sinon `NULL`.",
        "Contrairement a `strchr`, ne s'arrete pas au `'\\0'`."],
       [("ft_memchr(\"abc\", 'b', 3)", "pointe sur \"bc\"")],
       r'''
void run(void)
{
	const char *s = "ab\0cd";
	unsigned char bin[6] = {1, 2, 0xFF, 4, 5, 6};

	const char *w = "abcdef";

	CHECK("ft_memchr(\"abcdef\", 'c', 6) -> w + 2", ft_memchr(w, 'c', 6) == w + 2);
	CHECK("trouve apres un '\\0' : \"ab\\0cd\", 'd', 5 -> s + 4", ft_memchr(s, 'd', 5) == s + 4);
	CHECK("n trop petit -> NULL : \"abcdef\", 'e', 3", ft_memchr("abcdef", 'e', 3) == NULL);
	CHECK("n = 0 -> NULL", ft_memchr("abc", 'a', 0) == NULL);
	CHECK("recherche du '\\0' : \"ab\\0cd\", 0, 5 -> s + 2", ft_memchr(s, 0, 5) == s + 2);
	CHECK("octet 0xFF (unsigned char)", ft_memchr(bin, 0xFF, 6) == bin + 2);
	{
		const char *p = "aXbX";
		CHECK("premiere occurrence (pas la derniere) : \"aXbX\" -> p + 1", ft_memchr(p, 'X', 4) == p + 1);
	}
}
''',
       hints=["Comme strchr, mais borne par `n` et sans regarder le '\\0'.", "Caste `s` en `const unsigned char *`.",
              "Renvoie `(void *)(ptr + i)` quand tu trouves l'octet."]))

add(ex("int ft_memcmp(const void *s1, const void *s2, size_t n)", 2,
       "Compare deux zones memoire octet par octet.",
       ["Renvoie 0 si les `n` octets sont egaux, sinon la difference (en `unsigned char`) du premier octet different.",
        "Ne s'arrete pas au `'\\0'`."],
       [("ft_memcmp(\"abc\", \"abd\", 3)", "negatif")],
       r'''
static int sgn(int x) { return ((x > 0) - (x < 0)); }

void run(void)
{
	CHECK("zones egales -> 0", ft_memcmp("abc", "abc", 3) == 0);
	CHECK("\"abc\" vs \"abd\" -> negatif", ft_memcmp("abc", "abd", 3) < 0);
	CHECK("\"abd\" vs \"abc\" -> positif", ft_memcmp("abd", "abc", 3) > 0);
	CHECK("n = 0 -> 0", ft_memcmp("a", "b", 0) == 0);
	CHECK("octets apres un '\\0' sont compares : \"a\\0b\" vs \"a\\0c\"", ft_memcmp("a\0b", "a\0c", 3) < 0);
	CHECK("unsigned char : 0xFF > 0x01", ft_memcmp("\xff", "\x01", 1) > 0);
	CHECK("meme signe que memcmp (octets \\x80 / \\x7f)", sgn(ft_memcmp("\x80", "\x7f", 1)) == sgn(memcmp("\x80", "\x7f", 1)));
	CHECK("seuls n octets comptent : \"abcX\" vs \"abcY\", n = 3 -> 0", ft_memcmp("abcX", "abcY", 3) == 0);
}
''',
       hints=["Caste les deux pointeurs en `const unsigned char *`.", "Boucle sur `n` octets.",
              "Des qu'ils different : `return (p1[i] - p2[i]);`"]))

add(ex("size_t ft_strlcpy(char *dst, const char *src, size_t size)", 2,
       "Copie une chaine sans depasser la taille du tampon.",
       ["Copie au plus `size - 1` caracteres de `src` dans `dst` et termine par `'\\0'` (si `size > 0`).",
        "Renvoie la longueur de `src` : si le resultat est >= `size`, la chaine a ete tronquee.",
        "Si `size` vaut 0, n'ecrit rien."],
       [("ft_strlcpy(d, \"hello\", 4)", "renvoie 5, d = \"hel\"")],
       r'''
static int one(const char *src, size_t size)
{
	char	a[24], b[24];
	size_t	ra, rb;

	memset(a, 'Z', 24); memset(b, 'Z', 24);
	ra = ft_strlcpy(a, src, size);
	rb = ref_strlcpy(b, src, size);
	return (ra == rb && !memcmp(a, b, 24));
}

void run(void)
{
	size_t	s;
	int		ok;

	ok = 1;
	for (s = 0; s <= 8; s++)
		if (!one("hello", s))
			ok = 0;
	CHECK("\"hello\" avec size de 0 a 8 : retour et contenu identiques a la reference BSD", ok);
	CHECK("src vide, size = 1 : ecrit seulement '\\0'", one("", 1));
	CHECK("src plus longue que le tampon : tronquee proprement", one("abcdefghijklmnopqrst", 6));
	CHECK("size = 0 : rien n'est ecrit (retour = strlen(src))", one("abc", 0));
	CHECK("size juste suffisante : \"abc\", size 4", one("abc", 4));
	CHECK("retour = longueur de src meme si tronque", ({ char d[3]; ft_strlcpy(d, "abcdef", 3) == 6; }));
}
''',
       hints=["Copie tant que `src[i]` existe ET que `i < size - 1`.", "Ecris le '\\0' (seulement si `size > 0`).",
              "Retourne toujours `ft_strlen(src)`."]))

add(ex("int ft_atoi(const char *nptr)", 2,
       "Convertit une chaine en entier.",
       ["Saute les espaces de debut (`' '`, `\\t`, `\\n`, `\\v`, `\\f`, `\\r`).",
        "Lit un signe `+` ou `-` optionnel, puis les chiffres, et s'arrete au premier caractere non numerique.",
        "Les depassements d'`int` ne sont pas testes."],
       [("ft_atoi(\"  -42abc\")", "-42")],
       r'''
void run(void)
{
	const char *t[] = {"0", "42", "-42", "+42", "  42", "\t\n\v\f\r 42", "42abc", "abc", "", "+", "-",
		"--1", "+-1", "-+1", "0042", "-0", "2147483647", "-2147483648", "12 34", "   -7x"};
	int	i, ok;

	ok = 1;
	for (i = 0; i < 20; i++)
		if (ft_atoi(t[i]) != atoi(t[i]))
			ok = 0;
	CHECK("20 chaines identiques a atoi (signes, espaces, texte, vide)", ok);
	CHECK("ft_atoi(\"  -42abc\") == -42", ft_atoi("  -42abc") == -42);
	CHECK("tous les espaces blancs sont ignores (\\t\\n\\v\\f\\r)", ft_atoi("\t\n\v\f\r 5") == 5);
	CHECK("un seul signe : \"--5\" -> 0 et \"+-5\" -> 0", ft_atoi("--5") == 0 && ft_atoi("+-5") == 0);
	CHECK("INT_MAX et INT_MIN", ft_atoi("2147483647") == INT_MAX && ft_atoi("-2147483648") == INT_MIN);
}
''',
       hints=["Quatre etapes : espaces, signe, chiffres, resultat.", "Les espaces blancs : `c == ' ' || (c >= 9 && c <= 13)`.",
              "`result = result * 10 + (str[i] - '0');` puis `return (result * sign);`"]))

add(ex("char *ft_strdup(const char *s)", 2,
       "Duplique une chaine avec `malloc`.",
       ["Alloue `strlen(s) + 1` octets, y copie `s` (avec le `'\\0'`) et renvoie la copie.",
        "Si `malloc` echoue, renvoie `NULL`."],
       [("ft_strdup(\"abc\")", "une copie independante de \"abc\"")],
       r'''
void run(void)
{
	char	*d;
	char	src[8] = "abc";

	d = ft_strdup("hello");
	CHECK("ft_strdup(\"hello\") contient \"hello\"", d && !strcmp(d, "hello"));
	free(d);
	d = ft_strdup(src);
	CHECK("la copie est un autre bloc memoire", d && d != src);
	src[0] = 'X';
	CHECK("modifier l'original ne change pas la copie", d && !strcmp(d, "abc"));
	free(d);
	d = ft_strdup("");
	CHECK("ft_strdup(\"\") -> chaine vide allouee", d && d[0] == '\0');
	free(d);
	NOLEAK();
	t_fail_nth(1);
	d = ft_strdup("abc");
	t_fail_nth(0);
	CHECK("malloc qui echoue -> NULL", d == NULL);
}
''', allowed=["malloc"],
       hints=["Mesure la chaine, alloue `len + 1`, copie.", "Teste le retour de `malloc` !",
              "Termine la copie par '\\0'."]))

add(ex("void ft_putchar_fd(char c, int fd)", 2,
       "Ecrit un caractere sur un descripteur de fichier.",
       ["Ecrit `c` sur le descripteur `fd` avec `write`."],
       [("ft_putchar_fd('a', 1)", "affiche a")],
       r'''
void run(void)
{
	char	buf[16];
	int		fd, n;

	fd = cap_open();
	ft_putchar_fd('a', fd);
	n = cap_read(buf, sizeof(buf));
	CHECK("ft_putchar_fd('a') ecrit exactement 1 octet : 'a'", n == 1 && buf[0] == 'a');
	fd = cap_open();
	ft_putchar_fd('\n', fd);
	n = cap_read(buf, sizeof(buf));
	CHECK("ft_putchar_fd('\\n') ecrit exactement 1 octet", n == 1 && buf[0] == '\n');
	fd = cap_open();
	ft_putchar_fd((char)0xE9, fd);
	n = cap_read(buf, sizeof(buf));
	CHECK("un octet >= 128 est ecrit tel quel", n == 1 && (unsigned char)buf[0] == 0xE9);
}
''', allowed=["write"], part=2,
       hints=["`write(fd, &c, 1);`", "Une seule ligne dans la fonction.", "Le deuxieme argument de write est une adresse : `&c`."]))

add(ex("void ft_putstr_fd(char *s, int fd)", 2,
       "Ecrit une chaine sur un descripteur de fichier.",
       ["Ecrit la chaine `s` sur `fd` (sans retour a la ligne)."],
       [("ft_putstr_fd(\"abc\", 1)", "affiche abc")],
       r'''
void run(void)
{
	char	buf[1024];
	char	big[601];
	int		fd, n, i;

	fd = cap_open();
	ft_putstr_fd("hello", fd);
	n = cap_read(buf, sizeof(buf));
	CHECK("ft_putstr_fd(\"hello\") ecrit exactement \"hello\"", n == 5 && !memcmp(buf, "hello", 5));
	fd = cap_open();
	ft_putstr_fd("", fd);
	n = cap_read(buf, sizeof(buf));
	CHECK("ft_putstr_fd(\"\") n'ecrit rien", n == 0);
	fd = cap_open();
	ft_putstr_fd("a\tb c\n", fd);
	n = cap_read(buf, sizeof(buf));
	CHECK("caracteres speciaux conserves (tab, espace, \\n)", n == 6 && !memcmp(buf, "a\tb c\n", 6));
	for (i = 0; i < 600; i++)
		big[i] = 'a' + i % 26;
	big[600] = '\0';
	fd = cap_open();
	ft_putstr_fd(big, fd);
	n = cap_read(buf, sizeof(buf));
	CHECK("chaine de 600 caracteres ecrite en entier", n == 600 && !memcmp(buf, big, 600));
}
''', allowed=["write"], part=2,
       hints=["`write(fd, s, longueur)`.", "ft_strlen te donne la longueur.", "Un seul write suffit."]))

add(ex("void ft_putendl_fd(char *s, int fd)", 2,
       "Ecrit une chaine suivie d'un retour a la ligne.",
       ["Ecrit `s` puis `\\n` sur le descripteur `fd`."],
       [("ft_putendl_fd(\"abc\", 1)", "affiche abc puis un retour a la ligne")],
       r'''
void run(void)
{
	char	buf[256];
	int		fd, n;

	fd = cap_open();
	ft_putendl_fd("abc", fd);
	n = cap_read(buf, sizeof(buf));
	CHECK("ft_putendl_fd(\"abc\") ecrit exactement \"abc\\n\"", n == 4 && !memcmp(buf, "abc\n", 4));
	fd = cap_open();
	ft_putendl_fd("", fd);
	n = cap_read(buf, sizeof(buf));
	CHECK("ft_putendl_fd(\"\") ecrit un seul \"\\n\"", n == 1 && buf[0] == '\n');
	fd = cap_open();
	ft_putendl_fd("a b\tc", fd);
	n = cap_read(buf, sizeof(buf));
	CHECK("espaces et tabulations conserves", n == 6 && !memcmp(buf, "a b\tc\n", 6));
}
''', allowed=["write"], part=2,
       hints=["Un write pour la chaine, un write pour '\\n'.", "Ou reutilise ft_putstr_fd et ft_putchar_fd.",
              "`write(fd, \"\\n\", 1);`"]))

# ---------------------------------------------------------------- niveau 3
add(ex("void *ft_memmove(void *dest, const void *src, size_t n)", 3,
       "Copie `n` octets, meme si les zones se chevauchent.",
       ["Comme `memcpy`, mais le resultat est correct meme si `dest` et `src` se chevauchent.",
        "Renvoie `dest`.",
        "Astuce : si `dest < src`, copie de gauche a droite, sinon de droite a gauche."],
       [("ft_memmove(buf + 2, buf, 4)", "buf = \"abababcd\"... sans ecraser la source")],
       r'''
void run(void)
{
	char	a[16], b[16];
	void	*r;

	strcpy(a, "abcdefghij"); strcpy(b, "abcdefghij");
	r = ft_memmove(a + 2, a, 6); memmove(b + 2, b, 6);
	CHECK("chevauchement, dest > src : a+2 <- a (6 octets)", !memcmp(a, b, 11));
	CHECK("renvoie dest", r == a + 2);
	strcpy(a, "abcdefghij"); strcpy(b, "abcdefghij");
	ft_memmove(a, a + 3, 6); memmove(b, b + 3, 6);
	CHECK("chevauchement, dest < src : a <- a+3 (6 octets)", !memcmp(a, b, 11));
	strcpy(a, "abcdefghij"); strcpy(b, "abcdefghij");
	ft_memmove(a + 1, a, 9); memmove(b + 1, b, 9);
	CHECK("decalage d'un cran vers la droite (cas classique)", !memcmp(a, b, 11));
	strcpy(a, "abcdefghij"); strcpy(b, "abcdefghij");
	ft_memmove(a, a, 5);
	CHECK("meme adresse : rien ne change", !memcmp(a, b, 11));
	strcpy(a, "abcdefghij");
	ft_memmove(a, "XYZ", 0);
	CHECK("n = 0 : rien ne change", !strcmp(a, "abcdefghij"));
	strcpy(a, "abcdefghij"); strcpy(b, "abcdefghij");
	ft_memmove(a + 5, "XYZ", 3); memmove(b + 5, "XYZ", 3);
	CHECK("zones disjointes (comme memcpy)", !memcmp(a, b, 11));
}
''',
       hints=["Deux cas : `dest < src` -> copie normale ; sinon -> copie en partant de la fin.",
              "Copie a l'envers : `while (n > 0) { n--; d[n] = s[n]; }`", "Pense a renvoyer `dest`."]))

add(ex("size_t ft_strlcat(char *dst, const char *src, size_t size)", 3,
       "Concatene deux chaines sans depasser la taille du tampon.",
       ["Ajoute `src` a la fin de `dst` sans depasser `size` octets au total (`'\\0'` compris).",
        "Renvoie la longueur qu'aurait la chaine finale : `min(size, strlen(dst)) + strlen(src)`.",
        "Si `size <= strlen(dst)`, n'ecrit rien et renvoie `size + strlen(src)`."],
       [("ft_strlcat(d, \"cdef\", 5) avec d = \"ab\"", "renvoie 6, d = \"abcd\"")],
       r'''
static int one(const char *dst, const char *src, size_t size)
{
	char	a[32], b[32];
	size_t	ra, rb;

	memset(a, 'Z', 32); memset(b, 'Z', 32);
	strcpy(a, dst); strcpy(b, dst);
	ra = ft_strlcat(a, src, size);
	rb = ref_strlcat(b, src, size);
	return (ra == rb && !memcmp(a, b, 32));
}

void run(void)
{
	size_t	s;
	int		ok;

	ok = 1;
	for (s = 0; s <= 10; s++)
		if (!one("ab", "cdef", s))
			ok = 0;
	CHECK("\"ab\" + \"cdef\" avec size 0 a 10 : retour et contenu = reference BSD", ok);
	CHECK("size <= strlen(dst) : rien n'est ecrit", one("abc", "xyz", 2));
	CHECK("size == strlen(dst) : rien n'est ecrit", one("abc", "xyz", 3));
	CHECK("dst vide", one("", "hello", 10));
	CHECK("src vide", one("hello", "", 10));
	CHECK("tout rentre", one("ab", "cd", 20));
	CHECK("troncature : \"hello\" + \"world\", size 8", one("hello", "world", 8));
	CHECK("retour : \"ab\" + \"cdef\", size 5 -> 6", ({ char d[16] = "ab"; ft_strlcat(d, "cdef", 5) == 6 && !strcmp(d, "abcd"); }));
}
''',
       hints=["1) mesure `dst` (sans depasser `size`). 2) si plus de place, copie `src` en laissant 1 octet pour '\\0'.",
              "Cas `size <= dst_len` : retourne `size + ft_strlen(src)` sans ecrire.",
              "Retour final : `dst_len + ft_strlen(src)`."]))

add(ex("char *ft_strnstr(const char *big, const char *little, size_t len)", 3,
       "Cherche une sous-chaine dans les `len` premiers caracteres.",
       ["Cherche `little` dans `big`, sans regarder plus de `len` caracteres de `big`.",
        "Si `little` est vide, renvoie `big`.",
        "Renvoie un pointeur sur le debut de la premiere occurrence, ou `NULL`."],
       [("ft_strnstr(\"hello world\", \"world\", 11)", "pointe sur \"world\""),
        ("ft_strnstr(\"hello world\", \"world\", 8)", "NULL")],
       r'''
static int one(const char *h, const char *n, size_t len)
{
	return (ft_strnstr(h, n, len) == ref_strnstr(h, n, len));
}

void run(void)
{
	const char *h = "hello world";

	CHECK("needle vide -> renvoie big (meme avec len = 0)", ft_strnstr(h, "", 0) == h && ft_strnstr(h, "", 5) == h);
	CHECK("trouve \"world\" avec len = 11", ft_strnstr(h, "world", 11) == h + 6);
	CHECK("ne depasse pas len : \"world\" avec len = 10 -> NULL", ft_strnstr(h, "world", 10) == NULL);
	CHECK("len = 0 et needle non vide -> NULL", ft_strnstr(h, "h", 0) == NULL);
	CHECK("needle plus longue que big -> NULL", ft_strnstr("abc", "abcd", 10) == NULL);
	CHECK("big vide -> NULL", ft_strnstr("", "a", 5) == NULL);
	CHECK("debut de chaine : \"hello\"", ft_strnstr(h, "hello", 5) == h);
	CHECK("faux depart : \"aaabc\" / \"aab\"", one("aaabc", "aab", 5));
	CHECK("occurrences multiples -> la premiere : \"abcabc\" / \"bc\"", one("abcabc", "bc", 6));
	CHECK("len coupe la needle : \"abcdef\" / \"cde\" avec len 4", one("abcdef", "cde", 4));
	CHECK("len plus grand que big : \"abc\" / \"bc\" avec len 100", one("abc", "bc", 100));
}
''',
       hints=["Deux boucles imbriquees : position `i` dans big, `j` dans little.", "Condition : `i + j < len` pour ne jamais lire trop loin.",
              "Si `little[j] == '\\0'` -> trouve, renvoie `big + i`."]))

add(ex("void *ft_calloc(size_t nmemb, size_t size)", 3,
       "Alloue de la memoire et la met a zero.",
       ["Alloue `nmemb * size` octets avec `malloc`, les met tous a 0 et renvoie le pointeur.",
        "Si la multiplication depasse `SIZE_MAX` (debordement) ou si `malloc` echoue, renvoie `NULL`.",
        "Sujet v19.3 : si `nmemb` ou `size` vaut 0, `ft_calloc` renvoie un pointeur UNIQUE valide (pas `NULL`) que l'on peut passer a `free`."],
       [("ft_calloc(5, 4)", "20 octets, tous a 0")],
       r'''
void run(void)
{
	unsigned char	*p;
	unsigned char	*q;
	size_t			i;
	int				z;

	p = malloc(256);
	memset(p, 0xAA, 256);
	free(p);
	q = ft_calloc(16, 4);
	z = (q != NULL);
	for (i = 0; q && i < 64; i++)
		if (q[i])
			z = 0;
	CHECK("ft_calloc(16, 4) : 64 octets tous a zero (meme sur memoire reutilisee)", z);
	free(q);
	q = ft_calloc(1, 1);
	CHECK("ft_calloc(1, 1) : 1 octet a zero", q && q[0] == 0);
	free(q);
	q = ft_calloc(0, 4);
	CHECK("ft_calloc(0, 4) : pointeur valide (pas NULL), a passer a free", q != NULL);
	free(q);
	q = ft_calloc(4, 0);
	CHECK("ft_calloc(4, 0) : pointeur valide (pas NULL), a passer a free", q != NULL);
	free(q);
	q = ft_calloc(SIZE_MAX / 2 + 2, 2);
	CHECK("debordement de nmemb * size -> NULL", q == NULL);
	free(q);
	NOLEAK();
	t_fail_nth(1);
	q = ft_calloc(4, 4);
	t_fail_nth(0);
	CHECK("malloc qui echoue -> NULL", q == NULL);
}
''', allowed=["malloc"],
       hints=["`malloc(nmemb * size)` puis `ft_bzero` (tu l'as deja !).", "Teste le retour de malloc.",
              "Debordement : `if (nmemb != 0 && size > SIZE_MAX / nmemb) return (NULL);`"]))
