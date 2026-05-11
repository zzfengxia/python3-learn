#!/usr/bin/env python3
# *_*coding=utf-8
"""
@author : Francis.zz
@date   : 2026-05-11 10:00:00
@desc   : export_es_dialog.py - 从 ES 导出 work_wx_customer_dialog 文本消息到 Excel
"""

import pandas as pd
from datetime import datetime
from elasticsearch import Elasticsearch

# ============== 可修改配置 ==============
ES_HOST = "11"
ES_VERIFY_CERTS = False        # 火山引擎公网证书一般可信，关闭可避免证书问题
ES_USERNAME = "admin"
ES_PASSWORD = "11^GC"
ES_INDEX = "work_wx_customer_dialog"
EXPORT_TOTAL = 10000           # 导出总条数
SCROLL_SIZE = 1000             # 每批拉取条数
SCROLL_KEEP_ALIVE = "2m"
OUTPUT_FILE = f"企微群消息_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
# ========================================


def build_es_client():
    import warnings
    from urllib3.exceptions import InsecureRequestWarning
    warnings.filterwarnings("ignore", category=InsecureRequestWarning)
    return Elasticsearch(
        hosts=[ES_HOST],
        basic_auth=(ES_USERNAME, ES_PASSWORD),
        verify_certs=ES_VERIFY_CERTS,
        ssl_show_warn=False,
        request_timeout=60,
    )


def format_msgtime(ts):
    if ts is None:
        return ""
    try:
        ts = int(ts)
        # 毫秒时间戳
        if ts > 10_000_000_000:
            ts = ts / 1000
        return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
    except (ValueError, TypeError, OSError):
        return str(ts)


def extract_content(source):
    msgbody = source.get("msgbody") or {}
    if isinstance(msgbody, dict):
        return msgbody.get("content", "")
    return str(msgbody)


def export():
    es = build_es_client()

    query = {
        "query": {
            "term": {"msgtype": "text"}
        },
        "_source": ["from", "msgbody", "roomid", "msgtime"],
        "size": SCROLL_SIZE,
    }

    rows = []
    resp = es.search(index=ES_INDEX, body=query, scroll=SCROLL_KEEP_ALIVE)
    scroll_id = resp.get("_scroll_id")
    hits = resp["hits"]["hits"]

    try:
        while hits and len(rows) < EXPORT_TOTAL:
            for hit in hits:
                src = hit.get("_source", {})
                rows.append({
                    "群组ID": src.get("roomid", ""),
                    "消息发送人": src.get("from", ""),
                    "消息内容": extract_content(src),
                    "发送时间": format_msgtime(src.get("msgtime")),
                })
                if len(rows) >= EXPORT_TOTAL:
                    break

            if len(rows) >= EXPORT_TOTAL:
                break

            resp = es.scroll(scroll_id=scroll_id, scroll=SCROLL_KEEP_ALIVE)
            scroll_id = resp.get("_scroll_id")
            hits = resp["hits"]["hits"]
    finally:
        if scroll_id:
            try:
                es.clear_scroll(scroll_id=scroll_id)
            except Exception:
                pass

    df = pd.DataFrame(rows, columns=["群组ID", "消息发送人", "消息内容", "发送时间"])
    df.to_excel(OUTPUT_FILE, index=False)
    print(f"导出完成：共 {len(rows)} 条，文件：{OUTPUT_FILE}")


if __name__ == "__main__":
    export()
