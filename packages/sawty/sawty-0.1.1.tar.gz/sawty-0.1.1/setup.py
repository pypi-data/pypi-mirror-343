from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="sawty",
    version="0.1.1",  # <- bump your version number!
    author="NYUAD 2025 Team 6 SAWTY",
    description="Quantum-Secure Voting System",
    long_description=long_description,
    long_description_content_type="text/markdown",  # <- must be markdown
    url="https://github.com/AdrianHarkness/NYUAD2025",
    packages=find_packages(),
    install_requires=[
        "qiskit",
        "cryptography"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # or your license
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)