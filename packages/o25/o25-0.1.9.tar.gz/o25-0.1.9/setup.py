from setuptools import setup, find_packages

setup(
    name="o25",
    version="0.1.8",
    author="Jaime Pitarch",
    author_email="jaime.pitarch@cnr.it",
    description="Bidirectional correction and IOP retrieval for aquatic optics",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jaipipor/O25",
    packages=find_packages(),
    package_dir={"": "."},     # Look in root directory
    install_requires=[
        "numpy",
        "scipy"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
