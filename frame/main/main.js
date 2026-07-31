"use strict";
// Mirror Frame — processo principal.
// Papel: orquestrar. Toda mutação passa pelo command-registry (argv fixo);
// sessões Pi respeitam o SessionGate; segurança Electron: contextIsolation,
// sem nodeIntegration, sem conteúdo remoto.
const { app, BrowserWindow, ipcMain } = require("electron");
const { execFile } = require("node:child_process");
const path = require("node:path");
const fs = require("node:fs");
const os = require("node:os");

const { resolveMirrorRoot } = require("./root-resolve.js");
const { sessionEnv } = require("./env-profile.js");
const { buildCommand } = require("./command-registry.js");
const { SessionGate } = require("./session-gate.js");
const { loadEnvFile, saveEnvValues, isFirstRun } = require("./config-store.js");
const { PtyManager } = require("./pty-manager.js");

const MIRROR_ROOT = resolveMirrorRoot({});
const gate = new SessionGate();
const ptys = new PtyManager();
let win = null;

/* ---------- helpers ---------- */
const { execFileSync } = require("node:child_process");

// PATH fresco lido do registro: logo após a instalação, o PATH herdado pelo
// processo é obsoleto (git/node/uv/pi acabaram de entrar). Sem isso, o frame
// não enxerga as ferramentas até o usuário reiniciar a sessão do Windows.
function _regPath(hive, key) {
  try {
    const out = execFileSync("reg.exe", ["query", `${hive}\\${key}`, "/v", "Path"],
      { encoding: "utf8", windowsHide: true });
    const m = /Path\s+REG(?:_EXPAND)?_SZ\s+(.+)/i.exec(out);
    if (!m) return "";
    return m[1].trim().replace(/%([^%]+)%/g, (_s, v) => process.env[v] ?? `%${v}%`);
  } catch { return ""; }
}

function freshPath() {
  const sys = _regPath("HKLM", "SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment");
  const usr = _regPath("HKCU", "Environment");
  const parts = [process.env.PATH ?? "", sys, usr].join(";")
    .split(";").map((p) => p.trim()).filter(Boolean);
  return [...new Set(parts)].join(";");
}

function frameEnv() {
  const e = sessionEnv(process.env, MIRROR_ROOT);
  e.PATH = freshPath();
  return e;
}

function whichSync(cmd) {
  try {
    const out = execFileSync("where.exe", [cmd],
      { encoding: "utf8", windowsHide: true, env: { ...process.env, PATH: freshPath() } });
    return out.split(/\r?\n/)[0]?.trim() || null;
  } catch { return null; }
}

const TOOLS = () => ({
  pi: whichSync("pi.cmd") || whichSync("pi"),
  uv: whichSync("uv.exe") || whichSync("uv"),
  git: whichSync("git.exe") || whichSync("git"),
  node: whichSync("node.exe"),
});

function runCommand(id, opts = {}) {
  return new Promise((resolve) => {
    let c;
    try { c = buildCommand(id, opts); }
    catch (e) { return resolve({ ok: false, code: -1, out: "", err: String(e.message) }); }
    const cwd = c.cwd === "root" ? MIRROR_ROOT : __dirname;
    if (!cwd) return resolve({ ok: false, code: -1, out: "", err: "MIRROR_ROOT não resolvido" });
    const file = c.file === "npm" && process.platform === "win32" ? "npm.cmd" : c.file;
    execFile(file, c.args, {
      cwd, env: frameEnv(), timeout: c.timeoutMs,
      windowsHide: true, encoding: "utf8", maxBuffer: 4 * 1024 * 1024, shell: false,
    }, (error, stdout, stderr) => {
      resolve({
        ok: !error, code: error?.code ?? 0,
        out: String(stdout ?? ""), err: String(stderr ?? (error ? error.message : "")),
      });
    });
  });
}

function gateState() {
  return {
    warm: gate.isWarm, updating: gate.isUpdating, sessions: gate.openSessions,
    canOpenSession: gate.canOpenSession(), canUpdate: gate.canUpdate(),
  };
}
function pushGate() { win?.webContents.send("gate:changed", gateState()); }

/* ---------- IPC: config ---------- */
ipcMain.handle("config:get", () => {
  const env = MIRROR_ROOT ? loadEnvFile(MIRROR_ROOT) : {};
  return {
    mirrorRoot: MIRROR_ROOT,
    firstRun: MIRROR_ROOT ? isFirstRun(MIRROR_ROOT) : true,
    mirrorUser: env.MIRROR_USER ?? "",
    hasKey: Boolean(env.OPENROUTER_API_KEY && env.OPENROUTER_API_KEY.startsWith("sk-or-")),
    tools: TOOLS(),
    gate: gateState(),
    frameVersion: app.getVersion(),
  };
});

ipcMain.handle("config:save", (_e, values) => {
  if (!MIRROR_ROOT) return { ok: false, err: "MIRROR_ROOT não resolvido" };
  const allowed = {};
  if (typeof values?.MIRROR_USER === "string" && values.MIRROR_USER.trim()) {
    allowed.MIRROR_USER = values.MIRROR_USER.trim();
  }
  if (typeof values?.OPENROUTER_API_KEY === "string" && values.OPENROUTER_API_KEY.startsWith("sk-or-")) {
    allowed.OPENROUTER_API_KEY = values.OPENROUTER_API_KEY.trim();
  }
  if (Object.keys(allowed).length === 0) return { ok: false, err: "nada válido para salvar" };
  saveEnvValues(MIRROR_ROOT, allowed);
  return { ok: true };
});

/* ---------- IPC: comandos allowlisted ---------- */
ipcMain.handle("cmd:run", async (_e, id, opts) => {
  if (id === "updateMirror") {
    if (!gate.canUpdate()) return { ok: false, code: -1, out: "", err: "update bloqueado: feche as sessões primeiro (regra R2)" };
    gate.updateStarted(); pushGate();
    const r = await runCommand(id, opts ?? {});
    gate.updateFinished(); pushGate();
    return r;
  }
  const r = await runCommand(id, opts ?? {});
  if (id === "warmup" && r.ok) { gate.warmupDone(); pushGate(); }
  return r;
});

/* ---------- IPC: assinaturas do Pi (auth.json é a fonte da verdade) ---------- */
// O Pi grava os tokens OAuth em ~/.pi/agent/auth.json. O frame NUNCA toca o
// arquivo — só observa as chaves para saber quando um /login concluiu.
const AUTH_PATH = path.join(os.homedir(), ".pi", "agent", "auth.json");
function authProviders() {
  try { return Object.keys(JSON.parse(fs.readFileSync(AUTH_PATH, "utf8"))); }
  catch { return []; }
}
ipcMain.handle("login:providers", () => authProviders());

// Login fluido: Pi roda num PTY oculto com o slash command como mensagem
// inicial; o próprio Pi abre o navegador (OAuth). O frame só observa auth.json.
const LOGIN_PROVIDERS = new Set(["anthropic", "openai-codex"]);
ipcMain.handle("login:start", (_e, slug) => {
  try {
    if (!LOGIN_PROVIDERS.has(slug)) return { ok: false, err: `provedor não suportado: ${slug}` };
    if (!TOOLS().pi) return { ok: false, err: "Pi não encontrado no PATH — rode o bootstrap no Setup" };
    // Pi puro, sem argumentos: mensagem inicial via CLI vira PROMPT pro modelo
    // (não comando). O renderer digita '/login <slug>' quando o Pi anuncia
    // prontidão no output.
    const id = openPty({
      file: "cmd.exe", args: ["/c", "pi"],
      cwd: MIRROR_ROOT ?? process.cwd(), env: frameEnv(),
    }, "system");
    return { ok: true, id };
  } catch (e) {
    return { ok: false, err: `falha ao iniciar login: ${e.message}` };
  }
});

/* ---------- IPC: sessões PTY ---------- */
// ConPTY não lança .cmd diretamente — o Pi (shim npm) precisa do cmd.exe /c.
const SYSTEM_SCRIPTS = {
  shell: () => ({ file: "powershell.exe", args: ["-NoLogo", "-NoExit"], cwd: MIRROR_ROOT ?? process.cwd() }),
  bootstrap: () => ({
    file: "powershell.exe",
    args: ["-NoProfile", "-ExecutionPolicy", "Bypass", "-NoExit", "-File",
      path.join(MIRROR_ROOT ?? "", "installer", "bootstrap.ps1")],
    cwd: MIRROR_ROOT ?? process.cwd(),
  }),
  login: () => ({ file: "cmd.exe", args: ["/c", "pi"], cwd: MIRROR_ROOT ?? process.cwd() }),
};

function openPty(spec, kind) {
  const id = ptys.open(spec,
    (sid, data) => win?.webContents.send("session:data", sid, data),
    (sid, code) => {
      if (kind === "mirror") { gate.sessionClosed(sid); pushGate(); }
      win?.webContents.send("session:exit", sid, code);
    });
  return id;
}

ipcMain.handle("session:open", () => {
  try {
    if (!gate.canOpenSession()) return { ok: false, err: "warm-up necessário antes de abrir sessões" };
    if (!TOOLS().pi) return { ok: false, err: "Pi não encontrado no PATH — rode o bootstrap no Setup e reabra o app" };
    const id = openPty({
      file: "cmd.exe", args: ["/c", "pi"], cwd: MIRROR_ROOT, env: frameEnv(),
    }, "mirror");
    gate.sessionOpened(id); pushGate();
    return { ok: true, id };
  } catch (e) {
    return { ok: false, err: `falha ao abrir sessão: ${e.message}` };
  }
});

ipcMain.handle("session:openSystem", (_e, script) => {
  try {
    const mk = SYSTEM_SCRIPTS[script];
    if (!mk) return { ok: false, err: `script desconhecido: ${script}` };
    const spec = mk();
    if (script === "bootstrap" && !fs.existsSync(spec.args[spec.args.length - 1])) {
      return { ok: false, err: "installer/bootstrap.ps1 não encontrado no MIRROR_ROOT" };
    }
    const id = openPty({ ...spec, env: frameEnv() }, "system");
    return { ok: true, id };
  } catch (e) {
    return { ok: false, err: `falha ao abrir terminal: ${e.message}` };
  }
});

ipcMain.on("session:input", (_e, id, data) => {
  if (typeof data === "string" && data.length <= 8192) ptys.write(id, data);
});
ipcMain.on("session:resize", (_e, id, cols, rows) => ptys.resize(id, Number(cols) || 80, Number(rows) || 24));
ipcMain.handle("session:close", async (_e, id) => { await ptys.close(id); return { ok: true }; });

/* ---------- janela ---------- */
function createWindow() {
  win = new BrowserWindow({
    width: 1180, height: 760, minWidth: 900, minHeight: 560,
    backgroundColor: "#14151b",
    title: "Mirror Mind",
    icon: path.join(__dirname, "..", "assets", "mirror.ico"),
    webPreferences: {
      preload: path.join(__dirname, "..", "preload.js"),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: false,
      spellcheck: false,
    },
  });
  win.removeMenu();
  win.loadFile(path.join(__dirname, "..", "renderer", "index.html"));
}

app.whenReady().then(() => {
  createWindow();
  fs.watchFile(AUTH_PATH, { interval: 1200 }, () => {
    win?.webContents.send("login:changed", authProviders());
  });
});
app.on("window-all-closed", async () => { await ptys.closeAll(); app.quit(); });
