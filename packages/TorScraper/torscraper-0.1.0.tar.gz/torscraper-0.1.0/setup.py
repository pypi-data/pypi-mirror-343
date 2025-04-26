from setuptools import setup

setup(
    name='TorScraper',
    version='0.1.0',
    description='Your dark web scraper using Tor',
    author='DeadmanXXXII',
    author_email='themadhattersplayground@gmail.com',
    packages=['TorScrape'],
    install_requires=[
        'selenium'
    ],
    entry_points={
        'console_scripts': [
            'ls6=TorScrape.torscrape:main'
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
