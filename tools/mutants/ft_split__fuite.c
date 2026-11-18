#include "libft.h"
static int	count(const char *s, char c)
{
	int	n;
	int	in;

	n = 0;
	in = 0;
	while (*s)
	{
		if (*s != c && !in)
		{
			in = 1;
			n++;
		}
		else if (*s == c)
			in = 0;
		s++;
	}
	return (n);
}

char	**ft_split(char const *s, char c)
{
	char	**t;
	int		i;
	int		l;

	t = malloc(sizeof(char *) * (count(s, c) + 1));
	if (!t)
		return (NULL);
	i = 0;
	while (*s)
	{
		while (*s == c)
			s++;
		if (*s)
		{
			l = 0;
			while (s[l] && s[l] != c)
				l++;
			t[i] = ft_substr(s, 0, l);
			if (!t[i])
				return (NULL);
			i++;
			s += l;
		}
	}
	t[i] = NULL;
	return (t);
}
