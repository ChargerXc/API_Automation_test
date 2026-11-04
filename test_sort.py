import requests
import pytest
import conftest

BASE = 'http://127.0.0.1:8080'

def find_dept(node_list, target_id):
    for node in node_list:
        if node["id"] == target_id:
            return node
    pytest.fail(f" * 在部门树中未找到id={target_id} 的节点")


@pytest.mark.parametrize('payload,expect_code', [
    ({"form":"1447829893265002498","to":"1447829960050905090"},0),
    ({"form": "1447829893265002498", "to": "1447829960050905090"}, 1),
    ({"form": "1447829893265002498", "to": "1447829960050905091"}, 0),
    ({"form": "1447829893265002498", "to": "1447829960050905090"}, 0)
])

def test_sort_dept(payload,expect_code):
    token = conftest.get_token()
    form = payload.get('form')
    to = payload.get('to')

    r1 = requests.post(url=f"{BASE}/api/sys/depart/tree",headers={"token":token})
    flat1 = []
    conftest.walk(r1.json()['data'], flat1)
    form_node_before = find_dept(flat1, form)
    to_node_before = find_dept(flat1, to)
    form_before_sort = form_node_before["sort"]
    to_before_sort = to_node_before["sort"]

    r2 = requests.post(url=f"{BASE}/api/sys/depart/sort",json=payload,headers={"token":token})
    assert r2.json()["code"] == expect_code, f"排序接口返回码异常，实际：{r2.json()['code']}"

    r3 = requests.post(url=f"{BASE}/api/sys/depart/tree",headers={"token":token})
    flat2 = []
    conftest.walk(r3.json()['data'], flat2)
    form_node_after = find_dept(flat2, form)
    to_node_after = find_dept(flat2, to)

    assert form_node_after["sort"] == to_before_sort,f"源部门{form} sort校验失败，预期：{to_before_sort}，实际：{form_node_after['sort']}"
    assert to_node_after["sort"] == form_before_sort,f"目标部门{to} sort校验失败，预期：{form_before_sort}，实际：{to_node_after['sort']}"