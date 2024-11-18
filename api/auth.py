import json
import requests

"""
权限控制API
"""


def api_login_user(username, password, device, satoken=None):
    # 登录
    url = "http://124.222.40.17:48080/admin-api/account/user/login_user"

    payload = {
        'username': username,
        'password': password,
        'device': device
    }
    headers = {
        'satoken': satoken,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, params=payload,
                                data=json.dumps(payload, ensure_ascii=False))

    res = response.content.decode(encoding='utf-8')
    print(res)
    data = json.loads(res)
    demo = {
        "code": 0,
        "data": {
            "token_info": {
                "tokenName": "satoken",
                "tokenValue": "b3ff8b86-8f04-40ac-8be9-4f152329c68e",
                # "isLogin": true,
                "loginId": "14",
                "loginType": "login",
                "tokenTimeout": -1,
                "sessionTimeout": -1,
                "tokenSessionTimeout": -2,
                "tokenActiveTimeout": -1,
                "loginDevice": "客户端",
                # "tag": null
            },
            "user": {
                "createTime": 1731642065000,
                "updateTime": 1731625938000,
                "creator": "1",
                "updater": "1",
                # "deleted": false,
                "id": 14,
                "username": "test",
                "avatar": "http://test.yudao.iocoder.cn/557f12e13d781195f6c910a9986f7bff498c8b65bb5bb8b0848f43e8561c7294.jpg",
                "password": "***********",
                "nickname": "测试",
                "mobile": "15267398131",
                "status": 1,
                "allowTokenNumber": 2,
                "loginIp": "0.0.0.0",
                "loginDate": 1731600000000,
                "expirationDate": 1731656400000
            },
            "token": "b3ff8b86-8f04-40ac-8be9-4f152329c68e"
        },
        "msg": ""
    }
    return data


def api_token_check(satoken):
    # 令牌校验
    url = "http://124.222.40.17:48080/admin-api/account/user/token_check"

    payload = {
        'satoken': satoken,
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, params=payload)
    res = response.content.decode(encoding='utf-8')
    print(f"Token校验:{payload}")
    print(res)
    data = json.loads(res)
    demo1 = {"code": 0, "data": 'true', "msg": "消息xxx"}
    demo2 = {"code": 1_003_000_01, "data": 'null', "msg": "已过期"}
    demo2 = {"code": 100300006, "data": 'null', "msg": "未登录"}
    # 如果Token已过期，则强行登出。
    return data


def api_logout_user_by_satoken(satoken, logout_token):
    """
    根据token登出
    :param satoken: 操作者的token
    :param logout_token: 需要登出的token
    :return:
    """
    # 根据Token登出
    url = "http://124.222.40.17:48080/admin-api/account/user/logout_user_by_satoken"

    payload = {
        'satoken': satoken,
        'logout_token': logout_token,
    }
    headers = {
        'satoken': satoken,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, params=payload)
    res = response.content.decode(encoding='utf-8')
    print(f"Token登出:{payload}")
    print(res)
    data = json.loads(res)
    demo1 = {"code": 100300006, "data": 'null', "msg": "未登录"}
    demo2 = {"code": 0, "data": 'true', "msg": ""}
    return data


def api_logout_user(satoken):
    # 自身登出
    url = "http://124.222.40.17:48080/admin-api/account/user/logout_user"

    payload = {
        "satoken": satoken,
    }
    headers = {
        "satoken": satoken,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    res = response.content.decode(encoding='utf-8')
    print(res)
    data = json.loads(res)


def api_login_list(satoken):
    # 登录列表
    url = "http://124.222.40.17:48080/admin-api/account/user/login_list"

    payload = {
        "satoken": satoken
    }
    headers = {
        "satoken": satoken,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, params=payload)

    res = response.content.decode(encoding='utf-8')
    print(res)
    data = json.loads(res)
    print(f"登录列表:{payload}")
    if data['code'] == 0:
        return data['data']


if __name__ == '__main__':
    login_list = api_login_list("6809c311-1652-4e5c-9105-72771a2bde2d")
    # login_list = api_login_user("test", "test", device="电脑二")
    # login_list = api_logout_user_by_satoken("b3ff8b86-8f04-40ac-8be9-4f152329c68e","59e3b164-1fe9-44bb-a056-cb1f2dad6d73")
    # login_list = api_logout_user("b3ff8b86-8f04-40ac-8be9-4f152329c68e","59e3b164-1fe9-44bb-a056-cb1f2dad6d73")
    print(login_list)
