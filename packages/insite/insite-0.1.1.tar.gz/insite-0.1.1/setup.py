from setuptools import setup, find_packages
import os

# Read the contents of the README file
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

# Get version from module
with open(os.path.join('insite', '__init__.py'), encoding='utf-8') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.split('=')[1].strip().strip('"\'')
            break

setup(
    name="insite",
    version=version,
    description="A lightning fast tool for crawling websites and compiling PDFs of their pages",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Rose Bloom Research Co",
    author_email="rosebloomresearch@gmail.com",
    url="https://github.com/heleusbrands/insite",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "Topic :: Documentation",
        "Topic :: Utilities",
    ],
    license="GPL-3.0-only",
    keywords="web crawler, pdf, documentation, scraper, research, insite, bloom research",
    python_requires=">=3.10",
    install_requires=[
        "playwright>=1.42.0",
        "pypdf>=5.4.0",
        "asyncio>=3.4.3",
    ],
    entry_points={
        'console_scripts': [
            'insite=insite.cli:main',
        ],
    },
) 