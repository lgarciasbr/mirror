"use strict";
// Regras de orquestração do frame (da análise de riscos da ES-004):
// - warm-up serializado ANTES de qualquer sessão (mitiga a lacuna fcntl no Windows);
// - update NUNCA roda com sessões abertas (R2: arquivos em uso + uv sync);
// - após um update, o warm-up é exigido de novo (migrations podem ter rodado).
class SessionGate {
  constructor() {
    this._warm = false;
    this._updating = false;
    this._sessions = new Set();
  }
  warmupDone() { this._warm = true; }
  sessionOpened(id) { if (this.canOpenSession()) this._sessions.add(id); }
  sessionClosed(id) { this._sessions.delete(id); }
  updateStarted() { this._updating = true; }
  updateFinished() { this._updating = false; this._warm = false; }
  canOpenSession() { return this._warm && !this._updating; }
  canUpdate() { return this._warm && !this._updating && this._sessions.size === 0; }
  get openSessions() { return this._sessions.size; }
  get isWarm() { return this._warm; }
  get isUpdating() { return this._updating; }
}

module.exports = { SessionGate };
