from setuptools import setup, find_packages

setup(
    name='DBot_SDK',
    version='1.2',
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
        'watchdog'
    ],
    license='MIT',
    keywords='DBot, python',
    url='https://github.com/dzming-git/DBot_SDK',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
