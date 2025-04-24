# setup.py

from setuptools import setup, find_packages

setup(
    name="jonoer",  # Название пакета
    version="0.2.0",  # Версия пакета
    description="Мемный набор модулей с гимнами, странными и абсурдными эффектами",
    author="Андрей",
    author_email="danya10121985@gmail.com",
    packages=find_packages(),
    install_requires=[
        "sounddevice",  # Зависимость для звуковых эффектов
        "numpy",  # Для работы с синусоидами и массивами
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
