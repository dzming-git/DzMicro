from setuptools import setup, find_packages

setup(
    name='dzmicro',
    version='2.0.0',
    packages=find_packages(),
    author='dzming',
    author_email='dzming_work@163.com',
    description='用于微服务架构DBot服务程序快速开发的SDK',
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
    keywords='DBot, python',
    url='https://github.com/dzming-git/DzMicro',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
