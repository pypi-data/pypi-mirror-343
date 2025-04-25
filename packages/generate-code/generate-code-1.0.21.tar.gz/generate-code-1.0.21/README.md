# generate-code
一个简单的 Java 代码生成器

## 必备安装:

brew install python # 安装Python (Python 3.x.x) 检查是否成功: python3 --version

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

python3 get-pip.py # macOS安装pip 检查是否成功: pip3 --version

python -m ensurepip --default-pip

python -m pip install --upgrade pip # win安装pip 检查是否成功: pip3 --version

## PyPI方式: 

pip3 install generate-code # 安装代码生成器项目

### 生成代码命令:
generate-code --db "root:password@localhost:3306/database_name"

必填
--db: 指定需要连接的数据库

选填
--table "table_name"": 可以指定需要成代码的表,也可以是多个用逗号隔开; 如: sys_user,sys_dept (默认扫描全部的表)

选填
--project-path /User/luojizhen/IdeaProjects/test: 可以指定存放代码的目录路径 (默认存放在根目录的generate-code下)
 