FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# System dependencies
RUN apt-get update && apt-get install -y curl git apt-transport-https ca-certificates p7zip-full && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Deno
RUN curl -fsSL https://deno.land/x/install/install.sh | sh
ENV DENO_INSTALL=/root/.deno
ENV PATH=$DENO_INSTALL/bin:$PATH

# Install Node.js + npm
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Verify installations
RUN deno --version && node --version && npm --version

# Create app directory
WORKDIR /app

# Python dependencies
RUN uv init .
RUN uv add pydantic-ai fastapi aiohttp

# Copy runtime entry point script
COPY runtime_entry.py .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Entry point
ENTRYPOINT ["python", "runtime_entry.py"]