FROM python:3.11-slim-bullseye

# Set the working directory to /app
WORKDIR /app

# Install apt-get workspace packages
RUN apt-get update && \
    apt-get install -y \
    git \
    sudo \
    wget \
    zsh

# Create user with permissions in folder /app
ARG USERNAME=devcontainer
RUN useradd -ms /bin/bash $USERNAME && \
    chown -R $USERNAME:$USERNAME /app

# add user to sudoers
RUN echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Set zsh as default shell for user
RUN chsh -s $(which zsh) $USERNAME
    
# Update pip and install requirements
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Add pip to path
ENV PATH="/home/$USERNAME/.local/bin:${PATH}"

# Copy rest of files
COPY . .

USER $USERNAME