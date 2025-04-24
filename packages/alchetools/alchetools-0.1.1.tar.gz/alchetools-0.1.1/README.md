# alchetools

🚀 一个基于 SQLAlchemy 的轻量级 CRUD 工具库，封装了常用的增删改查、分页、过滤、批量操作等功能，帮助你更快速地构建数据库访问层。

---

## ✨ 功能特性

- ✅ 通用 `saveOrUpdate`（新增或更新记录）
- ✅ 支持批量插入/更新
- ✅ 分页查询与总数统计
- ✅ 自动格式化时间字段为字符串
- ✅ 支持动态条件过滤（精确 / 模糊）
- ✅ 支持动态排序（asc / desc）

---

## 📦 安装依赖

```bash
pip install sqlalchemy
```

---

## 📁 使用说明

### 1. 新增或更新一条记录

```python
from alchetools import DbTools

model_instance = DbTools.saveOrUpdate(
    session=session,
    request_body={"id": 1, "name": "Tom"},
    model=UserModel  # 替换为你的 SQLAlchemy 模型类
)
```

---

### 2. 批量插入或更新记录

```python
from alchetools import DbTools

data = [{"id": 1, "name": "Tom"}, {"id": 2, "name": "Jerry"}]

instances = DbTools.bulk_insert(session, data, UserModel)
```

---

### 3. 分页查询数据

```python
from alchetools import DbTools

query = session.query(UserModel)
result = DbTools.find_list_page(query, page_size=10, page_index=1)
```

---

### 4. 查询全部数据（带时间格式化）

```python
from alchetools import DbTools

records = DbTools.queryAll(session.query(UserModel))
```

---

### 5. 应用条件过滤

```python
from alchetools import DbTools

filters = {
    "name": {"value": "Tom", "is_fuzzy": True},
    "age": {"value": 18}
}

filtered_query = DbTools.apply_filters(session.query(UserModel), UserModel, json.dumps(filters))
```

---

### 6. 获取排序后的查询对象

```python
sorted_query = get_sorted_query(session, UserModel, sort_by="created_at", order="desc")
```

---

## 🛠 公共方法列表

| 方法名                          | 说明                  |
|------------------------------|---------------------|
| `saveOrUpdate`               | 新增或根据主键更新记录         |
| `bulk_insert`                | 批量新增或更新记录           |
| `queryAll`                   | 查询所有记录并格式化时间        |
| `find_list_page`             | 分页查询                |
| `pagination_function`        | 分页查询（另一个别名）         |
| `apply_filters`              | 动态构建 SQL 查询条件       |
| `get_sorted_query`           | 获取按字段排序的查询对象        |
| `format_model_data`          | 将 SQLAlchemy 模型转为字典 |
| `convert_timestamps_in_dict` | 格式化时间戳/时间字段为字符串     |

---

## 🧪 日志支持

该库依赖外部的 `setup_logger()` 方法记录数据库提交失败日志，请在你的项目中提前定义：

```python
# 示例：utils/logger.py
import logging


def setup_logger():
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger(__name__)
```

---

## 🔐 兼容性说明

- ✅ 支持 SQLAlchemy 2.0.29
- ✅ Python 3.8 及以上版本

---

## 📄 License

MIT License. 自由用于个人或商业项目。

---

## 🤝 欢迎贡献

欢迎提交 issue 或 PR，一起让 `alchetools` 更好用！