"""Serveur local de 42 Trainer (stdlib uniquement, ecoute sur 127.0.0.1 seulement).

    python server.py            demarre et ouvre le navigateur
    python server.py --no-open  demarre sans ouvrir le navigateur
"""
import json
import mimetypes
import os
import re
import sys
import threading
import time
import urllib.request
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import engine
import game
from catalog import BY_ID, EXERCISES, LESSONS, LESSONS_BY_ID
from catalog import func_courses

game.LESSON_COUNT["n"] = len(LESSONS)

BASE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.join(BASE, "web")
DATA = game.DATA
CFG_PATH = os.path.join(DATA, "config.json")
IDEAS_PATH = os.path.join(DATA, "ideas.json")
APP = "42-trainer"
PORTS = [int(os.environ["TRAINER_PORT"])] if os.environ.get("TRAINER_PORT") else list(range(4242, 4262))
MAX_BODY = 256 * 1024

store = game.Store()
grade_sem = threading.Semaphore(2)
file_lock = threading.Lock()


# ------------------------------------------------------------------ config / ideas
def load_json(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return default


def save_json(path, obj):
    os.makedirs(DATA, exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
    os.replace(tmp, path)


def get_cfg():
    cfg = {"login": "asrhiri", "email": "asrhiri@student.42.fr"}
    cfg.update(load_json(CFG_PATH, {}))
    return cfg


# ------------------------------------------------------------------ vues
def exercise_summary(e, st):
    status = "solved" if st and st.get("solved") else ("tried" if st and st.get("attempts") else "new")
    return {"id": e["id"], "title": e["title"], "part": e["part"], "level": e["level"], "xp": e["xp"],
            "proto": e["proto"], "summary": e["summary"], "status": status,
            "attempts": st.get("attempts", 0) if st else 0, "best": st.get("best", 0) if st else 0}


def build_state():
    d = store.data
    with store.lock:
        solved = {k for k, v in d["exercises"].items() if v.get("solved")}
        parts = {}
        for e in EXERCISES:
            p = parts.setdefault(str(e["part"]), {"solved": 0, "total": 0})
            p["total"] += 1
            p["solved"] += e["id"] in solved
        levels = {}
        for e in EXERCISES:
            p = levels.setdefault(str(e["level"]), {"solved": 0, "total": 0})
            p["total"] += 1
            p["solved"] += e["id"] in solved
        daily_id = game.daily_exercise(store, EXERCISES)
        history = []
        import datetime
        for i in range(13, -1, -1):
            day = (datetime.date.today() - datetime.timedelta(days=i)).isoformat()
            v = d["days"].get(day, {})
            history.append({"date": day, "xp": v.get("xp", 0), "solved": len(v.get("solved", []))})
        recommended = next((e["id"] for e in sorted(EXERCISES, key=lambda x: (x["level"], x["part"]))
                            if e["id"] not in solved), None)
        ach = [{"id": a[0], "title": a[1], "desc": a[2], "icon": a[3],
                "unlocked": a[0] in d["achievements"], "at": d["achievements"].get(a[0])}
               for a in game.ACHIEVEMENTS]
        exam = d["active_exam"]
        return {
            "level": game.level_info(d["xp"]), "streak": game.streak_info(d["days"]),
            "solved": len(solved), "total": len(EXERCISES), "parts": parts, "levels": levels,
            "daily": {"id": daily_id, "title": BY_ID[daily_id]["title"],
                      "done": game.today() in d["daily_done"] or daily_id in solved,
                      "xp": BY_ID[daily_id]["xp"]},
            "recommended": recommended, "history": history, "achievements": ach,
            "exams": d["exams"][-10:], "exam": game.exam_view(exam, BY_ID),
            "chain": game.chain_view(d.get("active_chain"), BY_ID, store),
            "lessons": {"done": sum(1 for v in d.get("lessons", {}).values() if v.get("done")),
                        "total": len(LESSONS)},
            "log": d["log"][-8:][::-1], "config": get_cfg(),
            "tools": {k: bool(v) for k, v in engine.tools(get_cfg()).items()},
        }


def exercise_detail(ex_id):
    e = BY_ID[ex_id]
    cfg = get_cfg()
    with store.lock:
        st = store.ex_state(ex_id)
        draft = store.data["drafts"].get(ex_id)
        solved = st["solved"]
        revealed = e["hints"] if solved else e["hints"][:st["hints"]]
    out = {k: e[k] for k in ("id", "title", "file", "proto", "part", "level", "xp", "summary",
                              "details", "examples", "allowed", "notes")}
    out.update({"starter": engine.starter_code(e, cfg), "draft": draft, "solved": solved,
                "hints_total": len(e["hints"]), "hints": revealed, "attempts": st["attempts"],
                "lessons": [{"id": l["id"], "title": l["title"], "icon": l["icon"]} for l in LESSONS if ex_id in l["related"]]})
    return out


# ------------------------------------------------------------------ actions
def do_run(body):
    ex_id = body.get("id")
    if ex_id not in BY_ID:
        return 404, {"error": "exercice inconnu"}
    code = body.get("code")
    if not isinstance(code, str) or len(code) > 60000:
        return 400, {"error": "code invalide ou trop long (60 000 caracteres max)"}
    exam_mode = bool(body.get("exam"))
    chain_mode = bool(body.get("chain")) and not exam_mode
    ex = BY_ID[ex_id]
    cfg = get_cfg()
    if chain_mode:
        with store.lock:
            ch = store.data.get("active_chain")
        if not ch or ch["current"] != ex_id:
            return 400, {"error": "ce n'est pas l'exercice courant de l'enchainement"}
    if exam_mode:
        with store.lock:
            exam = store.data["active_exam"]
            view = game.exam_view(exam, BY_ID)
        if not exam or exam["current"] != ex_id:
            return 400, {"error": "ce n'est pas l'exercice courant de l'examen"}
        if view["expired"]:
            return 400, {"error": "temps ecoule : termine l'examen", "expired": True}
        if view["cooldown"] > 0:
            return 429, {"error": "penalite : attends %d s avant de rendre a nouveau" % view["cooldown"],
                         "cooldown": view["cooldown"]}
    with grade_sem:
        res = engine.grade(ex, code, cfg, check_norm=not exam_mode)
    out = {"result": res}
    if res.get("fatal"):
        return 200, out
    with store.lock:
        day = store.data["days"].setdefault(game.today(), {"solved": [], "attempts": 0, "xp": 0})
        if res.get("code"):
            if exam_mode:   # le code d'examen reste separe des brouillons d'entrainement
                store.data["active_exam"]["draft"] = res["code"]
            else:
                store.data["drafts"][ex_id] = res["code"]
        if exam_mode:
            out["exam"] = game.exam_on_result(store, EXERCISES, res["validated"])
            out["exam_state"] = game.exam_view(store.data["active_exam"], BY_ID)
        else:
            st = store.ex_state(ex_id)
            st["attempts"] += 1
            day["attempts"] += 1
            st["best"] = max(st["best"], res["score"])
            if res["validated"]:
                out["xp"] = game.apply_validation(store, ex, EXERCISES)
                if chain_mode:
                    out["xp"]["new_achievements"] += game.chain_on_validated(store, EXERCISES)
                    out["chain"] = game.chain_view(store.data.get("active_chain"), BY_ID, store)
            else:
                if not st["solved"]:
                    st["fails"] += 1
                store.save()
    return 200, out


def do_hint(body):
    ex_id = body.get("id")
    if ex_id not in BY_ID:
        return 404, {"error": "exercice inconnu"}
    with store.lock:
        if store.data["active_exam"]:
            return 400, {"error": "pas d'indices pendant un examen"}
        e = BY_ID[ex_id]
        st = store.ex_state(ex_id)
        if not st["solved"] and st["hints"] < len(e["hints"]):
            st["hints"] += 1
            store.save()
        shown = e["hints"] if st["solved"] else e["hints"][:st["hints"]]
    return 200, {"hints": shown, "total": len(e["hints"]), "penalty": not st["solved"]}


def do_save(body):
    ex_id = body.get("id")
    code = body.get("code")
    if ex_id not in BY_ID or not isinstance(code, str) or len(code) > 60000:
        return 400, {"error": "invalide"}
    with store.lock:
        exam = store.data["active_exam"]
        if body.get("exam"):
            if not exam or exam["current"] != ex_id:
                return 400, {"error": "ce n'est pas l'exercice courant de l'examen"}
            exam["draft"] = code
        else:
            store.data["drafts"][ex_id] = code
        store.save()
    return 200, {"ok": True}


def do_config(body):
    login = str(body.get("login", "")).strip()
    email = str(body.get("email", "")).strip()
    if not re.fullmatch(r"[a-z0-9_-]{1,32}", login):
        return 400, {"error": "login invalide (minuscules, chiffres, - et _ ; 32 max)"}
    if not re.fullmatch(r"[^@\s]{1,64}@[^@\s]{1,128}", email):
        return 400, {"error": "email invalide"}
    save_json(CFG_PATH, {"login": login, "email": email})
    return 200, {"ok": True}


def do_idea(body):
    text = str(body.get("text", "")).strip()
    cat = str(body.get("category", "autre"))[:30]
    if not text or len(text) > 4000:
        return 400, {"error": "ecris une idee (4000 caracteres max)"}
    with file_lock:
        ideas = load_json(IDEAS_PATH, [])
        ideas.append({"id": int(time.time() * 1000), "date": time.strftime("%Y-%m-%d %H:%M"),
                      "category": cat, "text": text, "status": "nouveau"})
        save_json(IDEAS_PATH, ideas)
    return 200, {"ok": True, "count": len(ideas)}


def lessons_list():
    with store.lock:
        st = store.data.get("lessons", {})
        return [{"id": l["id"], "icon": l["icon"], "title": l["title"], "summary": l["summary"],
                 "questions": len(l["quiz"]), "done": bool(st.get(l["id"], {}).get("done")),
                 "best": st.get(l["id"], {}).get("best", 0), "related": l["related"],
                 "level": l.get("level", ""), "time": l.get("time", 0)} for l in LESSONS]


def funcs_list():
    with store.lock:
        exs = store.data["exercises"]
        return [{"id": e["id"], "part": e["part"], "level": e["level"], "proto": e["proto"],
                 "role": func_courses.FUNCS_BY_ID[e["id"]]["role"],
                 "solved": bool(exs.get(e["id"], {}).get("solved"))} for e in EXERCISES if e["id"] in func_courses.FUNCS_BY_ID]


def func_detail(fid):
    f = func_courses.FUNCS_BY_ID[fid]
    e = BY_ID[fid]
    ids = [x["id"] for x in EXERCISES if x["id"] in func_courses.FUNCS_BY_ID]
    i = ids.index(fid)
    lines = func_courses.code_lines(fid)
    while lines and lines[-1] == "":
        lines.pop()
    with store.lock:
        solved = bool(store.data["exercises"].get(fid, {}).get("solved"))
    return {"id": fid, "part": e["part"], "level": e["level"], "proto": e["proto"], "summary": e["summary"],
            "role": f["role"], "why": f["why"], "code": lines, "walk": f["walk"], "cases": f["cases"],
            "trace": f["trace"], "pitfalls": f["pitfalls"], "solved": solved,
            "prev": ids[i - 1] if i > 0 else None, "next": ids[i + 1] if i + 1 < len(ids) else None}


def lesson_detail(lid):
    l = LESSONS_BY_ID[lid]
    with store.lock:
        st = store.data.get("lessons", {}).get(lid, {})
    return {"id": l["id"], "icon": l["icon"], "title": l["title"], "summary": l["summary"], "blocks": l["blocks"],
            "quiz": [{"q": x["q"], "choices": x["choices"]} for x in l["quiz"]],      # sans les reponses
            "related": [{"id": r, "title": BY_ID[r]["title"]} for r in l["related"] if r in BY_ID],
            "done": bool(st.get("done")), "xp": game.LESSON_XP,
            "level": l.get("level", ""), "time": l.get("time", 0)}


def do_quiz(body):
    lid = body.get("id")
    if lid not in LESSONS_BY_ID:
        return 404, {"error": "cours inconnu"}
    return 200, game.lesson_submit(store, EXERCISES, LESSONS_BY_ID[lid], body.get("answers"))


def do_chain(action):
    if action == "start":
        game.chain_start(store, EXERCISES)
        return 200, game.chain_view(store.data.get("active_chain"), BY_ID, store)
    if action == "skip":
        if not game.chain_skip(store, EXERCISES):
            return 400, {"error": "plus de passes disponibles (2 par enchainement)"}
        return 200, game.chain_view(store.data.get("active_chain"), BY_ID, store)
    if action == "stop":
        res = game.chain_stop(store, EXERCISES)
        if not res:
            return 400, {"error": "aucun enchainement en cours"}
        return 200, res
    return 404, {"error": "action inconnue"}


def do_exam_finish():
    with store.lock:
        res = game.exam_finish(store, EXERCISES)
    if not res:
        return 400, {"error": "aucun examen en cours"}
    return 200, res


# ------------------------------------------------------------------ HTTP
class Handler(BaseHTTPRequestHandler):
    server_version = "42Trainer"

    def log_message(self, fmt, *args):  # silence
        pass

    # -- utilitaires
    def _host_ok(self):
        host = (self.headers.get("Host") or "").lower()
        return host.split(":")[0] in ("localhost", "127.0.0.1")

    def _send(self, code, obj=None, raw=None, ctype="application/json; charset=utf-8"):
        body = raw if raw is not None else json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def _body(self):
        n = int(self.headers.get("Content-Length") or 0)
        if n > MAX_BODY:
            raise ValueError("corps trop gros")
        raw = self.rfile.read(n) if n else b"{}"
        d = json.loads(raw.decode("utf-8") or "{}")
        if not isinstance(d, dict):
            raise ValueError("JSON attendu : objet")
        return d

    # -- routes
    def do_GET(self):
        if not self._host_ok():
            return self._send(403, {"error": "hote refuse"})
        path = self.path.split("?", 1)[0]
        try:
            if path == "/api/ping":
                return self._send(200, {"app": APP})
            if path == "/api/state":
                return self._send(200, build_state())
            if path == "/api/exercises":
                with store.lock:
                    items = [exercise_summary(e, store.data["exercises"].get(e["id"])) for e in EXERCISES]
                return self._send(200, items)
            m = re.fullmatch(r"/api/exercise/([A-Za-z0-9_]+)", path)
            if m:
                if m.group(1) not in BY_ID:
                    return self._send(404, {"error": "exercice inconnu"})
                return self._send(200, exercise_detail(m.group(1)))
            if path == "/api/ideas":
                return self._send(200, load_json(IDEAS_PATH, []))
            if path == "/api/lessons":
                return self._send(200, lessons_list())
            if path == "/api/funcs":
                return self._send(200, funcs_list())
            m = re.fullmatch(r"/api/func/([A-Za-z0-9_]+)", path)
            if m:
                if m.group(1) not in func_courses.FUNCS_BY_ID:
                    return self._send(404, {"error": "cours de fonction inconnu"})
                return self._send(200, func_detail(m.group(1)))
            m = re.fullmatch(r"/api/lesson/([A-Za-z0-9_]+)", path)
            if m:
                if m.group(1) not in LESSONS_BY_ID:
                    return self._send(404, {"error": "cours inconnu"})
                return self._send(200, lesson_detail(m.group(1)))
            return self._static(path)
        except Exception as e:  # noqa
            return self._send(500, {"error": "erreur interne : %s" % e})

    def do_POST(self):
        if not self._host_ok():
            return self._send(403, {"error": "hote refuse"})
        if self.headers.get("X-Trainer") != "1":
            return self._send(403, {"error": "en-tete manquant"})
        path = self.path.split("?", 1)[0]
        try:
            body = self._body()
            routes = {"/api/run": do_run, "/api/hint": do_hint, "/api/save": do_save,
                      "/api/config": do_config, "/api/ideas": do_idea}
            if path in routes:
                code, obj = routes[path](body)
                return self._send(code, obj)
            if path == "/api/exam/start":
                game.exam_start(store, EXERCISES)
                return self._send(200, build_state()["exam"] or {})
            if path == "/api/quiz":
                code, obj = do_quiz(body)
                return self._send(code, obj)
            m = re.fullmatch(r"/api/chain/(start|skip|stop)", path)
            if m:
                code, obj = do_chain(m.group(1))
                return self._send(code, obj)
            if path == "/api/exam/finish":
                code, obj = do_exam_finish()
                return self._send(code, obj)
            if path == "/api/reset":
                if body.get("confirm") != "RESET":
                    return self._send(400, {"error": "confirmation manquante"})
                store.reset()
                return self._send(200, {"ok": True})
            return self._send(404, {"error": "route inconnue"})
        except (ValueError, KeyError) as e:
            return self._send(400, {"error": str(e)})
        except Exception as e:  # noqa
            return self._send(500, {"error": "erreur interne : %s" % e})

    def _static(self, path):
        if path in ("", "/"):
            path = "/index.html"
        full = os.path.normpath(os.path.join(WEB, path.lstrip("/")))
        if not full.startswith(WEB + os.sep) or not os.path.isfile(full):
            return self._send(404, {"error": "introuvable"})
        ctype = mimetypes.guess_type(full)[0] or "application/octet-stream"
        if ctype.startswith("text/") or ctype in ("application/javascript", "application/json"):
            ctype += "; charset=utf-8"
        with open(full, "rb") as f:
            self._send(200, raw=f.read(), ctype=ctype)


def already_running(port):
    try:
        with urllib.request.urlopen("http://127.0.0.1:%d/api/ping" % port, timeout=1.5) as r:
            return json.loads(r.read().decode()).get("app") == APP
    except Exception:
        return False


def main():
    open_browser = "--no-open" not in sys.argv
    engine.disable_crash_dialogs()
    engine.cleanup_runs(0)
    httpd, port = None, None
    for p in PORTS:
        if already_running(p):
            print("42 Trainer tourne deja : http://localhost:%d" % p)
            if open_browser:
                webbrowser.open("http://localhost:%d" % p)
            return 0
        try:
            httpd = ThreadingHTTPServer(("127.0.0.1", p), Handler)
            port = p
            break
        except OSError:
            continue
    if not httpd:
        print("Aucun port libre entre %d et %d." % (PORTS[0], PORTS[-1]))
        return 1
    tl = engine.tools(get_cfg())
    print("=" * 56)
    print(" 42 Trainer  ->  http://localhost:%d" % port)
    print(" gcc        :", tl["gcc"] or "INTROUVABLE")
    print(" norminette :", "ok" if tl["norm_python"] else "INTROUVABLE (etape ignoree)")
    print(" Ferme cette fenetre pour arreter le serveur.")
    print("=" * 56)
    threading.Thread(target=lambda: engine.build_runtime(tl["gcc"], engine.child_env(tl["gcc"]))
                     if tl["gcc"] else None, daemon=True).start()
    if open_browser:
        threading.Timer(0.8, lambda: webbrowser.open("http://localhost:%d" % port)).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
