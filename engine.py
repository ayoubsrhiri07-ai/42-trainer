"""Moulinette de 42 Trainer : norminette + compilation + tests + fonctions interdites.

Tout est lance avec des listes d'arguments (pas de shell) : les chemins avec
espaces (Ecole 42) ne posent donc aucun probleme.
"""
import ctypes
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from concurrent.futures import ThreadPoolExecutor

BASE = os.path.dirname(os.path.abspath(__file__))
RUNTIME = os.path.join(BASE, "runtime")
REF_DIR = os.path.join(RUNTIME, "ref")
BUILD = os.path.join(BASE, "build")
RUNS = os.path.join(BASE, "runs")
IS_WIN = os.name == "nt"
NOWIN = getattr(subprocess, "CREATE_NO_WINDOW", 0)

MAX_OUTPUT = 256 * 1024
KILL_OUTPUT = 4 * 1024 * 1024

_lock = threading.Lock()
_tools = {}


# --------------------------------------------------------------------------
# Outils (gcc, python + norminette) : recherche par chemin absolu
# --------------------------------------------------------------------------
def disable_crash_dialogs():
    """Evite qu'un programme qui plante ouvre une fenetre d'erreur Windows."""
    if IS_WIN:
        try:
            ctypes.windll.kernel32.SetErrorMode(0x0001 | 0x0002 | 0x8000)
        except Exception:
            pass


def _run_quiet(args, timeout=20):
    try:
        p = subprocess.run(args, capture_output=True, text=True, timeout=timeout,
                           creationflags=NOWIN, encoding="utf-8", errors="replace")
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except Exception as e:  # noqa
        return -1, str(e)


def find_gcc(cfg=None):
    cands = []
    if cfg and cfg.get("gcc"):
        cands.append(cfg["gcc"])
    for name in ("gcc", "cc"):
        w = shutil.which(name)
        if w:
            cands.append(w)
    if IS_WIN:
        local = os.environ.get("LOCALAPPDATA", "")
        cands += glob.glob(os.path.join(local, "Microsoft", "WinGet", "Packages",
                                        "BrechtSanders.WinLibs*", "mingw64", "bin", "gcc.exe"))
        cands += ["C:\\msys64\\ucrt64\\bin\\gcc.exe", "C:\\msys64\\mingw64\\bin\\gcc.exe",
                  "C:\\mingw64\\bin\\gcc.exe"]
    for c in cands:
        if c and os.path.isfile(c):
            return c
    return None


def find_norminette_python(cfg=None):
    """Retourne un executable python qui sait faire `-m norminette`."""
    cands = [sys.executable]
    if cfg and cfg.get("python"):
        cands.insert(0, cfg["python"])
    w = shutil.which("python")
    if w:
        cands.append(w)
    if IS_WIN:
        local = os.environ.get("LOCALAPPDATA", "")
        roam = os.environ.get("APPDATA", "")
        cands += sorted(glob.glob(os.path.join(local, "Programs", "Python", "Python3*", "python.exe")),
                        reverse=True)
        cands += sorted(glob.glob(os.path.join(roam, "Python", "Python3*", "python.exe")), reverse=True)
    seen = set()
    for c in cands:
        if not c or c in seen or not os.path.isfile(c):
            continue
        seen.add(c)
        rc, out = _run_quiet([c, "-m", "norminette", "--version"], 30)
        if rc == 0 and "norminette" in out.lower():
            return c
    return None


def tools(cfg=None, refresh=False):
    with _lock:
        if refresh or not _tools:
            _tools["gcc"] = find_gcc(cfg)
            _tools["norm_python"] = find_norminette_python(cfg)
        return dict(_tools)


def child_env(gcc):
    env = dict(os.environ)
    if gcc:
        env["PATH"] = os.path.dirname(gcc) + os.pathsep + env.get("PATH", "")
    return env


# --------------------------------------------------------------------------
# En-tete 42 et fichier de depart
# --------------------------------------------------------------------------
def make_header(filename, login, email):
    now = time.strftime("%Y/%m/%d %H:%M:%S")
    l = "/* " + "*" * 74 + " */"
    e = "/*" + " " * 76 + "*/"
    lines = [
        l,
        e,
        "/*" + " " * 56 + ":::      ::::::::   */",
        ("/*   " + filename).ljust(56) + ":+:      :+:    :+:   */",
        "/*" + " " * 52 + "+:+ +:+         +:+     */",
        ("/*   By: %s <%s>" % (login, email)).ljust(52) + "+#+  +:+       +#+        */",
        "/*" + " " * 48 + "+#+#+#+#+#+   +#+           */",
        ("/*   Created: %s by %s" % (now, login)).ljust(55) + "#+#    #+#             */",
        ("/*   Updated: %s by %s" % (now, login)).ljust(54) + "###   ########.fr       */",
        e,
        l,
    ]
    return "\n".join(lines) + "\n\n"


_PROTO_RE = re.compile(r"^(?P<t>[\w\s]+?)\s*(?P<s>\**)(?P<n>ft_\w+)\((?P<a>.*)\)$")


def starter_code(ex, cfg):
    m = _PROTO_RE.match(ex["proto"].strip())
    if m:
        decl = "%s\t%s%s(%s)" % (m["t"].strip(), m["s"], m["n"], m["a"])
    else:
        decl = ex["proto"]
    hdr = make_header(ex["file"], cfg.get("login", "login"), cfg.get("email", "login@student.42.fr"))
    return hdr + '#include "libft.h"\n\n' + decl + "\n{\n\t\n}\n"


def normalize_code(code, ex, cfg):
    """CRLF -> LF, retour a la ligne final (comme l'option VS Code), en-tete 42
    ajoute s'il manque (comme le fait l'extension a la creation du fichier)."""
    code = (code or "").replace("\r\n", "\n").replace("\r", "\n")
    if not code.endswith("\n"):
        code += "\n"
    if not code.lstrip().startswith("/* ****"):
        code = make_header(ex["file"], cfg.get("login", "login"),
                           cfg.get("email", "login@student.42.fr")) + code.lstrip("\n")
    return code


# --------------------------------------------------------------------------
# Fonctions interdites (analyse du source, pas des symboles : evite les faux
# positifs dus aux appels generes par le compilateur)
# --------------------------------------------------------------------------
LIBC_NAMES = set("""
strlen strcpy strncpy strcat strncat strcmp strncmp strchr strrchr strstr strdup strndup
strlcpy strlcat strnstr strtok strspn strcspn strpbrk strtol strtoul strtoll strtoull strtod
atoi atol atoll atof itoa memset memcpy memmove memchr memcmp bzero calloc realloc malloc free
printf fprintf sprintf snprintf dprintf vprintf puts putchar fputs fputc putc scanf sscanf fscanf
gets fgets getchar getc fopen fclose fread fwrite fflush toupper tolower isalpha isdigit isalnum
isascii isprint isspace isupper islower ispunct iscntrl isgraph isxdigit abs labs llabs exit atexit
qsort bsearch rand srand system getenv write read open close perror sleep usleep
""".split())


def _strip_c(code):
    out = []
    i, n = 0, len(code)
    while i < n:
        c = code[i]
        nxt = code[i + 1] if i + 1 < n else ""
        if c == "/" and nxt == "*":
            j = code.find("*/", i + 2)
            i = n if j < 0 else j + 2
            out.append(" ")
        elif c == "/" and nxt == "/":
            j = code.find("\n", i)
            i = n if j < 0 else j
        elif c in "\"'":
            q = c
            i += 1
            while i < n and code[i] != q:
                i += 2 if code[i] == "\\" else 1
            i += 1
            out.append(" ")
        else:
            out.append(c)
            i += 1
    return "".join(out)


def check_forbidden(code, allowed):
    allowed = set(allowed or [])
    body = _strip_c(code)
    found = []
    for m in re.finditer(r"\b([A-Za-z_]\w*)\s*\(", body):
        name = m.group(1)
        if name in LIBC_NAMES and name not in allowed and name not in found:
            found.append(name)
    return found


# --------------------------------------------------------------------------
# Sous-processus avec limites (temps + taille de sortie)
# --------------------------------------------------------------------------
def run_limited(args, timeout, cwd=None, env=None):
    """Retourne (returncode, sortie, timed_out, too_much_output)."""
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         stdin=subprocess.DEVNULL, cwd=cwd, env=env, creationflags=NOWIN)
    chunks, total = [], [0]
    flood = [False]

    def reader():
        try:
            while True:
                data = p.stdout.read(8192)
                if not data:
                    break
                total[0] += len(data)
                if total[0] <= MAX_OUTPUT:
                    chunks.append(data)
                if total[0] > KILL_OUTPUT:
                    flood[0] = True
                    p.kill()
                    break
        except Exception:
            pass

    t = threading.Thread(target=reader, daemon=True)
    t.start()
    timed_out = False
    try:
        p.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        p.kill()
        p.wait()
    t.join(2)
    try:
        p.stdout.close()
    except Exception:
        pass
    return p.returncode, b"".join(chunks).decode("utf-8", errors="replace"), timed_out, flood[0]


# --------------------------------------------------------------------------
# Compilation des objets de reference (une seule fois, mis en cache)
# --------------------------------------------------------------------------
def _cflags_runtime():
    return ["-I", RUNTIME, "-I", REF_DIR]


def build_runtime(gcc, env):
    """Compile trace.o et les solutions de reference si necessaire. Retourne
    (liste d'objets ref, trace.o, erreur ou None)."""
    os.makedirs(os.path.join(BUILD, "ref"), exist_ok=True)
    trace_h = os.path.join(RUNTIME, "trace.h")
    h_time = max(os.path.getmtime(trace_h), os.path.getmtime(os.path.join(REF_DIR, "libft.h")))
    jobs = []
    trace_o = os.path.join(BUILD, "trace.o")
    src = os.path.join(RUNTIME, "trace.c")
    if not os.path.isfile(trace_o) or os.path.getmtime(trace_o) < os.path.getmtime(src):
        jobs.append((trace_o, [gcc, "-w", "-c", src, "-o", trace_o] + _cflags_runtime()))
    objs = {}
    for c in sorted(glob.glob(os.path.join(REF_DIR, "ft_*.c"))):
        name = os.path.splitext(os.path.basename(c))[0]
        o = os.path.join(BUILD, "ref", name + ".o")
        objs[name] = o
        if not os.path.isfile(o) or os.path.getmtime(o) < max(os.path.getmtime(c), h_time):
            jobs.append((o, [gcc, "-w", "-include", trace_h, "-c", c, "-o", o] + _cflags_runtime()))

    def work(job):
        out, args = job
        rc, text = _run_quiet_env(args, env)
        return out, rc, text

    err = None
    if jobs:
        with ThreadPoolExecutor(max_workers=8) as pool:
            for out, rc, text in pool.map(work, jobs):
                if rc != 0:
                    err = "Compilation du runtime impossible (%s) : %s" % (os.path.basename(out), text[:400])
    return objs, trace_o, err


def _run_quiet_env(args, env, timeout=60):
    try:
        p = subprocess.run(args, capture_output=True, text=True, timeout=timeout, env=env,
                           creationflags=NOWIN, encoding="utf-8", errors="replace")
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except Exception as e:  # noqa
        return -1, str(e)


# --------------------------------------------------------------------------
# Norminette
# --------------------------------------------------------------------------
def run_norm(py, path):
    rc, out = _run_quiet_env([py, "-m", "norminette", path], None, 60)
    errors = []
    for line in out.splitlines():
        m = re.match(r"Error:\s+(\w+)\s+\(line:\s*(\d+),\s*col:\s*(\d+)\):\s*(.*)", line)
        if m:
            errors.append({"code": m.group(1), "line": int(m.group(2)), "col": int(m.group(3)),
                           "msg": m.group(4).strip()})
        elif line.startswith("Error:") or "Error" in line and "line:" in line:
            errors.append({"code": "ERROR", "line": 0, "col": 0, "msg": line.strip()})
    ok = rc == 0 and not errors
    return {"ok": ok, "errors": errors[:40], "raw": out[:3000] if not ok else ""}


# --------------------------------------------------------------------------
# Resultat d'un crash
# --------------------------------------------------------------------------
def describe_exit(rc):
    if rc is None:
        return ""
    u = rc & 0xFFFFFFFF if rc >= 0 else rc
    table = {0xC0000005: "Segmentation fault (acces memoire invalide)",
             0xC00000FD: "Stack overflow (recursion infinie ?)",
             0xC0000094: "Division par zero", 0xC0000409: "Programme arrete (stack/abort)",
             -11: "Segmentation fault (acces memoire invalide)", 139: "Segmentation fault",
             -6: "Abort", 134: "Abort"}
    if u in table:
        return table[u]
    if rc in table:
        return table[rc]
    if rc < 0 or rc > 255:
        return "Crash (code 0x%X)" % (rc & 0xFFFFFFFF)
    return ""


# --------------------------------------------------------------------------
# Soumission complete
# --------------------------------------------------------------------------
def grade(ex, code, cfg, check_norm=True):
    """Fait passer le code de l'eleve a la 'moulinette'. Retourne un dict."""
    res = {"steps": {}, "validated": False, "score": 0, "messages": [], "code": None}
    tl = tools(cfg)
    gcc = tl["gcc"]
    if not gcc:
        res["fatal"] = "gcc introuvable. Installe un compilateur C (voir README)."
        return res
    env = child_env(gcc)
    code = normalize_code(code, ex, cfg)
    res["code"] = code
    os.makedirs(RUNS, exist_ok=True)
    work = tempfile.mkdtemp(prefix="run_", dir=RUNS)
    try:
        target = os.path.splitext(ex["file"])[0]
        src = os.path.join(work, ex["file"])
        with open(src, "w", encoding="utf-8", newline="\n") as f:
            f.write(code)

        # 1. fonctions interdites (rapide, avant tout)
        bad = check_forbidden(code, ex.get("allowed", []))
        res["steps"]["forbidden"] = {"ok": not bad, "functions": bad}

        # 2. norminette (lancee en parallele : elle est lente, ~4 s)
        norm_box = {}
        if check_norm and tl["norm_python"]:
            norm_thread = threading.Thread(
                target=lambda: norm_box.update(r=run_norm(tl["norm_python"], src)), daemon=True)
            norm_thread.start()
        else:
            norm_thread = None
            norm_box["r"] = {"ok": True, "skipped": True, "errors": [], "raw":
                             "" if not check_norm else "norminette introuvable : etape ignoree."}

        def _done():
            if norm_thread:
                norm_thread.join()
            res["steps"]["norm"] = norm_box["r"]
            return _finish(res)

        # 3. compilation
        objs, trace_o, err = build_runtime(gcc, env)
        if err:
            res["fatal"] = err
            return res
        sobj = os.path.join(work, target + ".o")
        # libft.h est inclus de force : un prototype different de celui de la libft
        # (ex. `int ft_strlen(char *)`) devient une erreur de compilation visible.
        rc, out = _run_quiet_env([gcc, "-Wall", "-Wextra", "-Werror", "-include",
                                  os.path.join(RUNTIME, "trace.h"), "-include", "libft.h",
                                  "-c", src, "-o", sobj]
                                 + _cflags_runtime(), env)
        out = out.replace(work + os.sep, "").replace(work, "")
        res["steps"]["compile"] = {"ok": rc == 0, "output": out[:3000]}
        if rc != 0:
            return _done()

        # 4. tests
        tsrc = os.path.join(work, "test.c")
        with open(tsrc, "w", encoding="utf-8", newline="\n") as f:
            f.write('#include "harness.h"\n' + ex["tests"])
        tobj = os.path.join(work, "test.o")
        rc, out = _run_quiet_env([gcc, "-w", "-c", tsrc, "-o", tobj] + _cflags_runtime(), env)
        if rc != 0:
            res["fatal"] = "Erreur interne dans les tests de cet exercice : " + out[:500]
            return res
        exe = os.path.join(work, "test.exe" if IS_WIN else "test")
        link = [gcc, tobj, sobj, trace_o] + [o for n, o in sorted(objs.items()) if n != target] + ["-o", exe]
        for _try in range(4):  # Windows : l'antivirus verrouille parfois collect2.exe un instant
            rc, out = _run_quiet_env(link, env)
            if rc == 0 or "CreateProcess" not in out:
                break
            time.sleep(0.6)
        if rc != 0:
            msg = out.replace(work + os.sep, "")
            res["steps"]["compile"] = {"ok": False, "output": "Erreur d'edition de liens :\n" + msg[:2000]}
            return _done()
        launch_err = None
        for _try in range(6):  # l'antivirus peut verrouiller un .exe tout neuf quelques instants
            try:
                rc, out, timed_out, flood = run_limited([exe], ex.get("timeout", 5), cwd=work, env=env)
                launch_err = None
                break
            except OSError as e:
                launch_err = e
                time.sleep(0.7)
        if launch_err:
            res["fatal"] = ("Impossible de lancer le programme de test (%s). "
                            "Reessaie dans quelques secondes (un antivirus ou un autre programme "
                            "bloque peut-etre le fichier)." % launch_err)
            return res
        res["steps"]["tests"] = parse_tests(out, rc, timed_out, flood)
        return _done()
    finally:
        th = locals().get("norm_thread")
        if th:
            th.join(90)
        shutil.rmtree(work, ignore_errors=True)


def parse_tests(out, rc, timed_out, flood):
    cases, current, total, ko = [], None, None, None
    for line in out.splitlines():
        if line.startswith("C|"):
            current = line[2:]
        elif line.startswith("T|OK|"):
            cases.append({"desc": line[5:], "ok": True})
            current = None
        elif line.startswith("T|KO|"):
            parts = line[5:].rsplit("|", 1)
            cases.append({"desc": parts[0], "ok": False})
            current = None
        elif line.startswith("S|"):
            try:
                _, total, ko = line.split("|")
                total, ko = int(total), int(ko)
            except ValueError:
                pass
    problem = ""
    if timed_out:
        problem = "Timeout : ton programme tourne trop longtemps (boucle infinie ?)"
    elif flood:
        problem = "Trop de sortie : ton programme affiche en boucle (boucle infinie ?)"
    elif total is None:
        problem = describe_exit(rc) or "Le programme s'est arrete avant la fin des tests."
    if problem and current:
        cases.append({"desc": current, "ok": False, "crash": True})
    n_ok = sum(1 for c in cases if c["ok"])
    expected = total if total is not None else len(cases)
    return {"ok": (not problem) and ko == 0 and total is not None and total > 0,
            "passed": n_ok, "total": max(expected, len(cases)), "cases": cases[:120],
            "problem": problem}


def _finish(res):
    st = res["steps"]
    t = st.get("tests")
    norm_ok = st.get("norm", {"ok": True})["ok"]
    comp_ok = st.get("compile", {"ok": False})["ok"]
    forb_ok = st.get("forbidden", {"ok": True})["ok"]
    if t:
        res["score"] = int(round(100.0 * t["passed"] / t["total"])) if t["total"] else 0
    res["validated"] = bool(t and t["ok"] and norm_ok and comp_ok and forb_ok)
    if res["validated"]:
        res["score"] = 100
    elif not (norm_ok and comp_ok and forb_ok):
        res["score"] = 0 if not t else min(res["score"], 99)
    return res


def cleanup_runs(max_age=3600):
    """Supprime les dossiers de run oublies (plantage du serveur)."""
    now = time.time()
    for d in glob.glob(os.path.join(RUNS, "run_*")):
        try:
            if now - os.path.getmtime(d) > max_age:
                shutil.rmtree(d, ignore_errors=True)
        except OSError:
            pass
