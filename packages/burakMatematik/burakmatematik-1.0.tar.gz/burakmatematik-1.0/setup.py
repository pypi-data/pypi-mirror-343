
from setuptools import setup,find_packages

with open('README.md', 'r') as f:
    LONG_DESCRIPTION = f.read()

NAME = 'burakMatematik'
VERSION = '1.0'
DESCRIPTION = 'Bu kütüphane Ödev için hazirlanmiştir'
LONG_DESCRIPTION_CONTENT_TYPE = 'text/markdown'
# URL = 'https://github.com/OmerFI/PyProbs'
AUTHOR = 'Burak Kocak'
AUTHOR_EMAIL = 'burakkck42@gmail.com'
LICENSE = 'MIT'
KEYWORDS = 'burak, matematik'

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
    # url=URL,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=LICENSE,
    keywords=KEYWORDS,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    # py_modules=['brkMatematik'],
    package_dir={'' : 'src'},
    packages=find_packages("src")
)