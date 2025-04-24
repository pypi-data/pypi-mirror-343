FROM python:3.12-slim AS builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml README.md ./
COPY src/ ./src/

# Install the project in development mode
RUN pip install --no-cache-dir .

# Final stage
FROM python:3.12-slim

WORKDIR /app

# Install only required system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends && \
    rm -rf /var/lib/apt/lists/* && \
    # Create non-root user
    groupadd --system mcp && \
    useradd --system --create-home --home-dir /home/mcp --gid mcp mcp

# Copy the installed package from the builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin/mcp-metricool /usr/local/bin/mcp-metricool

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV TZ=Etc/UTC

# Switch to non-privileged user
USER mcp

# Run the server
CMD ["python", "-m", "mcp_metricool"]