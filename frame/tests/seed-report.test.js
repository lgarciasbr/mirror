"use strict";
const { test } = require("node:test");
const assert = require("node:assert");
const { parseSeedReport } = require("../main/seed-report.js");

const REAL_OUTPUT = `Seeding identity into [production]...
Mirror home: C:\\Users\\x\\.mirror-minds\\Rodrigo
  → self/soul (skipped — use 'memory identity edit self soul')
Result: 19 created, 0 updated, 0 skipped
Errors: 1
  - ego/constraints: empty content
`;

test("valid partial creation with the known warning parses as a report, not a hard failure", () => {
  const r = parseSeedReport(REAL_OUTPUT);
  assert.deepStrictEqual(
    { created: r.created, updated: r.updated, skipped: r.skipped, errors: r.errors },
    { created: 19, updated: 0, skipped: 0, errors: 1 },
  );
  assert.strictEqual(r.firstError, "ego/constraints: empty content");
});

test("clean run parses with zero errors", () => {
  const r = parseSeedReport("Result: 20 created, 0 updated, 0 skipped\n");
  assert.strictEqual(r.errors, 0);
  assert.strictEqual(r.firstError, null);
});

test("a crash with no Result summary yields null — that IS a hard failure", () => {
  assert.strictEqual(parseSeedReport("Traceback (most recent call last): ..."), null);
  assert.strictEqual(parseSeedReport(""), null);
  assert.strictEqual(parseSeedReport(null), null);
});
