#include "libft.h"
void	ft_lstdelone(t_list *lst, void (*del)(void *))
{
	if (lst->next)
		del(lst->next->content);
	del(lst->content);
	free(lst);
}
