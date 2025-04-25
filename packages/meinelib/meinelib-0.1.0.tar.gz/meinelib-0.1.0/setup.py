from setuptools import setup, find_packages

setup(
    name="meinelib",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # Dependencias aquí, por ejemplo:
        # "requests>=2.25.1",
    ],
    author="Javier",
    author_email="deese2k@gmail.com",
    description="A set of functions that I use regularlly.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/deese/meinelib",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)", 
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
