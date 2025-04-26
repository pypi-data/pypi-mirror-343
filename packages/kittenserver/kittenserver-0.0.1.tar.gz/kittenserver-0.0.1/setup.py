
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kittenserver",
    version="0.0.1",
    author="Inventocode",
    author_email="359148497@qq.com",
    description="让您扩展海龟函数的功能",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.bilibili.com/video/BV1GJ411x7h7/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires='>=3.6',
)