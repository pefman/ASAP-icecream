import subprocess, http.client, json, uuid, sys, os, py_compile, tempfile

def get_model(host, path):
    try:
        conn = http.client.HTTPSConnection(host)
        conn.request("GET", "/v1/models")
        models = json.loads(conn.getresponse().read()).get("data", [])
        if models:
            return max(models, key=lambda m: m.get("meta",{}).get("n_params",0))["id"]
        return "default-model"
    except Exception:
        return "default-model"

def call_ai(host, path, model, system_msg, user_msg):
    try:
        conn = http.client.HTTPSConnection(host)
        data = json.dumps({"model": model, "messages": [
            {"role": "system", "content": system_msg},
            {"role": "user",   "content": user_msg}
        ]})
        conn.request("POST", path, data, {"Content-Type": "application/json"})
        resp = conn.getresponse()
        raw = resp.read()
        parsed = json.loads(raw)
        if "choices" not in parsed:
            raise RuntimeError(f"Unexpected API response: {raw.decode()[:500]}")
        content = parsed["choices"][0]["message"]["content"]
        lines = content.strip().splitlines()
        if lines and lines[0].startswith("```"): lines = lines[1:]
        if lines and lines[-1].startswith("```"): lines = lines[:-1]
        return "\n".join(lines)
    except Exception as e:
        print(f"AI Call Error: {e}")
        return ""

def run(file):
    try:
        py_compile.compile(file, doraise=True)
        return 0
    except py_compile.PyCompileError as e:
        print(f"Syntax error: {e}"); return 1

def push(repo, token, script_path):
    _repo = repo
    if _repo.startswith("git@"):
        _repo = _repo.replace(":", "/", 1).replace("git@", "https://", 1)
    _repo_parts = _repo.split("://", 1)
    url = f"{_repo_parts[0]}://{token}@{_repo_parts[1]}"
    try:
        subprocess.run(["git","add",script_path], capture_output=True)
        subprocess.run(["git","commit","-m",f"evolve [iteration]"], capture_output=True)
        r = subprocess.run(["git","push",url,"HEAD:main"], capture_output=True)
        if r.returncode == 0: print(f"Pushed to {repo}")
        else: print(f"Push failed: {r.stderr.decode().strip()}")
    except Exception:
        pass

if __name__ == "__main__":
    if len(sys.argv)<5:
        print("Usage: python notskynet.py endpoint prompt repo token")
        sys.exit(1)

    _url = sys.argv[1]
    if "://" in _url:
        _url = _url.split("://", 1)[1]
    _parts = _url.split("/", 1)
    host = _parts[0]
    _raw_path = "/" + _parts[1] if len(_parts) > 1 else ""
    path = _raw_path if _raw_path and _raw_path != "/" else "/v1/chat/completions"
    SCRIPT = __file__
    ITER   = 5
    PROMPT = sys.argv[2]

    MODEL = get_model(host, path)
    REPO  = sys.argv[3]
    TOKEN = sys.argv[4]
    print(f"Endpoint  : {host}{path}")
    print(f"Model     : {MODEL}")
    print(f"Script    : {SCRIPT}")
    print(f"Prompt    : {PROMPT}")
    print(f"Repo      : {REPO}")
    print(f"Iterations: {ITER}\n")

    system_msg = (
        "Return only improved Python code, no explanation, no markdown fences. "
        "Wrap all executable logic (network calls, main loop, etc.) inside "
        "'if __name__ == \"__main__\"' so the file can be safely imported for syntax checks."
    )

    for i in range(ITER):
        print(f"[{i}] Reading {SCRIPT}...")
        with open(SCRIPT) as f: code = f.read()
        print(f"[{i}] Asking AI to evolve ({len(code)} chars)...")
        new_code = call_ai(host, path, MODEL, system_msg, f"{PROMPT}:\n\n{code}")
        print(f"[{i}] Got response ({len(new_code)} chars). Testing...")
        tmp = f"{SCRIPT}_{uuid.uuid4().hex[:4]}.py"
        with open(tmp,"w") as f: f.write(new_code)
        if run(tmp)==0:
            print(f"[{i}] Test passed. Applying changes...")
            with open(SCRIPT,"w") as f: f.write(new_code)
            push(REPO, TOKEN, SCRIPT)
            print(f"[{i}] Done!")
        else:
            print(f"[{i}] Test failed, skipping.")
        if os.path.exists(tmp):
            os.remove(tmp)