#!/usr/bin/env python3
"""Isolated, synthetic disaster-recovery drill. Never accepts production paths."""
from __future__ import annotations
import argparse, hashlib, json, shutil, sqlite3, subprocess, tempfile
from datetime import datetime, timezone
from pathlib import Path

def sha256(p: Path) -> str:
    h=hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024), b""): h.update(chunk)
    return h.hexdigest()

def run(cmd, cwd, evidence, label):
    p=subprocess.run(cmd,cwd=cwd,text=True,capture_output=True,timeout=20)
    evidence.append({"case":label,"command":cmd,"exit_code":p.returncode,"stdout":p.stdout[-4000:],"stderr":p.stderr[-4000:]})
    return p

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--evidence",default="dr-drill-evidence.json")
    args=ap.parse_args()
    evidence={"schema":"hallet.dr-drill-evidence.v1","started_at":datetime.now(timezone.utc).isoformat(),"scope":"synthetic-temporary-only","checks":[],"commands":[]}
    root=Path(tempfile.mkdtemp(prefix="hallet-dr-drill-")).resolve()
    try:
        # All artifacts are confined to this disposable directory.
        work=root/"fixture"; work.mkdir()
        db=work/"synthetic.sqlite"; con=sqlite3.connect(db)
        con.execute("CREATE TABLE drill_fixture(id INTEGER PRIMARY KEY, value TEXT NOT NULL)")
        con.execute("INSERT INTO drill_fixture(value) VALUES ('synthetic-only')")
        con.commit(); con.close()
        backup=work/"backup.sqlite"; shutil.copy2(db,backup)
        manifest=work/"manifest.json"
        manifest.write_text(json.dumps({"created_at":datetime.now(timezone.utc).isoformat(),"backup":"backup.sqlite","sha256":sha256(backup)},sort_keys=True)+"\n")
        priv=root/"disposable-ed25519.pem"; pub=root/"disposable-ed25519.pub"; sig=root/"manifest.sig"
        checks=[]
        def check(name,ok,detail): checks.append({"name":name,"passed":bool(ok),"detail":detail})
        p=run(["openssl","genpkey","-algorithm","ED25519","-out",str(priv)],root,evidence["commands"],"generate-disposable-key")
        check("keygen",p.returncode==0,p.stderr.strip())
        p=run(["openssl","pkey","-in",str(priv),"-pubout","-out",str(pub)],root,evidence["commands"],"derive-public-key")
        check("public-key",p.returncode==0,p.stderr.strip())
        p=run(["openssl","pkeyutl","-sign","-inkey",str(priv),"-rawin","-in",str(manifest),"-out",str(sig)],root,evidence["commands"],"sign-manifest")
        check("sign",p.returncode==0,p.stderr.strip())
        p=run(["openssl","pkeyutl","-verify","-pubin","-inkey",str(pub),"-rawin","-in",str(manifest),"-sigfile",str(sig)],root,evidence["commands"],"verify-signature")
        check("signature-valid",p.returncode==0,p.stdout.strip()+p.stderr.strip())
        m=json.loads(manifest.read_text()); check("backup-hash",m["sha256"]==sha256(backup),"manifest hash matches backup")
        restored=root/"restored.sqlite"; shutil.copy2(backup,restored)
        con=sqlite3.connect(restored); row=con.execute("SELECT value FROM drill_fixture WHERE id=1").fetchone(); con.close()
        check("isolated-restore",row==("synthetic-only",),"restored synthetic row matches")
        # Negative gates must reject their specific faults.
        missing=root/"missing.json"
        p=run(["openssl","pkeyutl","-verify","-pubin","-inkey",str(pub),"-rawin","-in",str(missing),"-sigfile",str(sig)],root,evidence["commands"],"negative-missing-manifest")
        check("reject-missing-manifest",p.returncode!=0,"verification rejects absent manifest")
        altered=root/"altered.json"; altered.write_text(manifest.read_text()+"tamper")
        p=run(["openssl","pkeyutl","-verify","-pubin","-inkey",str(pub),"-rawin","-in",str(altered),"-sigfile",str(sig)],root,evidence["commands"],"negative-invalid-signature")
        check("reject-invalid-signature",p.returncode!=0,"signature rejects altered manifest")
        damaged=work/"tampered.sqlite"; shutil.copy2(backup,damaged); damaged.write_bytes(damaged.read_bytes()+b"tamper")
        check("reject-tampered-backup",sha256(damaged)!=m["sha256"],"tampered backup hash differs")
        # Force a restore failure through Python's bundled SQLite API (no sqlite3 CLI dependency).
        forced_failure=False
        try:
            sqlite3.connect(root/"missing-parent"/"restore.sqlite")
        except sqlite3.OperationalError as exc:
            forced_failure=True
            evidence["commands"].append({"case":"negative-forced-restore-failure","command":"sqlite3.connect(nonexistent-parent)","exit_code":1,"stdout":"","stderr":str(exc)})
        check("restore-failure-observed",forced_failure,"restore target failure is surfaced")
        evidence["checks"]=checks
        evidence["finished_at"]=datetime.now(timezone.utc).isoformat()
        evidence["result"]="PASS" if all(c["passed"] for c in checks) else "FAIL"
        evidence["artifact_sha256"]={"backup":sha256(backup),"manifest":sha256(manifest),"signature":sha256(sig),"restored":sha256(restored)}
        out=Path(args.evidence).resolve(); out.write_text(json.dumps(evidence,indent=2)+"\n")
        print(json.dumps({"result":evidence["result"],"checks":len(checks),"passed":sum(c["passed"] for c in checks),"evidence":str(out)},indent=2))
        return 0 if evidence["result"]=="PASS" else 1
    finally:
        shutil.rmtree(root,ignore_errors=True)

if __name__=="__main__": raise SystemExit(main())
