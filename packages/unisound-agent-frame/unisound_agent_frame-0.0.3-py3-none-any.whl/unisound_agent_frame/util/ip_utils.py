from fastapi import Request


def get_true_remote_addr(request: Request) -> str:
    """获取真实的客户端IP地址
    
    支持多种代理头的检查，按优先级依次检查以下头信息：
    1. X-Forwarded-For
    2. Proxy-Client-IP
    3. WL-Proxy-Client-IP
    4. HTTP_CLIENT_IP
    5. HTTP_X_FORWARDED_FOR
    6. request.client.host (FastAPI) 或 request.remote_addr (Flask)
    
    Args:
        request: FastAPI或Flask的请求对象
        
    Returns:
        str: 真实的客户端IP地址
    """
    UNKNOWN_USER_IP = "unknown"
    
    # 定义要检查的代理头列表
    proxy_headers = [
        "X-Forwarded-For",
        "Proxy-Client-IP",
        "WL-Proxy-Client-IP",
        "HTTP_CLIENT_IP",
        "HTTP_X_FORWARDED_FOR"
    ]
    
    # 检查所有代理头
    for header in proxy_headers:
        user_ip = request.headers.get(header)
        if user_ip and user_ip.lower() != UNKNOWN_USER_IP:
            # 处理多重代理的情况，获取第一个IP（真实客户端IP）
            if ',' in user_ip:
                user_ip = user_ip.split(',')[0].strip()
            return user_ip
    
    # 如果所有代理头都没有获取到有效IP，则使用直连IP
    if isinstance(request, Request):  # FastAPI
        return request.client.host if request.client else "127.0.0.1"