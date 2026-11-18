"""Libft, partie 2 : fonctions supplementaires."""
from ._util import ex

EXERCISES = []
add = EXERCISES.append

add(ex("char *ft_substr(char const *s, unsigned int start, size_t len)", 3,
       "Extrait une sous-chaine.",
       ["Alloue et renvoie une nouvelle chaine : au plus `len` caracteres de `s`, a partir de l'indice `start`.",
        "Si `start` est au-dela de la fin de `s`, renvoie une chaine vide (allouee, pas `NULL`).",
        "Si `malloc` echoue, renvoie `NULL`."],
       [("ft_substr(\"hello\", 1, 3)", "\"ell\""), ("ft_substr(\"hello\", 10, 3)", "\"\"")],
       r'''
static int is(char *r, const char *e)
{
	int ok = (r != NULL && !strcmp(r, e));
	free(r);
	return (ok);
}

void run(void)
{
	char	*r;

	CHECK("ft_substr(\"hello\", 1, 3) == \"ell\"", is(ft_substr("hello", 1, 3), "ell"));
	CHECK("ft_substr(\"hello\", 0, 5) == \"hello\"", is(ft_substr("hello", 0, 5), "hello"));
	CHECK("len trop grand : (\"hello\", 3, 100) == \"lo\"", is(ft_substr("hello", 3, 100), "lo"));
	CHECK("len = 0 : chaine vide", is(ft_substr("hello", 2, 0), ""));
	CHECK("start = strlen(s) : chaine vide (pas NULL)", is(ft_substr("hello", 5, 3), ""));
	CHECK("start > strlen(s) : chaine vide (pas NULL)", is(ft_substr("hello", 10, 3), ""));
	CHECK("s vide : chaine vide", is(ft_substr("", 0, 5), ""));
	CHECK("sous-chaine terminee par '\\0' (pas de debris apres)", is(ft_substr("abcdef", 2, 2), "cd"));
	NOLEAK();
	t_fail_nth(1);
	r = ft_substr("hello", 1, 2);
	t_fail_nth(0);
	CHECK("malloc qui echoue -> NULL", r == NULL);
}
''', allowed=["malloc"], part=2,
       hints=["Mesure `s`. Si `start >= len(s)`, renvoie une chaine vide allouee (`ft_strdup(\"\")`).",
              "Reduis `len` a `len(s) - start` s'il est trop grand.", "`malloc(len + 1)`, copie `len` caracteres, termine par '\\0'."]))

add(ex("char *ft_strjoin(char const *s1, char const *s2)", 2,
       "Concatene deux chaines dans une nouvelle chaine.",
       ["Alloue et renvoie une nouvelle chaine = `s1` suivie de `s2`.",
        "`s1` et `s2` ne sont pas modifiees.",
        "Attention : ce n'est PAS le `ft_strjoin` de la piscine (tableau + separateur)."],
       [("ft_strjoin(\"foo\", \"bar\")", "\"foobar\"")],
       r'''
static int is(char *r, const char *e)
{
	int ok = (r != NULL && !strcmp(r, e));
	free(r);
	return (ok);
}

void run(void)
{
	char	a[8] = "foo";
	char	b[8] = "bar";
	char	*r;

	CHECK("ft_strjoin(\"foo\", \"bar\") == \"foobar\"", is(ft_strjoin(a, b), "foobar"));
	CHECK("s1 et s2 ne sont pas modifiees", !strcmp(a, "foo") && !strcmp(b, "bar"));
	CHECK("deux chaines vides -> chaine vide", is(ft_strjoin("", ""), ""));
	CHECK("s2 vide -> copie de s1", is(ft_strjoin("abc", ""), "abc"));
	CHECK("s1 vide -> copie de s2", is(ft_strjoin("", "xyz"), "xyz"));
	CHECK("les espaces sont conserves : (\"a \", \" b\")", is(ft_strjoin("a ", " b"), "a  b"));
	r = ft_strjoin("ab", "cd");
	CHECK("le resultat est un nouveau bloc", r != NULL && r != a && r != b);
	free(r);
	NOLEAK();
	t_fail_nth(1);
	r = ft_strjoin("ab", "cd");
	t_fail_nth(0);
	CHECK("malloc qui echoue -> NULL", r == NULL);
}
''', allowed=["malloc"], part=2,
       hints=["Longueur totale = `len1 + len2 + 1`.", "Copie s1, puis s2 juste apres.",
              "N'oublie pas le '\\0' final."]))

add(ex("char *ft_strtrim(char const *s1, char const *set)", 3,
       "Supprime des caracteres au debut et a la fin d'une chaine.",
       ["Alloue et renvoie une copie de `s1` sans les caracteres de `set` au debut ni a la fin.",
        "Les caracteres au milieu ne sont pas touches.",
        "Si tout est supprime, renvoie une chaine vide."],
       [("ft_strtrim(\"  hi  \", \" \")", "\"hi\""), ("ft_strtrim(\"xxhixx\", \"x\")", "\"hi\"")],
       r'''
static int is(char *r, const char *e)
{
	int ok = (r != NULL && !strcmp(r, e));
	free(r);
	return (ok);
}

void run(void)
{
	char	*r;

	CHECK("(\"  hi  \", \" \") == \"hi\"", is(ft_strtrim("  hi  ", " "), "hi"));
	CHECK("(\"xxhixx\", \"x\") == \"hi\"", is(ft_strtrim("xxhixx", "x"), "hi"));
	CHECK("le milieu n'est pas touche : (\"  a b  \", \" \") == \"a b\"", is(ft_strtrim("  a b  ", " "), "a b"));
	CHECK("set vide : copie de s1", is(ft_strtrim("abc", ""), "abc"));
	CHECK("s1 vide : chaine vide", is(ft_strtrim("", "x"), ""));
	CHECK("tout est supprime : (\"xxx\", \"x\") == \"\"", is(ft_strtrim("xxx", "x"), ""));
	CHECK("plusieurs caracteres dans set : (\"abcba\", \"ab\") == \"c\"", is(ft_strtrim("abcba", "ab"), "c"));
	CHECK("rien a retirer : (\"hello\", \"xyz\") == \"hello\"", is(ft_strtrim("hello", "xyz"), "hello"));
	CHECK("debut seulement : (\"  hi\", \" \") == \"hi\"", is(ft_strtrim("  hi", " "), "hi"));
	CHECK("fin seulement : (\"hi  \", \" \") == \"hi\"", is(ft_strtrim("hi  ", " "), "hi"));
	NOLEAK();
	t_fail_nth(1);
	r = ft_strtrim(" ab ", " ");
	t_fail_nth(0);
	CHECK("malloc qui echoue -> NULL", r == NULL);
}
''', allowed=["malloc"], part=2,
       hints=["Avance `start` tant que `s1[start]` est dans `set` ; recule `end` pareil.",
              "`ft_strchr(set, c)` dit si `c` est dans `set`.", "Termine avec `ft_substr(s1, start, end - start)`."]))

add(ex("char **ft_split(char const *s, char c)", 4,
       "Decoupe une chaine en mots separes par un caractere.",
       ["Renvoie un tableau de chaines, termine par `NULL`, alloue avec `malloc`.",
        "Les separateurs consecutifs ou en bordure sont ignores (pas de mot vide).",
        "Si un `malloc` echoue, tout ce qui a deja ete alloue doit etre libere et la fonction renvoie `NULL`."],
       [("ft_split(\"--a-b--c-\", '-')", "{\"a\", \"b\", \"c\", NULL}"), ("ft_split(\"\", ',')", "{NULL}")],
       r'''
static int same(char **t, const char **e)
{
	int i;

	if (!t)
		return (0);
	i = 0;
	while (e[i])
	{
		if (!t[i] || strcmp(t[i], e[i]))
			return (0);
		i++;
	}
	return (t[i] == NULL);
}

static void free_tab(char **t)
{
	int i;

	i = 0;
	while (t && t[i])
		free(t[i++]);
	free(t);
}

void run(void)
{
	char	**t;
	int		n;
	int		ok;
	const char	*e1[] = {"a", "bb", "ccc", NULL};
	const char	*e2[] = {NULL};
	const char	*e3[] = {"abc", NULL};
	const char	*e4[] = {"a", "b", "c", "d", NULL};
	const char	*e5[] = {"a", "b", "c", NULL};

	t = ft_split("  a bb  ccc ", ' ');
	CHECK("(\"  a bb  ccc \", ' ') -> a, bb, ccc", same(t, e1));
	free_tab(t);
	t = ft_split("--a-b--c-", '-');
	CHECK("(\"--a-b--c-\", '-') -> a, b, c", same(t, e5));
	free_tab(t);
	t = ft_split("", ' ');
	CHECK("(\"\", ' ') -> tableau contenant seulement NULL", same(t, e2));
	free_tab(t);
	t = ft_split("     ", ' ');
	CHECK("que des separateurs -> {NULL}", same(t, e2));
	free_tab(t);
	t = ft_split("abc", ',');
	CHECK("aucun separateur -> un seul mot", same(t, e3));
	free_tab(t);
	t = ft_split("a,b,c,d", ',');
	CHECK("(\"a,b,c,d\", ',') -> a, b, c, d", same(t, e4));
	free_tab(t);
	NOLEAK();
	ok = 1;
	for (n = 1; n <= 8; n++)
	{
		t_fail_nth(n);
		t = ft_split("a b c d", ' ');
		t_fail_nth(0);
		if (t)
			free_tab(t);
		if (t_live() != 0)
			ok = 0;
	}
	CHECK("si un malloc echoue : NULL renvoye et plus rien d'alloue (pas de fuite)", ok);
}
''', allowed=["malloc", "free"], part=2,
       hints=["Trois etapes : compter les mots, allouer le tableau, puis allouer chaque mot.",
              "Une fonction `count_words` et une fonction `alloc_word` rendent le code lisible (norme : 25 lignes max).",
              "Si l'allocation du mot i echoue, libere les mots 0..i-1 puis le tableau."]))

add(ex("char *ft_itoa(int n)", 4,
       "Convertit un entier en chaine.",
       ["Alloue et renvoie la representation decimale de `n`, avec un `-` si negatif.",
        "Attention a `INT_MIN` (-2147483648) : sa valeur absolue ne rentre pas dans un `int`.",
        "Si `malloc` echoue, renvoie `NULL`."],
       [("ft_itoa(-123)", "\"-123\""), ("ft_itoa(0)", "\"0\"")],
       r'''
static int is(char *r, const char *e)
{
	int ok = (r != NULL && !strcmp(r, e));
	free(r);
	return (ok);
}

void run(void)
{
	char	*r;

	CHECK("ft_itoa(0) == \"0\"", is(ft_itoa(0), "0"));
	CHECK("ft_itoa(1) == \"1\"", is(ft_itoa(1), "1"));
	CHECK("ft_itoa(-1) == \"-1\"", is(ft_itoa(-1), "-1"));
	CHECK("ft_itoa(42) == \"42\"", is(ft_itoa(42), "42"));
	CHECK("ft_itoa(-42) == \"-42\"", is(ft_itoa(-42), "-42"));
	CHECK("ft_itoa(10) == \"10\" et ft_itoa(100) == \"100\"", is(ft_itoa(10), "10") && is(ft_itoa(100), "100"));
	CHECK("ft_itoa(-10) == \"-10\"", is(ft_itoa(-10), "-10"));
	CHECK("ft_itoa(INT_MAX) == \"2147483647\"", is(ft_itoa(INT_MAX), "2147483647"));
	CHECK("ft_itoa(INT_MIN) == \"-2147483648\"", is(ft_itoa(INT_MIN), "-2147483648"));
	NOLEAK();
	t_fail_nth(1);
	r = ft_itoa(123);
	t_fail_nth(0);
	CHECK("malloc qui echoue -> NULL", r == NULL);
}
''', allowed=["malloc"], part=2,
       hints=["Compte d'abord les chiffres (+1 pour le signe), puis alloue.", "Remplis la chaine de droite a gauche avec `% 10` et `/ 10`.",
              "Pour INT_MIN : copie `n` dans un `long long` avant de prendre la valeur absolue."]))

add(ex("char *ft_strmapi(char const *s, char (*f)(unsigned int, char))", 3,
       "Applique une fonction a chaque caractere et renvoie une nouvelle chaine.",
       ["Cree une nouvelle chaine ou le caractere `i` est le resultat de `f(i, s[i])`.",
        "`s` n'est pas modifiee."],
       [("ft_strmapi(\"abc\", f)", "avec f(i, c) = c + i -> \"ace\"")],
       r'''
static char add_i(unsigned int i, char c) { return ((char)(c + i)); }
static char up(unsigned int i, char c) { (void)i; return ((c >= 'a' && c <= 'z') ? c - 32 : c); }

void run(void)
{
	char	s[8] = "abc";
	char	*r;

	r = ft_strmapi(s, add_i);
	CHECK("f(i, c) = c + i : \"abc\" -> \"ace\"", r && !strcmp(r, "ace"));
	free(r);
	CHECK("la chaine d'origine n'est pas modifiee", !strcmp(s, "abc"));
	r = ft_strmapi("hello world", up);
	CHECK("mise en majuscules : \"hello world\" -> \"HELLO WORLD\"", r && !strcmp(r, "HELLO WORLD"));
	free(r);
	r = ft_strmapi("", add_i);
	CHECK("chaine vide -> chaine vide (pas NULL)", r && r[0] == '\0');
	free(r);
	NOLEAK();
	t_fail_nth(1);
	r = ft_strmapi("abc", add_i);
	t_fail_nth(0);
	CHECK("malloc qui echoue -> NULL", r == NULL);
}
''', allowed=["malloc"], part=2,
       hints=["Alloue `len + 1`.", "Boucle : `res[i] = f(i, s[i]);`", "Pense au '\\0' final."]))

add(ex("void ft_striteri(char *s, void (*f)(unsigned int, char *))", 3,
       "Applique une fonction a chaque caractere, directement dans la chaine.",
       ["Appelle `f(i, &s[i])` pour chaque indice `i`, dans l'ordre, de 0 a `strlen(s) - 1`.",
        "La chaine `s` est modifiee sur place."],
       [("ft_striteri(s, f)", "avec f(i, c) : *c += i, \"abc\" devient \"ace\"")],
       r'''
static unsigned int g_calls;
static unsigned int g_last;
static void add_i(unsigned int i, char *c) { *c = (char)(*c + i); g_calls++; g_last = i; }

void run(void)
{
	char	s[8] = "abc";
	char	e[4] = "";

	ft_striteri(s, add_i);
	CHECK("f(i, c) : *c += i, \"abc\" -> \"ace\"", !strcmp(s, "ace"));
	CHECK("f est appelee exactement 3 fois", g_calls == 3);
	CHECK("le dernier indice est 2", g_last == 2);
	g_calls = 0;
	ft_striteri(e, add_i);
	CHECK("chaine vide : f n'est jamais appelee", g_calls == 0);
}
''', part=2,
       hints=["Une boucle `while (s[i])`.", "Passe l'ADRESSE du caractere : `&s[i]`.", "Aucun malloc ici."]))

add(ex("void ft_putnbr_fd(int n, int fd)", 3,
       "Ecrit un entier sur un descripteur de fichier.",
       ["Ecrit `n` en decimal sur `fd` (avec `-` si negatif), sans retour a la ligne.",
        "Attention a `INT_MIN`."],
       [("ft_putnbr_fd(-42, 1)", "affiche -42")],
       r'''
static int out(int n, char *buf, int max)
{
	int fd = cap_open();
	ft_putnbr_fd(n, fd);
	return (cap_read(buf, max));
}

void run(void)
{
	char buf[64];
	int  n;

	n = out(0, buf, 64);
	CHECK("0 -> \"0\"", n == 1 && !strcmp(buf, "0"));
	n = out(42, buf, 64);
	CHECK("42 -> \"42\"", n == 2 && !strcmp(buf, "42"));
	n = out(-42, buf, 64);
	CHECK("-42 -> \"-42\"", n == 3 && !strcmp(buf, "-42"));
	n = out(10, buf, 64);
	CHECK("10 -> \"10\"", n == 2 && !strcmp(buf, "10"));
	n = out(-1, buf, 64);
	CHECK("-1 -> \"-1\"", n == 2 && !strcmp(buf, "-1"));
	n = out(INT_MAX, buf, 64);
	CHECK("INT_MAX -> \"2147483647\"", n == 10 && !strcmp(buf, "2147483647"));
	n = out(INT_MIN, buf, 64);
	CHECK("INT_MIN -> \"-2147483648\"", n == 11 && !strcmp(buf, "-2147483648"));
}
''', allowed=["write"], part=2,
       hints=["Une fonction recursive est la solution la plus courte.", "Ecris d'abord les chiffres de gauche : `ft_putnbr_fd(n / 10, fd)`.",
              "INT_MIN : passe par un `long long`."]))
