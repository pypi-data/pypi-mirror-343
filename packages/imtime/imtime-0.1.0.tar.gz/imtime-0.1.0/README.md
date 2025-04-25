# imtime

一个简单的时间格式化工具，提供 `get_now()` 函数，支持多种时间格式输出。

## 安装
```bash
pip install imtime

# 使用示例
from imtime import get_now

print(get_now('date'))      # 2025-04-25
print(get_now('time'))      # 14:30:45
print(get_now('datetime'))  # 2025-04-25 14:30:45
print(get_now('filename'))  # 20250425_143045
print(get_now('timestamp')) # 1684153845.123456