from setuptools import setup, find_packages

setup(
    name="tuminski_hash",
    version="1.0.0",
    description="Sistema de hash irreversível personalizado e seguro",
    author="Vilmar Tuminski",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
