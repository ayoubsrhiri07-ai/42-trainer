import re

XP_BY_LEVEL = {1: 20, 2: 35, 3: 55, 4: 80}
_NAME_RE = re.compile(r"(ft_\w+)\(")


def ex(proto, level, summary, details, examples, tests, allowed=(), hints=(), notes=(),
       part=1, xp=None, timeout=5, title=None):
    """Construit la fiche d'un exercice.

    proto    : prototype exact, ex. "char *ft_strchr(const char *s, int c)"
    level    : 1 (facile) .. 4 (difficile), sert aussi au mode examen
    tests    : code C d'une fonction `void run(void)` utilisant CHECK(...)
    allowed  : fonctions externes autorisees (en plus des fonctions ft_ de ta libft)
    """
    name = _NAME_RE.search(proto).group(1)
    return {
        "id": name,
        "title": title or name,
        "file": name + ".c",
        "proto": proto,
        "part": part,
        "level": level,
        "xp": xp or XP_BY_LEVEL[level],
        "summary": summary,
        "details": list(details),
        "examples": [{"call": c, "result": r} for c, r in examples],
        "allowed": list(allowed),
        "notes": list(notes),
        "hints": list(hints),
        "tests": tests,
        "timeout": timeout,
    }
