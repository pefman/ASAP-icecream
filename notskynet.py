import subprocess, http.client, json, uuid, sys, os

if len(sys.argv)<5:
    print("Usage: python notskynet.py endpoint prompt repo token")
    sys.exit(1)

host, path = sys.argv[1].split("/",1)
path = "/" + path
SCRIPT = "main.py"
ITER   = 5
PROMPT = sys.argv[2]

def get_model():
    conn = http.client.HTTPSConnection(host)
    conn.request("GET", "/v1/models")
    models = json.loads(conn.getresponse().read()).get("data", [])
    return max(models, key=lambda m: m.get("meta",{}).get("n_params",0))["id"]

MODEL = get_model()
print(f"Using model: {MODEL}")
REPO  = sys.argv[3]
TOKEN = sys.argv[4]

def call_ai(code):
    conn = http.client.HTTPSConnection(host)
    data = json.dumps({"model": MODEL, "messages": [
        {"role": "system", "content": "Return only improved Python code, no explanation."},
        {"role": "user",   "content": f"{PROMPT}:\n\n{code}"}
    ]})
    conn.request("POST", path, data, {"Content-Type": "application/json"})
    resp = conn.getresponse()
    return json.loads(resp.read())["choices"][0]["message"]["content"]

def run(file):
    try:
        return subprocess.run(["python", file], capture_output=True, timeout=3).returncode
    except Exception as e:
        print(e); return 1

def push(i):
    url = f"https://{TOKEN}@{REPO}"
    subprocess.run(["git","add",SCRIPT], capture_output=True)
    subprocess.run(["git","commit","-m",f"evolve [{i}]"], capture_output=True)
    subprocess.run(["git","push",url,"HEAD:main"], capture_output=True)

for i in range(ITER):
    with open(SCRIPT) as f: code = f.read()
    new_code = call_ai(code)
    tmp = f"{SCRIPT}_{uuid.uuid4().hex[:4]}.py"
    with open(tmp,"w") as f: f.write(new_code)
    if run(tmp)==0:
        with open(SCRIPT,"w") as f: f.write(new_code)
        push(i)
        print(f"[{i}] Success!")
    else:
        print(f"[{i}] Failed, skipping.")
    os.remove(tmp)
