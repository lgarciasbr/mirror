"use strict";
const { test } = require("node:test");
const assert = require("node:assert");
const path = require("node:path");
const { resolveMirrorRoot } = require("../main/root-resolve.js");

test("env MIRROR_FRAME_ROOT wins when it contains pyproject.toml", () => {
  const root = resolveMirrorRoot({
    env: { MIRROR_FRAME_ROOT: "C:\\custom\\mirror" },
    exists: (p) => p === path.join("C:\\custom\\mirror", "pyproject.toml"),
    startDir: "C:\\anywhere",
    localAppData: "C:\\Users\\x\\AppData\\Local",
  });
  assert.strictEqual(root, "C:\\custom\\mirror");
});

test("installer layout is used when present", () => {
  const app = path.join("C:\\Users\\x\\AppData\\Local", "Programs", "MirrorMind", "app");
  const root = resolveMirrorRoot({
    env: {},
    exists: (p) => p === path.join(app, "pyproject.toml"),
    startDir: "C:\\anywhere",
    localAppData: "C:\\Users\\x\\AppData\\Local",
  });
  assert.strictEqual(root, app);
});

test("dev mode walks up from startDir to find pyproject.toml", () => {
  const repo = "C:\\VSCode\\mirror-exe";
  const root = resolveMirrorRoot({
    env: {},
    exists: (p) => p === path.join(repo, "pyproject.toml"),
    startDir: path.join(repo, "frame", "main"),
    localAppData: "C:\\nope",
  });
  assert.strictEqual(root, repo);
});

test("returns null when nothing is found", () => {
  const root = resolveMirrorRoot({
    env: {}, exists: () => false, startDir: "C:\\a\\b", localAppData: "C:\\nope",
  });
  assert.strictEqual(root, null);
});

test("env root without pyproject.toml is rejected (falls through)", () => {
  const root = resolveMirrorRoot({
    env: { MIRROR_FRAME_ROOT: "C:\\bogus" },
    exists: () => false, startDir: "C:\\a", localAppData: "C:\\nope",
  });
  assert.strictEqual(root, null);
});
