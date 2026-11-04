# 云帆考试系统 · 接口自动化测试

基于 pytest + requests 的接口测试脚本，覆盖云帆考试系统部门管理、题库管理共 5 个接口。

## 技术栈

Python 3.14 / requests / pytest / openpyxl / pytest-html

## 目录结构

```
cases.xlsx        测试数据（新增用例只需加一行，无需改代码）
conftest.py       公共方法（登录、树遍历、按名称查找）
test_tree.py      部门树查询接口
test_save.py      部门新建 / 修改接口
test_sort.py      部门排序接口
report.html       测试报告
requirements.txt  依赖清单
```

## 运行

```bash
python -m pip install -r requirements.txt
python -m pytest -v
python -m pytest --html=report.html --self-contained-html
```

## 覆盖范围

| 接口 | 覆盖内容 |
|---|---|
| tree | 状态码、业务码、返回结构、数据非空 |
| save | 正常新增、名称为空、父级不存在，含落库校验 |
| sort | 正常交换、form 不存在、跨父级交换 |

## 设计说明

1. **数据与代码分离**：用例数据存放在 Excel，通过 `@pytest.mark.parametrize` 驱动，增删用例无需修改代码
2. **三层断言**：协议层（状态码）→ 业务层（code）→ 持久层（查询落库后校验）
3. **写操作验证方式**：save 之后追加一次 tree 查询确认数据落库，不依赖接口返回码判断成功

## 已知问题

当前 11 条用例中 4 条失败，均为被测系统的已确认缺陷，**不是脚本错误**：

- 部门名称为空时仍可创建（缺少非空校验）
- 父级 id 不存在时返回非标准错误格式（错误响应未统一）
- 排序接口未校验跨父级交换，导致同级 sort 重复

完整用例与缺陷分析见同目录上级的测试报告。