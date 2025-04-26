from setuptools import setup, find_packages

setup(
    name="omni-assistant-sdk",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["requests"],
    author="https://www.omnidim.io/",
    author_email="shounak@omnidim.io",
    description="Minimal SDK for Omni Assistant services",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kevin-omnidim/omnidim-sdk",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)