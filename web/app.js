"use strict";
/* 42 Trainer — interface (aucune dependance externe, fonctionne hors ligne). */
const $ = (s, el = document) => el.querySelector(s);
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const fmt = (s) => esc(s).replace(/`([^`]+)`/g, "<code>$1</code>").replace(/\*\*([^*]+)\*\*/g, "<b>$1</b>");

/* confettis (canvas, sans dépendance) */
function confetti(n = 140) {
  const cv = $("#confetti"); if (!cv) return;
  cv.width = innerWidth; cv.height = innerHeight;
  const ctx = cv.getContext("2d"), cols = ["#19d3c5", "#7c5cff", "#ffd166", "#34e08a", "#ff5f6d", "#4aa8ff"];
  const ps = Array.from({ length: n }, () => ({ x: innerWidth / 2 + (Math.random() - .5) * 200, y: innerHeight * .35, vx: (Math.random() - .5) * 14, vy: -Math.random() * 14 - 4,
    s: 5 + Math.random() * 6, c: cols[Math.floor(Math.random() * cols.length)], r: Math.random() * 6, vr: (Math.random() - .5) * .4 }));
  let t = 0;
  (function frame() {
    ctx.clearRect(0, 0, cv.width, cv.height);
    ps.forEach((p) => { p.vy += .35; p.x += p.vx; p.y += p.vy; p.r += p.vr; ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.r); ctx.fillStyle = p.c; ctx.fillRect(-p.s / 2, -p.s / 2, p.s, p.s * .6); ctx.restore(); });
    if (++t < 130) requestAnimationFrame(frame); else ctx.clearRect(0, 0, cv.width, cv.height);
  })();
}
const stars = (n) => "★".repeat(n) + "☆".repeat(4 - n);

async function api(path, body) {
  const opt = body === undefined ? {} : { method: "POST", headers: { "Content-Type": "application/json", "X-Trainer": "1" }, body: JSON.stringify(body) };
  const r = await fetch("/api/" + path, opt);
  let data = null;
  try { data = await r.json(); } catch (e) { /* vide */ }
  if (!r.ok) { const err = new Error((data && data.error) || ("Erreur " + r.status)); err.data = data; err.status = r.status; throw err; }
  return data;
}
function toast(html, cls = "", ms = 6000) {
  const t = document.createElement("div");
  t.className = "toast " + cls; t.innerHTML = html;
  $("#toasts").appendChild(t);
  setTimeout(() => t.remove(), ms);
}
function modal(html) { const m = $("#modal"); m.innerHTML = '<div class="box">' + html + "</div>"; m.classList.remove("hidden"); }
function closeModal() { $("#modal").classList.add("hidden"); }
$("#modal").addEventListener("click", (e) => { if (e.target.id === "modal") closeModal(); });

let S = null;           // etat global (serveur)
let timerId = null;     // minuteur examen
let lastCode = {};      // brouillons en cours (par exercice)

async function refresh() {
  S = await api("state");
  const l = S.level;
  $("#mini").innerHTML = `<div><b>Niv. ${l.level}</b> · ${esc(l.title)}</div>
    <div class="bar"><i style="width:${l.pct}%"></i></div>
    <div class="muted">${l.into} / ${l.span} XP · total ${l.xp}</div>
    <div class="muted" style="margin-top:6px">🔥 série ${S.streak.current} j · ✅ ${S.solved}/${S.total}</div>`;
  return S;
}

function setNav(r) { document.querySelectorAll("#nav a").forEach((a) => a.classList.toggle("on", a.dataset.r === r)); }
const FOOT = `<div class="foot">⚠️ 42 Trainer est un outil d'entraînement <b>non officiel</b> : sa moulinette imite celle de l'école mais peut différer de la vraie. Vérifie toujours avec le sujet de ton projet et les outils de l'école.</div>`;

/* ---------------------------------------------------------------- routeur */
async function route() {
  if (timerId) { clearInterval(timerId); timerId = null; }
  const h = location.hash.replace(/^#\/?/, "");
  const [page, arg] = h.split("/");
  try {
    await refresh();
    if (!page) { setNav("home"); return viewHome(); }
    if (page === "exercises") { setNav("exercises"); return viewExercises(); }
    if (page === "exercise") { setNav("exercises"); return viewExercise(arg, false); }
    if (page === "lessons") { setNav("lessons"); return viewLessons(); }
    if (page === "lesson") { setNav("lessons"); return viewLesson(arg); }
    if (page === "funcs") { setNav("funcs"); return viewFuncs(); }
    if (page === "func") { setNav("funcs"); return viewFunc(arg); }
    if (page === "chain") { setNav("chain"); return viewChain(); }
    if (page === "exam") { setNav("exam"); return viewExam(); }
    if (page === "achievements") { setNav("achievements"); return viewAchievements(); }
    if (page === "ideas") { setNav("ideas"); return viewIdeas(); }
    if (page === "settings") { setNav("settings"); return viewSettings(); }
    location.hash = "#/";
  } catch (e) {
    $("#main").innerHTML = `<div class="card"><h2>Oups</h2><p>${esc(e.message)}</p><p class="muted">Le serveur tourne-t-il encore ? Relance « Lancer 42 Trainer ».</p></div>`;
  }
}
window.addEventListener("hashchange", route);

/* ---------------------------------------------------------------- accueil */
function viewHome() {
  const l = S.level, d = S.daily;
  const max = Math.max(1, ...S.history.map((x) => x.xp));
  const chart = S.history.map((x) => `<div class="${x.xp ? "" : "zero"}" style="height:${x.xp ? Math.max(8, 100 * x.xp / max) : 4}%" title="${x.date} : ${x.xp} XP, ${x.solved} exo(s)"></div>`).join("");
  const labels = S.history.map((x) => `<span>${x.date.slice(8)}</span>`).join("");
  const bars = (obj, name) => Object.keys(obj).sort().map((k) => { const v = obj[k]; const p = v.total ? 100 * v.solved / v.total : 0;
    return `<div class="row"><span style="width:90px">${name} ${k}</span><div class="bar sp"><i style="width:${p}%"></i></div><span class="muted">${v.solved}/${v.total}</span></div>`; }).join("");
  const rec = S.recommended;
  const log = S.log.length ? S.log.map((x) => `<div class="row"><span>✅ ${esc(x.id)}</span><span class="sp"></span><span class="ok-t">+${x.xp} XP</span></div>`).join("") : '<div class="muted">Rien pour l\'instant : valide ton premier exercice !</div>';
  $("#main").innerHTML = `
  <h1>Salut ${esc(S.config.login)} 👋</h1>
  <div class="card hero" style="margin-bottom:18px">
    <div class="ring" style="--p:${l.pct}"><div>${l.level}<small>NIVEAU</small></div></div>
    <div class="sp" style="min-width:240px">
      <div class="muted small" style="letter-spacing:.12em;text-transform:uppercase">Ton rang</div>
      <h2 style="margin:0;font-size:1.6rem">${esc(l.title)}</h2>
      <div class="bar"><i style="width:${l.pct}%"></i></div>
      <div class="muted">${l.into} / ${l.span} XP pour le niveau ${l.level + 1} · ${l.xp} XP au total</div>
    </div>
    <div class="row">
      ${rec ? `<a class="btn xl" href="#/exercise/${rec}">▶ Continuer : ${esc(rec)}</a>` : '<span class="pill ok">Tout validé 🎉</span>'}
      <a class="btn ghost xl" href="#/chain">⚡ Enchaînement</a>
    </div>
  </div>
  <div class="grid g4" style="margin-bottom:16px">
    <div class="card tile"><div class="muted">Exercices validés</div><div class="big">${S.solved}/${S.total}</div></div>
    <div class="card tile"><div class="muted">Série en cours</div><div class="big">🔥 ${S.streak.current}</div><div class="muted">record : ${S.streak.best} j ${S.streak.today ? "· ✅ aujourd'hui" : ""}</div></div>
    <div class="card tile"><div class="muted">Examens passés</div><div class="big">${S.exams.length}</div><div class="muted">${S.exams.filter((e) => e.completed).length} parfait(s)</div></div>
    <div class="card tile"><div class="muted">Succès</div><div class="big">${S.achievements.filter((a) => a.unlocked).length}/${S.achievements.length}</div></div>
    <div class="card tile"><div class="muted">Cours réussis</div><div class="big">${S.lessons.done}/${S.lessons.total}</div><a href="#/lessons">Ouvrir les cours →</a></div>
    <div class="card tile"><div class="muted">Record d'enchaînement</div><div class="big">⚡ ${S.chain.best}</div><a href="#/chain">Relever le défi →</a></div>
  </div>
  <div class="grid g2" style="margin-bottom:16px">
    <div class="card quest"><h2>📅 Défi du jour</h2>
      <p><b>${esc(d.id)}</b> <span class="pill lvl">+50 % XP</span> <span class="pill">${d.xp} XP de base</span></p>
      ${d.done ? '<span class="pill ok">✅ Déjà réussi</span>' : `<a class="btn" href="#/exercise/${d.id}">Relever le défi</a>`}
    </div>
    <div class="card"><h2>📈 14 derniers jours (XP)</h2><div class="chart">${chart}</div><div class="chart-l">${labels}</div></div>
  </div>
  <div class="grid g2">
    <div class="card"><h2>Progression</h2>${bars(S.parts, "Partie")}<div style="height:10px"></div>${bars(S.levels, "Niveau")}</div>
    <div class="card"><h2>Derniers exercices validés</h2>${log}</div>
  </div>${FOOT}`;
}

/* ---------------------------------------------------------------- liste */
let exFilter = "all";
async function viewExercises() {
  const list = await api("exercises");
  const draw = () => {
    const f = exFilter;
    const shown = list.filter((e) => f === "all" || (f === "todo" && e.status !== "solved") || (f === "solved" && e.status === "solved") ||
      (f === "p1" && e.part === 1) || (f === "p2" && e.part === 2) || (f === "p3" && e.part === 3) || (f.startsWith("l") && e.level === +f.slice(1)));
    const chips = [["all", "Tous"], ["todo", "À faire"], ["solved", "Validés"], ["p1", "Partie 1"], ["p2", "Partie 2"], ["p3", "Partie 3 · listes"], ["l1", "Niveau 1"], ["l2", "Niveau 2"], ["l3", "Niveau 3"], ["l4", "Niveau 4"]]
      .map(([k, n]) => `<button class="chip ${f === k ? "on" : ""}" data-f="${k}">${n}</button>`).join("");
    $("#main").innerHTML = `<h1>Exercices <span class="muted" style="font-size:1rem">libft</span></h1>
      <div class="filters">${chips}</div>
      <div class="grid g3">${shown.map((e) => `
        <div class="card ex ${e.status}" data-go="${e.id}">
          <div class="row"><b>${esc(e.title)}</b><span class="sp"></span>${e.status === "solved" ? '<span class="pill ok">✅ validé</span>' : e.status === "tried" ? '<span class="pill tried">essayé</span>' : ""}</div>
          <div class="muted">${esc(e.summary)}</div>
          <div class="pr">${esc(e.proto)}</div>
          <div class="row"><span class="pill lvl">${stars(e.level)}</span><span class="pill">Partie ${e.part}</span><span class="pill">${e.xp} XP</span></div>
        </div>`).join("") || '<div class="muted">Aucun exercice ici.</div>'}</div>${FOOT}`;
    document.querySelectorAll(".chip").forEach((b) => b.onclick = () => { exFilter = b.dataset.f; draw(); });
    document.querySelectorAll("[data-go]").forEach((c) => c.onclick = () => { location.hash = "#/exercise/" + c.dataset.go; });
  };
  draw();
}

/* ---------------------------------------------------------------- exercice */
async function viewExercise(id, examMode, examState, chainState) {
  let ex;
  try { ex = await api("exercise/" + encodeURIComponent(id)); }
  catch (e) { $("#main").innerHTML = `<div class="card">Exercice introuvable. <a href="#/exercises">Retour</a></div>`; return; }
  let hints = ex.hints.slice();
  const subject = `
    <div class="card subject">
      <div class="row"><h1 style="margin:0">${esc(ex.title)}</h1><span class="sp"></span>
        <span class="pill lvl">${stars(ex.level)}</span><span class="pill">${ex.xp} XP</span>${ex.solved ? '<span class="pill ok">✅ validé</span>' : ""}</div>
      <p>${fmt(ex.summary)}</p>
      <h3>Fichier à rendre</h3><code>${esc(ex.file)}</code>
      <h3>Prototype</h3><pre class="proto">${esc(ex.proto)};</pre>
      <h3>Description</h3><ul>${ex.details.map((d) => `<li>${fmt(d)}</li>`).join("")}</ul>
      <h3>Exemples</h3><table class="t">${ex.examples.map((e) => `<tr><td>${esc(e.call)}</td><td>→ ${fmt(e.result)}</td></tr>`).join("")}</table>
      <h3>Règles</h3><ul>
        <li>Fonctions externes autorisées : ${ex.allowed.length ? ex.allowed.map((a) => `<code>${esc(a)}</code>`).join(", ") : "<b>aucune</b>"}. Tu peux utiliser tes autres fonctions <code>ft_*</code>.</li>
        ${examMode ? "<li>Mode examen : la norme n'est pas vérifiée, pas d'indices.</li>" : "<li>La <b>norme</b> (norminette) est vérifiée : un exercice n'est validé que si la norme est OK.</li>"}
        <li>Compilation avec <code>-Wall -Wextra -Werror</code>.</li>
        ${ex.notes.map((n) => `<li>${fmt(n)}</li>`).join("")}</ul>
      ${examMode ? "" : `<h3>Cours liés</h3><div class="row">${ex.lessons.map((l) => `<a class="btn ghost sm" href="#/lesson/${l.id}">${l.icon} ${esc(l.title)}</a>`).join("")}<a class="btn ghost sm" href="#/func/${ex.id}" title="Explique une solution complète ligne par ligne">🔬 Décortiquer ${esc(ex.id)}</a></div>`}
      ${examMode ? "" : `<h3>Indices <span class="muted">(chaque indice coûte 20 % d'XP)</span></h3>
        <div id="hints"></div><button class="btn ghost sm" id="hintBtn"></button>`}
    </div>`;
  const editor = `
    <div>
      <div class="row" style="margin-bottom:8px"><b>${esc(ex.file)}</b><span class="sp"></span>
        <span class="muted" id="saved"></span>
        <button class="btn ghost sm" id="resetBtn">↺ Réinitialiser</button>
        <button class="btn" id="runBtn">▶ Rendre (Ctrl+Entrée)</button></div>
      <div class="editor"><pre class="gutter" id="gut"></pre><textarea id="code" spellcheck="false" autocapitalize="off" autocomplete="off" autocorrect="off"></textarea></div>
      <div id="out"></div>
    </div>`;
  const head = examMode ? examHeader(examState) : chainState ? chainHeader(chainState) : `<a href="#/exercises" class="muted">← Exercices</a>`;
  $("#main").innerHTML = head + `<div class="ex-page" style="margin-top:10px">${subject}${editor}</div>`;
  if (examMode) startExamTimer(examState);
  if (chainState) bindChain();

  const ta = $("#code"), gut = $("#gut");
  // En examen on repart TOUJOURS du fichier de depart (jamais de ton ancien brouillon d'entrainement).
  ta.value = examMode ? ((examState && examState.draft) || ex.starter) : (ex.draft || ex.starter);
  const lines = () => { const n = ta.value.split("\n").length; gut.textContent = Array.from({ length: n }, (_, i) => i + 1).join("\n"); };
  lines();
  ta.addEventListener("scroll", () => { gut.scrollTop = ta.scrollTop; });
  let saveT = null;
  ta.addEventListener("input", () => {
    lines();
    $("#saved").textContent = "…";
    clearTimeout(saveT);
    saveT = setTimeout(() => api("save", { id, code: ta.value, exam: !!examMode }).then(() => { const s = $("#saved"); if (s) s.textContent = "brouillon enregistré"; }).catch(() => {}), 1200);
  });
  ta.addEventListener("keydown", (e) => {
    if (e.key === "Tab") {
      e.preventDefault();
      const s = ta.selectionStart, en = ta.selectionEnd;
      if (e.shiftKey) return;
      ta.setRangeText("\t", s, en, "end"); ta.dispatchEvent(new Event("input"));
    } else if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) { e.preventDefault(); run(); }
    else if (e.key === "Enter") {  /* auto-indentation comme dans VS Code */
      const s = ta.selectionStart, before = ta.value.slice(0, s);
      const ind = (before.split("\n").pop().match(/^\t*/) || [""])[0];
      const extra = /\{\s*$/.test(before.split("\n").pop()) ? "\t" : "";
      e.preventDefault(); ta.setRangeText("\n" + ind + extra, s, ta.selectionEnd, "end"); ta.dispatchEvent(new Event("input"));
    }
  });
  $("#resetBtn").onclick = () => { if (confirm("Remettre le fichier de départ ? Ton code actuel sera perdu.")) { ta.value = ex.starter; ta.dispatchEvent(new Event("input")); } };

  if (!examMode) {
    const drawHints = () => {
      $("#hints").innerHTML = hints.map((h, i) => `<div class="hintbox"><b>Indice ${i + 1}</b> — ${fmt(h)}</div>`).join("");
      const left = ex.hints_total - hints.length;
      $("#hintBtn").style.display = left > 0 ? "" : "none";
      $("#hintBtn").textContent = ex.solved ? "Voir l'indice suivant (gratuit)" : `Indice ${hints.length + 1} (−20 % XP)`;
    };
    drawHints();
    $("#hintBtn").onclick = async () => {
      try { const r = await api("hint", { id }); hints = r.hints; drawHints(); await refresh(); }
      catch (e) { toast("⚠️ " + esc(e.message), "err"); }
    };
  }

  let running = false;
  async function run() {
    if (running) return;
    running = true;
    const btn = $("#runBtn"); btn.disabled = true;
    $("#out").innerHTML = `<div class="card" style="margin-top:12px"><span class="spin"></span> Moulinette en cours… <span class="muted">(norminette, compilation, tests — environ 5 s)</span></div>`;
    try {
      const r = await api("run", { id, code: ta.value, exam: !!examMode, chain: !!chainState });
      if (r.result && r.result.code && r.result.code !== ta.value) { const pos = ta.selectionStart; ta.value = r.result.code; ta.selectionStart = ta.selectionEnd = Math.min(pos, ta.value.length); lines(); }
      renderResult(r, ex, examMode);
      await refresh();
      if (r.exam_state) { examState = r.exam_state; }
      if (examMode && r.exam && r.exam.advanced) {
        if (r.exam.finished) return finishExam();
        toast("✅ Niveau validé ! Exercice suivant…", "", 3000);
        setTimeout(() => viewExam(), 1400);
      }
      if (chainState && r.chain && r.result.validated) {
        toast(`⚡ <b>Combo ×${r.chain.n}</b> — exercice suivant dans un instant…`, "gold", 2600);
        setTimeout(() => { if (location.hash === "#/chain") viewChain(); }, 2200);
      }
    } catch (e) {
      $("#out").innerHTML = `<div class="verdict ko">⚠️ ${esc(e.message)}</div>`;
    } finally { running = false; const b = $("#runBtn"); if (b) b.disabled = false; }
  }
  $("#runBtn").onclick = run;
}

function renderResult(r, ex, examMode) {
  const res = r.result;
  if (res.fatal) { $("#out").innerHTML = `<div class="verdict ko">⚠️ ${esc(res.fatal)}</div>`; return; }
  const st = res.steps;
  const tag = (ok, skipped) => skipped ? '<span class="skip-t">⏭ ignoré</span>' : ok ? '<span class="ok-t">✔ OK</span>' : '<span class="ko-t">✘ KO</span>';
  let html = res.validated
    ? `<div class="verdict ok">✔ Validé · 100/100</div>`
    : `<div class="verdict ko">✘ Non validé · ${res.score}/100</div>`;
  const n = st.norm || {};
  html += `<div class="step"><div class="h">Norminette ${tag(n.ok, n.skipped)}</div>${n.errors && n.errors.length ?
    `<div class="b">${n.errors.map((e) => `ligne ${e.line}, col ${e.col} — <b>${esc(e.code)}</b> : ${esc(e.msg)}`).join("\n")}</div>` : (n.raw && !n.ok ? `<div class="b">${esc(n.raw)}</div>` : n.raw ? `<div class="b skip-t">${esc(n.raw)}</div>` : "")}</div>`;
  const f = st.forbidden || {};
  html += `<div class="step"><div class="h">Fonctions interdites ${tag(f.ok)}</div>${f.functions && f.functions.length ? `<div class="b ko-t">Tu utilises : ${f.functions.map(esc).join(", ")} (non autorisées pour cet exercice)</div>` : ""}</div>`;
  const c = st.compile || {};
  html += `<div class="step"><div class="h">Compilation ${tag(c.ok)}</div>${c.output ? `<div class="b ${c.ok ? "" : "ko-t"}">${esc(c.output)}</div>` : ""}</div>`;
  if (st.tests) {
    const t = st.tests;
    html += `<div class="step"><div class="h">Tests ${tag(t.ok)} <span class="muted">${t.passed}/${t.total}</span></div><div class="b">${t.problem ? `<div class="ko-t">⚠ ${esc(t.problem)}</div>` : ""}${t.cases.map((k) => `<div class="case ${k.ok ? "" : "ko"}">${k.ok ? "✔" : "✘"} ${esc(k.desc)}${k.crash ? " ← le programme a planté ici" : ""}</div>`).join("")}</div></div>`;
  } else if (c.ok === false) html += `<div class="muted">Les tests ne sont lancés que si la compilation réussit.</div>`;
  if (res.validated && !examMode && r.xp && !r.xp.first_time) html += r.xp.gained > 0
    ? `<div class="muted">Déjà validé : révision comptée (+${r.xp.gained} XP, et elle compte pour ta série).</div>`
    : `<div class="muted">Déjà validé : pas de nouvel XP (5 révisions par jour rapportent de l'XP).</div>`;
  if (!res.validated && st.tests && st.tests.ok && n.ok === false) html += `<div class="hintbox">Tes tests passent mais la <b>norme</b> est KO : à l'école, ça vaut 0. Corrige la norme pour valider.</div>`;
  $("#out").innerHTML = html;
  $("#out").scrollIntoView({ behavior: "smooth", block: "nearest" });
  if (r.xp && r.xp.gained > 0) showXp(r.xp);
}

function showXp(x) {
  const lines = x.lines.map(([n, v]) => `<div class="xpline"><span>${esc(n)}</span><span class="${v < 0 ? "ko-t" : "ok-t"}">${v >= 0 ? "+" : ""}${v}</span></div>`).join("");
  toast(`<b>🎉 +${x.gained} XP</b>${lines}`, "gold", 9000);
  confetti(x.first_time ? 160 : 60);
  if (x.level_up) setTimeout(() => modal(`<h2>⬆️ Niveau ${x.level.level} !</h2><p>Tu es maintenant <b>${esc(x.level.title)}</b>.</p><button class="btn" onclick="closeModal()">Continuer</button>`), 600);
  (x.new_achievements || []).forEach((a, i) => setTimeout(() => toast(`<b>${a.icon} Succès débloqué</b><br>${esc(a.title)}`, "gold", 7000), 900 * (i + 1)));
}

/* ---------------------------------------------------------------- enchaînement */
function chainHeader(c) {
  return `<div class="card row"><div><div class="muted small">COMBO</div><div class="combo">⚡ ${c.n}</div></div>
    <div class="muted">Termine maintenant : <b>+${c.bonus_if_stopped} XP</b> de bonus<br>Record : ${c.best}</div><div class="sp"></div>
    <button class="btn ghost sm" id="skipChain" ${c.skips_left <= 0 ? "disabled" : ""}>⏭ Passer (${c.skips_left} restante${c.skips_left > 1 ? "s" : ""})</button>
    <button class="btn danger sm" id="stopChain">⏹ Terminer</button></div>`;
}
function bindChain() {
  $("#skipChain").onclick = async () => { try { await api("chain/skip", {}); viewChain(); } catch (e) { toast("⚠️ " + esc(e.message), "err"); } };
  $("#stopChain").onclick = () => stopChain(false);
}
async function stopChain(allDone) {
  try {
    const r = await api("chain/stop", {});
    await refresh();
    const x = r.result;
    if (x.n >= 3) confetti(200);
    modal(`<h2>${allDone ? "🏆 Tous les exercices de la partie 1 !" : "⚡ Enchaînement terminé"}</h2>
      <p><b>${x.n}</b> exercice${x.n > 1 ? "s" : ""} d'affilée · ${Math.floor(x.seconds / 60)} min ${x.seconds % 60} s</p>
      <div class="xpline"><span>Bonus de combo</span><span class="ok-t">+${x.xp} XP</span></div>
      ${r.new_record ? '<p>🏅 <b>Nouveau record !</b></p>' : `<p class="muted">Ton record : ${r.best}</p>`}
      ${r.level_up ? `<p>⬆️ Niveau ${r.level.level} : <b>${esc(r.level.title)}</b></p>` : ""}
      <button class="btn" onclick="closeModal();location.hash='#/chain';route();">OK</button>`);
    (r.new_achievements || []).forEach((a, i) => setTimeout(() => toast(`<b>${a.icon} Succès débloqué</b><br>${esc(a.title)}`, "gold", 7000), 900 * (i + 1)));
  } catch (e) { toast(esc(e.message), "err"); location.hash = "#/chain"; }
}
async function viewChain() {
  await refresh();
  const c = S.chain;
  if (c.active && c.current) return viewExercise(c.current, false, null, c);
  if (c.active) return stopChain(true);
  $("#main").innerHTML = `<div class="pagehead"><div><h1>⚡ Enchaînement</h1>
    <p class="muted">Un exercice <b>au hasard</b> parmi la <b>partie 1</b> (les fonctions de la libc). Dès que tu le valides, un autre arrive, et ainsi de suite.</p></div>
    <div class="chipstat"><b>${c.best}</b><span>record d'affilée</span></div></div>
    <div class="card" style="max-width:780px"><ul>
      <li>Les règles sont celles de l'entraînement : <b>norme</b> vérifiée, indices possibles (−20 % XP chacun), XP habituelle.</li>
      <li>Chaque exercice validé fait monter ton <b>combo</b>. Tu peux <b>passer</b> 2 exercices par enchaînement.</li>
      <li>À la fin, un <b>bonus de combo</b> : 10 XP pour 2, 30 pour 3, 60 pour 4, 100 pour 5, 150 pour 6 et plus.</li>
      <li>Ton code est enregistré : tu peux fermer et reprendre l'enchaînement plus tard.</li></ul>
      <button class="btn xl" id="startChain">⚡ Lancer l'enchaînement</button></div>${FOOT}`;
  $("#startChain").onclick = async () => { await api("chain/start", {}); viewChain(); };
}

/* ---------------------------------------------------------------- examen */
function examHeader(ex) {
  const dots = Array.from({ length: ex.levels }, (_, i) => `<div class="dot ${i + 1 < ex.level ? "done" : i + 1 === ex.level ? "cur" : ""}">${i + 1}</div>`).join("");
  return `<div class="card row"><div><div class="muted">Temps restant</div><div class="timer" id="timer">--:--</div></div><div class="sp"></div>
    <div class="dots">${dots}</div><div class="sp"></div><div class="muted" id="penalty"></div>
    <button class="btn danger sm" id="stopExam">Abandonner / terminer</button></div>`;
}
let examDeadline = 0;
function startExamTimer(ex) {
  examDeadline = Date.now() + ex.left * 1000;
  const tick = () => {
    const left = Math.max(0, Math.round((examDeadline - Date.now()) / 1000));
    const t = $("#timer"); if (!t) return;
    t.textContent = String(Math.floor(left / 3600)).padStart(2, "0") + ":" + String(Math.floor(left % 3600 / 60)).padStart(2, "0") + ":" + String(left % 60).padStart(2, "0");
    t.classList.toggle("low", left < 600);
    if (left === 0) { clearInterval(timerId); timerId = null; toast("⏰ Temps écoulé !", "err"); finishExam(); }
  };
  tick(); timerId = setInterval(tick, 1000);
  const b = $("#stopExam"); if (b) b.onclick = () => { if (confirm("Terminer l'examen maintenant ? Les niveaux déjà validés comptent.")) finishExam(); };
}
async function viewExam() {
  await refresh();
  if (S.exam && !S.exam.expired && S.exam.current) { return viewExercise(S.exam.current, true, S.exam); }
  if (S.exam) { return finishExam(); }
  const hist = S.exams.slice().reverse().map((e) => `<div class="row"><span>${e.completed ? "🏆" : "📝"} ${e.validated}/4 niveaux</span><span class="sp"></span><span class="ok-t">+${e.xp} XP</span></div>`).join("") || '<div class="muted">Aucun examen pour l\'instant.</div>';
  $("#main").innerHTML = `<h1>📝 Mode examen</h1>
    <div class="card" style="max-width:760px"><p>Comme un vrai exam : <b>2 heures</b>, <b>4 niveaux</b> de difficulté croissante, un seul exercice à la fois, tiré au hasard.
      Tu passes au niveau suivant en validant l'exercice courant.</p>
      <ul><li>Pas d'indices, pas de vérification de la norme (comme à l'exam).</li>
      <li>Après 3 échecs sur un exercice, une <b>pénalité d'attente</b> s'applique avant de pouvoir rendre à nouveau.</li>
      <li>XP : 25 par niveau validé, +100 si tu réussis les 4 niveaux.</li></ul>
      <button class="btn" id="startExam">▶ Commencer l'examen</button></div>
    <div class="card" style="max-width:760px;margin-top:16px"><h2>Historique</h2>${hist}</div>${FOOT}`;
  $("#startExam").onclick = async () => { await api("exam/start", {}); viewExam(); };
}
async function finishExam() {
  if (timerId) { clearInterval(timerId); timerId = null; }
  try {
    const r = await api("exam/finish", {});
    await refresh();
    const x = r.result;
    modal(`<h2>${x.completed ? "🏆 Examen parfait !" : "📝 Examen terminé"}</h2>
      <p>${x.validated} niveau(x) validé(s) sur 4 · ${Math.floor(x.seconds / 60)} min</p>
      <div class="xpline"><span>XP gagnés</span><span class="ok-t">+${x.xp}</span></div>
      ${x.capped ? '<p class="muted">Plafond atteint : seuls les 3 premiers examens de la journée rapportent de l\'XP.</p>' : ""}
      ${r.level_up ? `<p>⬆️ Niveau ${r.level.level} : <b>${esc(r.level.title)}</b></p>` : ""}
      <button class="btn" onclick="closeModal();location.hash='#/exam';">OK</button>`);
    (r.new_achievements || []).forEach((a, i) => setTimeout(() => toast(`<b>${a.icon} Succès débloqué</b><br>${esc(a.title)}`, "gold", 7000), 900 * (i + 1)));
    location.hash = "#/exam"; route();
  } catch (e) { toast(esc(e.message), "err"); location.hash = "#/exam"; }
}

/* ---------------------------------------------------------------- succès */
function viewAchievements() {
  $("#main").innerHTML = `<h1>🏆 Succès</h1><div class="grid g4">${S.achievements.map((a) => `
    <div class="card ach ${a.unlocked ? "" : "locked"}"><div class="ic">${a.icon}</div><b>${esc(a.title)}</b><div class="muted">${esc(a.desc)}</div>
    ${a.unlocked ? `<div class="pill ok" style="margin-top:6px">débloqué</div>` : ""}</div>`).join("")}</div>${FOOT}`;
}

/* ---------------------------------------------------------------- idées */
async function viewIdeas() {
  const ideas = await api("ideas");
  $("#main").innerHTML = `<h1>💡 Idées & retours</h1>
    <p class="muted">Dis ce que tu aimerais améliorer ou ajouter. Tout est enregistré dans <code>data/ideas.json</code> : tu peux le montrer à Claude pour qu'il fasse évoluer l'appli.</p>
    <div class="card" style="max-width:760px"><select class="txt" id="cat" style="margin-bottom:8px">
      <option>nouvel exercice</option><option>nouvelle fonctionnalité</option><option>bug</option><option>design</option><option>moulinette</option><option>autre</option></select>
      <textarea class="txt" id="txt" placeholder="Ex : ajouter les exercices de listes chaînées (bonus), un mode révision…"></textarea>
      <div class="row" style="margin-top:8px"><button class="btn" id="sendIdea">Enregistrer</button></div></div>
    <div class="card" style="max-width:760px;margin-top:16px"><h2>Mes idées (${ideas.length})</h2>
      ${ideas.slice().reverse().map((i) => `<div style="padding:8px 0;border-top:1px solid var(--line)"><span class="pill">${esc(i.category)}</span> <span class="muted">${esc(i.date)}</span><div>${esc(i.text)}</div></div>`).join("") || '<div class="muted">Aucune idée pour l\'instant.</div>'}</div>`;
  $("#sendIdea").onclick = async () => {
    try { await api("ideas", { text: $("#txt").value, category: $("#cat").value }); toast("💡 Idée enregistrée !"); viewIdeas(); }
    catch (e) { toast(esc(e.message), "err"); }
  };
}

/* ---------------------------------------------------------------- réglages */
function viewSettings() {
  const c = S.config, t = S.tools;
  $("#main").innerHTML = `<h1>⚙️ Réglages</h1>
    <div class="card" style="max-width:640px"><h2>En-tête 42</h2>
      <p class="muted">Utilisé pour générer l'en-tête 42 de tes fichiers (comme l'extension de VS Code).</p>
      <label>Login<input class="txt" id="login" value="${esc(c.login)}"></label><div style="height:8px"></div>
      <label>Email<input class="txt" id="email" value="${esc(c.email)}"></label><div style="height:10px"></div>
      <button class="btn" id="saveCfg">Enregistrer</button></div>
    <div class="card" style="max-width:640px;margin-top:16px"><h2>Outils détectés</h2>
      <div>gcc : ${t.gcc ? '<span class="ok-t">✔ trouvé</span>' : '<span class="ko-t">✘ introuvable</span>'}</div>
      <div>norminette : ${t.norm_python ? '<span class="ok-t">✔ trouvée</span>' : '<span class="ko-t">✘ introuvable (étape ignorée)</span>'}</div></div>
    <div class="card" style="max-width:640px;margin-top:16px"><h2>Apparence</h2>
      <button class="btn ghost" id="theme">Basculer thème clair / sombre</button></div>
    <div class="card" style="max-width:640px;margin-top:16px"><h2>Zone dangereuse</h2>
      <button class="btn danger" id="reset">Remettre ma progression à zéro</button></div>${FOOT}`;
  $("#saveCfg").onclick = async () => { try { await api("config", { login: $("#login").value, email: $("#email").value }); toast("Enregistré ✔"); await refresh(); } catch (e) { toast(esc(e.message), "err"); } };
  $("#theme").onclick = () => { const l = document.documentElement.dataset.theme === "light" ? "dark" : "light"; document.documentElement.dataset.theme = l; try { localStorage.setItem("theme", l); } catch (e) { /* ignore */ } };
  $("#reset").onclick = async () => { if (prompt("Tape RESET pour tout effacer (XP, exercices, succès) :") === "RESET") { await api("reset", { confirm: "RESET" }); toast("Progression remise à zéro."); location.hash = "#/"; route(); } };
}

try { const th = localStorage.getItem("theme"); if (th) document.documentElement.dataset.theme = th; } catch (e) { /* ignore */ }
/* route() est lancé par index.html une fois lessons.js chargé */
