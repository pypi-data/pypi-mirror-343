from setuptools import setup, find_packages

setup(
    name='gestao-automovel',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        #dependências 
    ],
    author='João Braga, Diogo Fernandes, Gonçalo Condesso, Víctor Ramos',
    author_email='goncalocondesso2003@gmail.com',
    description='Projeto Gestão Automóvel',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Condesso15/Gestao_Automovel',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
