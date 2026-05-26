[< Story](index.md)

# Plan — CV13.E5.S6 Operations Runner surface

## Implementation plan

1. Add an `operations` tab to the web navigation.
2. Add `renderOperations()` to fetch catalog and recent runs.
3. Render operation cards with title, description, category, risk, dry-run behavior, execution state, and parameters.
4. Add run buttons/forms only for `execution: runnable` operations.
5. Build request payloads from declared parameters, with safe defaults:
   - `runtime-health`: no parameters,
   - `database-backup`: `verify` checkbox default true,
   - `conversation-journey-repair`: `dryRun` checkbox default true and bounded `limit` number.
6. Submit to `POST /api/operations/run` and render result/error inline.
7. Refresh recent run history after each operation.
8. Add minimal CSS for operations cards, result blocks, and run history.
9. Add JS syntax validation and focused existing web tests.
10. Stop for Navigator manual browser validation before story close.

## Design boundaries

- The UI only renders server-declared operations; it does not invent operation ids.
- Non-runnable operations are visible as future/not available, but have no run button.
- The page must make dry-run obvious for conversation repair.
- The page should show audit evidence without becoming a log explorer.
- This is not streaming; operations may take a moment and return a completed response.

## Risks and mitigations

- Risk: users click mutating operations without understanding. Mitigation: show risk and dry-run metadata, default conversation repair to dry-run, and label backup/repair actions clearly.
- Risk: UI diverges from server contract. Mitigation: build forms from catalog ids and declared parameter names.
- Risk: history overwhelms the surface. Mitigation: show recent compact run cards only.

## Verification approach

- Automated checks: existing web tests, ruff, JS syntax check, diff check.
- Manual browser validation is required because this story introduces a visible surface.
