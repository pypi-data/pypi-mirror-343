'''
Created on Sun Jul 21 09:54:07 2024

@authors:
    Antonio Pires
    Milton Ávila
    Wesley Oliveira

@License:
Este projeto está licenciado sob a Licença Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0). Você pode compartilhar, adaptar e construir sobre o material, desde que atribua crédito apropriado, não use o material para fins comerciais e distribua suas contribuições sob a mesma licença.
Para mais informações, consulte o arquivo [LICENSE](./LICENSE).
'''
from setuptools import setup, find_packages

with open('pdf_sanitizer_diacde/README.md', 'r', encoding='utf-8') as f:
    description = f.read()

setup(
    name='pdf_sanitizer_diacde',
    version='1.3.3',
    author='DIACDE - TJGO',
    python_requires=">=3.9.4",
    requirements=[
        'io',
        'PIL',
        'math',
        'base64',
        'pymupdf',
    ],
    license='Attribution-NonCommercial-ShareAlike',
    packages=find_packages(),
    long_description=description,
    long_description_content_type='text/markdown',
)