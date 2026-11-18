/* Runtime des tests : compte les allocations, capture les ecritures sur un fd,
** fournit main(). Compile SANS trace.h (il appelle le vrai malloc). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>
#ifdef _WIN32
# include <io.h>
#endif

static int	g_live = 0;
static int	g_fail_in = 0;
static int	g_nofail = 0;
static int	g_total = 0;
static int	g_ko = 0;
static const char	*g_desc = "";
static int	g_wfd = -1;
static int	g_rfd = -1;

void	*t_malloc(size_t n)
{
	void	*p;

	if (!g_nofail && g_fail_in > 0 && --g_fail_in == 0)
		return (NULL);
	p = malloc(n);
	if (p)
		g_live++;
	return (p);
}

void	t_free(void *p)
{
	if (p)
		g_live--;
	free(p);
}

int		t_live(void) { return (g_live); }
void	t_fail_nth(int n) { g_fail_in = n; }
/* Les allocations faites par la fonction de test elle-meme (pas par le code de
** l'eleve) ne comptent pas pour t_fail_nth : voir les tests de ft_lstmap. */
void	t_nofail(int on) { g_nofail = on; }

void	check_begin(const char *desc)
{
	g_desc = desc;
	printf("C|%s\n", desc);
	fflush(stdout);
}

void	check_end(int ok, int line)
{
	g_total++;
	if (ok)
		printf("T|OK|%s\n", g_desc);
	else
	{
		g_ko++;
		printf("T|KO|%s|%d\n", g_desc, line);
	}
	fflush(stdout);
}

/* Ouvre un tube : l'eleve ecrit dans g_wfd (valeur retournee), on lit ensuite
** avec cap_read. Mode binaire : pas de conversion \n -> \r\n sous Windows. */
int		cap_open(void)
{
	int	fds[2];

#ifdef _WIN32
	if (_pipe(fds, 65536, _O_BINARY) != 0)
		return (-1);
#else
	if (pipe(fds) != 0)
		return (-1);
#endif
	g_rfd = fds[0];
	g_wfd = fds[1];
	return (g_wfd);
}

int		cap_read(char *buf, int max)
{
	int	n;

	close(g_wfd);
	n = read(g_rfd, buf, max - 1);
	if (n < 0)
		n = 0;
	buf[n] = '\0';
	close(g_rfd);
	return (n);
}

size_t	ref_strlcpy(char *dst, const char *src, size_t size)
{
	size_t	i;
	size_t	len;

	len = strlen(src);
	if (size == 0)
		return (len);
	i = 0;
	while (src[i] && i < size - 1)
	{
		dst[i] = src[i];
		i++;
	}
	dst[i] = '\0';
	return (len);
}

size_t	ref_strlcat(char *dst, const char *src, size_t size)
{
	size_t	dl;
	size_t	sl;
	size_t	i;

	dl = 0;
	while (dl < size && dst[dl])
		dl++;
	sl = strlen(src);
	if (dl == size)
		return (size + sl);
	i = 0;
	while (src[i] && dl + i < size - 1)
	{
		dst[dl + i] = src[i];
		i++;
	}
	dst[dl + i] = '\0';
	return (dl + sl);
}

char	*ref_strnstr(const char *h, const char *n, size_t len)
{
	size_t	nl;
	size_t	i;

	nl = strlen(n);
	if (nl == 0)
		return ((char *)h);
	i = 0;
	while (h[i] && i + nl <= len)
	{
		if (strncmp(h + i, n, nl) == 0)
			return ((char *)h + i);
		i++;
	}
	return (NULL);
}

void	run(void);

int		main(void)
{
	setvbuf(stdout, NULL, _IONBF, 0);
#ifdef _WIN32
	_setmode(_fileno(stdout), _O_BINARY);
#endif
	run();
	printf("S|%d|%d\n", g_total, g_ko);
	return (g_ko ? 1 : 0);
}
