# Jsonp to json

jsonp 格式转换 json 格式

### Install

```bash
pip install p2json

```

```python
import p2json

jsonp1 = """__JSONP_XXX_1({"data": {"dt": "a123456","ac": {"a": 11,"b": 20}}});"""
jsonp2 = """__JSONP_XXX_1({"data": {"dt": "a1(234)56","ac": {"a": 11,"b": 20}}});"""

print(p2json.tojson(jsonp1)) # right

print(p2json.tojson(jsonp2)) # right
```
