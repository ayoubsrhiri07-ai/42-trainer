"""Auto-verification de 42 Trainer.

 1. Chaque solution de reference (runtime/ref) doit etre VALIDEE.
 2. Chaque mutant (tools/mutants/<exercice>__<nom>.c) doit etre REFUSE.
 3. Les cas de panne (segfault, boucle infinie, sortie infinie, erreur de
    compilation, erreur de norme) doivent rendre un verdict lisible vite.

Usage : python tools/selftest.py [id_exercice ...]
"""
import glob
import json
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import engine  # noqa: E402
from catalog import BY_ID, EXERCISES  # noqa: E402

CFG = {"login": "asrhiri", "email": "asrhiri@student.42.fr"}


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def summarize(r):
    st = r["steps"]
    t = st.get("tests") or {}
    return "norm=%s compile=%s forbidden=%s tests=%s/%s%s" % (
        st.get("norm", {}).get("ok"), st.get("compile", {}).get("ok"),
        st.get("forbidden", {}).get("ok"), t.get("passed"), t.get("total"),
        (" PROBLEM: " + t["problem"]) if t.get("problem") else "")


def main():
    engine.disable_crash_dialogs()
    only = set(sys.argv[1:])
    fails = 0
    print("outils :", engine.tools(CFG))
    print("== 1. solutions de reference ==")
    for ex in EXERCISES:
        if only and ex["id"] not in only:
            continue
        code = read(os.path.join(engine.REF_DIR, ex["file"]))
        t0 = time.time()
        r = engine.grade(ex, code, CFG, check_norm=True)
        ok = r.get("validated")
        print("%-5s %-16s %.1fs  %s" % ("OK" if ok else "FAIL", ex["id"], time.time() - t0, summarize(r)))
        if not ok:
            fails += 1
            if r.get("fatal"):
                print("   fatal:", r["fatal"])
            for c in (r["steps"].get("tests") or {}).get("cases", []):
                if not c["ok"]:
                    print("   KO:", c["desc"])
            for e in r["steps"].get("norm", {}).get("errors", [])[:5]:
                print("   norm:", e)
            print("   compile:", r["steps"].get("compile", {}).get("output", "")[:300])
    print("== 2. mutants (doivent etre refuses) ==")
    for path in sorted(glob.glob(os.path.join(ROOT, "tools", "mutants", "*.c"))):
        base = os.path.basename(path)[:-2]
        ex_id, _, label = base.partition("__")
        if ex_id not in BY_ID or (only and ex_id not in only):
            continue
        r = engine.grade(BY_ID[ex_id], read(path), CFG, check_norm=False)
        refused = not r.get("validated")
        print("%-5s %-16s %-22s %s" % ("OK" if refused else "FAIL", ex_id, label, summarize(r)))
        if not refused:
            fails += 1
    print("== 3. cas de panne ==")
    ex = BY_ID.get("ft_isalpha")
    if ex and (not only or "ft_isalpha" in only):
        hdr = engine.make_header("ft_isalpha.c", "asrhiri", "asrhiri@student.42.fr")
        cases = {
            "segfault": 'int\tft_isalpha(int c)\n{\n\tint\t*p;\n\n\tp = (int *)0;\n\treturn (*p + c);\n}\n',
            "boucle infinie": 'int\tft_isalpha(int c)\n{\n\twhile (1)\n\t\tc++;\n\treturn (c);\n}\n',
            "sortie infinie": '#include <stdio.h>\nint\tft_isalpha(int c)\n{\n\twhile (1)\n\t\twrite(1, "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", 38);\n\treturn (c);\n}\n',
            "erreur de compilation": 'int\tft_isalpha(int c)\n{\n\treturn (c +);\n}\n',
            "erreur de norme": 'int ft_isalpha(int c){return(c>=65&&c<=90||c>=97&&c<=122);}\n',
            "fonction interdite": 'int\tft_isalpha(int c)\n{\n\treturn (isalpha(c));\n}\n',
            "stack overflow": 'int\tft_isalpha(int c)\n{\n\treturn (ft_isalpha(c + 1) + 1);\n}\n',
        }
        for name, body in cases.items():
            code = hdr + '#include "libft.h"\n\n' + body
            t0 = time.time()
            r = engine.grade(ex, code, CFG, check_norm=True)
            dt = time.time() - t0
            fine = (not r.get("validated")) and dt < 20
            print("%-5s %-22s %.1fs  %s" % ("OK" if fine else "FAIL", name, dt, summarize(r)))
            if not fine:
                fails += 1
    left = [d for d in os.listdir(engine.RUNS)] if os.path.isdir(engine.RUNS) else []
    print("dossiers temporaires restants :", len(left))
    print("RESULTAT :", "tout est bon" if not fails and not left else "%d probleme(s)" % fails)
    return 1 if fails or left else 0


if __name__ == "__main__":
    sys.exit(main())
