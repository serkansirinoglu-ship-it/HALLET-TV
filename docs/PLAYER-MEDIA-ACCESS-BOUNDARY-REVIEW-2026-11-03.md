# Player media access boundary review — 2026-11-03

## Scope
Static review of the isolated v6.52.31 source ZIP and its locally patched presenter download route. This is not a production penetration test or live deployment validation.

## Observed controls in `src/server.mjs`
- Player API rejects requests when `PLAYER_TOKEN` is missing/short (minimum 32 chars).
- Staged media/caption URLs use scoped, expiring one-use tickets; otherwise the player token is required.
- Staged presenter media checks current rights context, editorial approval, safe storage name, descriptor/path inode identity, file size, media integrity, rights SHA-256, and revalidates rights before sending bytes.
- Program content-rights media requires presenter mode, an approved plan, a run sheet tied to that plan/channel, the currently active segment, and a running run sheet.
- Playback evaluates commercial/worldwide rights and exact media hash before response; responses use no-store and nosniff headers.
- Run-sheet retrieval is player-token gated and channel scoped; telemetry is presenter-mode gated and revision-conflict checked.

## Validation evidence
- `node scripts/check.mjs`: PASS (423 JS files).
- `node scripts/smoke-test.mjs`: PASS (41 checks).
- Focused rights/presenter/production-pack tests: PASS (43/43).
- Test stream URL is not contacted; no live player/browser session was exercised.

## Follow-up / limitations
- Add HTTP integration tests for unauthorized token, expired/replayed staged tickets, revoked rights between queue and playback, mismatched segment, and range responses.
- Exercise actual browser playback and HLS separately before a release claim.
- Source ZIP is still not imported into this GitHub repository; these findings are evidence only. No production deployment or live broadcast was changed.
