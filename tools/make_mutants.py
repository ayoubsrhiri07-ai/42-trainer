"""Genere des solutions volontairement FAUSSES (mutants). selftest.py verifie que
chacune est refusee par la moulinette : c'est le test des tests."""
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mutants")
os.makedirs(OUT, exist_ok=True)

M = {}

M["ft_isalpha__borne"] = '''#include "libft.h"
int\tft_isalpha(int c)
{
\tif ((c > 'A' && c <= 'Z') || (c >= 'a' && c <= 'z'))
\t\treturn (1);
\treturn (0);
}
'''
M["ft_isdigit__tout"] = '''#include "libft.h"
int\tft_isdigit(int c)
{
\tif (c >= '0')
\t\treturn (1);
\treturn (0);
}
'''
M["ft_toupper__tout"] = '''#include "libft.h"
int\tft_toupper(int c)
{
\tif (c >= 'a')
\t\treturn (c - 32);
\treturn (c);
}
'''
M["ft_strlen__plus1"] = '''#include "libft.h"
size_t\tft_strlen(const char *s)
{
\tsize_t\ti;

\ti = 0;
\twhile (s[i])
\t\ti++;
\treturn (i + 1);
}
'''
M["ft_strlen__protomismatch"] = '''int\tft_strlen(char *str)
{
\tint\ti;

\ti = 0;
\twhile (str[i])
\t\ti++;
\treturn (i);
}
'''
M["ft_bzero__debord"] = '''#include "libft.h"
void\tft_bzero(void *s, size_t n)
{
\tsize_t\ti;

\ti = 0;
\twhile (i <= n)
\t{
\t\t((unsigned char *)s)[i] = 0;
\t\ti++;
\t}
}
'''
M["ft_memset__pasderet"] = '''#include "libft.h"
void\t*ft_memset(void *s, int c, size_t n)
{
\tsize_t\ti;

\ti = 0;
\twhile (i < n)
\t{
\t\t((unsigned char *)s)[i] = (unsigned char)c;
\t\ti++;
\t}
\treturn (NULL);
}
'''
M["ft_memcpy__moins1"] = '''#include "libft.h"
void\t*ft_memcpy(void *dest, const void *src, size_t n)
{
\tsize_t\ti;

\ti = 0;
\twhile (i + 1 < n)
\t{
\t\t((unsigned char *)dest)[i] = ((unsigned char *)src)[i];
\t\ti++;
\t}
\treturn (dest);
}
'''
M["ft_memmove__avant"] = '''#include "libft.h"
void\t*ft_memmove(void *dest, const void *src, size_t n)
{
\tsize_t\ti;

\ti = 0;
\twhile (i < n)
\t{
\t\t((unsigned char *)dest)[i] = ((unsigned char *)src)[i];
\t\ti++;
\t}
\treturn (dest);
}
'''
M["ft_strchr__pasdenul"] = '''#include "libft.h"
char\t*ft_strchr(const char *s, int c)
{
\twhile (*s)
\t{
\t\tif (*s == (char)c)
\t\t\treturn ((char *)s);
\t\ts++;
\t}
\treturn (NULL);
}
'''
M["ft_strrchr__premiere"] = '''#include "libft.h"
char\t*ft_strrchr(const char *s, int c)
{
\twhile (*s)
\t{
\t\tif (*s == (char)c)
\t\t\treturn ((char *)s);
\t\ts++;
\t}
\tif (c == 0)
\t\treturn ((char *)s);
\treturn (NULL);
}
'''
M["ft_strncmp__signe"] = '''#include "libft.h"
int\tft_strncmp(const char *s1, const char *s2, size_t n)
{
\tsize_t\ti;

\ti = 0;
\twhile (i < n && (s1[i] || s2[i]))
\t{
\t\tif (s1[i] != s2[i])
\t\t\treturn (s1[i] - s2[i]);
\t\ti++;
\t}
\treturn (0);
}
'''
M["ft_memchr__nul"] = '''#include "libft.h"
void\t*ft_memchr(const void *s, int c, size_t n)
{
\tsize_t\ti;
\tconst unsigned char\t*p;

\tp = (const unsigned char *)s;
\ti = 0;
\twhile (i < n && p[i])
\t{
\t\tif (p[i] == (unsigned char)c)
\t\t\treturn ((void *)(p + i));
\t\ti++;
\t}
\treturn (NULL);
}
'''
M["ft_memcmp__signe"] = '''#include "libft.h"
int\tft_memcmp(const void *s1, const void *s2, size_t n)
{
\tsize_t\ti;
\tconst char\t*a;
\tconst char\t*b;

\ta = s1;
\tb = s2;
\ti = 0;
\twhile (i < n)
\t{
\t\tif (a[i] != b[i])
\t\t\treturn (a[i] - b[i]);
\t\ti++;
\t}
\treturn (0);
}
'''
M["ft_strlcpy__retour"] = '''#include "libft.h"
size_t\tft_strlcpy(char *dst, const char *src, size_t size)
{
\tsize_t\ti;

\ti = 0;
\tif (size == 0)
\t\treturn (0);
\twhile (src[i] && i < size - 1)
\t{
\t\tdst[i] = src[i];
\t\ti++;
\t}
\tdst[i] = '\\0';
\treturn (i);
}
'''
M["ft_strlcat__retour"] = '''#include "libft.h"
size_t\tft_strlcat(char *dst, const char *src, size_t size)
{
\tsize_t\tdl;
\tsize_t\ti;

\tdl = ft_strlen(dst);
\ti = 0;
\twhile (src[i] && dl + i + 1 < size)
\t{
\t\tdst[dl + i] = src[i];
\t\ti++;
\t}
\tif (dl < size)
\t\tdst[dl + i] = '\\0';
\treturn (dl + ft_strlen(src));
}
'''
M["ft_strnstr__debord"] = '''#include "libft.h"
char\t*ft_strnstr(const char *big, const char *little, size_t len)
{
\tsize_t\ti;
\tsize_t\tj;

\tif (!*little)
\t\treturn ((char *)big);
\ti = 0;
\twhile (big[i] && i < len)
\t{
\t\tj = 0;
\t\twhile (big[i + j] && big[i + j] == little[j])
\t\t\tj++;
\t\tif (!little[j])
\t\t\treturn ((char *)big + i);
\t\ti++;
\t}
\treturn (NULL);
}
'''
M["ft_atoi__espaces"] = '''#include "libft.h"
int\tft_atoi(const char *nptr)
{
\tint\ti;
\tint\ts;
\tint\tr;

\ti = 0;
\ts = 1;
\tr = 0;
\twhile (nptr[i] == ' ')
\t\ti++;
\tif (nptr[i] == '-' || nptr[i] == '+')
\t{
\t\tif (nptr[i] == '-')
\t\t\ts = -1;
\t\ti++;
\t}
\twhile (nptr[i] >= '0' && nptr[i] <= '9')
\t\tr = r * 10 + nptr[i++] - '0';
\treturn (r * s);
}
'''
M["ft_calloc__debord"] = '''#include "libft.h"
void\t*ft_calloc(size_t nmemb, size_t size)
{
\tvoid\t*p;

\tp = malloc(nmemb * size);
\tif (!p)
\t\treturn (NULL);
\tft_bzero(p, nmemb * size);
\treturn (p);
}
'''
M["ft_calloc__pasdezero"] = '''#include "libft.h"
void\t*ft_calloc(size_t nmemb, size_t size)
{
\tif (nmemb != 0 && size > SIZE_MAX / nmemb)
\t\treturn (NULL);
\treturn (malloc(nmemb * size));
}
'''
M["ft_strdup__memecopie"] = '''#include "libft.h"
char\t*ft_strdup(const char *s)
{
\treturn ((char *)s);
}
'''
M["ft_substr__null"] = '''#include "libft.h"
char\t*ft_substr(char const *s, unsigned int start, size_t len)
{
\tchar\t*r;
\tsize_t\ti;

\tif (start >= ft_strlen(s))
\t\treturn (NULL);
\tif (len > ft_strlen(s) - start)
\t\tlen = ft_strlen(s) - start;
\tr = malloc(len + 1);
\tif (!r)
\t\treturn (NULL);
\ti = 0;
\twhile (i < len)
\t{
\t\tr[i] = s[start + i];
\t\ti++;
\t}
\tr[i] = '\\0';
\treturn (r);
}
'''
M["ft_strjoin__piscine"] = '''#include "libft.h"
char\t*ft_strjoin(int size, char **strs, char *sep)
{
\t(void)size;
\t(void)strs;
\t(void)sep;
\treturn (NULL);
}
'''
M["ft_strtrim__debut"] = '''#include "libft.h"
char\t*ft_strtrim(char const *s1, char const *set)
{
\tsize_t\tstart;

\tstart = 0;
\twhile (s1[start] && ft_strchr(set, s1[start]))
\t\tstart++;
\treturn (ft_substr(s1, start, ft_strlen(s1) - start));
}
'''
M["ft_split__fuite"] = '''#include "libft.h"
static int\tcount(const char *s, char c)
{
\tint\tn;
\tint\tin;

\tn = 0;
\tin = 0;
\twhile (*s)
\t{
\t\tif (*s != c && !in)
\t\t{
\t\t\tin = 1;
\t\t\tn++;
\t\t}
\t\telse if (*s == c)
\t\t\tin = 0;
\t\ts++;
\t}
\treturn (n);
}

char\t**ft_split(char const *s, char c)
{
\tchar\t**t;
\tint\t\ti;
\tint\t\tl;

\tt = malloc(sizeof(char *) * (count(s, c) + 1));
\tif (!t)
\t\treturn (NULL);
\ti = 0;
\twhile (*s)
\t{
\t\twhile (*s == c)
\t\t\ts++;
\t\tif (*s)
\t\t{
\t\t\tl = 0;
\t\t\twhile (s[l] && s[l] != c)
\t\t\t\tl++;
\t\t\tt[i] = ft_substr(s, 0, l);
\t\t\tif (!t[i])
\t\t\t\treturn (NULL);
\t\t\ti++;
\t\t\ts += l;
\t\t}
\t}
\tt[i] = NULL;
\treturn (t);
}
'''
M["ft_itoa__int"] = '''#include "libft.h"
char\t*ft_itoa(int n)
{
\tchar\t*r;
\tint\t\tlen;
\tint\t\tt;

\tlen = (n <= 0);
\tt = n;
\twhile (t)
\t{
\t\tt /= 10;
\t\tlen++;
\t}
\tr = malloc(len + 1);
\tif (!r)
\t\treturn (NULL);
\tr[len] = '\\0';
\tif (n < 0)
\t\tn = -n;
\tif (n == 0)
\t\tr[0] = '0';
\twhile (n)
\t{
\t\tr[--len] = n % 10 + '0';
\t\tn /= 10;
\t}
\tif (len == 1 && !r[0])
\t\tr[0] = '-';
\tif (len == 1)
\t\tr[0] = '-';
\treturn (r);
}
'''
M["ft_strmapi__pasdenul"] = '''#include "libft.h"
char\t*ft_strmapi(char const *s, char (*f)(unsigned int, char))
{
\tchar\t*r;
\tunsigned int\ti;

\tr = malloc(ft_strlen(s));
\tif (!r)
\t\treturn (NULL);
\ti = 0;
\twhile (s[i])
\t{
\t\tr[i] = f(i, s[i]);
\t\ti++;
\t}
\treturn (r);
}
'''
M["ft_striteri__indice"] = '''#include "libft.h"
void\tft_striteri(char *s, void (*f)(unsigned int, char *))
{
\tunsigned int\ti;

\ti = 1;
\twhile (s[i - 1])
\t{
\t\tf(i, &s[i - 1]);
\t\ti++;
\t}
}
'''
M["ft_putchar_fd__deux"] = '''#include "libft.h"
void\tft_putchar_fd(char c, int fd)
{
\twrite(fd, &c, 1);
\twrite(fd, &c, 1);
}
'''
M["ft_putstr_fd__retour"] = '''#include "libft.h"
void\tft_putstr_fd(char *s, int fd)
{
\twrite(fd, s, ft_strlen(s));
\twrite(fd, "\\n", 1);
}
'''
M["ft_putendl_fd__sansnl"] = '''#include "libft.h"
void\tft_putendl_fd(char *s, int fd)
{
\twrite(fd, s, ft_strlen(s));
}
'''
M["ft_putnbr_fd__intmin"] = '''#include "libft.h"
void\tft_putnbr_fd(int n, int fd)
{
\tif (n < 0)
\t{
\t\tft_putchar_fd('-', fd);
\t\tn = -n;
\t}
\tif (n >= 10)
\t\tft_putnbr_fd(n / 10, fd);
\tft_putchar_fd(n % 10 + '0', fd);
}
'''

# --- sujet v19.3 : retours exactement 1/0, calloc(0) ---------------------------------
M["ft_isalpha__nonun"] = '''#include "libft.h"
int\tft_isalpha(int c)
{
\tif ((c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z'))
\t\treturn (2);
\treturn (0);
}
'''
M["ft_isprint__valeurc"] = '''#include "libft.h"
int\tft_isprint(int c)
{
\tif (c >= 32 && c <= 126)
\t\treturn (c);
\treturn (0);
}
'''
M["ft_calloc__zero"] = '''#include "libft.h"
void\t*ft_calloc(size_t count, size_t size)
{
\tvoid\t*ptr;

\tif (count == 0 || size == 0)
\t\treturn (NULL);
\tif (size > SIZE_MAX / count)
\t\treturn (NULL);
\tptr = malloc(count * size);
\tif (!ptr)
\t\treturn (NULL);
\tft_bzero(ptr, count * size);
\treturn (ptr);
}
'''

# --- partie 3 : listes chainees --------------------------------------------------------
M["ft_lstnew__nextpoubelle"] = '''#include "libft.h"
t_list\t*ft_lstnew(void *content)
{
\tt_list\t*node;

\tnode = malloc(sizeof(t_list));
\tif (!node)
\t\treturn (NULL);
\tnode->content = content;
\treturn (node);
}
'''
M["ft_lstnew__contenunul"] = '''#include "libft.h"
t_list\t*ft_lstnew(void *content)
{
\tt_list\t*node;

\t(void)content;
\tnode = malloc(sizeof(t_list));
\tif (!node)
\t\treturn (NULL);
\tnode->content = NULL;
\tnode->next = NULL;
\treturn (node);
}
'''
M["ft_lstnew__pasdetest"] = '''#include "libft.h"
t_list\t*ft_lstnew(void *content)
{
\tt_list\t*node;

\tnode = malloc(sizeof(t_list));
\tnode->content = content;
\tnode->next = NULL;
\treturn (node);
}
'''
M["ft_lstadd_front__perdu"] = '''#include "libft.h"
void\tft_lstadd_front(t_list **lst, t_list *new)
{
\tnew->next = *lst;
}
'''
M["ft_lstadd_front__ordre"] = '''#include "libft.h"
void\tft_lstadd_front(t_list **lst, t_list *new)
{
\t*lst = new;
\tnew->next = new;
}
'''
M["ft_lstsize__protomismatch"] = '''#include "libft.h"
int\tft_lstsize(t_list *lst)
{
\tint\tn;

\tn = 0;
\twhile (lst)
\t{
\t\tn++;
\t\tlst = lst->next;
\t}
\treturn (n);
}
'''
M["ft_lstsize__decalage"] = '''#include "libft.h"
unsigned int\tft_lstsize(t_list *lst)
{
\tunsigned int\tn;

\tn = 0;
\tif (!lst)
\t\treturn (0);
\twhile (lst->next)
\t{
\t\tn++;
\t\tlst = lst->next;
\t}
\treturn (n);
}
'''
M["ft_lstlast__null"] = '''#include "libft.h"
t_list\t*ft_lstlast(t_list *lst)
{
\twhile (lst)
\t\tlst = lst->next;
\treturn (lst);
}
'''
M["ft_lstadd_back__vide"] = '''#include "libft.h"
void\tft_lstadd_back(t_list **lst, t_list *new)
{
\tft_lstlast(*lst)->next = new;
}
'''
M["ft_lstadd_back__tete"] = '''#include "libft.h"
void\tft_lstadd_back(t_list **lst, t_list *new)
{
\tif (!*lst)
\t\t*lst = new;
\telse
\t{
\t\tnew->next = *lst;
\t\t*lst = new;
\t}
}
'''
M["ft_lstdelone__fuite"] = '''#include "libft.h"
void\tft_lstdelone(t_list *lst, void (*del)(void *))
{
\tdel(lst->content);
}
'''
M["ft_lstdelone__sansdel"] = '''#include "libft.h"
void\tft_lstdelone(t_list *lst, void (*del)(void *))
{
\t(void)del;
\tfree(lst);
}
'''
M["ft_lstdelone__suite"] = '''#include "libft.h"
void\tft_lstdelone(t_list *lst, void (*del)(void *))
{
\tif (lst->next)
\t\tdel(lst->next->content);
\tdel(lst->content);
\tfree(lst);
}
'''
M["ft_lstclear__pasnull"] = '''#include "libft.h"
void\tft_lstclear(t_list **lst, void (*del)(void *))
{
\tt_list\t*cur;
\tt_list\t*next;

\tcur = *lst;
\twhile (cur)
\t{
\t\tnext = cur->next;
\t\tft_lstdelone(cur, del);
\t\tcur = next;
\t}
}
'''
M["ft_lstclear__premier"] = '''#include "libft.h"
void\tft_lstclear(t_list **lst, void (*del)(void *))
{
\tif (*lst)
\t\tft_lstdelone(*lst, del);
\t*lst = NULL;
}
'''
M["ft_lstiter__premier"] = '''#include "libft.h"
void\tft_lstiter(t_list *lst, void (*f)(void *))
{
\tif (lst)
\t\tf(lst->content);
}
'''
M["ft_lstmap__fuite"] = '''#include "libft.h"
t_list\t*ft_lstmap(t_list *lst, void *(*f)(void *), void (*del)(void *))
{
\tt_list\t*new_list;
\tt_list\t*node;

\t(void)del;
\tnew_list = NULL;
\twhile (lst)
\t{
\t\tnode = ft_lstnew(f(lst->content));
\t\tif (!node)
\t\t\treturn (NULL);
\t\tft_lstadd_back(&new_list, node);
\t\tlst = lst->next;
\t}
\treturn (new_list);
}
'''
M["ft_lstmap__contenu"] = '''#include "libft.h"
t_list\t*ft_lstmap(t_list *lst, void *(*f)(void *), void (*del)(void *))
{
\tt_list\t*new_list;
\tt_list\t*node;

\tnew_list = NULL;
\twhile (lst)
\t{
\t\tnode = ft_lstnew(f(lst->content));
\t\tif (!node)
\t\t{
\t\t\tft_lstclear(&new_list, del);
\t\t\treturn (NULL);
\t\t}
\t\tft_lstadd_back(&new_list, node);
\t\tlst = lst->next;
\t}
\treturn (new_list);
}
'''
M["ft_lstmap__modifie"] = '''#include "libft.h"
t_list\t*ft_lstmap(t_list *lst, void *(*f)(void *), void (*del)(void *))
{
\tt_list\t*cur;

\t(void)del;
\tcur = lst;
\twhile (cur)
\t{
\t\tcur->content = f(cur->content);
\t\tcur = cur->next;
\t}
\treturn (lst);
}
'''
M["ft_lstmap__inverse"] = '''#include "libft.h"
t_list\t*ft_lstmap(t_list *lst, void *(*f)(void *), void (*del)(void *))
{
\tt_list\t*new_list;
\tt_list\t*node;
\tvoid\t*content;

\tnew_list = NULL;
\twhile (lst)
\t{
\t\tcontent = f(lst->content);
\t\tnode = ft_lstnew(content);
\t\tif (!node)
\t\t{
\t\t\tdel(content);
\t\t\tft_lstclear(&new_list, del);
\t\t\treturn (NULL);
\t\t}
\t\tft_lstadd_front(&new_list, node);
\t\tlst = lst->next;
\t}
\treturn (new_list);
}
'''

for name, code in M.items():
    with open(os.path.join(OUT, name + ".c"), "w", encoding="utf-8", newline="\n") as f:
        f.write(code)
print(len(M), "mutants ecrits dans", OUT)
