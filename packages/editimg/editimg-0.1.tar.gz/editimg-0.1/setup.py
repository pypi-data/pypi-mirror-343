from setuptools import setup, find_packages

setup(
    name="editimg",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    author="Gustavo",
    author_email="gustavo.wbu@gmail.com",
    description="A collection of simple and easy to use image editing tools.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/gustavowbu/editimg",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
