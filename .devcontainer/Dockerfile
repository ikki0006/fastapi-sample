ARG PYTHON_VERSION=3.13.0-bookworm
FROM python:${PYTHON_VERSION}

ARG USERNAME=vscode
ARG USER_UID=1001
ARG USER_GID=$USER_UID

# ARG AWS_CLI_VERSION for checking the latest version
# https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-linux.html
ARG AWS_CLI_VERSION=2.19.1

# change WORKDIR to /workspace
ARG WORKSPACE=/fastapi-sample
WORKDIR ${WORKSPACE}

# change default shell to bash
SHELL ["/bin/bash", "-o" , "pipefail", "-c"]
RUN chsh -s /bin/bash

# increase timeout for apt-get to 5 minutes
RUN echo "Acquire::http::Timeout \"300\";" > /etc/apt/apt.conf.d/99timeout
RUN echo "Acquire::ftp::Timeout \"300\";" >> /etc/apt/apt.conf.d/99timeout

# install necessary packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    less \
    curl \
    wget \
    unzip \
    jq \
    vim \
    sudo \
    git \
    gnupg \
    pip \
    lsb-release \
    openssh-client \
    pre-commit \
    && apt-get clean

# install aws-cli
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64-${AWS_CLI_VERSION}.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install \
    && rm -rf awscliv2.zip aws

# Create a non-root user to use if preferred - see https://aka.ms/vscode-remote/containers/non-root-user.
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

USER $USERNAME

# install rye
RUN curl -sSf https://rye.astral.sh/get | RYE_INSTALL_OPTION="--yes" bash && \
    source "$HOME/.rye/env" \
    rye config --set-bool behavior.global-python=true

# to show Japanese git log
ENV LESSCHARSET=utf-8
