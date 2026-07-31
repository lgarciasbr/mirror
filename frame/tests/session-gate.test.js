"use strict";
const { test } = require("node:test");
const assert = require("node:assert");
const { SessionGate } = require("../main/session-gate.js");

test("sessions are blocked before warm-up", () => {
  const g = new SessionGate();
  assert.strictEqual(g.canOpenSession(), false);
  g.warmupDone();
  assert.strictEqual(g.canOpenSession(), true);
});

test("update is blocked while any session is open (rule R2)", () => {
  const g = new SessionGate();
  g.warmupDone();
  g.sessionOpened("s1");
  assert.strictEqual(g.canUpdate(), false);
  g.sessionClosed("s1");
  assert.strictEqual(g.canUpdate(), true);
});

test("update is blocked before warm-up", () => {
  const g = new SessionGate();
  assert.strictEqual(g.canUpdate(), false);
});

test("no sessions can open during an update; warm-up is required again after it", () => {
  const g = new SessionGate();
  g.warmupDone();
  g.updateStarted();
  assert.strictEqual(g.canOpenSession(), false);
  g.updateFinished();
  assert.strictEqual(g.canOpenSession(), false, "warm-up must run again after update");
  g.warmupDone();
  assert.strictEqual(g.canOpenSession(), true);
});

test("closing an unknown session is a no-op", () => {
  const g = new SessionGate();
  g.warmupDone();
  g.sessionClosed("ghost");
  assert.strictEqual(g.canUpdate(), true);
});
