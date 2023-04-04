from setuptools import setup, find_packages

setup(
    name='dzmicro',
    version='2.0.1',
    packages=find_packages(),
    author='dzming',
    author_email='dzm_work@163.com',
    description='用于微服务架构快速开发的微服务引擎',
    install_requires=[
        'Flask',
        'numpy',
        'PyYAML',
        'python-consul',
        'ruamel.yaml',
        'watchdog',
        'pika'
    ],
    license='MIT',
    keywords='DzMicro, python',
    url='https://github.com/dzming-git/DzMicro',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
