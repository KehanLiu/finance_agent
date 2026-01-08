# Dev container that matches Railway production environment
# Based on Python 3.11 slim (same as production)
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Required for production
    curl \
    # Development tools
    git \
    wget \
    vim \
    nano \
    sudo \
    # Node.js for frontend development
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    # Cleanup
    && rm -rf /var/lib/apt/lists/*

# Install UV for fast Python package management (same as local dev)
RUN pip install --no-cache-dir uv

# Create non-root user (matches production user setup)
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Switch to non-root user
USER $USERNAME

# Set working directory
WORKDIR /workspace

# Install Python tools in user space
RUN pip install --user --no-cache-dir \
    black \
    pylint \
    pytest

# Set Python path
ENV PATH="/home/${USERNAME}/.local/bin:${PATH}"

# Default command
CMD ["bash"]
