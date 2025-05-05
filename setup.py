from setuptools import setup, find_packages
import os

# Get the long description from the README file
with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="low_level_pipa",
    version="0.1.0",
    description="Low-level Python interface for PAPI (Performance Application Programming Interface)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="PIPA Team",
    author_email="pipa@example.com",
    url="https://github.com/your-organization/low_level_pipa",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Hardware",
        "Topic :: System :: Monitoring",
    ],
    python_requires=">=3.6",
    install_requires=[
        "cffi>=1.0.0",
    ],
    setup_requires=["cffi>=1.0.0"],
    cffi_modules=["low_level_pipa/papi_build.py:ffibuilder"],
)
