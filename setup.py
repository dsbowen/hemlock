import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hemlock-survey",
    version="0.0.5",
    author="Dillon Bowen",
    author_email="dsbowen@wharton.upenn.edu",
    description="A package for creating and deploying surveys",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dsbowen/hemlock",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)