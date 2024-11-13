def api_login(username, password):
    # 这里模拟HTTP登录的请求结果
    result = {
        "code": 200,
        "msg": "登录成功",
        "token": "0123456789876543210",
        "data": {
            "username": "",  # 登录用户名
            "avatar": "http://test.yudao.iocoder.cn/bf2002b38950c904243be7c825d3f82e29f25a44526583c3fde2ebdff3a87f75.png",
            "nickname": "煜稻",  # 昵称
            "mobile": "15267398131",  # 手机号
            "status": "正常",  # 账号状态
            "login_ip": "192.168.1.1",  # 登录IP
            "login_date": "2024:11:13 13:13:01",  # 登录时间
            "expiration_date": "2025:11:13 13:13:01",  # 过期时间
        }
    }
    return result


def api_check_token(token):
    # 检测Token是否有效
    result = {
        "code": 200,
        "msg": "登录成功",
        "token": "0123456789876543210",
        "data": {
            "username": "",  # 登录用户名
            "avatar": "http://test.yudao.iocoder.cn/bf2002b38950c904243be7c825d3f82e29f25a44526583c3fde2ebdff3a87f75.png",
            "nickname": "煜稻",  # 昵称
            "mobile": "15267398131",  # 手机号
            "status": "正常",  # 账号状态
            "login_ip": "192.168.1.1",  # 登录IP
            "login_date": "2024:11:13 13:13:01",  # 登录时间
            "expiration_date": "2025:11:13 13:13:01",  # 过期时间
        }
    }
    return result
