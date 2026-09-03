import uuid, json, os

REG = {}
REG_FILE = os.path.join(os.path.dirname(__file__), "registry.json")

def g(key):
    if key not in REG:
        REG[key] = str(uuid.uuid4())
    return REG[key]

def save():
    with open(REG_FILE, "w") as f:
        json.dump(REG, f, indent=1)

def load():
    global REG
    if os.path.exists(REG_FILE):
        with open(REG_FILE) as f:
            REG = json.load(f)

def get(key):
    return g(key)

if __name__ == "__main__":
    load()
    g("config")
    save()
    print("registry ready", len(REG))
