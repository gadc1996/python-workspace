FROM python:3.11-bullseye

ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd -g $USER_GID vscode \
    && useradd -m -s /bin/bash -u $USER_UID -g $USER_GID $USERNAME \
    && usermod --gid $USER_GID $USERNAME \
    && usermod --uid $USER_UID --gid $USER_GID $USERNAME \
    && chown -R $USER_UID:$USER_GID /home/$USERNAME \
    && chsh -s /bin/bash vscode

WORKDIR /var/app

COPY . /var/app

RUN chown -R vscode:vscode /var/app
RUN chmod -R 755 /var/app

USER vscode

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r /var/app/requirements.txt
