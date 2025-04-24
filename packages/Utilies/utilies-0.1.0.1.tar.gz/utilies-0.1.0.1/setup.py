from setuptools import setup, find_packages

setup(
    name="Utilies",  # Replace with your package name
    version="0.1.0.1",
    packages=find_packages(),  # Automatically find submodules
    install_requires=['numpy','pandas','selenium'],  # List dependencies here, e.g., ["numpy", "pandas"]
)
