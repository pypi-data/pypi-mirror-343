# setup.py
import pathlib
from setuptools import setup, find_packages

# The directory containing this file
here = pathlib.Path(__file__).parent.resolve()

# Read the long description from README.md
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="qiskit-connector",
    version="0.7.9",
    author="Dr. Jeffrey Chijioke-Uche",
    author_email="sj@chijioke-uche.com",
    description="IBM Quantum Qiskit Connector For Backend RuntimeService",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/schijioke-uche/qiskit-connector",
    project_urls={
        "Homepage": "https://github.com/schijioke-uche/qiskit-connector",
        "Source":   "https://github.com/schijioke-uche/qiskit-connector",
        "Tracker":  "https://github.com/schijioke-uche/qiskit-connector/issues",
    },
    classifiers=[
        "Development Status :: 6 - Mature",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Quantum Computing",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(include=["qiskit_connector", "qiskit_connector.*"]),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.32.3",
        "python-dotenv>=1.1.0",
        "qiskit-ibm-runtime>=0.38.0",
        "qiskit>=2.0.0",
    ],
    license="MIT-License",
    license_files=("LICENSE",),
)
