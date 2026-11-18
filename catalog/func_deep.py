"""Explications approfondies « pourquoi on écrit ça » des cours fonction par fonction.
deep(id_fonction, ligne_de_depart, paragraphe, ...) : la ligne de depart est celle du debut d'un
bloc d'explication de func_courses.py (le 1er nombre du tuple). Un paragraphe qui contient un
retour a la ligne est affiche comme un schema (texte brut), les autres comme du texte."""
DEEP = {}


def deep(fid, a, *paras):
    DEEP.setdefault(fid, {})[a] = list(paras)


from . import func_deep_p1  # noqa: E402,F401
from . import func_deep_p2  # noqa: E402,F401
