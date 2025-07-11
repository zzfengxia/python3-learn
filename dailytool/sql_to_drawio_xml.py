import re
from lxml import etree


def parse_sql(sql_file):
    """解析SQL文件，提取表结构信息"""
    try:
        with open(sql_file, "r", encoding="utf-8") as f:
            sql = f.read()
    except FileNotFoundError:
        print(f"❌ 文件 {sql_file} 不存在")
        return {}
    except Exception as e:
        print(f"❌ 读取文件时出错: {e}")
        return {}

    # 移除SQL注释
    sql = re.sub(r'/\*.*?\*/', '', sql, flags=re.DOTALL)
    sql = re.sub(r'--.*?\n', '\n', sql)

    # 改进的CREATE TABLE解析 - 使用更智能的方法
    tables = {}

    # 先找到所有CREATE TABLE的起始位置
    create_starts = []
    for match in re.finditer(r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?`?(\w+)`?\s*\(', sql, re.IGNORECASE):
        create_starts.append({
            'table_name': match.group(1),
            'start_pos': match.start(),
            'body_start': match.end() - 1  # 括号位置
        })

    # 为每个表找到完整的定义
    for i, table_info in enumerate(create_starts):
        table_name = table_info['table_name']
        body_start = table_info['body_start']

        # 找到对应的结束位置
        if i < len(create_starts) - 1:
            # 不是最后一个表，搜索到下一个CREATE TABLE之前
            search_end = create_starts[i + 1]['start_pos']
        else:
            # 最后一个表，搜索到文件末尾
            search_end = len(sql)

        # 在指定范围内找到表定义的结束
        table_def = sql[body_start:search_end]

        # 使用括号匹配找到真正的表定义结束
        paren_count = 0
        body_end = -1

        for j, char in enumerate(table_def):
            if char == '(':
                paren_count += 1
            elif char == ')':
                paren_count -= 1
                if paren_count == 0:
                    body_end = j
                    break

        if body_end == -1:
            print(f"⚠️ 表 {table_name} 的定义不完整，跳过")
            continue

        # 提取表体内容
        table_body = table_def[1:body_end]  # 去掉开头和结尾的括号

        # 提取表注释
        table_comment = ""
        remaining_def = table_def[body_end + 1:]  # 括号后面的内容
        comment_match = re.search(r'COMMENT\s*=\s*[\'"]([^\'"]*)[\'"]', remaining_def, re.IGNORECASE)
        if comment_match:
            table_comment = comment_match.group(1)

        # 解析表体
        parse_table_body(table_name, table_body, table_comment, tables)

    return tables


def parse_table_body(table_name, table_body, table_comment, tables):
    """解析表体内容"""
    # 需要过滤的系统字段
    filtered_fields = {
        'create_time', 'update_time', 'create_user', 'create_user_name',
        'update_user', 'update_user_name', 'is_deleted'
    }

    fields = []
    pk_fields = set()

    # 按行分割表体
    lines = [line.strip() for line in table_body.strip().split('\n') if line.strip()]

    for line in lines:
        line = line.rstrip(',').strip()

        # 解析字段定义
        if line.startswith("`") or (
                line and not line.upper().startswith(('PRIMARY', 'KEY', 'UNIQUE', 'INDEX', 'CONSTRAINT', 'FOREIGN'))):
            # 增强的字段解析，支持注释提取
            field_match = re.match(r'`?(\w+)`?\s+(\w+(?:\(\d+(?:,\d+)?\))?)', line)
            if field_match:
                col_name = field_match.group(1)
                col_type = field_match.group(2)

                # 跳过系统字段
                if col_name.lower() in filtered_fields:
                    continue

                # 提取注释
                comment = ""
                comment_match = re.search(r'COMMENT\s+[\'"]([^\'"]*)[\'"]', line, re.IGNORECASE)
                if comment_match:
                    comment = comment_match.group(1)
                if "废弃" in comment:
                    continue

                # 检查是否为主键（AUTO_INCREMENT通常是主键）
                is_pk = 'AUTO_INCREMENT' in line.upper() or 'PRIMARY KEY' in line.upper()
                if is_pk:
                    pk_fields.add(col_name)

                fields.append((col_name, col_type, comment))

        # 解析PRIMARY KEY约束
        elif line.upper().startswith("PRIMARY KEY"):
            pk_match = re.findall(r'`(\w+)`', line)
            pk_fields.update(pk_match)

        # 解析KEY约束
        elif line.upper().startswith("KEY"):
            continue

    # 标记主键字段
    final_fields = []
    for name, col_type, comment in fields:
        mark = "PK" if name in pk_fields else ""
        final_fields.append((name, col_type, comment, mark))

    tables[table_name] = {"fields": final_fields, "comment": table_comment}


def calculate_table_positions(tables, table_width=250, header_height=30, row_height=25):
    """计算表格位置，避免重叠"""
    positions = {}

    # 按字段数量排序，字段多的表优先放置
    sorted_tables = sorted(tables.items(), key=lambda x: len(x[1]["fields"]), reverse=True)

    # 布局参数
    margin = 50  # 表格间距
    canvas_width = 1200  # 画布宽度
    start_x, start_y = 50, 50

    current_x = start_x
    current_y = start_y
    row_max_height = 0

    for table_name, table_data in sorted_tables:
        field_count = len(table_data["fields"])
        table_height = header_height + row_height * field_count

        # 检查是否需要换行
        if current_x + table_width > canvas_width:
            current_x = start_x
            current_y += row_max_height + margin
            row_max_height = 0

        positions[table_name] = (current_x, current_y)

        # 更新位置和最大高度
        current_x += table_width + margin
        row_max_height = max(row_max_height, table_height)

    return positions


def create_drawio_er_xml(tables):
    """创建Draw.io格式的ER图XML"""
    # 创建根节点
    mxfile = etree.Element("mxfile", host="app.diagrams.net", modified="2024-01-01T00:00:00.000Z",
                           agent="Mozilla/5.0", etag="drawio", version="22.1.16")

    diagram = etree.SubElement(mxfile, "diagram", name="ER Diagram", id="er-diagram")

    # 创建mxGraphModel
    mxGraphModel = etree.SubElement(diagram, "mxGraphModel",
                                    dx="1422", dy="794", grid="1", gridSize="10",
                                    guides="1", tooltips="1", connect="1",
                                    arrows="1", fold="1", page="1", pageScale="1",
                                    pageWidth="1600", pageHeight="1200", math="0", shadow="0")

    root = etree.SubElement(mxGraphModel, "root")

    # 添加默认的根单元格
    etree.SubElement(root, "mxCell", id="0")
    etree.SubElement(root, "mxCell", id="1", parent="0")

    # 布局参数
    table_width = 280  # 增加宽度以容纳注释
    row_height = 25
    header_height = 30
    counter = 2

    # 计算表格位置，避免重叠
    table_positions = calculate_table_positions(tables, table_width, header_height, row_height)

    for table_name, table_data in tables.items():
        field_count = len(table_data["fields"])
        total_height = header_height + row_height * field_count

        # 获取计算好的位置
        x, y = table_positions[table_name]

        table_id = str(counter)
        counter += 1

        # 构建表名显示文本，包含表注释
        table_display_name = table_name
        if table_data.get("comment"):
            table_display_name += f" ({table_data['comment']})"

        # 创建表格容器（swimlane样式）
        table_style = ("swimlane;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;"
                       "startSize=26;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;"
                       "marginBottom=0;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=12;")

        cell = etree.SubElement(root, "mxCell", id=table_id, value=table_display_name,
                                style=table_style, vertex="1", parent="1")

        geo = etree.SubElement(cell, "mxGeometry", **{"as": "geometry"})
        geo.attrib.update({
            "x": str(x),
            "y": str(y),
            "width": str(table_width),
            "height": str(total_height)
        })

        # 添加字段
        for i, (field_name, field_type, comment, mark) in enumerate(table_data["fields"]):
            field_id = str(counter)
            counter += 1

            # 构建字段显示文本 - 改进格式
            display_text = field_name
            if field_type:
                display_text += f" : {field_type}"
            if mark == "PK":
                display_text = f"🔑 {display_text}"
            if comment:
                display_text += f" ({comment})"

            # 字段样式 - 改进样式
            field_style = ("text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=8;"
                           "spacingRight=8;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;"
                           "fontSize=11;")

            # 主键字段使用不同样式
            if mark == "PK":
                field_style += "fontStyle=1;fontColor=#d79b00;fillColor=#fff2cc;"
            else:
                field_style += "fontColor=#333333;"

            field_cell = etree.SubElement(root, "mxCell", id=field_id, value=display_text,
                                          style=field_style, vertex="1", parent=table_id)

            field_geo = etree.SubElement(field_cell, "mxGeometry", **{"as": "geometry"})
            field_geo.attrib.update({
                "y": str(header_height + i * row_height),
                "width": str(table_width),
                "height": str(row_height)
            })

    return etree.tostring(mxfile, pretty_print=True, encoding="utf-8", xml_declaration=True)


def main():
    """主函数"""
    # 配置文件路径
    sql_file_path = "C:\\Users\\zzfen\\Desktop\\ai_taskpack.sql"  # 修改为您的SQL文件路径
    output_file_path = "C:\\Users\\zzfen\\Desktop\\er_diagram2.drawio"  # 输出文件路径

    print("🔍 开始解析SQL文件...")
    tables = parse_sql(sql_file_path)

    if not tables:
        print("❌ 没有找到有效的表结构")
        return

    print(f"✅ 成功解析 {len(tables)} 个表:")
    for table_name, table_data in tables.items():
        print(f"  📋 {table_name}: {len(table_data['fields'])} 个字段")

    print("\n📝 生成Draw.io XML文件...")
    xml_content = create_drawio_er_xml(tables)

    try:
        with open(output_file_path, "wb") as f:
            f.write(xml_content)
        print(f"✅ 成功生成: {output_file_path}")
    except Exception as e:
        print(f"❌ 保存文件时出错: {e}")


if __name__ == '__main__':
    main()
