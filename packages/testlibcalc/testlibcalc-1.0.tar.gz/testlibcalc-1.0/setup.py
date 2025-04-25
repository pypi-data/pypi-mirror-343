# setup.py

from setuptools import setup

setup(
    name="testlibcalc",   # Nome do projeto
    version="v1.0", # Versão do projeto
    description="Uma biblioteca de exemplo simples para ensino", # Descrição do projeto
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="math", # Nome do autor
    author_email="adrillima455@gmail.com",   # Endereço de Email
    url="https://github.com/adrillima/testlibcalc",   # Endereço Git do desenvolvedor
    packages=['testlibcalc'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        'Natural Language :: Portuguese (Brazilian)',
    ],
    python_requires=">=3.6",    # Limita à versão que o python vai trabalhar(só as versões anteriores que não pegam)!
)