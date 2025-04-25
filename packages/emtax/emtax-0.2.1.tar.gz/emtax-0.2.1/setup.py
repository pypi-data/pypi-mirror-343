from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="emtax",
    version="0.2.1",
    author="Dhruvil Chodvadiya",
    author_email="your.email@example.com",  # Update with your actual email
    description="EM-TAX: Bioinformatics workflow management tool for taxonomic profiling on HPC systems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dhruvac29/emtax",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "emtax": [
            "templates/*.sh",
            "templates/*.py",
            "templates/*.yaml",
            "templates/*.smk",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    python_requires=">=3.9",
    install_requires=[
        "paramiko>=2.7.2",
        "click>=7.1.2",
        "pyyaml>=5.4.1",
        "tqdm>=4.61.0",
        "pandas>=1.3.0",
    ],
    entry_points={
        "console_scripts": [
            "emtax=emtax.cli:main",
        ],
    },
)
