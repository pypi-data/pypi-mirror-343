import argparse
from jinja2 import Environment, FileSystemLoader
from sqlalchemy import create_engine, MetaData
import os
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
import sys


def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="Java 代码生成器")
    parser.add_argument("--db", type=str, required=True,
                        help="数据库连接字符串，例如：mysql+pymysql://root:password@localhost:3306/test_db")
    parser.add_argument("--table", type=str, help="指定要生成的表名，多个表用逗号分隔（默认全部表）", default="all")
    parser.add_argument("--project-path", type=str, help="指定 IDEA 项目路径（代码将直接生成到 src/main/java）")

    author_name = os.getenv("CODE_AUTHOR", "luojizhen")

    try:
        args = parser.parse_args()
    except SystemExit:
        # 捕获 SystemExit 异常，输出自定义错误信息
        print("❌ 错误: --db 参数是必填项！")
        print("使用示例: auto-code --db root:password@localhost:3306/test_db --table all --project-path /Users/luojizhen/IdeaProjects/projectName")
        sys.exit(1)  # 确保程序退出

    # 如果参数解析成功，可以继续执行后续逻辑
    print(f"数据库连接: {args.db}")

    # 连接数据库
    try:
        engine = create_engine("mysql+pymysql://" + args.db)
        metadata = MetaData()
        metadata.reflect(bind=engine)
        if not metadata.tables:
            print("❌ 未找到表！请确认数据库是否存在且包含表。")
            exit(1)
    except OperationalError as e:
        print(f"❌ 数据库连接失败或数据库不存在!")
        exit(1)

    # 获取当前脚本所在目录的上一级目录（项目根目录）
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # 指定模板路径
    TEMPLATE_DIR = os.path.join(BASE_DIR, "generate_code/templates/")

    # 配置 Jinja2
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

    # 代码输出目录
    if args.project_path is None:
        base_output_dir = os.path.expanduser("~/generated")  # 用家目录路径
    else:
        base_output_dir = os.path.join(args.project_path, "src/main/java")

    # 确保目录存在
    os.makedirs(base_output_dir, exist_ok=True)

    # 获取注解的函数
    def get_annotation_for_field(field_name):
        if field_name.lower() == "user_id":
            return "@TableId(type = IdType.ASSIGN_ID)"
        elif field_name.lower() == "deleted":
            return "@TableLogic"
        elif field_name.lower() == "created_by_id":
            return "@CreatedById"
        elif field_name.lower() == "created_by":
            return "@CreatedBy"
        elif field_name.lower() == "created_time":
            return "@CreatedDate"
        elif field_name.lower() == "updated_by_id":
            return "@LastModifiedById"
        elif field_name.lower() == "updated_by":
            return "@LastModifiedBy"
        elif field_name.lower() == "updated_time":
            return "@LastModifiedDate"
        else:
            return ""  # 对于没有特殊注解的字段，返回空字符串

    # 去掉表名前缀
    def remove_prefix(table_name):
        parts = table_name.split("_", 1)
        return parts[1] if len(parts) > 1 else table_name

    # 转换字段为驼峰格式
    def to_camel_case(name):
        parts = name.split("_")
        return parts[0].lower() + ''.join([part.capitalize() for part in parts[1:]])

    # 获取表描述
    def get_table_comment(table_name):
        query = text(f"SELECT TABLE_COMMENT FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table_name}'")
        with engine.connect() as connection:
            result = connection.execute(query).fetchone()
        return result[0] if result and result[0] else table_name  # 如果没有描述，则返回表名

    # 新增方法：将 sys_user 转换为 sys-user
    def to_dash_case(name):
        return name.replace("_", "-")

    # 将 sys_user 转换为 sysUser
    def to_lower_camel_case(name):
        parts = name.split("_")
        return parts[0].lower() + ''.join([part.capitalize() for part in parts[1:]])

    # 数据库类型转换（MySQL -> Java）
    def get_java_type(col):
        raw_type = str(col.type).upper()
        if "VARCHAR" in raw_type or "TEXT" in raw_type:
            return "String"
        elif "DECIMAL" in raw_type or "NUMERIC" in raw_type:
            return "BigDecimal"
        elif "INT" in raw_type and "BIG" not in raw_type:
            return "Integer"
        elif "BIGINT" in raw_type:
            return "Long"
        elif "DATETIME" in raw_type or "TIMESTAMP" in raw_type:
            return "LocalDateTime"
        elif "DATE" in raw_type or "TIMESTAMP" in raw_type:
            return "LocalDate"
        elif "TINYINT" in raw_type:
            return "Boolean"
        else:
            return "String"

    # 生成 Entity, DTO, VO 和 Controller, Service 代码的函数
    def generate_code(table_name, columns, primary_key_column):
        global max_length
        # 去掉前缀后生成类名（如 sys_user -> User）
        cleaned_table_name = remove_prefix(table_name)
        class_name = "".join([word.capitalize() for word in cleaned_table_name.split("_")])

        fields = []
        for col in columns:
            # 强制将 "deleted" 字段转换为 Boolean 类型
            if col.name.lower() == "deleted":
                field_type = "Boolean"
            else:
                field_type = get_java_type(col)

                # 获取字段长度（仅针对 String 类型）
                max_length = getattr(col.type, "length", None) if field_type == "String" else None
            field = {
                "name": to_camel_case(col.name),  # 转换为驼峰格式
                "type": field_type,
                "description": col.comment if col.comment else "无描述",  # 获取字段描述，若无则填“无描述”
                "is_primary": col.name == primary_key_column,  # 判断是否是主键
                "annotation": get_annotation_for_field(col.name),  # 获取字段注解
                "is_long": field_type == "Long",  # 判断是否是 Long 类型
                "max_length": max_length  # 记录字段的最大长度（如果有的话）
            }
            fields.append(field)

        table_name_dash = to_dash_case(cleaned_table_name)  # 转换 sys_user -> sys-user
        table_description = get_table_comment(table_name)  # 获取表描述
        table_name_camel = to_lower_camel_case(cleaned_table_name)  # 转换 sys_user -> sysUser

        # 渲染 Entity 模板
        entity_template = env.get_template("entity_template.jinja2")
        entity_code = entity_template.render(
            class_name=class_name,
            table_name=table_name,
            author=author_name,  # 可以动态传入
            date=datetime.now().strftime("%Y/%m/%d"),  # 当前日期
            fields=fields  # 渲染字段信息
        )

        # 渲染 DTO 模板
        dto_template = env.get_template("dto_template.jinja2")
        dto_code = dto_template.render(
            class_name=class_name,
            author=author_name,  # 可以动态传入
            date=datetime.now().strftime("%Y/%m/%d"),  # 当前日期
            fields=fields  # DTO 使用相同的字段
        )

        # 渲染 DTO 模板
        dto_query_template = env.get_template("dto_query_template.jinja2")
        dto_query_code = dto_query_template.render(
            class_name=class_name,
            author=author_name,  # 可以动态传入
            date=datetime.now().strftime("%Y/%m/%d"),  # 当前日期
            fields=fields  # DTO 使用相同的字段
        )

        # 渲染 VO 模板
        vo_template = env.get_template("vo_template.jinja2")
        vo_code = vo_template.render(
            class_name=class_name,
            author=author_name,  # 可以动态传入
            date=datetime.now().strftime("%Y/%m/%d"),  # 当前日期
            fields=fields  # VO 使用相同的字段
        )

        # 渲染 Controller 模板
        controller_template = env.get_template("controller_template.jinja2")
        controller_code = controller_template.render(
            class_name=class_name,
            table_name=table_description,  # 使用表描述代替表名
            urlName=table_name_dash,  # 传递 sys-user 形式的表名
            table_name_camel=table_name_camel,  # 传递 sysUser 形式的表名
            author=author_name,  # 可以动态传入
            date=datetime.now().strftime("%Y/%m/%d")  # 当前日期
        )

        # 渲染 Service 模板
        service_template = env.get_template("service_template.jinja2")
        service_code = service_template.render(
            class_name=class_name,
            table_name=table_description,  # 使用表描述代替表名
            urlName=table_name_dash,  # 传递 sys-user 形式的表名
            table_name_camel=table_name_camel,  # 传递 sysUser 形式的表名
            author=author_name,  # 可以动态传入
            date=datetime.now().strftime("%Y/%m/%d")  # 当前日期
        )

        # 渲染 Mapper 模板
        mapper_template = env.get_template("mapper_template.jinja2")
        mapper_code = mapper_template.render(
            class_name=class_name,
            table_name=table_description,  # 使用表描述代替表名
            urlName=table_name_dash,  # 传递 sys-user 形式的表名
            table_name_camel=table_name_camel,  # 传递 sysUser 形式的表名
            author=author_name,  # 可以动态传入
            date=datetime.now().strftime("%Y/%m/%d")  # 当前日期
        )

        # 确保文件夹存在
        os.makedirs(base_output_dir, exist_ok=True)

        # 写入 Entity 类 Java 文件，文件名是表名的驼峰格式
        output_dir = os.path.join(base_output_dir, "domain/entity")
        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, f"{class_name}.java"), "w", encoding="utf-8") as f:
            f.write(entity_code)

        # 写入 DTO 类 Java 文件，文件名是表名的驼峰格式
        output_dir2 = os.path.join(base_output_dir, "domain/dto")
        os.makedirs(output_dir2, exist_ok=True)
        with open(os.path.join(output_dir2, f"{class_name}DTO.java"), "w", encoding="utf-8") as f:
            f.write(dto_code)

        # 写入 QueryDTO 类 Java 文件，文件名是表名的驼峰格式
        output_dir7 = os.path.join(base_output_dir, "domain/dto")
        os.makedirs(output_dir7, exist_ok=True)
        with open(os.path.join(output_dir7, f"{class_name}QueryDTO.java"), "w", encoding="utf-8") as f:
            f.write(dto_query_code)

        # 写入 VO 类 Java 文件，文件名是表名的驼峰格式
        output_dir3 = os.path.join(base_output_dir, "domain/vo")
        os.makedirs(output_dir3, exist_ok=True)
        with open(os.path.join(output_dir3, f"{class_name}VO.java"), "w", encoding="utf-8") as f:
            f.write(vo_code)

        # 写入 Controller 类 Java 文件，文件名是表名的驼峰格式
        output_dir4 = os.path.join(base_output_dir, "controller")
        os.makedirs(output_dir4, exist_ok=True)
        with open(os.path.join(output_dir4, f"{class_name}Controller.java"), "w", encoding="utf-8") as f:
            f.write(controller_code)

        # 写入 Service 类 Java 文件，文件名是表名的驼峰格式
        output_dir5 = os.path.join(base_output_dir, "service")
        os.makedirs(output_dir5, exist_ok=True)
        with open(os.path.join(output_dir5, f"{class_name}Service.java"), "w", encoding="utf-8") as f:
            f.write(service_code)

        # 写入 Mapper 类 Java 文件
        output_dir6 = os.path.join(base_output_dir, "mapper")
        os.makedirs(output_dir6, exist_ok=True)
        with open(os.path.join(output_dir6, f"{class_name}Mapper.java"), "w", encoding="utf-8") as f:
            f.write(mapper_code)

    # 遍历表，生成代码
    if args.table.lower() == "all":
        for table_name, table in metadata.tables.items():
            generate_code(table_name, table.columns, table.primary_key.columns.keys())
    else:
        table_names = args.table.split(",")  # 支持多个表名
        for table_name in table_names:
            table_name = table_name.strip()
            if table_name in metadata.tables:
                table = metadata.tables[table_name]
                generate_code(table_name, table.columns, table.primary_key.columns.keys())
            else:
                print(f"⚠️  表 {table_name} 不存在！")

    print("✅ Java 代码生成完毕！")

    # 目标目录映射
    target_dirs = {
        "domain/entity": "domain/entity/",
        "domain/dto": "domain/dto/",
        "domain/vo": "domain/vo/",
        "controller": "controller/",
        "service": "service/",
        "mapper": "mapper/"
    }

    print(f"🚀 Java 代码已存放到   {base_output_dir} 目录下 赶快去看看吧！✈️")


if __name__ == "__main__":
    main()
