from setuptools import setup, find_packages

setup(
    name="yyAutoAiframework",         # 包名（必须唯一，PyPI上不能重复）
    version="1.0.10",          # 版本号（每次更新需递增）
    author="zhangxianchao",
    author_email="342588666@qq.com",
    description="将各种模型的实现差异进行封装，以适配大多数的模型",
    # long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/zhangxcYouyou/ai_framework",  # 项目主页
    packages=find_packages(), # 自动发现包
    install_requires=[        # 依赖项（可选）
        "elasticsearch7>=7.17.12",
        "nltk>=3.9.1",
        "numpy>=2.2.4",
        "openai>=1.3.5",
        "pandas>=2.2.3",
        "pdfplumber>=0.11.6",
        "pydantic>=2.11.3",
        "python-dotenv>=1.1.0",
        "qianfan>=0.4.12.3",
        "requests>=2.32.3",
        "volcengine-python-sdk>=1.0.118",
        "chromadb>=0.7.6",  # 添加 chromadb 依赖
        "setuptools>=78.1.0"
    ],
    classifiers=[            # 分类标签（可选）
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",  # Python 版本要求
)