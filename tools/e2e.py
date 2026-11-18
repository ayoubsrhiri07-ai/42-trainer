"""Test de bout en bout de l'API (serveur lance dans ce processus, donnees dans un
dossier temporaire : ta vraie progression n'est jamais touchee).   python tools/e2e.py"""
import json
import os
import sys
import tempfile
import threading
import time
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.environ["TRAINER_DATA"] = tempfile.mkdtemp(prefix="trainer_e2e_")
import engine  # noqa: E402
import server  # noqa: E402
from http.server import ThreadingHTTPServer  # noqa: E402

PORT = 4299
BAD = []


def call(path, body=None, expect=200):
    req = urllib.request.Request("http://127.0.0.1:%d/api/%s" % (PORT, path),
                                 data=None if body is None else json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json", "X-Trainer": "1"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            code, data = r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        code, data = e.code, json.loads(e.read().decode() or "{}")
    return code, data


def check(name, cond, detail=""):
    print(("OK   " if cond else "FAIL ") + name + ((" -> " + str(detail)) if not cond and detail else ""))
    if not cond:
        BAD.append(name)


def ref(ex_id):
    with open(os.path.join(engine.REF_DIR, ex_id + ".c"), encoding="utf-8") as f:
        return f.read()


def main():
    engine.disable_crash_dialogs()
    httpd = ThreadingHTTPServer(("127.0.0.1", PORT), server.Handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    try:
        # 1. XP de premiere validation + revision
        c, r = call("run", {"id": "ft_isalpha", "code": ref("ft_isalpha")})
        x = r.get("xp", {})
        check("ft_isalpha valide", r["result"]["validated"], r["result"]["steps"])
        check("XP premiere validation > 0 et detail present", x.get("gained", 0) > 0 and x.get("lines"), x)
        check("succes 'Premier sang'", any(a["id"] == "first_blood" for a in x.get("new_achievements", [])))
        c, r = call("run", {"id": "ft_isalpha", "code": ref("ft_isalpha")})
        check("revision : petit XP (>0, < XP de base)", 0 < r["xp"]["gained"] < 20 and not r["xp"]["first_time"], r.get("xp"))
        c, r = call("run", {"id": "ft_isalpha", "code": ref("ft_isalpha")})
        check("2e revision le meme jour : 0 XP", r["xp"]["gained"] == 0, r.get("xp"))
        # 2. indices
        c, r = call("hint", {"id": "ft_isdigit"})
        check("indice 1 renvoye", c == 200 and len(r["hints"]) == 1 and r["penalty"], r)
        c, r = call("run", {"id": "ft_isdigit", "code": ref("ft_isdigit")})
        lines = r["xp"]["lines"]
        check("penalite d'indice dans le detail XP", any("Indices" in n and v < 0 for n, v in lines), lines)
        # 3. echec : compteur, pas d'XP
        c, r = call("run", {"id": "ft_isprint", "code": "int ft_isprint(int c)\n{\n\treturn (c +);\n}\n"})
        check("code faux : non valide, pas d'XP", not r["result"]["validated"] and "xp" not in r)
        # 4. examen
        c, r = call("exam/start", {})
        cur = r["current"]
        check("examen demarre (niveau 1)", c == 200 and r["level"] == 1 and cur, r)
        c, _ = call("save", {"id": cur, "code": "PRACTICE_SECRET"})            # brouillon d'entrainement
        c, st = call("exam/start", {})
        check("le brouillon d'entrainement ne fuit pas dans l'examen", st.get("draft") in (None, ""), st.get("draft"))
        c, d = call("exercise/" + cur)
        check("brouillon d'entrainement conserve cote entrainement", d["draft"] == "PRACTICE_SECRET")
        c, _ = call("save", {"id": cur, "code": "EXAM_CODE", "exam": True})
        c, st = call("exam/start", {})
        check("brouillon d'examen separe", st.get("draft") == "EXAM_CODE")
        c, d = call("exercise/" + cur)
        check("... et n'ecrase pas le brouillon d'entrainement", d["draft"] == "PRACTICE_SECRET")
        c, r = call("hint", {"id": "ft_isalpha"})
        check("indice refuse pendant l'examen (400 + message)", c == 400 and r.get("error"), (c, r))
        bad = "int f(void)\n{\n\treturn (1 +);\n}\n"
        for i in range(3):
            c, r = call("run", {"id": cur, "code": bad, "exam": True})
        check("3 echecs : penalite active", r.get("exam_state", {}).get("cooldown", 0) > 0, r.get("exam_state"))
        c, r = call("run", {"id": cur, "code": ref(cur), "exam": True})
        check("pendant la penalite : 429 + delai", c == 429 and r.get("cooldown", 0) > 0, (c, r))
        with server.store.lock:        # on saute la penalite
            server.store.data["active_exam"]["cooldown_until"] = 0
        c, r = call("run", {"id": cur, "code": ref(cur), "exam": True})
        check("apres la penalite : valide et passe au niveau 2", r["result"]["validated"] and r["exam"]["advanced"], r.get("exam"))
        # 5. expiration
        with server.store.lock:
            server.store.data["active_exam"]["started"] -= 3 * 3600
        nxt = server.store.data["active_exam"]["current"]
        c, r = call("run", {"id": nxt, "code": ref(nxt), "exam": True})
        check("examen expire : soumission refusee", c == 400 and r.get("expired"), (c, r))
        xp0 = server.store.data["xp"]
        c, r = call("exam/finish", {})
        check("fin d'examen expire : 25 XP pour 1 niveau", c == 200 and r["result"]["validated"] == 1 and r["result"]["xp"] == 25, r)
        check("XP ajoute au total", server.store.data["xp"] == xp0 + 25)
        # 6. anti-farm : 3 examens/jour rapportent de l'XP, le 4e non
        gains = []
        for i in range(3):
            call("exam/start", {})
            c, r = call("exam/finish", {})
            gains.append(r["result"]["xp"])
        check("examens vides : 0 XP, le plafond du jour est atteint (3 examens deja faits)", gains[-1] == 0 and r["result"]["capped"], gains)
        # 6b. mode enchainement (partie 1 uniquement)
        c, r = call("chain/start", {})
        cur = r["current"]
        check("enchainement demarre sur un exercice de la partie 1", c == 200 and r["active"] and server.BY_ID[cur]["part"] == 1, r)
        c, r = call("chain/start", {})
        check("2e demarrage : meme enchainement (pas de doublon)", r["current"] == cur and r["n"] == 0)
        c, r = call("run", {"id": "ft_isalpha", "code": ref("ft_isalpha"), "chain": True})
        check("mauvais exercice dans l'enchainement : refuse", c == 400 or cur == "ft_isalpha", (c, r))
        seen = []
        for i in range(3):
            c, r = call("run", {"id": cur, "code": ref(cur), "chain": True})
            ok = r["result"]["validated"] and r["chain"]["active"]
            seen.append(cur)
            if not ok:
                break
            cur = r["chain"]["current"]
            check("enchainement #%d : valide, exercice suivant tire (partie 1, nouveau)" % (i + 1),
                  server.BY_ID[cur]["part"] == 1 and cur not in seen, r["chain"])
        c, r = call("chain/skip", {})
        c2, r2 = call("chain/skip", {})
        c3, r3 = call("chain/skip", {})
        check("2 passes autorisees, la 3e refusee", c == 200 and c2 == 200 and c3 == 400, (c, c2, c3))
        xp0 = server.store.data["xp"]
        c, r = call("chain/stop", {})
        check("fin d'enchainement : bonus pour 3 exercices = 30 XP", c == 200 and r["result"]["n"] == 3 and r["result"]["xp"] == 30, r)
        check("XP du bonus ajoute", server.store.data["xp"] == xp0 + 30)
        c, r = call("chain/stop", {})
        check("arreter sans enchainement : 400", c == 400)
        # 6c. cours et quiz
        from catalog import LESSONS
        c, lst = call("lessons")
        check("18 cours listes (dont les listes chainees, Makefile, memoire, debug)", c == 200 and len(lst) == len(LESSONS) >= 18
              and {"lists", "compile", "memory", "conv", "recursion", "debug"} <= {l["id"] for l in lst}, len(lst))
        check("tous les cours ont un niveau et une duree", all(l.get("level") and l.get("time") for l in lst), [l["id"] for l in lst if not l.get("level")])
        parts = {}
        for e in server.EXERCISES:
            parts[e["part"]] = parts.get(e["part"], 0) + 1
        check("catalogue v19.3 : 23 + 11 + 9 exercices (parties 1, 2, 3)", parts == {1: 23, 2: 11, 3: 9}, parts)
        from catalog import func_courses
        probs = func_courses.check([e["id"] for e in server.EXERCISES])
        check("cours fonction par fonction : 43 fonctions, toutes les lignes de code expliquees", not probs and len(func_courses.FUNCS) == 43, probs[:5])
        nodeep = [(x["id"], w[0]) for x in func_courses.FUNCS for w in x["walk"] if len(w) < 4 or not w[3]]
        check("chaque explication de ligne a son detail « pourquoi on ecrit ca »", not nodeep, nodeep[:5])
        c, fl = call("funcs")
        check("API /funcs : 43 cours", c == 200 and len(fl) == 43, c)
        c, fd = call("func/ft_split")
        check("API /func/ft_split : code, explications, voisins", c == 200 and fd["code"] and fd["walk"] and fd["prev"] and fd["next"], fd.get("prev"))
        c, _ = call("func/inconnu")
        check("cours de fonction inconnu : 404", c == 404)
        L = LESSONS[0]
        c, d = call("lesson/" + L["id"])
        check("le detail du cours ne contient PAS les reponses", c == 200 and "answer" not in json.dumps(d) and "explain" not in json.dumps(d))
        wrong = [(q["answer"] + 1) % len(q["choices"]) for q in L["quiz"]]
        xp0 = server.store.data["xp"]
        c, r = call("quiz", {"id": L["id"], "answers": wrong})
        check("quiz faux : pas d'XP, explications renvoyees", c == 200 and not r["perfect"] and r["gained"] == 0 and r["results"][0]["explain"], r)
        right = [q["answer"] for q in L["quiz"]]
        c, r = call("quiz", {"id": L["id"], "answers": right})
        check("quiz parfait : +15 XP", r["perfect"] and r["gained"] == 15 and server.store.data["xp"] == xp0 + 15, r)
        c, r = call("quiz", {"id": L["id"], "answers": right})
        check("quiz deja reussi : 0 XP", r["perfect"] and r["gained"] == 0)
        c, r = call("quiz", {"id": L["id"], "answers": [1]})
        check("reponses invalides : 400", c == 400)
        # 7. securite
        c, r = call("run", {"id": "../../etc", "code": "x"})
        check("id d'exercice invalide : 404", c == 404)
        c, r = call("run", {"id": "ft_isalpha", "code": "x" * 70000})
        check("code trop long : 400", c == 400)
    finally:
        httpd.shutdown()
    left = os.listdir(engine.RUNS) if os.path.isdir(engine.RUNS) else []
    check("aucun dossier temporaire restant", not left, left)
    print("RESULTAT :", "tout est bon" if not BAD else "%d echec(s) : %s" % (len(BAD), BAD))
    return 1 if BAD else 0


if __name__ == "__main__":
    sys.exit(main())
