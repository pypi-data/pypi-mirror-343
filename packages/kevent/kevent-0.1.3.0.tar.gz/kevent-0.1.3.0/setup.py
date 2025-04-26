from setuptools import setup, find_packages

setup(
    author="kokaito-git",
    name="kevent",
    version="0.1.3.0",
    description="KEvent",
    author_email="kokaito.git@gmail.com",
    url="https://github.com/kokaito-git/kevent",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=[
        "klocker",
        "kmodels",
        "typeguard",
    ],
    packages=find_packages(),
    python_requires=">=3.13",
    include_package_data=True,
)
