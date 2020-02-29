import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hemlock-survey",
    version="0.0.12",
    author="Dillon Bowen",
    author_email="dsbowen@wharton.upenn.edu",
    description="A package for creating and deploying surveys",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dsbowen/hemlock",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        'bs4==0.0.1',
        'eventlet==0.25.1',
        'flask==1.1.1',
        'flask-apscheduler==1.11.0',
        'flask-bootstrap4==4.0.2',
        'flask-download-btn==0.0.18',
        'flask-login==0.4.1',
        'flask-socketio==4.2.1',
        'flask-sqlalchemy==2.4.1',
        'flask-worker==0.0.7',
        'google-cloud-storage==1.23.0',
        'pandas==1.0.1',
        'pandas-profiling==2.3.0',
        'python-docx==0.8.10',
        'redis==3.3.11',
        'rq==1.2.0',
        'selenium==3.141.0',
        'sqlalchemy==1.3.12',
        'sqlalchemy-function==0.0.5',
        'sqlalchemy-modelid==0.0.2',
        'sqlalchemy-mutable==0.0.7',
        'sqlalchemy-mutablesoup==0.0.6',
        'sqlalchemy-nav==0.0.4',
        'sqlalchemy-orderingitem==0.0.3',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)