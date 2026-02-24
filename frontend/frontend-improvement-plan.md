# Frontend Improvement Plan

## Goals
- Improve accessibility of custom form controls.
- Fix semantic layout issues for screen readers.
- Make search UX consistent with URL state.
- Keep quality gates green (`lint`, unit tests, e2e).

## Execution Steps
1. Accessibility for custom selectors (`DropdownSelectField`, `TagDropdownSelector`)
- Add keyboard navigation (`ArrowUp`, `ArrowDown`, `Home`, `End`, `Enter`, `Space`, `Escape`).
- Ensure focused option management and proper `listbox` semantics.
- Preserve current click/touch behavior.

2. Semantic layout cleanup
- Keep a single page-level `<main>` in `App.vue`.
- Replace nested `<main>` in route views with `<section>`/`<div>`.

3. Search UX consistency
- Sync search input with route query (`?q=`).
- Handle clear action from search bar in header.
- Clear pending debounce timers on unmount.

4. Validation
- Run `bun run --cwd frontend lint`.
- Run `bun run --cwd frontend test`.
- Run `bun run --cwd frontend test:e2e -- e2e/smoke.spec.js`.

## Definition of Done
- Keyboard-only users can fully operate custom selectors.
- No nested `<main>` landmarks remain.
- Search field reflects URL query and clear action is deterministic.
- All listed checks pass.
