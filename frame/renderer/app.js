"use strict";
/* Mirror Frame — renderer. Conversa com o main só pela API window.mirror. */

const $ = (id) => document.getElementById(id);
let CFG = null;                 // config:get
let tabs = [];                  // {sid, title, kind:'mirror'|'system', term, fit, slot, exited}
let activeTab = -1;             // índice em tabs
let activeView = "sessions";    // sessions | setup | personas
let warmupOut = "";

/* ============ terminal ============ */
const TERM_THEME = {
  background: "#0e0f14", foreground: "#eceff7", cursor: "#9dbeff",
  selectionBackground: "#3d4d75",
  black: "#1b1d26", brightBlack: "#9aa1b8",
  blue: "#8fb4ff", brightBlue: "#a9c4ff",
  magenta: "#b79cff", brightMagenta: "#cbb6ff",
  green: "#58c08a", brightGreen: "#79d3a6",
  yellow: "#e0b45c", brightYellow: "#eccb85",
  red: "#d16060", brightRed: "#e08585",
  cyan: "#58bfb0", brightCyan: "#7fd3c7",
  white: "#c9cdd9", brightWhite: "#eceef4",
};

function makeTab(sid, title, kind) {
  const slot = document.createElement("div");
  slot.className = "term-slot";
  $("term-host").appendChild(slot);
  const term = new Terminal({
    theme: TERM_THEME, fontFamily: '"Cascadia Mono", Consolas, monospace',
    fontSize: 14, cursorBlink: true, allowProposedApi: true, scrollback: 5000,
  });
  const fit = new FitAddon.FitAddon();
  term.loadAddon(fit);
  term.open(slot);
  term.onData((d) => window.mirror.session.input(sid, d));
  term.onResize(({ cols, rows }) => window.mirror.session.resize(sid, cols, rows));
  const t = { sid, title, kind, term, fit, slot, exited: false };
  tabs.push(t);
  activeTab = tabs.length - 1;
  activeView = "sessions";
  render();
  requestAnimationFrame(() => { fit.fit(); term.focus(); });
  return t;
}

window.mirror.session.onData((sid, data) => {
  tabs.find((t) => t.sid === sid)?.term.write(data);
});
window.mirror.session.onExit((sid, code) => {
  const t = tabs.find((x) => x.sid === sid);
  if (t) {
    t.exited = true;
    t.term.write(`\r\n\x1b[90m[sessão encerrada · exit ${code}]\x1b[0m\r\n`);
    renderStatus();
  }
});
window.mirror.gate.onChange((g) => { if (CFG) { CFG.gate = g; renderStatus(); } });
window.addEventListener("resize", () => currentTab()?.fit.fit());

function currentTab() { return activeTab >= 0 ? tabs[activeTab] : null; }

async function openMirrorSession() {
  try {
    const r = await window.mirror.session.open();
    if (!r.ok) { flashEmpty("Não deu para abrir a sessão", r.err, true); return; }
    makeTab(r.id, `◇ sessão ${tabs.filter(t => t.kind === "mirror").length + 1}`, "mirror");
  } catch (e) {
    flashEmpty("Erro inesperado ao abrir a sessão", String(e?.message ?? e), true);
  }
}
async function openSystem(script, title) {
  try {
    const r = await window.mirror.session.openSystem(script);
    if (!r.ok) { flashEmpty("Não deu para abrir o terminal", r.err, true); return; }
    makeTab(r.id, title, "system");
  } catch (e) {
    flashEmpty("Erro inesperado ao abrir o terminal", String(e?.message ?? e), true);
  }
}
async function closeTab(i) {
  const t = tabs[i];
  await window.mirror.session.close(t.sid);
  t.term.dispose(); t.slot.remove();
  tabs.splice(i, 1);
  if (activeTab >= tabs.length) activeTab = tabs.length - 1;
  if (tabs.length === 0 && activeView === "sessions") activeView = "setup";
  render();
}

/* ============ render ============ */
function render() {
  renderTabs();
  const showingSessions = activeView === "sessions" && tabs.length > 0;
  tabs.forEach((t, i) => t.slot.classList.toggle("hidden", !(showingSessions && i === activeTab)));
  $("panel-setup").classList.toggle("hidden", activeView !== "setup");
  $("panel-personas").classList.toggle("hidden", activeView !== "personas");
  $("empty-state").classList.toggle("hidden", !(activeView === "sessions" && tabs.length === 0));
  if (activeView === "setup") renderSetup();
  if (activeView === "personas") renderPersonas();
  if (activeView === "sessions" && tabs.length === 0) renderEmpty();
  if (showingSessions) requestAnimationFrame(() => { currentTab()?.fit.fit(); currentTab()?.term.focus(); });
  renderStatus();
}

function renderTabs() {
  const stz = $("tabstrip");
  stz.innerHTML = tabs.map((t, i) => `
    <button class="tab ${activeView === "sessions" && i === activeTab ? "active" : ""}" data-tab="${i}">
      <span class="dot ${t.kind === "system" ? "sys" : ""}"></span> ${t.title}
      <span class="x" data-close="${i}" title="fechar">✕</span>
    </button>`).join("") + `
    <button class="tab newtab" id="tab-new" title="nova sessão Mirror">＋</button>
    <div class="tabspacer"></div>
    <button class="tab util ${activeView === "personas" ? "active" : ""}" id="tab-personas">◇ Personas</button>
    <button class="tab util ${activeView === "setup" ? "active" : ""}" id="tab-setup">⚙ Setup</button>`;
  stz.querySelectorAll("[data-tab]").forEach((b) => b.addEventListener("click", (e) => {
    if (e.target.dataset.close !== undefined) return;
    activeTab = +b.dataset.tab; activeView = "sessions"; render();
  }));
  stz.querySelectorAll("[data-close]").forEach((x) => x.addEventListener("click", (e) => {
    e.stopPropagation(); closeTab(+x.dataset.close);
  }));
  $("tab-new").addEventListener("click", openMirrorSession);
  $("tab-personas").addEventListener("click", () => { activeView = "personas"; render(); });
  $("tab-setup").addEventListener("click", () => { activeView = "setup"; render(); });
}

function renderEmpty() {
  const g = CFG?.gate;
  if (!g?.warm) {
    $("empty-title").textContent = "Preparando o Mirror…";
    $("empty-msg").textContent = "Rodando o warm-up (runtime status) antes de liberar sessões.";
    $("btn-open-session").classList.add("hidden");
    $("btn-goto-setup").classList.add("hidden");
  } else {
    $("empty-title").textContent = "Pronto para conversar";
    $("empty-msg").textContent = "Abra uma sessão — o Pi assume daqui, com a memória do Mirror ligada.";
    $("btn-open-session").classList.remove("hidden");
    $("btn-goto-setup").classList.add("hidden");
  }
}
function flashEmpty(title, msg, showSetup) {
  activeView = "sessions";
  render();
  $("empty-state").classList.remove("hidden");
  $("empty-title").textContent = title;
  $("empty-msg").textContent = msg;
  $("btn-open-session").classList.toggle("hidden", !CFG?.gate?.warm);
  $("btn-goto-setup").classList.toggle("hidden", !showSetup);
}

/* ============ setup ============ */
function chk(l, name, detail, btn) {
  return `<div class="check"><span class="light ${l}"></span><span class="name">${name}</span>
    <span class="detail">${detail}</span>${btn ?? ""}</div>`;
}

function renderSetup() {
  const t = CFG.tools, g = CFG.gate;
  const sess = tabs.filter((x) => x.kind === "mirror" && !x.exited).length;
  $("panel-setup").innerHTML = `
    <h2>Setup do Mirror</h2>
    <p class="sub">Cada item é um check real. Os botões executam apenas comandos oficiais
    (argv fixo) — nada é editado à mão.</p>
    <div class="checks">
      ${chk(CFG.mirrorRoot ? "g" : "r", "Instalação do Mirror", CFG.mirrorRoot ?? "não encontrada — rode o instalador")}
      ${chk(CFG.mirrorUser ? "g" : "y", "Identidade", CFG.mirrorUser ? `MIRROR_USER = ${CFG.mirrorUser}` : "não configurada")}
      ${chk(CFG.hasKey ? "g" : "y", "Chave OpenRouter (memória)", CFG.hasKey ? "configurada no .env" : "ausente")}
      ${chk(t.uv ? "g" : "r", "uv (runtime Python)", t.uv ?? "ausente", t.uv ? "" : `<button id="su-boot1">Instalar pré-requisitos</button>`)}
      ${chk(t.pi ? "g" : "r", "Pi (harness da conversa)", t.pi ?? "ausente", t.pi ? "" : `<button id="su-boot2">Instalar pré-requisitos</button>`)}
      ${chk(t.git ? "g" : "r", "Git", t.git ?? "ausente")}
      ${chk(g.warm ? "g" : "y", "Warm-up (runtime status)", g.warm ? "concluído — sessões liberadas" : "pendente",
        `<button id="su-warm">${g.warm ? "Rodar de novo" : "Rodar warm-up"}</button>`)}
      ${chk("g", "Update do Mirror", "git fast-forward + backup + migrations, sem reinstalar",
        `<button id="su-upmirror" ${g.canUpdate ? "" : "disabled"}>Atualizar Mirror</button>`)}
      ${chk("g", "Update do Pi", "@earendil-works/pi-coding-agent@latest (npm)",
        `<button id="su-uppi">Atualizar Pi</button>`)}
      ${chk("g", "Terminal do sistema", "PowerShell dentro do frame", `<button id="su-shell">Abrir terminal</button>`)}
    </div>
    ${sess > 0 ? `<p class="setup-note">⚠ Update do Mirror bloqueado: feche as ${sess} sessão(ões) Mirror abertas (regra R2 — backup e migrations exigem exclusividade).</p>` : ""}
    <div class="mono-out ${warmupOut ? "" : "hidden"}" id="su-out">${escapeHtml(warmupOut)}</div>`;
  const wire = (id, fn) => { const b = $(id); if (b) b.addEventListener("click", fn); };
  wire("su-warm", runWarmup);
  wire("su-boot1", () => openSystem("bootstrap", "⚙ bootstrap"));
  wire("su-boot2", () => openSystem("bootstrap", "⚙ bootstrap"));
  wire("su-shell", () => openSystem("shell", "› powershell"));
  wire("su-uppi", async (e) => {
    e.target.disabled = true; e.target.textContent = "atualizando…";
    const r = await window.mirror.cmd.run("updatePi");
    warmupOut = (r.out + "\n" + r.err).trim(); renderSetup();
  });
  wire("su-upmirror", async (e) => {
    e.target.disabled = true; e.target.textContent = "atualizando…";
    const r = await window.mirror.cmd.run("updateMirror");
    warmupOut = (r.out + "\n" + r.err).trim();
    CFG = await window.mirror.config.get();
    renderSetup();
  });
}

async function runWarmup() {
  warmupOut = "rodando: uv run python -m memory runtime status …";
  renderSetup();
  const r = await window.mirror.cmd.run("warmup");
  warmupOut = (r.out + (r.err ? "\n" + r.err : "")).trim() || "(sem saída)";
  CFG = await window.mirror.config.get();
  render();
}

/* ============ personas ============ */
let personasOut = "";
function renderPersonas() {
  $("panel-personas").innerHTML = `
    <h2>Personas &amp; Modos</h2>
    <p class="sub">Direto da sua base local (<code>memory identity list</code>). O Mirror ativa a
    persona sozinho — aqui você aprende a reconhecê-las.</p>
    <div class="mono-out" id="p-out">${escapeHtml(personasOut || "carregando…")}</div>
    <div class="tryit">
      <div class="lbl">Experimente — qual persona responderia? (detect-persona real)</div>
      <input id="p-try" placeholder='ex.: "o deploy quebrou depois do merge"'>
      <div class="res" id="p-tryres"></div>
    </div>`;
  if (!personasOut) {
    window.mirror.cmd.run("identityList").then((r) => {
      personasOut = (r.out || r.err || "(sem saída)").trim();
      const el = $("p-out"); if (el) el.textContent = personasOut;
    });
  }
  let timer = null;
  $("p-try").addEventListener("input", (e) => {
    clearTimeout(timer);
    const q = e.target.value.trim();
    if (!q) { $("p-tryres").textContent = ""; return; }
    timer = setTimeout(async () => {
      $("p-tryres").textContent = "consultando detect-persona…";
      const r = await window.mirror.cmd.run("detectPersona", { query: q });
      $("p-tryres").textContent = (r.out || r.err || "(sem saída)").trim();
    }, 500);
  });
}

/* ============ statusbar ============ */
function renderStatus() {
  const g = CFG?.gate ?? {};
  const t = currentTab();
  const left = t && activeView === "sessions"
    ? `<span><b>${t.title}</b>${t.exited ? " · encerrada" : ""}</span>`
    : `<span>◇ <b>Mirror Mind</b></span>`;
  $("statusbar").innerHTML = left + `
    <span>warm-up <b>${g.warm ? "ok" : "pendente"}</b></span>
    <span>sessões <b>${g.sessions ?? 0}</b></span>
    <span class="right">
      <span>${CFG?.mirrorUser ? escapeHtml(CFG.mirrorUser) + " · " : ""}frame v${CFG?.frameVersion ?? "?"}</span>
      <span class="okdot">● local</span>
    </span>`;
}

function escapeHtml(s) {
  return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

/* ============ boot ============ */
async function boot() {
  CFG = await window.mirror.config.get();
  if (CFG.firstRun && CFG.mirrorRoot) {
    $("view-wizard").classList.remove("hidden");
    $("w-user").addEventListener("input", (e) => {
      $("w-user-hint").textContent = e.target.value.trim()
        ? `Casa: ~\\.mirror-minds\\${e.target.value.trim()}` : "";
    });
    $("w-save").addEventListener("click", async () => {
      const user = $("w-user").value.trim();
      const key = $("w-key").value.trim();
      if (!/^[A-Za-z0-9_-]{1,64}$/.test(user)) {
        $("w-msg").textContent = "Nome sem espaços/acentos (letras, números, - e _)."; return;
      }
      if (key && !key.startsWith("sk-or-")) { $("w-msg").textContent = "A chave OpenRouter começa com sk-or-…"; return; }
      const btn = $("w-save"); btn.disabled = true;
      const vals = { MIRROR_USER: user };
      if (key) vals.OPENROUTER_API_KEY = key;
      const r = await window.mirror.config.save(vals);
      if (!r.ok) { $("w-msg").textContent = r.err; btn.disabled = false; return; }
      // onboarding real, como o configure.ps1: init → seed (idempotente)
      $("w-msg").textContent = "Criando sua identidade local (memory init)…";
      const ri = await window.mirror.cmd.run("initIdentity", { user });
      if (!ri.ok && !/already|exists|existe/i.test(ri.out + ri.err)) {
        $("w-msg").textContent = "init falhou: " + (ri.err || ri.out).slice(0, 300);
        btn.disabled = false; return;
      }
      $("w-msg").textContent = "Semeando identidade (memory seed)…";
      await window.mirror.cmd.run("seed");
      CFG = await window.mirror.config.get();
      $("view-wizard").classList.add("hidden");
      enterFrame();
    });
    return;
  }
  enterFrame();
}

async function enterFrame() {
  $("view-frame").classList.remove("hidden");
  $("btn-open-session").addEventListener("click", openMirrorSession);
  $("btn-goto-setup").addEventListener("click", () => { activeView = "setup"; render(); });
  activeView = "sessions";
  render();
  // warm-up serializado antes de liberar sessões (mitiga a lacuna fcntl)
  if (CFG.mirrorRoot && CFG.tools.uv) {
    const r = await window.mirror.cmd.run("warmup");
    warmupOut = (r.out + (r.err ? "\n" + r.err : "")).trim();
    CFG = await window.mirror.config.get();
    render();
    if (!CFG.gate.warm) flashEmpty("Warm-up falhou", "Veja o Setup para diagnosticar (saída registrada).", true);
  } else {
    flashEmpty("Mirror ainda não instalado por completo",
      CFG.mirrorRoot ? "uv ausente — instale os pré-requisitos no Setup." : "Instalação não encontrada — rode o instalador ou o bootstrap.", true);
  }
}

boot();
