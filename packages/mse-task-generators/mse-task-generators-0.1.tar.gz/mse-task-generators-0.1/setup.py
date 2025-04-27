from setuptools import setup, find_packages

with open("README.md","r",encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mse-task-generators",  # название пакета
    version="0.1",  # версия
    packages=find_packages(),  # автоматически находит все пакеты в проекте
    include_package_data=True,
    install_requires=[  # зависимости, если есть
        'cfile>=0.4.0',
        'wonderwords>=2.2.0'
    ],
    entry_points={  # для командной строки
        'console_scripts': [
            'generators-leak-generator = generators.leak_generator.__main__:main',
            'generators-profiling1 = generators.profiling1.__main__:main',
            'generators-cycle-generator = generators.cycle_generator.__main__:main',
        ],
    },
    description='Набор генераторов программ для работы с отладчиками языка С',
    long_description=long_description,
    long_description_content_type="text/markdown"
)