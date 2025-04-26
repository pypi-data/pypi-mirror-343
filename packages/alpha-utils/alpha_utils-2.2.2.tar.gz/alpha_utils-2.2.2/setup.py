from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [
    Extension(
        "alpha_utils.function",
        ["alpha_utils/function.py"]
    )
]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='alpha_utils',
    version="2.2.2",
    ext_modules=cythonize(extensions),
    packages=["alpha_utils"],

    author="ZENGBAOCHENG",
    author_email="3180102361@zju.edu.cn",
    description="alpha utils",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zengbaocheng-996/alpha_utils",  # 项目的URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # 指定支持的Python版本
)