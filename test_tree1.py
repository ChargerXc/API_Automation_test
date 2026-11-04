import requests
import conftest
BASE = "http://127.0.0.1:8080"


def test_tree_status():
    token = conftest.get_token()
    r = requests.post(f"{BASE}/api/sys/depart/tree", headers={"token": token})
    assert r.status_code == 200

def test_tree_code():
    token = conftest.get_token()
    r = requests.post(f"{BASE}/api/sys/depart/tree", headers={"token": token})
    assert r.json()["code"] == 0

def test_tree_data_is_list():
    token = conftest.get_token()
    r = requests.post(f"{BASE}/api/sys/depart/tree", headers={"token": token})
    assert isinstance(r.json()['data'], list)