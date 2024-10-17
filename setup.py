from setuptools import setup, find_packages

setup(
    name='ts_tokenizer',
    version='0.1.10',
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
    description='TS Tokenizer is a hybrid tokenizer designed for Turkish text.'
                ' It uses a hybrid (lexicon-based and rule-based) approach to split text into tokens.'
                ' The tokenizer leverages regular expressions to handle non-standard text elements like dates, percentages, URLs, and punctuation marks.'
                'Key Features:'
                ' Hybrid Approach: Uses a hybrid (lexicon-based and rule-based approach) for tokenization.'
                ' Handling of Special Tokens: Recognizes special tokens like mentions, hashtags, emails, URLs, numbers, smiley, emoticons, etc..'
                ' Highly Configurable: Provides multiple output formats to suit different NLP processing needs,'
                ' including plain tokens, tagged tokens, and token-tag pairs in list or line formats.',
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
