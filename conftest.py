import requests

BASE = "http://127.0.0.1:8080"

def get_token():
    r = requests.post(f"{BASE}/api/sys/user/login",
                      json={"userName": "admin", "password": "admin"})
    return r.json()["data"]["token"]

def walk(nodes, out):
    for n in nodes:
        out.append(n)
        walk(n.get("children", []), out)