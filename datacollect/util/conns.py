#!/usr/bin/env python3
# *_*coding=utf-8
# @author : Francis.zz
# @date   : 2023-09-26 16:34
# @desc   : 调用通达信接口，使用`pip install pytdx`安装


from datacollect import cons as ct


def api(retry_count=3):
    from pytdx.hq import TdxHq_API
    for _ in range(retry_count):
        try:
            api = TdxHq_API(heartbeat=True)
            api.connect(ct._get_server(), ct.T_PORT)
        except Exception as e:
            print(e)
        else:
            return api
    raise IOError(ct.NETWORK_URL_ERROR_MSG)


def xapi(retry_count=3):
    from pytdx.exhq import TdxExHq_API
    for _ in range(retry_count):
        try:
            api = TdxExHq_API(heartbeat=True)
            api.connect(ct._get_xserver(), ct.X_PORT)
        except Exception as e:
            print(e)
        else:
            return api
    raise IOError(ct.NETWORK_URL_ERROR_MSG)


def xapi_x(retry_count=3):
    from pytdx.exhq import TdxExHq_API
    for _ in range(retry_count):
        try:
            api = TdxExHq_API(heartbeat=True)
            api.connect(ct._get_xxserver(), ct.X_PORT)
        except Exception as e:
            print(e)
        else:
            return api
    raise IOError(ct.NETWORK_URL_ERROR_MSG)


def get_apis():
    return api(), xapi()


def close_apis(conn):
    api, xapi = conn
    try:
        api.disconnect()
        xapi.disconnect()
    except Exception as e:
        print(e)
