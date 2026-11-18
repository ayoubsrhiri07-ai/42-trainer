from . import libft_p1, libft_p2, libft_p3

from .lessons import LESSONS, LESSONS_BY_ID  # noqa: F401
from . import lessons_more  # noqa: F401  (approfondit les cours, ajoute de nouveaux cours, fixe l'ordre)

EXERCISES = libft_p1.EXERCISES + libft_p2.EXERCISES + libft_p3.EXERCISES
BY_ID = {e["id"]: e for e in EXERCISES}
