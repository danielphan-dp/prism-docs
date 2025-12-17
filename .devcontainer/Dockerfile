FROM ubuntu:24.04

ARG DEBIAN_FRONTEND=noninteractive

# System dependencies:
# - poppler-utils: required by pdf2image (pdftoppm/pdftocairo)
# - tesseract-ocr (+ eng): required by OCR features
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    git \
    nodejs \
    npm \
    sudo \
    python3 \
    python3-venv \
    python3-pip \
    poppler-utils \
    tesseract-ocr \
    tesseract-ocr-eng \
    libglib2.0-0 \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user for development (VS Code default)
RUN useradd -m -s /bin/bash vscode \
    && echo "vscode ALL=(ALL) NOPASSWD:ALL" >/etc/sudoers.d/vscode \
    && chmod 0440 /etc/sudoers.d/vscode

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR=/usr/local/bin sh

WORKDIR /workspaces/prism-docs
USER vscode
