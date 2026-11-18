#include "libft.h"
t_list	*ft_lstmap(t_list *lst, void *(*f)(void *), void (*del)(void *))
{
	t_list	*cur;

	(void)del;
	cur = lst;
	while (cur)
	{
		cur->content = f(cur->content);
		cur = cur->next;
	}
	return (lst);
}
