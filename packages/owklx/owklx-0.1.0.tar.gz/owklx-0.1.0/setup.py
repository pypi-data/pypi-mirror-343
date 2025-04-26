from setuptools import setup, find_packages

setup(
    name="owklx",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="owklx",
    author_email="cpascontent@proton.me",
    description="le meilleur module de 2025 pour discord (bypass api, nouvelle bibliothèque...)",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/owklx",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)
