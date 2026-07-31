"use strict";
// Resolve MIRROR_ROOT (a raiz do checkout git do Mirror) na mesma filosofia do
// installer/launcher/mirror.cmd: caminhos explícitos primeiro, depois o layout
// do instalador, depois o modo dev (subir a árvore até achar pyproject.toml).
const path = require("node:path");
const fs = require("node:fs");

function resolveMirrorRoot(opts = {}) {
  const env = opts.env ?? process.env;
  const exists = opts.exists ?? fs.existsSync;
  const startDir = opts.startDir ?? __dirname;
  const localAppData = opts.localAppData ?? env.LOCALAPPDATA ?? "";

  const hasPyproject = (dir) => exists(path.join(dir, "pyproject.toml"));

  if (env.MIRROR_FRAME_ROOT && hasPyproject(env.MIRROR_FRAME_ROOT)) {
    return env.MIRROR_FRAME_ROOT;
  }

  if (localAppData) {
    const installed = path.join(localAppData, "Programs", "MirrorMind", "app");
    if (hasPyproject(installed)) return installed;
  }

  let dir = startDir;
  for (let i = 0; i < 12; i++) {
    if (hasPyproject(dir)) return dir;
    const parent = path.dirname(dir);
    if (parent === dir) break;
    dir = parent;
  }
  return null;
}

module.exports = { resolveMirrorRoot };
