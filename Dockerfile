# Use a specific version of Go
FROM golang:1.24 AS go-builder

# Install necessary system packages
RUN apt-get update && \
    apt-get install -y \
    git \
    curl \
    wget \
    gnupg \
    unzip \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Install required Go tools
RUN go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest && \
    go install github.com/tomnomnom/waybackurls@latest && \
    go install github.com/projectdiscovery/dnsx/cmd/dnsx@latest && \
    go install github.com/projectdiscovery/alterx/cmd/alterx@latest && \
    go install github.com/projectdiscovery/shuffledns/cmd/shuffledns@latest && \
    go install github.com/projectdiscovery/httpx/cmd/httpx@latest

# Install massdns
RUN git clone https://github.com/blechschmidt/massdns.git && \
    cd massdns && make && \
    cp bin/massdns /usr/local/bin/

# Use a lightweight base image
FROM python:3.9-slim

# Install necessary system packages
RUN apt-get update && \
    apt-get install -y \
    libssl-dev \
    libffi-dev \
    chromium \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /moonveil

# Copy and install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy binaries from the previous stage to /usr/local/bin
COPY --from=go-builder /go/bin/* /usr/local/bin/
COPY --from=go-builder /usr/local/lib /usr/local/lib

# Copy massdns binary separately to retain it
COPY --from=go-builder /usr/local/bin/massdns /usr/local/bin/massdns

# Set an environment variable to point to the Chrome executable on your local machine
ENV CHROME_PATH=/usr/bin/chromium

# Command to run your application
CMD ["python", "run.py"]
