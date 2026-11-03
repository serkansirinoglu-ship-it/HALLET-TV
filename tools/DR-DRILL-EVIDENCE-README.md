# DR Drill Evidence CLI

This utility runs a disposable, synthetic disaster-recovery exercise. It creates a temporary SQLite fixture, an ephemeral Ed25519 keypair, a backup/manifest/signature, verifies the signature and backup hash, restores into a temporary file, and records JSON evidence.

## Requirements
- Python 3.10+
- OpenSSL 3.x command-line executable on PATH

## Run
```bash
python tools/dr-drill-evidence.py --evidence dr-drill-evidence.json
```

The utility prints a PASS/FAIL summary and writes evidence at the requested path. All fixture/key/restore artifacts are created under a unique temporary directory and removed in a finally block. Evidence is intentionally retained at the output path.

## Safety boundary
- Synthetic data only; never points to a configured application database.
- Generates a disposable private key; no production key inputs are accepted.
- Does not call hosting, deployment, cloud storage, or production services.
- Do not use real backups or production credentials in this drill.

## Evidence contents
Timestamp, command records (exit code/stdout/stderr), individual acceptance checks, and SHA-256 hashes for synthetic backup, manifest, signature, and restored DB.
