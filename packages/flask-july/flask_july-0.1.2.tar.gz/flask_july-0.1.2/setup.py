from setuptools import setup, find_packages

setup(
    name="flask_july",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "flask"
    ],
    description="Minimalist Flask Addon for slapping bots using Proof-of-Work",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/ten-faced-carrot/flask-july",
    author="June",
    author_email="june@junimond161.de",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
