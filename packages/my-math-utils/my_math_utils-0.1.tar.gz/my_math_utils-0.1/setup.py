from setuptools import setup, find_packages

setup(
    name="my_math_utils",
    version="0.1",
    # 自动查找所有包（包含 __init__.py 的目录）
    packages=find_packages(),
    # 或手动指定包（如果自动查找失败）
    # packages=["tx_math"],
    # 包含非代码文件（如数据文件）
    include_package_data=True,
    # 其他元数据（作者、依赖等）
    author="John Goo",
    # install_requires=[
    #     "numpy>=1.0",
    # ],
)