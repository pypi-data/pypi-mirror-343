from setuptools import setup, find_packages

setup(
    name='pingpoint',  # New package name
    version='1.0.0',  # Start fresh as version 1.0.0 under new name
    description='A fast CLI tool for HTTP, DNS, and SSL diagnostics',
    author='Zack Adams',
    author_email='imZackAdams@protonmail.com',
    url='https://github.com/ImZackAdams/pingpoint',
    packages=find_packages(),
    install_requires=[
        'click',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'pingpoint=pingpoint.cli:cli',
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: System :: Networking :: Monitoring",
    ],
    python_requires='>=3.6',
)
