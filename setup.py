from setuptools import setup, find_packages

setup(
    name='ts_tokenizer',
    version='0.1.3',
    packages=find_packages(),
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
    description='TS Tokenizer is a rule-based tokenizer'
                'specifically designed for processing Turkish text.'
                'It provides functionalities to split text into tokens'
                'following the grammatical and linguistic rules of the Turkish language.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/tanerim/ts_tokenizer',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
    repository='https://github.com/tanerim/ts_tokenizer'
)
