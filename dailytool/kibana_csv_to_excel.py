#!/usr/bin/env python3
# *_*coding=utf-8
"""
@author : Francis.zz
@date   : 2026-05-11 15:00:00
@desc   : kibana_csv_to_excel.py - 把 Kibana 导出的 CSV 转成格式化好的 Excel
"""

import pandas as pd
from datetime import datetime

# ============== 可修改配置 ==============
CSV_FILE = r"C:\Users\zzfen\Downloads\dialog_text_export.csv"  # Kibana 下载的 CSV 路径
OUTPUT_FILE = f"企微群消息_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
# ========================================


def format_msgtime(ts):
    if pd.isna(ts) or ts == "":
        return ""
    try:
        ts = int(float(ts))
        if ts > 10_000_000_000:  # 毫秒
            ts = ts / 1000
        return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
    except (ValueError, TypeError, OSError):
        return str(ts)


def main():
    # Kibana CSV 默认 UTF-8，dtype=str 防止 ID 被识别成数字
    df = pd.read_csv(CSV_FILE, encoding="utf-8", dtype=str, keep_default_na=False)
    print("原始列名:", list(df.columns))

    # 兼容字段名：msgbody.content 有时会变成 msgbody_content
    content_col = next((c for c in df.columns if "content" in c.lower()), None)

    out = pd.DataFrame({
        "群组ID": df.get("roomid", ""),
        "消息发送人": df.get("from", ""),
        "消息内容": df[content_col] if content_col else "",
        "发送时间": df["msgtime"].apply(format_msgtime) if "msgtime" in df.columns else "",
    })

    out.to_excel(OUTPUT_FILE, index=False)
    print(f"导出完成：共 {len(out)} 条，文件：{OUTPUT_FILE}")


if __name__ == "__main__":
    main()
