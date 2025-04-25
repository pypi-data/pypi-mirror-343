from datetime import datetime
from typing import Literal, Union

TimeFormatType = Literal['date', 'time', 'datetime', 'filename', 'timestamp']

def get_now(time_type: TimeFormatType) -> str:
    """
获取当前时间的各种格式化字符串

Args:
time_type: 时间格式类型，可选值:
'date' - 返回年月日 (YYYY-MM-DD)
'time' - 返回时分秒 (HH:MM:SS)
'datetime' - 返回年月日时分秒 (YYYY-MM-DD HH:MM:SS)
'filename' - 返回文件名格式时间 (YYYYMMDD_HHMMSS)
'timestamp' - 返回时间戳

Returns:
格式化后的时间字符串或时间戳字符串。如果输入无效，返回错误提示。
    """
    now = datetime.now()

    format_mapping = {
        'date': '%Y-%m-%d',
        'time': '%H:%M:%S',
        'datetime': '%Y-%m-%d %H:%M:%S',
        'filename': '%Y%m%d_%H%M%S',
        'timestamp': lambda: str(now.timestamp())
    }

    try:
        format_spec = format_mapping[time_type]
        if callable(format_spec):
            return format_spec()
        return now.strftime(format_spec)
    except KeyError:
        return f"错误：无效的时间类型 '{time_type}'。可用类型: {list(format_mapping.keys())}"


if __name__ == '__main__':
    # 测试用例
    print(get_now('date'))      # 例如: 2023-05-15
    print(get_now('time'))      # 例如: 14:30:45
    print(get_now('datetime'))  # 例如: 2023-05-15 14:30:45
    print(get_now('filename'))  # 例如: 20230515_143045
    print(get_now('timestamp')) # 例如: 1684153845.123456
    print(get_now('invalid'))   # 例如: 错误：无效的时间类型 'invalid'。可用类型: ['date', 'time', 'datetime', 'filename', 'timestamp']