"""Libft, partie 3 : listes chainees (obligatoire depuis le sujet v19.3)."""
from functools import partial

from ._util import ex as _ex

ex = partial(_ex, part=3)
EXERCISES = []
add = EXERCISES.append

# Briques communes des tests (chaque test est compile seul, on les recopie).
# Les noeuds de test sont construits "a la main" avec malloc : un exercice ne
# depend donc jamais d'une autre fonction ft_lst* pour construire ses donnees.
COMMON = r'''
static int	g_del;
static void	*g_last;

static void	del_free(void *p)
{
	g_del++;
	g_last = p;
	free(p);
}

static char	*mk(const char *s)
{
	char	*r;

	r = malloc(strlen(s) + 1);
	strcpy(r, s);
	return (r);
}

static t_list	*node(const char *s)
{
	t_list	*n;

	n = malloc(sizeof(t_list));
	n->content = mk(s);
	n->next = NULL;
	return (n);
}

static t_list	*chain(int n)
{
	t_list	*h;
	t_list	*x;
	char	s[2];

	h = NULL;
	while (n > 0)
	{
		s[0] = 'a' + (n - 1) % 26;
		s[1] = '\0';
		x = node(s);
		x->next = h;
		h = x;
		n--;
	}
	return (h);
}
'''

NOTE_STRUCT = ("Dans ton `libft.h`, ajoute la structure du sujet (avant les prototypes `ft_lst*`) : "
               "`typedef struct s_list { void *content; struct s_list *next; } t_list;` "
               "(ecrite sur plusieurs lignes, comme dans le sujet).")

# ---------------------------------------------------------------- niveau 1
add(ex("unsigned int ft_lstsize(t_list *lst)", 1,
       "Compte les noeuds d'une liste.",
       ["Renvoie le nombre de noeuds de la liste commencant a `lst`.",
        "Une liste vide (`lst == NULL`) a 0 noeud.",
        "ATTENTION : le sujet (v19.3) demande un retour `unsigned int`, pas `int`. "
        "Avec un autre type, le prototype ne correspond plus a ton `libft.h` et le code ne compile pas."],
       [("ft_lstsize(NULL)", "0"), ("ft_lstsize(a -> b -> c)", "3")],
       COMMON + r'''
void run(void)
{
	t_list	*l;

	CHECK("liste vide (NULL) -> 0", ft_lstsize(NULL) == 0);
	l = node("a");
	CHECK("un seul noeud -> 1", ft_lstsize(l) == 1);
	ft_lstclear(&l, del_free);
	l = chain(5);
	CHECK("cinq noeuds -> 5", ft_lstsize(l) == 5);
	CHECK("la liste n'est pas modifiee (on peut recompter)", ft_lstsize(l) == 5);
	CHECK("on peut compter depuis le milieu : ft_lstsize(l->next) == 4", ft_lstsize(l->next) == 4);
	ft_lstclear(&l, del_free);
	l = chain(1000);
	CHECK("mille noeuds -> 1000", ft_lstsize(l) == 1000);
	ft_lstclear(&l, del_free);
	NOLEAK();
}
''', notes=[NOTE_STRUCT],
       hints=["Un compteur `n` a 0, et un pointeur que tu fais avancer : `lst = lst->next`.",
              "`while (lst) { n++; lst = lst->next; }` : la liste s'arrete quand le pointeur vaut `NULL`.",
              "Le type de retour est `unsigned int` : declare ton compteur du meme type."]))

add(ex("t_list *ft_lstlast(t_list *lst)", 1,
       "Renvoie le dernier noeud d'une liste.",
       ["Renvoie un pointeur sur le dernier noeud (celui dont `next` vaut `NULL`).",
        "Si la liste est vide, renvoie `NULL`.",
        "La liste n'est pas modifiee."],
       [("ft_lstlast(a -> b -> c)", "pointeur sur c"), ("ft_lstlast(NULL)", "NULL")],
       COMMON + r'''
void run(void)
{
	t_list	*l;
	t_list	*x;

	CHECK("liste vide -> NULL", ft_lstlast(NULL) == NULL);
	l = node("a");
	CHECK("un seul noeud -> ce noeud", ft_lstlast(l) == l);
	ft_lstclear(&l, del_free);
	l = chain(4);
	x = l->next->next->next;
	CHECK("liste de 4 -> le quatrieme noeud", ft_lstlast(l) == x);
	CHECK("le dernier noeud a next == NULL", ft_lstlast(l)->next == NULL);
	CHECK("on peut partir du milieu : ft_lstlast(l->next) == dernier", ft_lstlast(l->next) == x);
	CHECK("la liste n'est pas modifiee", l->next != NULL && !strcmp(l->content, "a") && x->next == NULL);
	ft_lstclear(&l, del_free);
	NOLEAK();
}
''', notes=[NOTE_STRUCT],
       hints=["Il faut s'arreter sur le dernier noeud, pas apres lui : teste `lst->next`, pas `lst`.",
              "Commence par traiter le cas `lst == NULL`.",
              "`while (lst->next) lst = lst->next; return (lst);`"]))

# ---------------------------------------------------------------- niveau 2
add(ex("t_list *ft_lstnew(void *content)", 2,
       "Cree un nouveau noeud.",
       ["Alloue (`malloc`) un noeud `t_list`, met `content` dans le champ `content` et `NULL` dans `next`.",
        "Renvoie le noeud, ou `NULL` si `malloc` echoue.",
        "Ne copie pas `content` : tu ranges juste l'adresse recue."],
       [("ft_lstnew(\"hi\")", "noeud { content = \"hi\", next = NULL }")],
       COMMON + r'''
void run(void)
{
	void	*junk[8];
	int		i;
	int		x;
	t_list	*n;
	t_list	*m;

	i = 0;
	while (i < 8)
	{
		junk[i] = malloc(sizeof(t_list));
		memset(junk[i], 0xAA, sizeof(t_list));
		i++;
	}
	i = 0;
	while (i < 8)
		free(junk[i++]);
	x = 42;
	n = ft_lstnew(&x);
	CHECK("renvoie un noeud (pas NULL)", n != NULL);
	CHECK("content = l'adresse recue (pas une copie)", n && n->content == &x);
	CHECK("next vaut NULL (meme sur de la memoire reutilisee)", n && n->next == NULL);
	m = ft_lstnew(NULL);
	CHECK("content NULL accepte", m && m->content == NULL && m->next == NULL);
	CHECK("deux appels -> deux noeuds differents", n != m);
	free(n);
	free(m);
	NOLEAK();
	t_fail_nth(1);
	n = ft_lstnew(&x);
	t_fail_nth(0);
	CHECK("malloc qui echoue -> NULL", n == NULL);
}
''', allowed=["malloc"], notes=[NOTE_STRUCT],
       hints=["`malloc(sizeof(t_list))`, puis teste le retour.", "Initialise les DEUX champs : `content` ET `next`.",
              "`next` doit valoir `NULL` : un `malloc` ne met rien a zero tout seul."]))

add(ex("void ft_lstadd_front(t_list **lst, t_list *new)", 2,
       "Ajoute un noeud au debut de la liste.",
       ["`lst` est l'ADRESSE du pointeur de tete : on doit pouvoir changer la tete.",
        "Le nouveau noeud devient la tete ; son `next` pointe vers l'ancienne tete.",
        "Marche aussi avec une liste vide (`*lst == NULL`)."],
       [("ft_lstadd_front(&l, new)", "l == new, new->next == ancienne tete")],
       COMMON + r'''
void run(void)
{
	t_list	*l;
	t_list	*a;
	t_list	*b;
	t_list	*c;

	a = node("a");
	b = node("b");
	c = node("c");
	l = NULL;
	ft_lstadd_front(&l, a);
	CHECK("liste vide : le noeud devient la tete", l == a);
	CHECK("liste vide : next reste NULL", a->next == NULL);
	ft_lstadd_front(&l, b);
	CHECK("la tete devient le nouveau noeud", l == b);
	CHECK("l'ancienne tete est derriere : b->next == a", b->next == a);
	ft_lstadd_front(&l, c);
	CHECK("ordre final c -> b -> a", l == c && c->next == b && b->next == a && a->next == NULL);
	CHECK("les contenus ne sont pas touches", !strcmp(c->content, "c") && !strcmp(a->content, "a"));
	ft_lstclear(&l, del_free);
	NOLEAK();
}
''', notes=[NOTE_STRUCT],
       hints=["Deux pointeurs : `lst` (adresse de la tete) et `*lst` (la tete elle-meme).",
              "D'abord `new->next = *lst;` (le nouveau pointe sur l'ancienne tete).",
              "Ensuite `*lst = new;` (la tete devient le nouveau). L'ordre compte !"]))

add(ex("void ft_lstadd_back(t_list **lst, t_list *new)", 2,
       "Ajoute un noeud a la fin de la liste.",
       ["Place `new` apres le dernier noeud de la liste.",
        "Si la liste est vide (`*lst == NULL`), `new` devient la tete : c'est pour ca que `lst` est un `t_list **`.",
        "Tu peux reutiliser `ft_lstlast`."],
       [("ft_lstadd_back(&l, new)", "new est le dernier noeud")],
       COMMON + r'''
void run(void)
{
	t_list	*l;
	t_list	*a;
	t_list	*b;
	t_list	*c;

	a = node("a");
	b = node("b");
	c = node("c");
	l = NULL;
	ft_lstadd_back(&l, a);
	CHECK("liste vide : le noeud devient la tete", l == a);
	ft_lstadd_back(&l, b);
	CHECK("la tete ne change pas : l == a", l == a);
	CHECK("a->next == b et b->next == NULL", a->next == b && b->next == NULL);
	ft_lstadd_back(&l, c);
	CHECK("ordre final a -> b -> c", a->next == b && b->next == c && c->next == NULL);
	ft_lstclear(&l, del_free);
	l = chain(50);
	a = node("z");
	ft_lstadd_back(&l, a);
	CHECK("liste de 50 + 1 : le dernier est le nouveau noeud", ft_lstlast(l) == a);
	CHECK("liste de 50 + 1 : 51 noeuds", ft_lstsize(l) == 51);
	CHECK("le debut de liste est inchange", !strcmp(l->content, "a"));
	ft_lstclear(&l, del_free);
	NOLEAK();
}
''', notes=[NOTE_STRUCT],
       hints=["Deux cas : liste vide (`*lst == NULL`) et liste non vide.",
              "Liste vide : `*lst = new;` et c'est fini.",
              "Sinon : `ft_lstlast(*lst)->next = new;`."]))

add(ex("void ft_lstiter(t_list *lst, void (*f)(void *))", 2,
       "Applique une fonction au contenu de chaque noeud.",
       ["Parcourt la liste et appelle `f(noeud->content)` pour chaque noeud, dans l'ordre.",
        "La liste elle-meme (les noeuds) n'est pas modifiee, seul `f` peut modifier les contenus."],
       [("ft_lstiter(l, f)", "f appelee une fois par noeud, de la tete a la fin")],
       COMMON + r'''
static int	g_order[8];
static int	g_n;

static void	rec(void *p)
{
	g_order[g_n++] = *(int *)p;
	*(int *)p += 100;
}

void run(void)
{
	int		v[4];
	t_list	*n[4];
	int		i;

	i = 0;
	while (i < 4)
	{
		v[i] = i + 1;
		n[i] = malloc(sizeof(t_list));
		n[i]->content = &v[i];
		n[i]->next = NULL;
		if (i > 0)
			n[i - 1]->next = n[i];
		i++;
	}
	ft_lstiter(n[0], rec);
	CHECK("f est appelee 4 fois (une par noeud)", g_n == 4);
	CHECK("dans l'ordre de la liste : 1, 2, 3, 4", g_order[0] == 1 && g_order[1] == 2 && g_order[2] == 3 && g_order[3] == 4);
	CHECK("f a bien recu les contenus (ils ont ete modifies)", v[0] == 101 && v[3] == 104);
	CHECK("le chainage est intact", n[0]->next == n[1] && n[2]->next == n[3] && n[3]->next == NULL);
	g_n = 0;
	ft_lstiter(NULL, rec);
	CHECK("liste vide : f n'est jamais appelee", g_n == 0);
	i = 0;
	while (i < 4)
		free(n[i++]);
	NOLEAK();
}
''', notes=[NOTE_STRUCT],
       hints=["`while (lst) { f(lst->content); lst = lst->next; }`",
              "On passe a `f` le CONTENU (`lst->content`), pas le noeud.",
              "Cas liste vide : la boucle ne s'execute pas, rien d'autre a faire."]))

# ---------------------------------------------------------------- niveau 3
add(ex("void ft_lstdelone(t_list *lst, void (*del)(void *))", 3,
       "Supprime un seul noeud (son contenu puis le noeud).",
       ["Appelle `del(lst->content)` pour liberer le contenu, puis libere le noeud lui-meme avec `free`.",
        "Ne libere PAS les noeuds suivants et ne touche pas a `next`.",
        "Tu ne sais pas ce que contient le noeud : c'est `del` qui sait le liberer."],
       [("ft_lstdelone(node, free)", "contenu et noeud liberes, la suite de la liste reste valide")],
       COMMON + r'''
void run(void)
{
	t_list	*a;
	t_list	*b;
	void	*ca;

	a = node("a");
	b = node("b");
	a->next = b;
	ca = a->content;
	ft_lstdelone(a, del_free);
	CHECK("del est appelee exactement une fois", g_del == 1);
	CHECK("del recoit le content du noeud supprime", g_last == ca);
	CHECK("le noeud suivant n'est PAS libere", !strcmp(b->content, "b") && b->next == NULL);
	CHECK("le noeud suivant n'a pas ete passe a del", g_del == 1);
	ft_lstdelone(b, del_free);
	CHECK("deuxieme noeud : del appelee (2 au total)", g_del == 2);
	NOLEAK();
}
''', allowed=["free"], notes=[NOTE_STRUCT],
       hints=["Deux liberations : le contenu (via `del`) ET le noeud (via `free`).",
              "Ordre : `del(lst->content);` puis `free(lst);` (apres, `lst->content` n'existe plus).",
              "Ne regarde jamais `lst->next` : ce n'est pas ton travail ici."]))

add(ex("void ft_lstclear(t_list **lst, void (*del)(void *))", 3,
       "Supprime et libere tous les noeuds d'une liste.",
       ["Pour chaque noeud (tete jusqu'a la fin) : `del` sur le contenu, puis `free` du noeud.",
        "A la fin, `*lst` doit valoir `NULL`.",
        "Pense a retenir `next` AVANT de liberer le noeud. Tu peux reutiliser `ft_lstdelone`."],
       [("ft_lstclear(&l, free)", "plus aucun noeud, l == NULL")],
       COMMON + r'''
static void	mark(void *p)
{
	g_del++;
	(*(int *)p)++;
}

void run(void)
{
	int		v[5];
	t_list	*l;
	t_list	*x;
	int		i;

	l = NULL;
	i = 0;
	while (i < 5)
	{
		v[i] = 0;
		x = malloc(sizeof(t_list));
		x->content = &v[i];
		x->next = l;
		l = x;
		i++;
	}
	ft_lstclear(&l, mark);
	CHECK("del est appelee 5 fois (une par noeud)", g_del == 5);
	CHECK("chaque contenu est traite exactement une fois", v[0] == 1 && v[1] == 1 && v[2] == 1 && v[3] == 1 && v[4] == 1);
	CHECK("*lst vaut NULL apres l'appel", l == NULL);
	CHECK("tous les noeuds sont liberes (pas de fuite)", t_live() == 0);
	g_del = 0;
	ft_lstclear(&l, mark);
	CHECK("liste deja vide : aucun appel de del, pas de crash", g_del == 0 && l == NULL);
	l = chain(3);
	g_del = 0;
	ft_lstclear(&l, del_free);
	CHECK("contenus alloues : 3 appels de del", g_del == 3);
	CHECK("*lst vaut NULL", l == NULL);
	NOLEAK();
}
''', allowed=["free"], notes=[NOTE_STRUCT],
       hints=["Boucle : `while (*lst)`. A chaque tour, garde `next = (*lst)->next;`.",
              "Libere le noeud courant avec `ft_lstdelone(*lst, del)`, puis avance : `*lst = next;`.",
              "A la sortie de la boucle `*lst` vaut deja `NULL` : c'est ce que demande le sujet."]))

# ---------------------------------------------------------------- niveau 4
add(ex("t_list *ft_lstmap(t_list *lst, void *(*f)(void *), void (*del)(void *))", 4,
       "Cree une nouvelle liste en appliquant une fonction a chaque contenu.",
       ["Parcourt `lst`, appelle `f(content)` pour chaque noeud et range le resultat dans un NOUVEAU noeud : la liste d'origine n'est pas modifiee.",
        "Renvoie la nouvelle liste (meme ordre).",
        "Si une allocation echoue : libere tout ce qui a deja ete cree (nouveaux noeuds ET le contenu produit par `f` qu'on n'a pas pu ranger, avec `del`), puis renvoie `NULL`.",
        "Tu peux utiliser `ft_lstnew`, `ft_lstadd_back` et `ft_lstclear`."],
       [("ft_lstmap(\"ab\" -> \"cd\", to_upper, free)", "\"AB\" -> \"CD\" (nouvelle liste)")],
       COMMON + r'''
static int	g_f;

static void	*up(void *p)
{
	char	*r;
	size_t	i;

	g_f++;
	t_nofail(1);
	r = malloc(strlen(p) + 1);
	t_nofail(0);
	i = 0;
	while (((char *)p)[i])
	{
		r[i] = ((char *)p)[i] - (((char *)p)[i] >= 'a' && ((char *)p)[i] <= 'z') * 32;
		i++;
	}
	r[i] = '\0';
	return (r);
}

static t_list	*orig(void)
{
	t_list	*l;

	l = node("ab");
	l->next = node("cd");
	l->next->next = node("ef");
	return (l);
}

static int	same(t_list *l, const char *a, const char *b, const char *c)
{
	return (l && !strcmp(l->content, a) && l->next && !strcmp(l->next->content, b)
		&& l->next->next && !strcmp(l->next->next->content, c) && l->next->next->next == NULL);
}

void run(void)
{
	t_list	*l;
	t_list	*r;
	int		base;
	int		k;
	int		bad;
	int		leak;
	int		intact;

	l = orig();
	r = ft_lstmap(l, up, del_free);
	CHECK("renvoie une liste de 3 noeuds avec f appliquee : AB, CD, EF", same(r, "AB", "CD", "EF"));
	CHECK("f est appelee une fois par noeud", g_f == 3);
	CHECK("la liste d'origine n'est pas modifiee", same(l, "ab", "cd", "ef"));
	CHECK("ce sont de NOUVEAUX noeuds", r && r != l && r->next != l->next);
	CHECK("del n'est pas appelee quand tout se passe bien", g_del == 0);
	ft_lstclear(&r, del_free);
	g_f = 0;
	CHECK("liste vide -> NULL, f jamais appelee", ft_lstmap(NULL, up, del_free) == NULL && g_f == 0);
	base = t_live();
	bad = 0;
	leak = 0;
	intact = 1;
	k = 1;
	while (k <= 3)
	{
		t_fail_nth(k);
		r = ft_lstmap(l, up, del_free);
		t_fail_nth(0);
		if (r != NULL)
			bad = 1;
		if (t_live() != base)
			leak = 1;
		if (!same(l, "ab", "cd", "ef"))
			intact = 0;
		ft_lstclear(&r, del_free);
		k++;
	}
	CHECK("malloc qui echoue (1er, 2e ou 3e noeud) -> NULL", !bad);
	CHECK("apres un echec : rien n'a fuite (noeuds crees ET contenu de f)", !leak);
	CHECK("apres un echec : la liste d'origine est intacte", intact);
	ft_lstclear(&l, del_free);
	NOLEAK();
}
''', allowed=["malloc", "free"], notes=[NOTE_STRUCT],
       hints=["Pour chaque noeud : `content = f(lst->content);` puis `node = ft_lstnew(content);`.",
              "Si `node` vaut `NULL` : `del(content);` (il n'est dans aucune liste !) puis `ft_lstclear(&new_list, del);` puis `return (NULL);`.",
              "Sinon `ft_lstadd_back(&new_list, node);` et on avance dans `lst`. Ne touche jamais a la liste d'origine."]))
