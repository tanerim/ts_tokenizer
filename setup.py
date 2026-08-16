from pathlib import Path
import re

from setuptools import setup, find_packages


ROOT_DIR = Path(__file__).parent
INIT_FILE = ROOT_DIR / "ts_tokenizer" / "__init__.py"
README_FILE = ROOT_DIR / "README.md"


def read_version():
    match = re.search(r'^__version__ = ["\']([^"\']+)["\']', INIT_FILE.read_text(encoding="utf-8"), re.MULTILINE)
    if not match:
        raise RuntimeError("Version could not be determined from ts_tokenizer/__init__.py")
    return match.group(1)

setup(
    name='ts_tokenizer',
    version=read_version(),
    packages=find_packages(),
    include_package_data=True,
    package_data={
    'ts_tokenizer': ['data/*.txt'],
    },
    install_requires=[
        'tqdm~=4.66.4'
    ],
    entry_points={
        'console_scripts': [
            'ts-tokenizer=ts_tokenizer.cli:main',
        ],
    },
    author='Taner Sezer',
    author_email='tanersezerr@gmail.com',
    description='TS Tokenizer is a hybrid (lexicon-based and rule-based) tokenizer designed specifically for tokenizing Turkish texts.',
    long_description=README_FILE.read_text(encoding="utf-8"),
    long_description_content_type='text/markdown',
    url='https://github.com/tanerim/ts_tokenizer',
    project_urls={
        'Bug Tracker': 'https://github.com/tanerim/ts_tokenizer/issues',
        'Documentation': 'https://github.com/tanerim/ts_tokenizer#readme',
        'Source Code': 'https://github.com/tanerim/ts_tokenizer',
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'License :: OSI Approved :: MIT License',
        "Natural Language :: Turkish",
        "Topic :: Text Processing :: Linguistic",
        'Operating System :: OS Independent',
    ],
    keywords=['turkish tokenizer', 'tokenizer', 'turkish', 'nlp', 'text-processing', 'language-processing'],
    license='MIT',
    python_requires='>=3.9',
    repository='https://github.com/tanerim/ts_tokenizer'
)
