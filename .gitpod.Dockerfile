FROM gitpod/workspace-full:latest

ENV PYTHON_VERSION=3.9.7
RUN pyenv install $PYTHON_VERSION \
    && pyenv global $PYTHON_VERSION \
    && python3 -m pip install --upgrade pip