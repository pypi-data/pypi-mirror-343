# Importations des modules

from setuptools import setup, find_packages

# Définition du setup

setup(
    name = "secugenpy",
    version = "1.0.1",
    author = "MAZIKOU Franck Souverain",
    author_email = "franckmazikous@gmail.com",
    description = "Secugenpy est un module Python conçu pour la capture et la comparaison d'empreintes digitales à l'aide des lecteurs biométriques SecuGen.",
    long_description = open("README.md", encoding = "utf-8").read(),
    long_description_content_type = "text/markdown",
    packages = find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires = '>=3.10',
    install_requires = [
        "Pillow>=9.0.0"
    ],
)
