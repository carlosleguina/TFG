# Use an official Python runtime as a parent image
FROM ubuntu:latest

# Set the working directory in the container
WORKDIR /usr/app/src

ARG LANG= 'en_us.UTF-8'

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        apt-utils \
        locales \
        python3-pip \
        python3-venv \
        python3-yaml \
        rsyslog systemd systemd-cron sudo \
        xvfb \
        x11-xserver-utils \
        x11-apps \
    && apt-get clean

# Create a virtual environment and install dependencies
RUN python3 -m venv venv
# Activate the virtual environment and upgrade pip
RUN . venv/bin/activate && pip install --upgrade pip

RUN git clone https://github.com/carlosleguina/TFG.git .

RUN . venv/bin/activate && pip install -r requirements.txt



# Set the default command to run the app using Streamlit and Xvfb
CMD ["/usr/app/src/venv/bin/streamlit", "run", "main.py"]