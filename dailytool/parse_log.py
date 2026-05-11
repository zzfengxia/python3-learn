import json
import re
from collections import Counter

file_path = "C:\\Users\\zzfen\\Desktop\\log\\log.json"

counter = Counter()

if __name__ == '__main__':

    # 逐行读取文件并匹配 to_user_id
    with open(file_path, "rb") as f:
        for raw in f:
            try:
                line = raw.decode("utf-8", errors="ignore").strip()
                if not line:
                    continue

                # 每行是一个 JSON 对象
                record = json.loads(line)
                content = record.get("__content__") or record.get("content")
                if not content:
                    continue
                # 尝试直接匹配 to_user_id
                pattern = r'to_user_id[\\]*"[:\\]*"([^"\\]+)'
                match = re.search(pattern, content)
                if match:
                    counter[match.group(1)] += 1
                    continue
            except Exception:
                continue

    # 获取出现次数最多的20个
    top20 = counter.most_common(20)
    # 换行打印每个的值和次数
    print(f"{'排序':<5} {'to_user_id':<40} {'出现次数':<10}")
    print("=" * 55)
    for index, (user_id, count) in enumerate(top20, 1):
        print(f"{index:<5} {user_id:<40} {count:<10}")
