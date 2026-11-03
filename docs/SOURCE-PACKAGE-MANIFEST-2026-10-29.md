# Source Package Manifest — 2026-10-29

## Source archive
- Archive: `HALLET-TV-v6.12.1-source-tree-2026-10-29.zip`
- SHA-256: `83e66109f95213d860aa2076ed66db769a75b18f1432442581e12364fa7701ca`
- Archive integrity: ZIP test passed.
- Included files: 216
- Uncompressed file bytes: 1,539,316
- Exclusions: environment secrets other than `.env.example`, private keys, generated runtime/database files, nested ZIPs, and logs.

## Fresh test run
- `npm test`: 398 passed, 0 failed.
- `npm run check`: passed; 101 JavaScript files checked.
- Smoke tests: 13 checks passed. Test-only stream URL was not contacted.
- Warning: these checks ran in the local release folder, not on GitHub Actions.

## Important limitation
This manifest documents the source archive prepared in the working environment. It does not mean the archive's 216 files have been imported into the GitHub tree. The full-source import remains pending until a supported transfer path is available and the GitHub tree can be compared against this manifest.
