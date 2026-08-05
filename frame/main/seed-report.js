"use strict";
// Classifica o resultado do `memory seed` a partir do relatório impresso.
// Motivação (homologação, cenário 1): o seed sai com exit code 1 quando há
// QUALQUER aviso — inclusive o conhecido 'ego/constraints: empty content' do
// template vazio no main — mesmo tendo criado todas as entradas. Criação
// parcial VÁLIDA (há linha "Result: N created...") não pode virar falha dura
// do onboarding; avisos são exibidos, nunca silenciados (blocker 4, item 7).
function parseSeedReport(stdout) {
  const text = String(stdout ?? "");
  const m = /Result:\s*(\d+)\s*created,\s*(\d+)\s*updated,\s*(\d+)\s*skipped/.exec(text);
  if (!m) return null;
  const e = /Errors:\s*(\d+)/.exec(text);
  const firstError = (/Errors:\s*\d+\s*\n\s*-\s*(.+)/.exec(text) ?? [])[1]?.trim() ?? null;
  return {
    created: Number(m[1]),
    updated: Number(m[2]),
    skipped: Number(m[3]),
    errors: e ? Number(e[1]) : 0,
    firstError,
  };
}

module.exports = { parseSeedReport };
