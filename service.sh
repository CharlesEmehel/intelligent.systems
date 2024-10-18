#!/bin/bash

# Set the directory for local Python libraries
LOCAL_PYTHON_LIBS="./local-python-libs"
CERT_FILE="server.crt.pem"
KEY_FILE="server.key.pem"

# Function to install system build dependencies
install_system_dependencies() {
    echo "Installing system build dependencies for andromeda, please wait!..."
    sudo apt-get update
    sudo apt-get install -y inotify-tools build-essential cython3 openssl libyaml-dev nano

    if [ $? -ne 0 ]; then
        echo "Failed to install andromeda build system dependencies."
        exit 1
    fi

    echo "Cleaning up APT cache..."
    sudo apt-get clean

    if [ $? -ne 0 ]; then
        echo "Failed to clean APT cache."
        exit 1
    fi
}

# Function to upgrade pip, setuptools, and wheel, and install a specific version of cython
upgrade_python_tools() {
    echo "Upgrading pip, setuptools, and wheel..."
    pip install --upgrade pip setuptools==58.0.4 wheel

    if [ $? -ne 0 ]; then
        echo "Failed to upgrade pip, setuptools, and wheel."
        exit 1
    fi

    echo "Installing specific version of cython..."
    pip install --upgrade --ignore-installed cython==0.29.24

    if [ $? -ne 0 ]; then
        echo "Failed to install cython."
        exit 1
    fi
}

# Function to install andromeda Python run dependencies
install_dependencies() {
    echo "Checking if Python dependencies are already installed..."
    if [ ! -d "$LOCAL_PYTHON_LIBS" ] || [ -z "$(ls -A $LOCAL_PYTHON_LIBS)" ]; then
        echo "Creating directory for local Python libraries..."
        mkdir -p $LOCAL_PYTHON_LIBS
        
        echo "Installing Python dependencies into $LOCAL_PYTHON_LIBS..."
        pip install -r requirements.txt -t $LOCAL_PYTHON_LIBS

        if [ $? -ne 0 ]; then
            echo "Failed to install Python dependencies."
            exit 1
        fi
    else
        echo "Python dependencies are already installed."
    fi
}

# Function to generate SSL key and certificate
generate_ssl_certificates() {
    if [ ! -f "$KEY_FILE" ] || [ ! -f "$CERT_FILE" ]; then
        echo "Generating SSL key and certificate..."
        openssl req -newkey rsa:2048 -nodes -keyout $KEY_FILE -x509 -days 3650 -out $CERT_FILE -subj "/CN=localhost"

        if [ $? -ne 0 ]; then
            echo "Failed to generate SSL key and certificate."
            exit 1
        fi

        echo "Setting permissions on the key file..."
        chmod 755 $KEY_FILE

        if [ $? -ne 0 ]; then
            echo "Failed to set permissions on the key file."
            exit 1
        fi
    else
        echo "SSL key and certificate already exist."
    fi
}

# Function to rebuild and restart the Docker containers
rebuild_and_restart() {
    echo "Building and running Docker containers, please wait..."
    docker-compose up --build -d

    if [ $? -ne 0 ]; then
        echo "Failed to build and run Docker containers."
        exit 1
    fi

    echo "Docker containers for andromeda are running."
}

# Install system dependencies
install_system_dependencies

# Upgrade pip, setuptools, and wheel, and install specific version of cython
upgrade_python_tools

# Install dependencies only if not already present
install_dependencies

# Generate SSL certificates if not present
generate_ssl_certificates

# Initial build and run
rebuild_and_restart

# Watch for changes in the local-python-libs directory and update the Docker container
while true; do
    inotifywait -e modify,create,delete -r $LOCAL_PYTHON_LIBS
    echo "Changes detected in local dependencies. Rebuilding Docker containers, please wait..."
    rebuild_and_restart
done
