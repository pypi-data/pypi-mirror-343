from setuptools import setup, find_packages
import os

# 读取requirements.txt中的依赖项
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

# 确保关键依赖项版本正确
pydantic_installed = False
for i, req in enumerate(requirements):
    if req.startswith('pydantic'):
        pydantic_installed = True
        # 确保使用兼容版本
        if '==' in req:
            version = req.split('==')[1]
            if version.startswith('1.'):
                # 如果是1.x版本，确保代码与1.x兼容
                requirements[i] = 'pydantic>=1.9.0,<2.0.0'
            else:
                # 如果是2.x版本，确保代码与2.x兼容
                requirements[i] = 'pydantic>=2.0.0'
        else:
            # 如果没有指定版本，添加兼容版本
            requirements[i] = 'pydantic>=1.9.0'

if not pydantic_installed:
    # 如果没有pydantic依赖，添加一个
    requirements.append('pydantic>=1.9.0')

# 读取README.md作为长描述
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="orion_browser",
    version="0.1.4",
    author="BTY Team",
    author_email="qianhai@bantouyan.com",
    description="浏览器代理服务器",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bantouyan/orion",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'orion-server=app:start_server',
        ],
    },
) 