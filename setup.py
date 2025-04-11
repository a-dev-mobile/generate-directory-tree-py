from setuptools import setup, find_packages

setup(
    name="dirstructure",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "prettytable>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "dirstructure=dirstructure.main:main",
        ],
    },
    python_requires=">=3.6",
    author="Dmitriy",
    author_email="wayofdt@gmail.com",
    description="Directory structure analysis tool",
    keywords="directory, structure, analysis",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)