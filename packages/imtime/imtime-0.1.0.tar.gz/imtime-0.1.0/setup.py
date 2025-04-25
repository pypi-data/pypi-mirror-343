from setuptools import setup, find_packages

setup(
    name="imtime",
    version="0.1.0",
    author="imaitian",
    author_email="2018500@qq.com",
    description="一个简单的时间格式化工具",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)