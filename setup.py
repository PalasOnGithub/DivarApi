from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '2.0.1'
DESCRIPTION = 'Unofficial api of Divar(Scrapping Divar)'
LONG_DESCRIPTION = 'A package that allows to get informations from Divar.ir'

# Setting up
setup(
    name="divar",
    version=VERSION,
    author="RealPalas",
    author_email="palasongithub@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    python_requires = '>=3.8',
    install_requires=['requests', 'aiohttp'],
    keywords=['python', 'divar', 'api', 'iran', 'web scraping', 'bot' , 'V1Z'],
    classifiers=[
        "Development Status :: 2 - Developed",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)