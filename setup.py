from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.3'
DESCRIPTION = 'Unofficial api of Divar - by Reverse Engineering'
LONG_DESCRIPTION = 'A package that allows to get informations from Divar.ir'

# Setting up
setup(
    name="DivarApi",
    version=VERSION,
    author="RealPalas",
    author_email="palasongithub@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    python_requires = '>=3.9',
    install_requires=['requests', 'beautifulsoup4', 'jwt'],
    keywords=['python', 'divar', 'api', 'iran', 'web scraping', 'bot' , 'palas'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
