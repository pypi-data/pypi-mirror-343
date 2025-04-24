from setuptools import setup, find_packages

setup(
    name="my_package",                    # your package name
    version="0.1.0",                    # any version
    packages=find_packages(),          # automatically finds the package folder
    description="Say hello from Zhe!", # short description
    author="Gama",
    author_email="wumian1996@gmail.com",
    python_requires=">=3.7"
)

