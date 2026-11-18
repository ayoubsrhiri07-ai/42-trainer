#include "libft.h"
size_t	ft_strlcat(char *dst, const char *src, size_t size)
{
	size_t	dl;
	size_t	i;

	dl = ft_strlen(dst);
	i = 0;
	while (src[i] && dl + i + 1 < size)
	{
		dst[dl + i] = src[i];
		i++;
	}
	if (dl < size)
		dst[dl + i] = '\0';
	return (dl + ft_strlen(src));
}
