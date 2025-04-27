from setuptools import setup, find_packages

setup(
    name='zqykjclient',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        # 列出你的包依赖的其他包
        'requests>=2.0.0'
    ],
    python_requires='>=3.6',
    # 其他元数据
    author='cxx',
    author_email='cuixiaoxiao@zqykj.com',
    description='lbsys',
    long_description=open('README.md',encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/mypackage',
)
