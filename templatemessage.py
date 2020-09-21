import requests
def aform1(ad,openid):
    requests.packages.urllib3.disable_warnings()
    payload = {
    'grant_type': 'client_credential',
    'appid':'wx870f2da4363840c4',
    'secret': '658976ad33ec3b6d1cdbe2c84b71b8da'
    }

    req = requests.get('https://api.weixin.qq.com/cgi-bin/token', params=payload, timeout=3, verify=False)
    access_token = req.json().get('access_token')

    data = {
        "touser": openid,
        "template_id": 'ICStK5Qv31uRUzPH7Gg_BTMmoFOliZbE1uMkybwpdaU',
        "page": 'pages/index/index',
        "data": {
            'thing1': {
                'value': ad[0]
            },
            'date2': {
                'value': ad[1]
            },
            'thing3': {
                'value':ad[2]
            },
            'thing4': {
                'value':ad[3]
            }

        },
        "emphasis_keyword": ''
    }

    push_url = 'https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token={}'.format(access_token)
    response=requests.post(push_url, json=data, timeout=3, verify=False)
    return response.text
def aform2(ad,openid):
    requests.packages.urllib3.disable_warnings()
    payload = {
    'grant_type': 'client_credential',
    'appid':'wx870f2da4363840c4',
    'secret': '658976ad33ec3b6d1cdbe2c84b71b8da'
    }

    req = requests.get('https://api.weixin.qq.com/cgi-bin/token', params=payload, timeout=3, verify=False)
    access_token = req.json().get('access_token')

    data = {
        "touser": openid,
        "template_id": 'qSVRv0fOHWeLD28fM3t76kgIcn3EXG8g_jN0cemSrCI',
        "page": 'pages/index/index',
        "data": {
            'phrase1': {
                'value': ad[0]
            },
            'thing2': {
                'value': ad[1]
            },
            'date3': {
                'value':ad[2]
            },
            'date4': {
                'value':ad[3]
            },
            'thing5': {
                'value': ad[4]
            },
        },
        "emphasis_keyword": ''
    }

    push_url = 'https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token={}'.format(access_token)
    requests.post(push_url, json=data, timeout=3, verify=False)




def aform3(ad,openid):
    requests.packages.urllib3.disable_warnings()
    payload = {
    'grant_type': 'client_credential',
    'appid':'wx870f2da4363840c4',
    'secret': '658976ad33ec3b6d1cdbe2c84b71b8da'
    }

    req = requests.get('https://api.weixin.qq.com/cgi-bin/token', params=payload, timeout=3, verify=False)
    access_token = req.json().get('access_token')

    data = {
        "touser": openid,
        "template_id": 'LfXNwHewkFIlbyDKJ6mID0BagPxouyLUh_iuTR1Jrd4',
        "page": 'pages/index/index',
        "data": {
            'thing4': {
                'value': ad[0]
            },
            'name1': {
                'value': ad[1]
            },
            'time2': {
                'value':ad[2]
            },
            'date6': {
                'value':ad[3]
            },
            'phrase12': {
                'value': ad[4]
            },
        },
        "emphasis_keyword": ''
    }

    push_url = 'https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token={}'.format(access_token)
    requests.post(push_url, json=data, timeout=3, verify=False)

# if __name__=="__main__":
#     db=sdb
#     query=db.query("select wxid from acinfo where priority!='z'")
#     while query.next():
#         print(query.value('wxid'))
#     openid='o6cVM5a_PkMckOqXAKJ6e1Jcfb30'
#     ac=['还是测试一些','2020-02-01','订阅消息','精益']
#
#     print(ac)
#     print(aform1(ac,openid))