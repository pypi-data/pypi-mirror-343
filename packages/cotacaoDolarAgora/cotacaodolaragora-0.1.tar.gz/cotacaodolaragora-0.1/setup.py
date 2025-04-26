from setuptools import setup, find_packages

with open('README.md') as f:
    descricao_pagina = f.read()
    
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="cotacaoDolarAgora",
    version="0.1",
    author="Ricardo Conrado",
    author_email="riconrado1976@hotmail.com",
    description="Busca a cotação do dólar em tempo real utilizando a API da AwesomeAPI",
    long_description=descricao_pagina,
    long_description_content_type="text/markdown",
    url="https://github.com/riconrado/cotacaoDiaria",
    packages=find_packages(),
    python_requires='>=3',
    install_requires=requirements
)