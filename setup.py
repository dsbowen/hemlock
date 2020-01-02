import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hemlock-survey",
    version="0.0.6",
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
        'flask-download-btn',
        'flask-login==0.4.1',
        'flask-socketio==4.2.1',
        'flask-sqlalchemy==2.4.1',
        'flask-worker',
        'google-cloud-storage==1.23.0',
        'pandas==0.25.3',
        'pandas-profiling==2.3.0',
        'python-docx==0.8.10',
        'redis==3.3.11',
        'selenium==3.141.0',
        'sqlalchemy==1.3.12',
        'sqlalchemy-function',
        'sqlalchemy-modelid',
        'sqlalchemy-mutable',
        'sqlalchemy-mutablesoup',
        'sqlalchemy-nav',
        'sqlalchemy-orderingitem',
    ]
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)