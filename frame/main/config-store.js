"use strict";
// Leitura/escrita do .env na raiz do Mirror.
// Regras Windows da ES-004: UTF-8 SEM BOM, LF, preservar comentários e chaves
// desconhecidas (o .env é compartilhado com o core Python e com o mirror-logger).
const fs = require("node:fs");
const path = require("node:path");

function envPath(root) { return path.join(root, ".env"); }

function stripBom(s) { return s.charCodeAt(0) === 0xfeff ? s.slice(1) : s; }

function loadEnvFile(root) {
  const file = envPath(root);
  if (!fs.existsSync(file)) return {};
  const text = stripBom(fs.readFileSync(file, "utf8"));
  const out = {};
  for (const line of text.split(/\r?\n/)) {
    const m = /^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)\s*$/.exec(line);
    if (m && !line.trimStart().startsWith("#")) out[m[1]] = m[2];
  }
  return out;
}

function saveEnvValues(root, values) {
  const file = envPath(root);
  let lines = [];
  if (fs.existsSync(file)) {
    lines = stripBom(fs.readFileSync(file, "utf8")).split(/\r?\n/);
  }
  const pending = new Map(Object.entries(values));
  const next = lines.map((line) => {
    const m = /^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=/.exec(line);
    if (m && pending.has(m[1]) && !line.trimStart().startsWith("#")) {
      const k = m[1];
      const v = pending.get(k);
      pending.delete(k);
      return `${k}=${v}`;
    }
    return line;
  });
  while (next.length && next[next.length - 1] === "") next.pop();
  for (const [k, v] of pending) next.push(`${k}=${v}`);
  fs.writeFileSync(file, next.join("\n") + "\n", { encoding: "utf8" });
}

function isFirstRun(root) {
  const env = loadEnvFile(root);
  return !env.MIRROR_USER && !env.MIRROR_HOME;
}

module.exports = { loadEnvFile, saveEnvValues, isFirstRun };
