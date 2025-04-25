import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fhermocunha2025-meu_primeiro_pacote", # <- SEU NOME DE USUÁRIO DO TESTPYPI! Nome deve ser ÚNICO no TestPyPI
    version="0.0.1",
    author="Seu Nome",
    author_email="seu_email@exemplo.com",
    description="Um pacote Python simples para demonstração",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fhermocunha2025/meu_primeiro_pacote", # <- URL do seu repositório (pode ser um link qualquer por enquanto)
    packages=setuptools.find_packages(), # Encontra automaticamente seus pacotes
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)