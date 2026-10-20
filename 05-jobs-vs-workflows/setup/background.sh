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
  if ! find / -xdev -maxdepth 6 -ipath '*vscode-yaml*' -print -quit 2>/dev/null | grep -q .; then
    url=$(curl -fsSL https://open-vsx.org/api/redhat/vscode-yaml/latest \
          | python3 -c 'import sys,json; print(json.load(sys.stdin)["files"]["download"])')
    [ -n "$url" ] && curl -fsSL -o /root/.theia/plugins/redhat.vscode-yaml.vsix "$url"
  fi
  echo "--- theia processes"; ps -eo args | grep -i theia | grep -v grep | cut -c1-250
  echo "--- /root/.theia"; ls -la /root/.theia /root/.theia/plugins /root/.theia/extensions
) > /tmp/hydra-ext.log 2>&1 &
mkdir -p /root/lab
cd /root/lab
apt-get install -y -qq python3-venv >/dev/null 2>&1 || true
python3 -m venv /opt/hydra
/opt/hydra/bin/pip install --quiet "hydra-etl>=0.11.4"
ln -sf /opt/hydra/bin/hdrctl /usr/local/bin/hdrctl
touch /tmp/setup-done
