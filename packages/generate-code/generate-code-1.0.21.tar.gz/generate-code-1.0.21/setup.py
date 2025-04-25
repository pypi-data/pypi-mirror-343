from setuptools import setup, find_packages

setup(
    name="generate-code",
    version="1.0.21",
    packages=find_packages(),  # 发现所有 Python 包
    include_package_data=True,
    package_data={
        'generate_code': ['templates/*.jinja2'],  # 这里指定要包含的模板文件
    },
    install_requires=[
        "sqlalchemy",
        "pymysql",
        "jinja2"
    ],
    entry_points={
        "console_scripts": [
            "auto-code=generate_code.__main__:main"
        ]
    },
    author="骆吉振",
    description="一个简单的 Java 代码生成器",
    author_email="luojizhen99@gmail.com",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/luojizhen99/generate-code.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)