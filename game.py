"""Progression : XP, niveaux, serie, defi du jour, succes, examen.
Tout le calcul est fait cote serveur : le navigateur ne peut pas tricher.
"""
import datetime
import hashlib
import json
import os
import random
import threading
import time

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.environ.get("TRAINER_DATA") or os.path.join(BASE, "data")   # surcharge pour les tests

TITLES = [(1, "Cadet"), (2, "Piscineux"), (3, "Apprenti libft"), (4, "Codeur"),
          (5, "Normé"), (6, "Pointeur"), (7, "Malloc Master"), (8, "Moulinette Slayer"),
          (10, "Légende 42")]

EXAM_SECONDS = 2 * 60 * 60
EXAM_LEVELS = 4


def today():
    return datetime.date.today().isoformat()


def cum_xp(level):
    """XP total necessaire pour ATTEINDRE le niveau `level` (niveau 1 = 0)."""
    return 50 * level * (level - 1)


def level_info(xp):
    lvl = 1
    while cum_xp(lvl + 1) <= xp:
        lvl += 1
    start, end = cum_xp(lvl), cum_xp(lvl + 1)
    title = TITLES[0][1]
    for n, t in TITLES:
        if lvl >= n:
            title = t
    return {"level": lvl, "title": title, "xp": xp, "into": xp - start, "span": end - start,
            "pct": round(100.0 * (xp - start) / (end - start), 1), "next_at": end}


ACHIEVEMENTS = [
    ("first_blood", "Premier sang", "Valide ton premier exercice.", "🩸"),
    ("ten", "Dizaine", "Valide 10 exercices.", "🔟"),
    ("twenty_five", "Vingt-cinq", "Valide 25 exercices.", "🎯"),
    ("all", "Libft complète", "Valide tous les exercices du catalogue.", "👑"),
    ("part1", "Maître de la libc", "Valide tous les exercices de la partie 1.", "📚"),
    ("part2", "Fonctions en plus", "Valide tous les exercices de la partie 2.", "🧩"),
    ("part3", "Maître des listes", "Valide tous les exercices de la partie 3 (listes chaînées).", "🔗"),
    ("first_try_5", "Du premier coup", "Valide 5 exercices dès la première soumission.", "⚡"),
    ("no_hint_5", "Sans filet", "Valide 5 exercices sans utiliser d'indice.", "🧠"),
    ("split", "Tueur de split", "Valide ft_split.", "🗡️"),
    ("itoa", "Piège INT_MIN évité", "Valide ft_itoa.", "🔢"),
    ("streak3", "Régulier", "3 jours d'entraînement d'affilée.", "🔥"),
    ("streak7", "Assidu", "7 jours d'entraînement d'affilée.", "🌋"),
    ("daily5", "Habitué du défi", "Réussis 5 défis du jour.", "📅"),
    ("exam_start", "Premier examen", "Termine un examen.", "📝"),
    ("exam_full", "Examen parfait", "Valide les 4 niveaux d'un examen.", "🏆"),
    ("chain5", "Enchaîneur", "Valide 5 exercices d'affilée en mode enchaînement.", "⚡"),
    ("chain10", "Machine", "Valide 10 exercices d'affilée en mode enchaînement.", "🤖"),
    ("lessons5", "Bon élève", "Réussis 5 quiz de cours (sans faute).", "🎓"),
    ("lessons_all", "Cours terminés", "Réussis tous les quiz de cours.", "📚"),
    ("level5", "Niveau 5", "Atteins le niveau 5.", "⭐"),
    ("level8", "Niveau 8", "Atteins le niveau 8.", "🌟"),
]
ACH_BY_ID = {a[0]: a for a in ACHIEVEMENTS}


def default_progress():
    return {"version": 1, "created": time.time(), "xp": 0, "exercises": {}, "drafts": {},
            "days": {}, "daily": {}, "daily_done": [], "achievements": {}, "exams": [],
            "active_exam": None, "log": [], "chains": [], "active_chain": None, "lessons": {}}


class Store:
    def __init__(self, path=None):
        os.makedirs(DATA, exist_ok=True)
        self.path = path or os.path.join(DATA, "progress.json")
        self.lock = threading.RLock()
        self.data = self._load()

    def _load(self):
        for p in (self.path, self.path + ".bak"):
            try:
                with open(p, encoding="utf-8") as f:
                    d = json.load(f)
                base = default_progress()
                base.update(d)
                return base
            except (OSError, ValueError):
                continue
        return default_progress()

    def save(self):
        with self.lock:
            tmp = self.path + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=1)
            if os.path.exists(self.path):
                try:
                    os.replace(self.path, self.path + ".bak")
                except OSError:
                    pass
            os.replace(tmp, self.path)

    def reset(self):
        with self.lock:
            self.data = default_progress()
            self.save()

    def ex_state(self, ex_id):
        return self.data["exercises"].setdefault(ex_id, {
            "attempts": 0, "fails": 0, "solved": False, "hints": 0, "best": 0,
            "xp": 0, "solved_at": None})


# ------------------------------------------------------------------ serie
def streak_info(days):
    """Serie en cours (jours consecutifs avec au moins une validation)."""
    active = sorted(d for d, v in days.items() if v.get("solved") or v.get("revised"))
    if not active:
        return {"current": 0, "best": 0, "today": False}
    dates = [datetime.date.fromisoformat(d) for d in active]
    best = run = 1
    for a, b in zip(dates, dates[1:]):
        run = run + 1 if (b - a).days == 1 else 1
        best = max(best, run)
    t = datetime.date.today()
    last = dates[-1]
    current = 0
    if (t - last).days <= 1:
        current = 1
        for i in range(len(dates) - 1, 0, -1):
            if (dates[i] - dates[i - 1]).days == 1:
                current += 1
            else:
                break
    return {"current": current, "best": best, "today": last == t}


# ------------------------------------------------------------------ defi du jour
def daily_exercise(store, exercises):
    d = today()
    with store.lock:
        cur = store.data["daily"]
        if cur.get("date") != d:
            solved = {k for k, v in store.data["exercises"].items() if v.get("solved")}
            pool = [e["id"] for e in exercises if e["id"] not in solved] or [e["id"] for e in exercises]
            h = int(hashlib.sha256(d.encode()).hexdigest(), 16)
            store.data["daily"] = {"date": d, "id": sorted(pool)[h % len(pool)]}
            store.save()
        return store.data["daily"]["id"]


# ------------------------------------------------------------------ XP
def compute_xp(ex, st, streak_current, is_daily):
    """Retourne (total, liste de lignes de detail)."""
    base = ex["xp"]
    lines = [("Exercice " + ex["id"], base)]
    pct = 0.0
    if st["fails"] == 0:
        lines.append(("Du premier coup", round(base * 0.2)))
        pct += 0.2
    if st["hints"] == 0:
        lines.append(("Sans indice", round(base * 0.2)))
        pct += 0.2
    else:
        pen = min(st["hints"], 3) * 0.2
        lines.append(("Indices utilisés (%d)" % st["hints"], -round(base * pen)))
        pct -= pen
    if streak_current >= 2:
        b = min(streak_current, 6) * 0.05
        lines.append(("Série de %d jours" % streak_current, round(base * b)))
        pct += b
    if is_daily:
        lines.append(("Défi du jour", round(base * 0.5)))
        pct += 0.5
    total = max(round(base * 0.4), sum(v for _, v in lines))
    return total, lines


def apply_validation(store, ex, exercises):
    """Appele quand l'eleve valide un exercice. Retourne le recapitulatif XP."""
    with store.lock:
        d = store.data
        st = store.ex_state(ex["id"])
        info_before = level_info(d["xp"])
        day = d["days"].setdefault(today(), {"solved": [], "attempts": 0, "xp": 0})
        first_time = not st["solved"]
        gained, lines = 0, []
        if first_time:
            st["solved"] = True
            st["solved_at"] = time.time()
            if ex["id"] not in day["solved"]:
                day["solved"].append(ex["id"])
            streak = streak_info(d["days"])
            is_daily = (d["daily"].get("date") == today() and d["daily"].get("id") == ex["id"])
            gained, lines = compute_xp(ex, st, streak["current"], is_daily)
            st["xp"] = gained
            d["xp"] += gained
            day["xp"] += gained
            if is_daily:
                d["daily_done"].append(today())
            d["log"].append({"t": time.time(), "kind": "solved", "id": ex["id"], "xp": gained})
            d["log"] = d["log"][-200:]
        else:
            # Revision : refaire un exercice deja valide rapporte un peu d'XP (5 par jour max)
            # et compte pour la serie, pour que l'entrainement quotidien serve a quelque chose.
            revised = day.setdefault("revised", [])
            if ex["id"] not in revised and len(revised) < 5:
                revised.append(ex["id"])
                gained = max(2, round(ex["xp"] * 0.1))
                lines = [("Révision de " + ex["id"], gained)]
                d["xp"] += gained
                day["xp"] += gained
                d["log"].append({"t": time.time(), "kind": "revised", "id": ex["id"], "xp": gained})
                d["log"] = d["log"][-200:]
        info_after = level_info(d["xp"])
        new_ach = check_achievements(store, exercises)
        store.save()
        return {"first_time": first_time, "gained": gained, "lines": lines,
                "level_up": info_after["level"] > info_before["level"],
                "level": info_after, "new_achievements": new_ach}


LESSON_COUNT = {"n": 0}   # renseigne par le serveur (nombre de lecons au catalogue)


def check_achievements(store, exercises):
    d = store.data
    solved = {k for k, v in d["exercises"].items() if v.get("solved")}
    n = len(solved)
    by_part = {}
    for e in exercises:
        by_part.setdefault(e["part"], set()).add(e["id"])
    st = d["exercises"]
    first_try = sum(1 for k in solved if st[k]["fails"] == 0)
    no_hint = sum(1 for k in solved if st[k]["hints"] == 0)
    streak = streak_info(d["days"])
    lvl = level_info(d["xp"])["level"]
    cond = {
        "first_blood": n >= 1, "ten": n >= 10, "twenty_five": n >= 25,
        "all": n >= len(exercises),
        "part1": bool(by_part.get(1)) and by_part[1] <= solved,
        "part2": bool(by_part.get(2)) and by_part[2] <= solved,
        "part3": bool(by_part.get(3)) and by_part[3] <= solved,
        "first_try_5": first_try >= 5, "no_hint_5": no_hint >= 5,
        "split": "ft_split" in solved, "itoa": "ft_itoa" in solved,
        "streak3": streak["best"] >= 3, "streak7": streak["best"] >= 7,
        "daily5": len(d["daily_done"]) >= 5,
        "exam_start": len(d["exams"]) >= 1,
        "exam_full": any(x.get("completed") for x in d["exams"]),
        "chain5": max([c.get("n", 0) for c in d.get("chains", [])] + [len(d["active_chain"]["done"]) if d.get("active_chain") else 0]) >= 5,
        "chain10": max([c.get("n", 0) for c in d.get("chains", [])] + [len(d["active_chain"]["done"]) if d.get("active_chain") else 0]) >= 10,
        "lessons5": sum(1 for v in d.get("lessons", {}).values() if v.get("done")) >= 5,
        "lessons_all": LESSON_COUNT["n"] > 0 and sum(1 for v in d.get("lessons", {}).values() if v.get("done")) >= LESSON_COUNT["n"],
        "level5": lvl >= 5, "level8": lvl >= 8,
    }
    new = []
    for aid, ok in cond.items():
        if ok and aid not in d["achievements"]:
            d["achievements"][aid] = time.time()
            new.append({"id": aid, "title": ACH_BY_ID[aid][1], "icon": ACH_BY_ID[aid][3]})
    return new


# ------------------------------------------------------------------ enchainement
CHAIN_PART = 1          # l'enchainement ne propose que des exercices de la partie 1
CHAIN_MAX_SKIPS = 2


def _chain_pool(exercises):
    return [e for e in exercises if e["part"] == CHAIN_PART]


def _chain_pick(exercises, exclude):
    pool = [e for e in _chain_pool(exercises) if e["id"] not in exclude]
    return random.choice(pool)["id"] if pool else None


def chain_bonus(n):
    """Bonus de fin d'enchainement : 0, 10, 30, 60, 100, 150 (plafonne) pour 1..6+ exercices."""
    return min(150, 10 * n * (n - 1) // 2)


def chain_view(chain, by_id, store=None):
    best = max([c.get("n", 0) for c in (store.data.get("chains", []) if store else [])] + [0])
    if not chain:
        return {"active": False, "best": best}
    return {"active": True, "current": chain["current"], "done": chain["done"], "n": len(chain["done"]),
            "skips_left": CHAIN_MAX_SKIPS - chain["skips"], "started": chain["started"],
            "bonus_if_stopped": chain_bonus(len(chain["done"])), "best": best,
            "finished_all": chain["current"] is None,
            "title": by_id[chain["current"]]["title"] if chain["current"] else None}


def chain_start(store, exercises):
    with store.lock:
        if not store.data.get("active_chain"):
            store.data["active_chain"] = {"started": time.time(), "done": [], "skips": 0,
                                          "current": _chain_pick(exercises, set())}
            store.save()
        return store.data["active_chain"]


def chain_on_validated(store, exercises):
    with store.lock:
        ch = store.data.get("active_chain")
        if not ch or not ch["current"]:
            return []
        if ch["current"] not in ch["done"]:
            ch["done"].append(ch["current"])
        ch["current"] = _chain_pick(exercises, set(ch["done"]))   # None si tout est fait
        new_ach = check_achievements(store, exercises)
        store.save()
        return new_ach


def chain_skip(store, exercises):
    """Passe l'exercice courant (2 passes par enchainement). Retourne False si plus de passes."""
    with store.lock:
        ch = store.data.get("active_chain")
        if not ch or not ch["current"] or ch["skips"] >= CHAIN_MAX_SKIPS:
            return False
        nxt = _chain_pick(exercises, set(ch["done"]) | {ch["current"]})
        if not nxt:
            return False
        ch["skips"] += 1
        ch["current"] = nxt
        store.save()
        return True


def chain_stop(store, exercises):
    with store.lock:
        ch = store.data.get("active_chain")
        if not ch:
            return None
        n = len(ch["done"])
        bonus = chain_bonus(n)
        before = level_info(store.data["xp"])
        store.data["xp"] += bonus
        rec = {"t": time.time(), "n": n, "xp": bonus, "seconds": int(time.time() - ch["started"])}
        store.data.setdefault("chains", []).append(rec)
        day = store.data["days"].setdefault(today(), {"solved": [], "attempts": 0, "xp": 0})
        day["xp"] += bonus
        best = max(c["n"] for c in store.data["chains"])
        store.data["active_chain"] = None
        new_ach = check_achievements(store, exercises)
        after = level_info(store.data["xp"])
        store.save()
        return {"result": rec, "best": best, "new_record": n > 0 and n >= best and
                n > max([c["n"] for c in store.data["chains"][:-1]] + [0]),
                "level_up": after["level"] > before["level"], "level": after, "new_achievements": new_ach}


# ------------------------------------------------------------------ cours (quiz)
LESSON_XP = 15


def lesson_submit(store, exercises, lesson, answers):
    """Corrige un quiz cote serveur. XP une seule fois, si aucune faute."""
    qs = lesson["quiz"]
    if not isinstance(answers, list) or len(answers) != len(qs):
        raise ValueError("reponses invalides")
    results, good = [], 0
    for q, a in zip(qs, answers):
        ok = a == q["answer"]
        good += ok
        results.append({"ok": ok, "answer": q["answer"], "explain": q["explain"]})
    with store.lock:
        st = store.data.setdefault("lessons", {}).setdefault(lesson["id"], {"best": 0, "done": False, "tries": 0})
        st["tries"] += 1
        st["best"] = max(st["best"], good)
        gained, new_ach, lvl_up = 0, [], False
        perfect = good == len(qs)
        if perfect and not st["done"]:
            st["done"] = True
            before = level_info(store.data["xp"])
            gained = LESSON_XP
            store.data["xp"] += gained
            day = store.data["days"].setdefault(today(), {"solved": [], "attempts": 0, "xp": 0})
            day["xp"] += gained
            new_ach = check_achievements(store, exercises)
            lvl_up = level_info(store.data["xp"])["level"] > before["level"]
        store.save()
        return {"good": good, "total": len(qs), "perfect": perfect, "results": results, "gained": gained,
                "new_achievements": new_ach, "level_up": lvl_up, "level": level_info(store.data["xp"])}


# ------------------------------------------------------------------ examen
def exam_view(exam, by_id):
    if not exam:
        return None
    left = max(0, int(exam["started"] + exam["duration"] - time.time()))
    cooldown = max(0, int(exam.get("cooldown_until", 0) - time.time()))
    return {"started": exam["started"], "duration": exam["duration"], "left": left,
            "level": exam["level"], "levels": EXAM_LEVELS, "current": exam["current"],
            "done": exam["done"], "fails": exam["fails"], "cooldown": cooldown,
            "expired": left == 0, "title": by_id[exam["current"]]["title"] if exam["current"] else None,
            "draft": exam.get("draft")}


def exam_pick(exercises, level, used):
    pool = [e for e in exercises if e["level"] == level and e["id"] not in used]
    if not pool:
        pool = [e for e in exercises if e["level"] == level] or exercises
    return random.choice(pool)["id"]


def exam_start(store, exercises):
    with store.lock:
        if store.data["active_exam"]:
            return store.data["active_exam"]
        first = exam_pick(exercises, 1, set())
        store.data["active_exam"] = {"started": time.time(), "duration": EXAM_SECONDS,
                                     "level": 1, "current": first, "done": [], "fails": 0,
                                     "cooldown_until": 0}
        store.save()
        return store.data["active_exam"]


def exam_on_result(store, exercises, validated):
    """Met a jour l'examen apres une soumission. Retourne un dict d'info."""
    with store.lock:
        ex = store.data["active_exam"]
        if validated:
            ex["done"].append(ex["current"])
            ex["draft"] = None
            ex["fails"] = 0
            ex["cooldown_until"] = 0
            ex["level"] += 1
            if ex["level"] > EXAM_LEVELS:
                ex["current"] = None
                store.save()
                return {"advanced": True, "finished": True}
            ex["current"] = exam_pick(exercises, ex["level"], set(ex["done"]))
            store.save()
            return {"advanced": True, "finished": False}
        ex["fails"] += 1
        if ex["fails"] >= 3:
            ex["cooldown_until"] = time.time() + min(30 * (ex["fails"] - 2), 120)
        store.save()
        return {"advanced": False, "finished": False}


def exam_finish(store, exercises):
    with store.lock:
        ex = store.data["active_exam"]
        if not ex:
            return None
        validated = len(ex["done"])
        completed = validated >= EXAM_LEVELS
        xp = 25 * validated + (100 if completed else 0)
        # anti-farm : seuls les 3 premiers examens de la journee rapportent de l'XP
        done_today = sum(1 for e in store.data["exams"] if time.strftime("%Y-%m-%d", time.localtime(e["t"])) == today())
        capped = done_today >= 3
        if capped:
            xp = 0
        before = level_info(store.data["xp"])
        store.data["xp"] += xp
        rec = {"t": time.time(), "validated": validated, "completed": completed, "xp": xp, "capped": capped,
               "seconds": int(min(time.time() - ex["started"], ex["duration"]))}
        store.data["exams"].append(rec)
        day = store.data["days"].setdefault(today(), {"solved": [], "attempts": 0, "xp": 0})
        day["xp"] += xp
        store.data["active_exam"] = None
        new_ach = check_achievements(store, exercises)
        after = level_info(store.data["xp"])
        store.save()
        return {"result": rec, "level_up": after["level"] > before["level"], "level": after,
                "new_achievements": new_ach}
