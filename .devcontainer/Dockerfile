# Extends Microsoft dev container for Python and installs Tkinter
FROM mcr.microsoft.com/devcontainers/python:0-3.11

# Install system dependency for Tkinter (Debian/Ubuntu)
RUN apt-get update \
    && apt-get install -y python3-tk \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
