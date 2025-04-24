import os
from setuptools import setup, find_packages

# Читаем содержимое README.md для использования в long_description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Читаем зависимости из requirements.txt
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh.readlines()]

setup(
    name="vk-parser",
    version="0.1.0",
    author="Efimovich Evgenii",
    author_email="neon.1598@mail.ru",
    description="Модульный парсер данных пользователей из социальной сети ВКонтакте",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/johnneon/vk-parser",
    packages=find_packages(include=["vk_parser", "vk_parser.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    package_data={
        "vk_parser": ["config.ini.example"],
    },
    entry_points={
        "console_scripts": [
            "vk-parser=vk_parser.main:cli_main",
        ],
    },
    include_package_data=True,
) 