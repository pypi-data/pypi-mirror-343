from setuptools import setup, find_packages

"""
uv run setup.py sdist bdist_wheel
uv run twine upload dist/*  

MCP测试：npx @modelcontextprotocol/inspector uvx KxmcMcpFileSystemWin


setup.py参考：https://github.com/cs01/pycowsay
"""
setup(
    name='KxmcMcpFileSystemWin',
    version='0.1.7',
    packages=find_packages(),
    url='',
    license='',
    author='kxmc',
    author_email='rekxmc@163.com',
    description='本地文件和目录操作',
    entry_points={"console_scripts": ["KxmcMcpFileSystemWin=kmsfsw.main:main"]},
)
