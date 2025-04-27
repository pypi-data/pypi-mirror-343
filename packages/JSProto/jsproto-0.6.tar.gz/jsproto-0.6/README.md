一种新的表达和语法，综合了Python的简洁和JavaScript的灵活，同时保留了Python的静态类型和JavaScript的动态类型。

可以使用
```bash
pip install jsproto
```
安装。
使用方法：
```python
from jsproto import *

(var(['apple', 'banana', 'pear'])
 .forEach(function(lambda s: 'long' if len(s) > 5 else 'short')
          .then(print)))

(var({
    "name": "John",
    "age": 30,
    "contact": {
        "email": "john@example.com",
        "phone": "1234567890"
    },
    "hobbies": var(["reading", "swimming", "traveling"])
    .map(lambda s:s.upper())(),
    "is_student": False
}).contact.email
 .then(print))

# 输出
# short
# long
# short
# john@example.com

```

