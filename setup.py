import os
from setuptools import find_packages, setup


with open(os.path.join(os.path.dirname(__file__), "README.md")) as readme:
    README = readme.read()

# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    author="Zagaran, Inc.",
    author_email="info@zagaran.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    description="An expanded version of Django's FormViews to handle multiple forms with separate submission",
    install_requires=["django"],
    license="MIT",
    long_description=README,
    long_description_content_type="text/markdown",
    name="django-multiform-views",
    packages=find_packages(),
    url="https://github.com/zagaran/django-multiform-views",
    version="0.1.0a7",
)
