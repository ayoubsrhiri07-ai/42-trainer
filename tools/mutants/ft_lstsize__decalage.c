#include "libft.h"
unsigned int	ft_lstsize(t_list *lst)
{
	unsigned int	n;

	n = 0;
	if (!lst)
		return (0);
	while (lst->next)
	{
		n++;
		lst = lst->next;
	}
	return (n);
}
