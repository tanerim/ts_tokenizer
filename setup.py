from setuptools import setup, find_packages

setup(
    name='ts_tokenizer',
    version='0.1.0',
    packages=find_packages(),
    package_data={
    'my_package': ['data/*.txt'],
    },
    install_requires=[
        # Add any dependencies here
    ],
    entry_points={
        'console_scripts': [
            # Add command line scripts here
        ],
    },
    author='Taner Sezer',
    author_email='tanersezerr@gmail.com',
    description='An old fashioned rule-based tokenizer for Turkish',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/tanerim/ts_tokenizer',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)