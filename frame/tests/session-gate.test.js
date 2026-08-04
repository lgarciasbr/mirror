"use strict";
const { test } = require("node:test");
const assert = require("node:assert");
const { SessionGate } = require("../main/session-gate.js");

test("sessions open freely — a Mirror failure must never block conversing", () => {
  const g = new SessionGate();
  assert.strictEqual(g.canOpenSession(), true);
});

test("update is blocked while any session is open (rule R2)", () => {
  const g = new SessionGate();
  g.sessionOpened("s1");
  assert.strictEqual(g.canUpdate(), false);
  g.sessionClosed("s1");
  assert.strictEqual(g.canUpdate(), true);
});

test("an update in progress blocks opening new sessions", () => {
  const g = new SessionGate();
  g.updateStarted();
  assert.strictEqual(g.canOpenSession(), false);
  assert.strictEqual(g.canUpdate(), false);
  g.updateFinished();
  assert.strictEqual(g.canOpenSession(), true);
});

test("update is re-blocked after a session is reopened", () => {
  const g = new SessionGate();
  g.sessionOpened("s1");
  g.sessionClosed("s1");
  assert.strictEqual(g.canUpdate(), true);
  g.sessionOpened("s2");
  assert.strictEqual(g.canUpdate(), false);
});

test("closing an unknown session is a no-op", () => {
  const g = new SessionGate();
  g.sessionClosed("ghost");
  assert.strictEqual(g.canUpdate(), true);
});
