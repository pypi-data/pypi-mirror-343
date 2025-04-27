from setuptools import setup, find_packages

setup(
    name="TuModeloDeClientes_Navarro",  
    version="4.0.0",  # Versión
    packages=find_packages(),  # Encuentra todas las carpetas de código
    entry_points={
        "console_scripts": [
            "TuModeloDeClientes_Navarro = TuModeloDeClientes_Navarro.main:main",
        ],
    },
    include_package_data=True,
    description="Modelo de clientes para practicar Herencia, modulos y polimorfismo en Python",
    author="Juan Navarro",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
)
