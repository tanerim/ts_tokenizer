from setuptools import setup, find_packages

setup(
    name='ts_tokenizer',
    version='0.1.19',
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
    long_description=open('README.md').read(),
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
