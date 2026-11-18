/* Petit framework de test pour 42 Trainer.
** Chaque test ecrit des lignes lisibles par le serveur :
**   C|<description>          debut d'un cas (utile pour localiser un crash)
**   T|OK|<description>       cas reussi
**   T|KO|<description>|<ligne> cas rate
*/
#ifndef HARNESS_H
# define HARNESS_H

# include <stdio.h>
# include <string.h>
# include <limits.h>
# include <stddef.h>
# include "trace.h"
# include "libft.h"

void	check_begin(const char *desc);
void	check_end(int ok, int line);
int		cap_open(void);
int		cap_read(char *buf, int max);

# define CHECK(desc, cond) \
	do { check_begin(desc); check_end((cond) ? 1 : 0, __LINE__); } while (0)

# define NOLEAK() CHECK("aucune fuite memoire", t_live() == 0)

/* Valeur de reference BSD (absentes de la libc MinGW) */
size_t	ref_strlcpy(char *dst, const char *src, size_t size);
size_t	ref_strlcat(char *dst, const char *src, size_t size);
char	*ref_strnstr(const char *h, const char *n, size_t len);

void	run(void);

#endif
