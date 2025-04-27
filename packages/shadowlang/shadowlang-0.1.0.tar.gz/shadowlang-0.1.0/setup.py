from setuptools import setup, find_packages

setup(
    name="shadowlang",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "shadow=shadowlang.runner:main",
        ],
    },
    author="Aditya Jain",
    author_email="adityaj0714@gmail.com",
    description="ShadowLang: A simple programming language",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
