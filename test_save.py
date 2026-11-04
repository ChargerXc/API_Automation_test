import pytest
import requests
import openpyxl
import json
import conftest

BASE = "http://127.0.0.1:8080"

def load_cases(path):
    wb = openpyxl.load_workbook(path)
    ws = wb.active
    cases = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        case_id, case_name, payload_json, expect_code, expect_exists= row
        cases.append((case_id, case_name, json.loads(payload_json), int(expect_code), bool(int(expect_exists))))
    return cases

CASES = load_cases("cases.xlsx")

def find_dept(name):
    token = conftest.get_token()
    r = requests.post(f"{BASE}/api/sys/depart/tree", headers={"token": token})
    flat = []
    conftest.walk(r.json()["data"], flat)
    return [n for n in flat if n["deptName"] == name]

@pytest.mark.parametrize(
    "payload, expect_code, expect_exists",
    [(c[2], c[3], c[4]) for c in CASES],
    ids=[f"{c[0]}" for c in CASES]
)

def test_save_dept(payload, expect_code, expect_exists):
    token = conftest.get_token()
    r = requests.post(f"{BASE}/api/sys/depart/save",
                      headers={"token": token}, json=payload)
    body = r.json()
    assert "code" in body, f"响应缺少 code：{r.status_code} {body}"
    assert body["code"] == expect_code

    name = payload.get("deptName")
    if name:
        found = find_dept(name)
        assert (len(found) > 0) == expect_exists