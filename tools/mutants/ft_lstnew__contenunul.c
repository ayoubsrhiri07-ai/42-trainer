#include "libft.h"
t_list	*ft_lstnew(void *content)
{
	t_list	*node;

	(void)content;
	node = malloc(sizeof(t_list));
	if (!node)
		return (NULL);
	node->content = NULL;
	node->next = NULL;
	return (node);
}
