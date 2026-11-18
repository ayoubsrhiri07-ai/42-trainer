/* Inclus de force (-include) dans le code de l'eleve, dans les solutions de
** reference et dans les tests : permet de compter les allocations (fuites)
** et de simuler un malloc qui echoue. */
#ifndef TRACE_H
# define TRACE_H

# include <stdlib.h>
# include <stddef.h>

void	*t_malloc(size_t n);
void	t_free(void *p);
int		t_live(void);
void	t_fail_nth(int n);
void	t_nofail(int on);

# define malloc(n) t_malloc(n)
# define free(p) t_free(p)

#endif
