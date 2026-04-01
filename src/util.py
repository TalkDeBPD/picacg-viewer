from datetime import datetime
from httpx import HTTPError


def format_time(timestamp: float) -> str:
    dt = datetime.fromtimestamp(timestamp)
    now = datetime.now()
    if dt.year == now.year:
        if dt.month == now.month and dt.day == now.day:
            return dt.strftime('%H:%M:%S')
        else:
            return dt.strftime('%m月%d日 %H:%M:%S')
    else:
        return dt.strftime('%Y年%m月%d日 %H:%M:%S')


def format_http_error(e: HTTPError) -> str:
    result = type(e).__name__
    if hasattr(e, 'request'):
        result += f'\n请求：{e.request.method} {e.request.url}'
    if hasattr(e, 'response'):
        result += f'\n响应：{e.response.method} {e.response.url}'
    return result
