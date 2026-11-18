#include "libft.h"
char	*ft_itoa(int n)
{
	char	*r;
	int		len;
	int		t;

	len = (n <= 0);
	t = n;
	while (t)
	{
		t /= 10;
		len++;
	}
	r = malloc(len + 1);
	if (!r)
		return (NULL);
	r[len] = '\0';
	if (n < 0)
		n = -n;
	if (n == 0)
		r[0] = '0';
	while (n)
	{
		r[--len] = n % 10 + '0';
		n /= 10;
	}
	if (len == 1 && !r[0])
		r[0] = '-';
	if (len == 1)
		r[0] = '-';
	return (r);
}
