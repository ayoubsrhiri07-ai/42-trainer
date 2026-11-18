#include "libft.h"
char	*ft_strtrim(char const *s1, char const *set)
{
	size_t	start;

	start = 0;
	while (s1[start] && ft_strchr(set, s1[start]))
		start++;
	return (ft_substr(s1, start, ft_strlen(s1) - start));
}
