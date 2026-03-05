import subprocess, http.client, json, uuid, sys, os

if len(sys.argv)<5:
    print("Usage: python notskynet.py endpoint prompt repo token")
    sys.exit(1)

_url = sys.argv[1]
if "://" in _url:
    _url = _url.split("://", 1)[1]
_parts = _url.split("/", 1)
host = _parts[0]
path = "/" + _parts[1] if len(_parts) > 1 else "/"
SCRIPT = __file__
ITER   = 5
PROMPT = sys.argv[2]

def get_model():
    conn = http.client.HTTPSConnection(host)
    conn.request("GET", "/v1/models")
    models = json.loads(conn.getresponse().read()).get("data", [])
    return max(models, key=lambda m: m.get("meta",{}).get("n_params",0))["id"]

MODEL = get_model()
REPO  = sys.argv[3]
TOKEN = sys.argv[4]
print(f"Endpoint  : {host}{path}")
print(f"Model     : {MODEL}")
print(f"Script    : {SCRIPT}")
print(f"Prompt    : {PROMPT}")
print(f"Repo      : {REPO}")
print(f"Iterations: {ITER}\n")

def call_ai(code):
    conn = http.client.HTTPSConnection(host)
    data = json.dumps({"model": MODEL, "messages": [
        {"role": "system", "content": "Return only improved Python code, no explanation."},
        {"role": "user",   "content": f"{PROMPT}:\n\n{code}"}
    ]})
    conn.request("POST", path, data, {"Content-Type": "application/json"})
    resp = conn.getresponse()
    content = json.loads(resp.read())["choices"][0]["message"]["content"]
    # strip markdown code fences if model wraps response
    lines = content.strip().splitlines()
    if lines[0].startswith("```"): lines = lines[1:]
    if lines and lines[-1].startswith("```"): lines = lines[:-1]
    return "\n".join(lines)

def run(file):
    try:
        return subprocess.run([sys.executable, file], capture_output=True, timeout=3).returncode
    except Exception as e:
        print(e); return 1

def push(i):
    url = f"https://{TOKEN}@{REPO}"
    subprocess.run(["git","add",SCRIPT], capture_output=True)
    subprocess.run(["git","commit","-m",f"evolve [{i}]"], capture_output=True)
    r = subprocess.run(["git","push",url,"HEAD:main"], capture_output=True)
    if r.returncode == 0: print(f"[{i}] Pushed to {REPO}")
    else: print(f"[{i}] Push failed: {r.stderr.decode().strip()}")

for i in range(ITER):
    print(f"[{i}] Reading {SCRIPT}...")
    with open(SCRIPT) as f: code = f.read()
    print(f"[{i}] Asking AI to evolve ({len(code)} chars)...")
    new_code = call_ai(code)
    print(f"[{i}] Got response ({len(new_code)} chars). Testing...")
    tmp = f"{SCRIPT}_{uuid.uuid4().hex[:4]}.py"
    with open(tmp,"w") as f: f.write(new_code)
    if run(tmp)==0:
        print(f"[{i}] Test passed. Applying changes...")
        with open(SCRIPT,"w") as f: f.write(new_code)
        push(i)
        print(f"[{i}] Done!")
    else:
        print(f"[{i}] Test failed, skipping.")
    os.remove(tmp)
