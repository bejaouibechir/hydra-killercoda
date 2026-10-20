#!/bin/bash
set -e
# --- HYDRA ETL extension for the Editor tab (Theia). Runs on its own, never blocks or fails the setup.
(
  set +e
  VSIX=/root/.hydra-vscode/hydra-etl-0.1.4.vsix
  for _ in $(seq 1 60); do [ -f "$VSIX" ] && break; sleep 1; done
  mkdir -p /root/.theia/plugins /root/.theia/extensions
  cp "$VSIX" /root/.theia/plugins/
  python3 - "$VSIX" /root/.theia/extensions/hydraetl.hydra-etl-0.1.4 <<'PY'
import sys, zipfile, pathlib
src, dst = sys.argv[1], pathlib.Path(sys.argv[2])
with zipfile.ZipFile(src) as z:
    for m in z.namelist():
        if m.startswith("extension/") and not m.endswith("/"):
            out = dst / m[len("extension/"):]
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(z.read(m))
PY
  # The extension relies on Red Hat YAML. Fetch it from Open VSX if the editor does not already have it.
  YAML_FOUND=$(find / -xdev -maxdepth 6 -ipath '*vscode-yaml*' -print -quit 2>/dev/null)
  echo "--- red hat yaml: ${YAML_FOUND:-not found, downloading}"
  if [ -z "$YAML_FOUND" ]; then
    url=$(curl -fsSL https://open-vsx.org/api/redhat/vscode-yaml/latest \
          | python3 -c 'import sys,json; print(json.load(sys.stdin)["files"]["download"])' 2>/dev/null)
    [ -n "$url" ] && curl -fsSL -o /root/.theia/plugins/redhat.vscode-yaml.vsix "$url"
  fi
  # Theia only scans its plugin folders at startup, and it starts before this script.
  # Restart its backend once, with the same command line, environment and working directory.
  python3 - <<'PY'
import os, time, signal, subprocess, pathlib

def theia_backends():
    found = []
    for d in pathlib.Path("/proc").iterdir():
        if not d.name.isdigit():
            continue
        try:
            args = (d / "cmdline").read_bytes().split(b"\0")
        except OSError:
            continue
        if len(args) > 1 and args[1].endswith(b"src-gen/backend/main.js"):
            found.append(int(d.name))
    return found

pids = theia_backends()
print("theia backend pids:", pids)
if pids:
    pid = pids[0]
    cmd = open(f"/proc/{pid}/cmdline", "rb").read().split(b"\0")[:-1]
    env = dict(e.split(b"=", 1) for e in open(f"/proc/{pid}/environ", "rb").read().split(b"\0") if b"=" in e)
    cwd = os.readlink(f"/proc/{pid}/cwd")
    ppid = open(f"/proc/{pid}/stat").read().rsplit(")", 1)[1].split()[1]
    print("parent:", open(f"/proc/{ppid}/cmdline", "rb").read().replace(b"\0", b" ")[:200].decode(errors="replace"))
    print("restarting:", b" ".join(cmd).decode(errors="replace")[:250])
    os.kill(pid, signal.SIGTERM)
    for _ in range(20):
        time.sleep(0.5)
        if not os.path.exists(f"/proc/{pid}"):
            break
    time.sleep(3)
    again = [p for p in theia_backends() if p not in pids]
    if again:
        print("restarted by its supervisor, pid", again)
    else:
        log = open("/tmp/theia-restart.log", "ab")
        p = subprocess.Popen(cmd, env=env, cwd=cwd, stdin=subprocess.DEVNULL,
                             stdout=log, stderr=log, start_new_session=True)
        print("relaunched by this script, pid", p.pid)
PY
  echo "--- /root/.theia"; ls -la /root/.theia/plugins /root/.theia/extensions
) > /tmp/hydra-ext.log 2>&1 &
# --- end of HYDRA ETL extension block
mkdir -p /root/lab
cd /root/lab
apt-get install -y -qq python3-venv >/dev/null 2>&1 || true
python3 -m venv /opt/hydra
/opt/hydra/bin/pip install --quiet "hydra-etl>=0.11.4"
ln -sf /opt/hydra/bin/hdrctl /usr/local/bin/hdrctl
touch /tmp/setup-done
