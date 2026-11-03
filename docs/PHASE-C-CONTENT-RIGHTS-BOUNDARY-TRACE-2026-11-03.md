# Phase C — content-rights boundary trace (v6.52.31 source)
Date: 2026-11-03
Source archive SHA-256: `f9868afacc32a4d2a1a893e8bcc0c5ec3ccc9e2dd83864baefbfdfb70bf4246c`

## Traced controls (static review + existing tests)
- **Catalogue intake** — `POST /api/content-rights` is admin-only and accepts only structurally valid `candidate` records. Rights approval is a separate revision-checked decision.
- **Media intake** — `POST /api/content-rights/:id/asset` is admin-only, candidate/pending-review video only, checks revision and filename/size/MIME/signature/media inspection, stores exact bytes in SQLite quarantine and binds SHA-256.
- **Approval** — approved transition rechecks attached BLOB, size, storage ID and SHA-256. Record validation requires reviewer/date/evidence/hash and cleared components; CC URL↔license ID and ShareAlike rules are enforced.
- **Plan linkage** — `POST /api/content-plans/:id/rights-assets` links only approved rights assets with verified stored bytes; draft-only plan state.
- **Production pack** — GET export requires an approved plan, rejects client-supplied `assets`, resolves rights IDs server-side, validates approval/storage binding/byte count/hash, and calls `createProductionPack` which re-evaluates territory/commercial/derivative rights and attribution. Export is a draft artifact, not a broadcast.
- **Presenter playout** — staged queue and media delivery require presenter approval plus approved linked rights record, matching exact SHA-256/size/MIME, commercial-use evaluation, and revalidation immediately before streaming.
- **Program-run-sheet player media** — requires approved plan, current segment match, running run sheet, approved rights/media asset, and fresh rights/hash validation; playback is authenticated and no-store.
- **Takedown/expiry** — usage evaluation blocks takedown and expired records; streaming and pack paths re-evaluate at use time.

## Test evidence
- `test/content-rights-registry.test.mjs`
- `test/content-rights-persistence.test.mjs`
- `test/production-pack.test.mjs`
- `test/presenter-rights-link-ui.test.mjs`
- `npm run check`: 423 JavaScript files passed
- `npm run smoke`: 41/41 passed
- All 211 `test/*.test.mjs` files executed in bounded batches; all batch processes exited 0.

## Remaining review (not a closure claim)
- This is a code-path trace, not an independent legal/security audit.
- Next inspect every external media/publication surface and ensure no alternate path bypasses the same rights decision (including all admin download, presenter asset, content plan and broadcast endpoints).
- Add negative integration tests for status change/takedown/expiry between queueing and playback, and for every final media delivery boundary.
- Real production config, live HLS, browser E2E and release readiness remain unverified.
