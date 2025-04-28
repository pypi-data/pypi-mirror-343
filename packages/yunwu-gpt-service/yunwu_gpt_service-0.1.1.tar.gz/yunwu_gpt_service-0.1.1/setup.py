from setuptools import setup, find_packages

setup(
    name="yunwu_gpt_service",        # 包名称，可自行命名，但要唯一
    version="0.1.1",                 # 版本号
    packages=find_packages(),        # 自动发现项目中的包
    install_requires=[               # 指定依赖，与 requirements.txt 相匹配
        "requests>=2.0"
    ],
    entry_points={                   # 定义控制台脚本入口（可选）
        "console_scripts": [
            "yunwu-gpt-service=yunwu_gpt_service.__main__:main"
        ]
    }
)
