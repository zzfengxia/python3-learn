import hashlib
from collections import OrderedDict
import time

"""
租户表查询租户的tenantKey和sign字段的内容
"""
def gen_sign(tenant_key, timestamp, sign):
    if not timestamp:
        timestamp = int(time.time() * 1000)
    print(f"timestamp: {timestamp}")

    # 使用OrderedDict来保持键的顺序，模拟TreeMap的排序行为
    sort_map = OrderedDict()
    sort_map["tenantKey"] = tenant_key  # 假设TENANT_KEY常量为"tenantKey"
    sort_map["timestamp"] = str(timestamp)  # 假设TIMESTAMP常量为"timestamp"

    param_list = []
    for key, value in sort_map.items():
        sb = f"{key}="
        if value is not None:
            sb += value
        param_list.append(sb)

    param_list.append(f"key={sign}")
    param_text = "&".join(param_list)

    # 计算MD5
    param_sign = hashlib.md5(param_text.encode('utf-8')).hexdigest()
    print(f"加密结果: {param_sign}")

if __name__ == "__main__":
    gen_sign("wpLHbUCwAAjnMUfpdw_xR2F1-PW8Lutw", None, "zdfhzsjfgzxfzhbfk4375sdfcxvkj")