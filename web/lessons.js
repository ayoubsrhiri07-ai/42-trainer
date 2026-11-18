"use strict";
/* Cours intégrés : liste, leçon, quiz (corrigé par le serveur) et visualiseurs interactifs. */

async function viewLessons() {
  const list = await api("lessons");
  const done = list.filter((l) => l.done).length;
  $("#main").innerHTML = `
    <div class="pagehead"><div><h1>📚 Cours</h1>
      <p class="muted">Un parcours dans l'ordre conseillé : explications pas à pas, <b>pièges classiques</b>, mini-exercices avec correction, <b>visualiseurs interactifs</b> et un quiz par cours (+15 XP au premier sans-faute).</p></div>
      <div class="chipstat"><b>${done}/${list.length}</b><span>quiz réussis</span></div></div>
    <div class="grid g3">${list.map((l, i) => `
      <div class="card lesson ${l.done ? "done" : ""}" data-l="${l.id}">
        <div class="lic">${l.icon}</div>
        <div class="muted small">Leçon ${i + 1}${l.level ? " · " + esc(l.level) : ""}${l.time ? " · ~" + l.time + " min" : ""}</div>
        <h3>${esc(l.title)}</h3>
        <div class="muted">${fmt(l.summary)}</div>
        <div class="row" style="margin-top:auto">${l.done ? '<span class="pill ok">✅ quiz réussi</span>' : `<span class="pill">Quiz : ${l.questions} questions</span>`}</div>
      </div>`).join("")}</div>${FOOT}`;
  document.querySelectorAll("[data-l]").forEach((c) => c.onclick = () => { location.hash = "#/lesson/" + c.dataset.l; });
}

async function viewLesson(id) {
  let L;
  try { L = await api("lesson/" + encodeURIComponent(id)); }
  catch (e) { $("#main").innerHTML = `<div class="card">Cours introuvable. <a href="#/lessons">Retour</a></div>`; return; }
  const block = (b, i) => {
    switch (b.t) {
      case "p": return `<p>${fmt(b.x)}</p>`;
      case "ul": return `<ul>${b.x.map((x) => `<li>${fmt(x)}</li>`).join("")}</ul>`;
      case "ol": return `<ol>${b.x.map((x) => `<li>${fmt(x)}</li>`).join("")}</ol>`;
      case "code": return `<pre class="proto">${esc(b.x)}</pre>`;
      case "tip": return `<div class="tipbox">💡 ${fmt(b.x)}</div>`;
      case "h": return `<h2 class="lsec">${fmt(b.x)}</h2>`;
      case "warn": return `<div class="warnbox">⚠️ <b>Piège</b> — ${fmt(b.x)}</div>`;
      case "try": return `<details class="trybox"><summary>✍️ À toi : ${fmt(b.q)}</summary><div class="tryans">${fmt(b.a)}</div></details>`;
      case "recap": return `<div class="recapbox"><b>📌 À retenir</b><ul>${b.x.map((x) => `<li>${fmt(x)}</li>`).join("")}</ul></div>`;
      case "viz": return `<div class="viz card" id="viz${i}" data-viz="${esc(b.x)}"></div>`;
      default: return "";
    }
  };
  $("#main").innerHTML = `
    <a href="#/lessons" class="muted">← Cours</a>
    <div class="lessonpage">
      <div class="card">
        <div class="row"><span class="lic" style="font-size:2.2rem">${L.icon}</span><h1 style="margin:0">${esc(L.title)}</h1></div>
        <p class="muted">${fmt(L.summary)}</p>
        <div class="row" style="margin-bottom:6px">${L.level ? `<span class="pill lvl">${esc(L.level)}</span>` : ""}${L.time ? `<span class="pill">⏱ ~${L.time} min</span>` : ""}</div>
        ${L.blocks.map(block).join("")}
        ${L.related.length ? `<h3>Exercices liés</h3><div class="row">${L.related.map((r) => `<a class="btn ghost sm" href="#/exercise/${r.id}">${esc(r.title)}</a>`).join("")}</div>` : ""}
      </div>
      <div class="card quizbox">
        <h2>🧠 Quiz ${L.done ? '<span class="pill ok">réussi</span>' : `<span class="pill lvl">+${L.xp} XP</span>`}</h2>
        <form id="quiz">${L.quiz.map((q, qi) => `
          <fieldset class="q" data-q="${qi}"><legend>${qi + 1}. ${fmt(q.q)}</legend>
            ${q.choices.map((c, ci) => `<label class="choice"><input type="radio" name="q${qi}" value="${ci}"> <span>${fmt(c)}</span></label>`).join("")}
            <div class="explain"></div></fieldset>`).join("")}
          <button class="btn" type="submit">Valider mes réponses</button>
          <div id="quizres" style="margin-top:12px"></div>
        </form>
      </div>
    </div>${FOOT}`;
  document.querySelectorAll("[data-viz]").forEach((el) => { const f = VIZ[el.dataset.viz]; if (f) f(el); });
  $("#quiz").onsubmit = async (e) => {
    e.preventDefault();
    const answers = L.quiz.map((_, qi) => { const c = document.querySelector(`input[name=q${qi}]:checked`); return c ? +c.value : -1; });
    if (answers.includes(-1)) { toast("Réponds à toutes les questions 🙂", "err", 3000); return; }
    try {
      const r = await api("quiz", { id, answers });
      r.results.forEach((x, qi) => {
        const fs = document.querySelector(`[data-q="${qi}"]`);
        fs.classList.toggle("good", x.ok); fs.classList.toggle("bad", !x.ok);
        fs.querySelector(".explain").innerHTML = (x.ok ? "✔ " : "✘ ") + fmt(x.explain);
        fs.querySelectorAll("label.choice").forEach((lb, ci) => lb.classList.toggle("right", ci === x.answer));
      });
      $("#quizres").innerHTML = r.perfect
        ? `<div class="verdict ok">✔ Sans faute ! ${r.gained ? "+" + r.gained + " XP" : "(déjà réussi : pas de nouvel XP)"}</div>`
        : `<div class="verdict ko">${r.good}/${r.total} — relis la leçon et réessaie (la bonne réponse est en vert).</div>`;
      if (r.gained) { toast(`<b>🎉 +${r.gained} XP</b><br>Quiz « ${esc(L.title)} » réussi`, "gold", 6000); confetti(); }
      if (r.level_up) setTimeout(() => modal(`<h2>⬆️ Niveau ${r.level.level} !</h2><p>Tu es maintenant <b>${esc(r.level.title)}</b>.</p><button class="btn" onclick="closeModal()">Continuer</button>`), 700);
      (r.new_achievements || []).forEach((a, i) => setTimeout(() => toast(`<b>${a.icon} Succès débloqué</b><br>${esc(a.title)}`, "gold", 7000), 900 * (i + 1)));
      await refresh();
    } catch (err) { toast(esc(err.message), "err"); }
  };
}

/* ------------------------------------------------------------------ visualiseurs */
const VIZ = {};
const cellsHtml = (chars, cls = {}) => `<div class="cells">${chars.map((c, i) => `<div class="cell ${cls[i] || ""}"><b>${c === "\0" ? "\\0" : c === " " ? "␣" : esc(c)}</b><i>${i}</i></div>`).join("")}</div>`;

/* 1. Table ASCII */
VIZ.ascii = (el) => {
  const fns = [["ft_isalpha", (c) => (c >= 65 && c <= 90) || (c >= 97 && c <= 122)], ["ft_isdigit", (c) => c >= 48 && c <= 57],
    ["ft_isalnum", (c) => (c >= 48 && c <= 57) || (c >= 65 && c <= 90) || (c >= 97 && c <= 122)], ["ft_isascii", (c) => c >= 0 && c <= 127],
    ["ft_isprint", (c) => c >= 32 && c <= 126]];
  el.innerHTML = `<h3>🔬 Testeur de caractère</h3>
    <div class="row"><label>Tape un caractère : <input class="txt" id="ac" maxlength="1" value="a" style="width:70px;text-align:center;font-size:1.3rem"></label>
    <div id="ainfo" class="muted"></div></div><div id="ares" class="row" style="margin:10px 0"></div>
    <div class="muted small">Clique un caractère de la table :</div><div class="asciigrid" id="agrid"></div>`;
  const grid = $("#agrid", el);
  grid.innerHTML = Array.from({ length: 95 }, (_, i) => { const c = i + 32; const k = c >= 48 && c <= 57 ? "dg" : (c >= 65 && c <= 90) || (c >= 97 && c <= 122) ? "al" : ""; return `<button class="ag ${k}" data-c="${c}" title="${c}">${c === 32 ? "␣" : esc(String.fromCharCode(c))}</button>`; }).join("");
  const draw = () => {
    const v = $("#ac", el).value; if (!v) return;
    const c = v.charCodeAt(0);
    $("#ainfo", el).innerHTML = `code <b>${c}</b> · hexa <b>0x${c.toString(16).toUpperCase()}</b> · binaire <b>${c.toString(2).padStart(8, "0")}</b>`;
    $("#ares", el).innerHTML = fns.map(([n, f]) => `<span class="pill ${f(c) ? "ok" : ""}">${n} → ${f(c) ? "1" : "0"}</span>`).join("") +
      `<span class="pill">ft_toupper → ${c >= 97 && c <= 122 ? `'${String.fromCharCode(c - 32)}' (${c} − 32)` : "inchangé"}</span><span class="pill">ft_tolower → ${c >= 65 && c <= 90 ? `'${String.fromCharCode(c + 32)}' (${c} + 32)` : "inchangé"}</span>`;
  };
  $("#ac", el).oninput = draw; draw();
  grid.onclick = (e) => { const b = e.target.closest("button"); if (b) { $("#ac", el).value = String.fromCharCode(+b.dataset.c); draw(); } };
};

/* 2. Parcours d'une chaîne (strlen / strchr / strrchr) */
VIZ.strstep = (el) => {
  el.innerHTML = `<h3>🔬 Parcours pas à pas</h3>
    <div class="row"><label>Chaîne <input class="txt" id="ss" value="hello" maxlength="14" style="width:150px"></label>
    <label>Fonction <select class="txt" id="sf" style="width:auto"><option>ft_strlen</option><option>ft_strchr</option><option>ft_strrchr</option></select></label>
    <label id="scw">Caractère <input class="txt" id="sc" value="l" maxlength="1" style="width:60px"></label></div>
    <div id="sview"></div><div class="row" style="margin-top:8px"><button class="btn sm" id="snext">Étape suivante ▶</button><button class="btn ghost sm" id="sauto">▶▶ Tout jouer</button><button class="btn ghost sm" id="sreset">↺</button></div>
    <div id="smsg" class="msgline"></div>`;
  let i = 0, done = false, last = -1, result = "";
  const text = () => $("#ss", el).value;
  const fn = () => $("#sf", el).value;
  const ch = () => $("#sc", el).value || "\0";
  const reset = () => { i = 0; done = false; last = -1; result = ""; draw(); };
  const draw = () => {
    const chars = [...text()].concat(["\0"]);
    $("#scw", el).style.display = fn() === "ft_strlen" ? "none" : "";
    const cls = {}; cls[Math.min(i, chars.length - 1)] = "cur"; chars.forEach((c, k) => { if (k < i) cls[k] = "seen"; });
    if (last >= 0) cls[last] = (cls[last] || "") + " found";
    $("#sview", el).innerHTML = cellsHtml(chars, cls);
    $("#smsg", el).innerHTML = result || `i = <b>${i}</b> → <code>s[${i}]</code> = <b>${chars[Math.min(i, chars.length - 1)] === "\0" ? "'\\0'" : "'" + esc(chars[Math.min(i, chars.length - 1)]) + "'"}</b>`;
  };
  const step = () => {
    if (done) return;
    const chars = [...text()].concat(["\0"]), n = chars.length - 1, f = fn();
    if (i >= n) {      // sur le '\0'
      done = true;
      if (f === "ft_strlen") result = `✔ On est sur le '\\0' : <b>ft_strlen = ${n}</b> (le '\\0' n'est pas compté).`;
      else if (f === "ft_strchr") result = ch() === "\0" ? `✔ c vaut '\\0' : on renvoie un pointeur sur le '\\0' final (indice ${n}).` : `✘ Fin de chaîne sans trouver : <b>NULL</b>.`;
      else result = ch() === "\0" ? `✔ c vaut '\\0' : pointeur sur le '\\0' final (indice ${n}).` : last >= 0 ? `✔ Fin de chaîne : on renvoie la <b>dernière</b> position trouvée (indice ${last}).` : `✘ Jamais trouvé : <b>NULL</b>.`;
      draw(); $("#smsg", el).innerHTML = result; return;
    }
    if (f === "ft_strchr" && chars[i] === ch()) { done = true; last = i; result = `✔ Trouvé en <b>s[${i}]</b> : <b>ft_strchr</b> renvoie un pointeur sur l'indice ${i}.`; draw(); $("#smsg", el).innerHTML = result; return; }
    if (f === "ft_strrchr" && chars[i] === ch()) last = i;
    i++; draw();
  };
  $("#snext", el).onclick = step;
  $("#sauto", el).onclick = () => { let g = 0; while (!done && g++ < 40) step(); };
  $("#sreset", el).onclick = reset;
  ["ss", "sf", "sc"].forEach((id) => { $("#" + id, el).oninput = reset; $("#" + id, el).onchange = reset; });
  reset();
};

/* 3. memcpy naïf vs memmove */
VIZ.memmove = (el) => {
  el.innerHTML = `<h3>🔬 Chevauchement : copie naïve vs memmove</h3>
    <div class="row"><label>Tampon <input class="txt" id="mb" value="abcdefgh" maxlength="12" style="width:150px"></label>
    <label>src <input class="txt" id="ms" type="number" value="0" min="0" style="width:64px"></label>
    <label>dest <input class="txt" id="md" type="number" value="2" min="0" style="width:64px"></label>
    <label>n <input class="txt" id="mn" type="number" value="5" min="0" style="width:64px"></label></div>
    <div class="row" style="margin:8px 0"><button class="btn sm" id="mnaive">Copie naïve (gauche → droite)</button><button class="btn sm" id="mgood">Copie memmove (bon sens)</button></div>
    <div id="mview"></div><div id="mmsg" class="msgline"></div>`;
  const read = () => {
    const buf = [...$("#mb", el).value]; const L = buf.length;
    const s = Math.max(0, Math.min(+$("#ms", el).value || 0, L)), d = Math.max(0, Math.min(+$("#md", el).value || 0, L));
    const n = Math.max(0, Math.min(+$("#mn", el).value || 0, L - s, L - d));
    return { buf, s, d, n, L };
  };
  const show = (arr, s, d, n, label, note) => {
    const cls = {};
    for (let k = 0; k < n; k++) { cls[s + k] = (cls[s + k] || "") + " src"; cls[d + k] = (cls[d + k] || "") + " dst"; }
    return `<div class="muted small">${label}</div>${cellsHtml(arr, cls)}${note || ""}`;
  };
  const run = (mode) => {
    const { buf, s, d, n } = read();
    const exp = buf.slice(); const tmp = buf.slice(s, s + n); for (let k = 0; k < n; k++) exp[d + k] = tmp[k];   // résultat attendu (memmove correct)
    const a = buf.slice();
    const backward = mode === "good" && d > s;
    if (backward) for (let k = n - 1; k >= 0; k--) a[d + k] = a[s + k]; else for (let k = 0; k < n; k++) a[d + k] = a[s + k];
    const okRes = a.join("") === exp.join("");
    $("#mview", el).innerHTML = show(buf, s, d, n, "Avant (bleu = source, orange = destination)") + show(a, s, d, n, `Après (${backward ? "copie de droite à gauche" : "copie de gauche à droite"})`);
    $("#mmsg", el).innerHTML = okRes ? `✔ Résultat correct : <b>${esc(a.join(""))}</b>` : `✘ Résultat <b>${esc(a.join(""))}</b> au lieu de <b>${esc(exp.join(""))}</b> : on a écrasé des octets de la source avant de les lire !`;
    $("#mmsg", el).className = "msgline " + (okRes ? "okm" : "kom");
  };
  $("#mnaive", el).onclick = () => run("naive");
  $("#mgood", el).onclick = () => run("good");
  $("#mview", el).innerHTML = show([...$("#mb", el).value], 0, 2, 5, "Choisis un mode de copie ci-dessus (essaie dest > src pour voir le piège).");
};

/* 5. Listes chaînées */
VIZ.list = (el) => {
  el.innerHTML = `<h3>🔬 Liste chaînée en direct</h3>
    <div class="row"><label>Valeur <input class="txt" id="lv" value="x" maxlength="3" style="width:80px"></label>
    <button class="btn sm" id="lfront">ft_lstadd_front</button><button class="btn sm" id="lback">ft_lstadd_back</button>
    <button class="btn ghost sm" id="ldel">ft_lstdelone (tête)</button><button class="btn ghost sm" id="lclear">ft_lstclear</button></div>
    <div id="lview" style="margin:12px 0;overflow-x:auto"></div><div id="lmsg" class="msgline"></div>`;
  let items = [], nid = 1, msg = "Ajoute des noeuds : observe la <b>tête</b> (<code>*lst</code>) et le <code>next</code> du dernier.";
  const addr = (n) => "0x" + (0x1000 + n * 0x40).toString(16);
  const draw = () => {
    const nodes = items.map((it, i) => `<div class="cell ${i === 0 ? "cur" : ""}" style="min-width:74px;height:auto;padding:6px 8px;flex-direction:column;gap:2px">
        <b>"${esc(it.v)}"</b><i style="position:static">${addr(it.id)}</i><span class="muted small">next → ${i + 1 < items.length ? addr(items[i + 1].id) : "NULL"}</span></div>`);
    $("#lview", el).innerHTML = `<div class="cells" style="align-items:center;flex-wrap:nowrap"><div class="muted small" style="margin-right:8px">*lst →</div>${items.length ? nodes.join('<div style="padding:0 6px;font-size:1.3rem">→</div>') + '<div style="padding:0 6px;font-size:1.3rem">→</div><b>NULL</b>' : "<b>NULL</b> (liste vide)"}</div>`;
    $("#lmsg", el).innerHTML = msg + `<br>Noeuds alloués : <b>${items.length}</b> · <code>ft_lstsize</code> = <b>${items.length}</b>`;
  };
  const val = () => $("#lv", el).value || "?";
  $("#lfront", el).onclick = () => { items.unshift({ v: val(), id: nid++ }); msg = "<code>new->next = *lst; *lst = new;</code> : la <b>tête change</b> (d'où le <code>t_list **</code>)."; draw(); };
  $("#lback", el).onclick = () => { items.push({ v: val(), id: nid++ }); msg = items.length === 1 ? "Liste vide : <code>*lst = new;</code> (la tête change aussi !)." : "<code>ft_lstlast(*lst)->next = new;</code> : seul le <code>next</code> de l'ancien dernier change."; draw(); };
  $("#ldel", el).onclick = () => { if (!items.length) { msg = "Liste vide : rien à supprimer."; draw(); return; } const g = items.shift(); msg = `<code>ft_lstdelone</code> : <code>del("${esc(g.v)}")</code> puis <code>free(noeud)</code>. Il faut avoir retenu <code>next</code> <b>avant</b> pour ne pas perdre le reste de la liste.`; draw(); };
  $("#lclear", el).onclick = () => { const k = items.length; items = []; msg = `<code>ft_lstclear</code> : ${k} appel(s) de <code>del</code> + ${k} <code>free</code>, puis <code>*lst = NULL</code>.`; draw(); };
  draw();
};

/* 4. ft_split */
VIZ.split = (el) => {
  el.innerHTML = `<h3>🔬 Découpage en mots</h3>
    <div class="row"><label>Chaîne <input class="txt" id="sp" value="--a-b--c-" maxlength="30" style="width:230px"></label>
    <label>Séparateur <input class="txt" id="sq" value="-" maxlength="1" style="width:60px"></label></div>
    <div id="spview"></div><div id="spmsg" class="msgline"></div>`;
  const draw = () => {
    const s = [...$("#sp", el).value]; const c = $("#sq", el).value || " ";
    const cls = {}; const words = []; let cur = "", count = 0, inw = false;
    s.forEach((ch, i) => { if (ch === c) { cls[i] = "sep"; if (cur) { words.push(cur); cur = ""; } inw = false; } else { if (!inw) { count++; inw = true; cls[i] = "word start"; } else cls[i] = "word"; cur += ch; } });
    if (cur) words.push(cur);
    $("#spview", el).innerHTML = cellsHtml(s.length ? s : ["\0"], cls);
    $("#spmsg", el).innerHTML = `<code>count_words</code> = <b>${count}</b> (un mot commence quand on passe d'un séparateur à autre chose).<br>
      Tableau alloué : <b>${count + 1}</b> cases (${count} mots + <code>NULL</code>). Résultat : <code>{ ${words.map((w) => `"${esc(w)}"`).concat(["NULL"]).join(", ")} }</code><br>
      Appels à <code>malloc</code> : <b>${1 + count}</b> (1 tableau + ${count} mots) → <b>${1 + count}</b> <code>free</code> pour tout libérer.`;
  };
  $("#sp", el).oninput = draw; $("#sq", el).oninput = draw; draw();
};

/* ---------------------------------------------------------------- cours « fonction par fonction » */
const PART_NAMES = { 1: "Partie 1 · libc", 2: "Partie 2 · en plus", 3: "Partie 3 · listes" };

async function viewFuncs() {
  const list = await api("funcs");
  const seen = list.filter((f) => f.solved).length;
  const parts = [1, 2, 3];
  $("#main").innerHTML = `
    <div class="pagehead"><div><h1>🔬 Fonction par fonction</h1>
      <p class="muted">Pour chaque fonction de la libft : à quoi elle sert, le code <b>expliqué ligne par ligne</b>, les cas limites, un exemple déroulé à la main et les pièges. ⚠️ Chaque cours montre <b>une solution complète</b> : essaie d'abord l'exercice, ou lis le cours pour comprendre puis refais la fonction de mémoire.</p></div>
      <div class="chipstat"><b>${seen}/${list.length}</b><span>fonctions validées</span></div></div>
    ${parts.map((p) => {
      const fs = list.filter((f) => f.part === p);
      return fs.length ? `<h2 style="margin:18px 0 8px">${PART_NAMES[p]} <span class="muted small">(${fs.length})</span></h2>
        <div class="grid g3">${fs.map((f) => `
          <div class="card lesson ${f.solved ? "done" : ""}" data-f="${f.id}">
            <div class="muted small">${"★".repeat(f.level)}</div>
            <h3>${esc(f.id)}</h3>
            <div class="muted">${fmt(f.role)}</div>
            <div class="row" style="margin-top:auto">${f.solved ? '<span class="pill ok">✅ exercice validé</span>' : '<span class="pill">à découvrir</span>'}</div>
          </div>`).join("")}</div>` : "";
    }).join("")}${FOOT}`;
  document.querySelectorAll("[data-f]").forEach((c) => c.onclick = () => { location.hash = "#/func/" + c.dataset.f; });
}

async function viewFunc(id) {
  let F;
  try { F = await api("func/" + encodeURIComponent(id)); }
  catch (e) { $("#main").innerHTML = `<div class="card">Cours introuvable. <a href="#/funcs">Retour</a></div>`; return; }
  const num = (n) => String(n).padStart(2, " ");
  const snippet = (a, b) => F.code.slice(a - 1, b).map((l, i) => `<span class="ln">${num(a + i)}</span>${esc(l)}`).join("\n");
  const list = (title, arr, cls) => arr && arr.length ? `<h2 class="lsec">${title}</h2>${cls ? `<div class="${cls}"><ul>${arr.map((x) => `<li>${fmt(x)}</li>`).join("")}</ul></div>` : `<ul>${arr.map((x) => `<li>${fmt(x)}</li>`).join("")}</ul>`}` : "";
  $("#main").innerHTML = `
    <a href="#/funcs" class="muted">← Fonction par fonction</a>
    <div class="card funcpage">
      <div class="row"><h1 style="margin:0">🔬 ${esc(F.id)}</h1><span class="pill lvl">${PART_NAMES[F.part]}</span><span class="pill">${"★".repeat(F.level)}</span>${F.solved ? '<span class="pill ok">✅ exercice validé</span>' : ""}</div>
      <pre class="proto">${esc(F.proto)}</pre>
      <p>${fmt(F.role)}</p>
      <div class="warnbox">⚠️ Ce cours montre <b>une solution complète</b>. Pour t'entraîner, tente l'exercice avant de lire, ou relis le cours puis réécris la fonction sans regarder.
        <a class="btn ghost sm" href="#/exercise/${F.id}">🧪 Faire l'exercice</a></div>
      ${F.why.length ? `<div class="tipbox">💡 ${F.why.map(fmt).join("<br>")}</div>` : ""}
      <h2 class="lsec">Le code complet</h2>
      <pre class="proto code">${snippet(1, F.code.length)}</pre>
      <h2 class="lsec">Explication ligne par ligne</h2>
      ${F.walk.map(([a, b, text, deep]) => `<div class="walkrow"><pre class="proto">${snippet(a, b)}</pre><div class="walktext">${fmt(text)}${(deep && deep.length) ? `<details class="walkdeep" open><summary>🔎 Pourquoi on écrit ça ? (en détail)</summary>${deep.map((p) => p.includes("\n") ? `<pre class="proto">${esc(p)}</pre>` : `<p>${fmt(p)}</p>`).join("")}</details>` : ""}</div></div>`).join("")}
      ${F.trace ? `<h2 class="lsec">Exemple déroulé à la main</h2><pre class="proto">${esc(F.trace)}</pre>` : ""}
      ${list("Cas limites à connaître", F.cases)}
      ${list("Pièges classiques", F.pitfalls, "warnbox")}
      <div class="row" style="margin-top:18px;justify-content:space-between">
        ${F.prev ? `<a class="btn ghost" href="#/func/${F.prev}">← ${esc(F.prev)}</a>` : "<span></span>"}
        <a class="btn" href="#/exercise/${F.id}">🧪 Faire l'exercice</a>
        ${F.next ? `<a class="btn ghost" href="#/func/${F.next}">${esc(F.next)} →</a>` : "<span></span>"}
      </div>
    </div>${FOOT}`;
}
