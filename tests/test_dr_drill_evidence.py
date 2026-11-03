"""Contract tests for the isolated DR drill CLI (run by GitHub Actions)."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "dr-drill-evidence.py"

class DrillEvidenceContract(unittest.TestCase):
    def test_full_drill_emits_pass_evidence_and_expected_negative_gates(self):
        with tempfile.TemporaryDirectory(prefix="hallet-dr-test-") as td:
            evidence = Path(td) / "evidence.json"
            proc = subprocess.run(
                [sys.executable, str(SCRIPT), "--evidence", str(evidence)],
                text=True, capture_output=True, timeout=60,
            )
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            payload = json.loads(evidence.read_text(encoding="utf-8"))
            self.assertEqual(payload["schema"], "hallet.dr-drill-evidence.v1")
            self.assertEqual(payload["scope"], "synthetic-temporary-only")
            self.assertEqual(payload["result"], "PASS")
            names = {item["name"] for item in payload["checks"]}
            self.assertTrue({
                "keygen", "public-key", "sign", "signature-valid",
                "backup-hash", "isolated-restore", "reject-missing-manifest",
                "reject-invalid-signature", "reject-tampered-backup",
                "restore-failure-observed",
            }.issubset(names))
            self.assertTrue(all(item["passed"] for item in payload["checks"]))
            self.assertEqual(set(payload["artifact_sha256"]), {
                "backup", "manifest", "signature", "restored"
            })

    def test_evidence_output_is_not_written_inside_temporary_fixture(self):
        with tempfile.TemporaryDirectory(prefix="hallet-dr-test-") as td:
            evidence = Path(td) / "evidence.json"
            proc = subprocess.run(
                [sys.executable, str(SCRIPT), "--evidence", str(evidence)],
                text=True, capture_output=True, timeout=60,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            # Temporary fixture roots are cleaned; only the caller-requested evidence remains.
            self.assertEqual(sorted(p.name for p in Path(td).iterdir()), ["evidence.json"])

if __name__ == "__main__":
    unittest.main(verbosity=2)
