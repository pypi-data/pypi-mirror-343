
from setuptools import setup, find_packages

setup(
    name='gestao-imc',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'matplotlib',
        'datetime'
    ],
    author='Gonçalo Soares, Ruben Abreu, Flávio Santos, Jessica Gonçalves', 
    author_email='seu@email.com',
    description='Ferramenta para gestão de IMC com base em dados de pessoas.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/seu-usuario/gestao-imc',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)
