from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    LONG_DESCRIPTION = f.read()

NAME = 'pypoai'
VERSION = '1.0'
DESCRIPTION = 'poai: A comprehensive tool for Gettext PO (.po) translation files. It automates translations using artificial intelligence and provides seamless bidirectional conversion between PO and JSON formats.'
LONG_DESCRIPTION_CONTENT_TYPE = 'text/markdown'

URL = 'https://github.com/hasancagrigungor/poai'
AUTHOR = 'Hasan Çağrı Güngör'
AUTHOR_EMAIL = 'iletisim@cagrigungor.com'
LICENSE = 'MIT'
KEYWORDS = '.po translate, po to json, json to po'

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
    url=URL,
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
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
    ],
    py_modules=["pypoai"],
  
)