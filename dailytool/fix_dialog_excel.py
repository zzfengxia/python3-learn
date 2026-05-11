#!/usr/bin/env python3
# *_*coding=utf-8
"""
@author : Francis.zz
@date   : 2026-05-11 16:00:00
@desc   : fix_dialog_excel.py - 修正企微群会话时区+格式，输出真正 xlsx
"""

import pandas as pd
from datetime import datetime, timedelta

SRC = r"C:\Users\zzfen\Desktop\企微群会话.xlsx"   # 实际是 GBK 制表符分隔
DST = r"C:\Users\zzfen\Desktop\企微群会话_处理后.xlsx"
TZ_OFFSET_HOURS = 8

TIME_FORMATS = [
    "%m/%d/%Y %I:%M:%S %p",   # 05/08/2026 6:38:00 am
    "%m/%d/%Y %H:%M:%S",
    "%Y-%m-%d %H:%M:%S",
]


def parse_and_shift(s):
    if not s or pd.isna(s):
        return ""
    s = str(s).strip()
    # 小写 am/pm 适配
    s_norm = s.replace("am", "AM").replace("pm", "PM")
    for fmt in TIME_FORMATS:
        try:
            dt = datetime.strptime(s_norm, fmt)
            dt += timedelta(hours=TZ_OFFSET_HOURS)
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            continue
    return s  # 解析不了就原样返回


def main():
    df = pd.read_csv(
        SRC, sep="\t", encoding="gb18030",
        dtype=str, keep_default_na=False,
        encoding_errors="replace",
    )
    print(f"读取到 {len(df)} 行, 列: {list(df.columns)}")

    if "msgtime" in df.columns:
        df["msgtime"] = df["msgtime"].apply(parse_and_shift)

    # 重命名为中文列头
    rename_map = {
        "from": "消息发送人",
        "roomid": "群组ID",
        "msgtime": "发送时间",
        "msgbody.content": "消息内容",
    }
    df = df.rename(columns=rename_map)

    # 重新排列列顺序
    wanted = ["群组ID", "消息发送人", "消息内容", "发送时间"]
    cols = [c for c in wanted if c in df.columns] + \
           [c for c in df.columns if c not in wanted]
    df = df[cols]

    df.to_excel(DST, index=False)
    print(f"已输出: {DST}  共 {len(df)} 行")


if __name__ == "__main__":
    main()
