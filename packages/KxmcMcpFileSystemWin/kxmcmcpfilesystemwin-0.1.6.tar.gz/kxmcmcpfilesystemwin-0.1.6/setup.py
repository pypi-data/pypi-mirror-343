from setuptools import setup, find_packages

setup(
    name='KxmcMcpFileSystemWin',
    version='0.1.6',
    packages=find_packages(),
    url='',
    license='',
    author='kxmc',
    author_email='rekxmc@163.com',
    description='本地文件和目录操作',
    entry_points={"console_scripts": ["KxmcMcpFileSystemWin=kxmc_mcp_server_file_system_win.main:main"]},
)
