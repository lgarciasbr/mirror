"use strict";
const { test } = require("node:test");
const assert = require("node:assert");
const { buildCommand, COMMANDS } = require("../main/command-registry.js");

test("unknown command id throws", () => {
  assert.throws(() => buildCommand("rm-rf", {}), /unknown command/i);
});

test("warmup opens the DB (identity list) so migrations actually run — not just inspect", () => {
  const c = buildCommand("warmup", {});
  assert.strictEqual(c.file, "uv");
  assert.deepStrictEqual(c.args, ["run", "python", "-m", "memory", "identity", "list"]);
});

test("initIdentity validates the user slug strictly", () => {
  const c = buildCommand("initIdentity", { user: "Rodrigo_01" });
  assert.deepStrictEqual(c.args.slice(-2), ["init", "Rodrigo_01"]);
  assert.throws(() => buildCommand("initIdentity", {}), /user/i);
  assert.throws(() => buildCommand("initIdentity", { user: "a b" }), /user/i);
  assert.throws(() => buildCommand("initIdentity", { user: "x;rm" }), /user/i);
});

test("seed is fixed argv (bootstrap-only, idempotent upstream)", () => {
  const c = buildCommand("seed", {});
  assert.deepStrictEqual(c.args, ["run", "python", "-m", "memory", "seed"]);
});

test("detectPersona embeds the query as ONE argv element — never shell", () => {
  const q = 'x" & del C:\\ /q & "';
  const c = buildCommand("detectPersona", { query: q });
  assert.strictEqual(c.args[c.args.length - 1], q);
  assert.strictEqual(c.shell, undefined);
});

test("detectPersona requires a non-empty query and caps its size", () => {
  assert.throws(() => buildCommand("detectPersona", {}), /query/i);
  assert.throws(() => buildCommand("detectPersona", { query: "a".repeat(2001) }), /query/i);
});

test("updateMirror accepts no extra arguments at all", () => {
  const c = buildCommand("updateMirror", { query: "ignored" });
  assert.deepStrictEqual(c.args, ["run", "python", "-m", "memory", "runtime", "update"]);
});

test("updatePi pins the official package name", () => {
  const c = buildCommand("updatePi", {});
  assert.ok(c.args.join(" ").includes("@earendil-works/pi-coding-agent@latest"));
});

test("every registered command declares cwd policy", () => {
  for (const id of Object.keys(COMMANDS)) {
    assert.ok(["root", "frame"].includes(COMMANDS[id].cwd), `${id} sem cwd policy`);
  }
});
