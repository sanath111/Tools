#!/usr/bin/env python3

import subprocess
import os
import sys
import logging

# Determine log file path
SCRIPT_NAME = os.path.splitext(os.path.basename(sys.argv[0]))[0]
if os.access("/var/log", os.W_OK):
    LOGFILE = f"/var/log/{SCRIPT_NAME}.log"
else:
    LOGFILE = os.path.expanduser(f"~/.{SCRIPT_NAME}.log")

# Setup logging
logging.basicConfig(
    filename=LOGFILE,
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(SCRIPT_NAME)

def get_all_services():
    try:
        result = subprocess.run(
            ["supervisorctl", "status"],
            capture_output=True, text=True, check=True
        )
        lines = result.stdout.strip().splitlines()
        services = []
        for line in lines:
            parts = line.split()
            if parts:
                service_name = parts[0]
                service_status = parts[1]
                services.append((service_name, service_status))
        return services
    except subprocess.CalledProcessError as e:
        logger.error(f"Error retrieving service status: {e}")
        return []

def restart_service(service_name):
    logger.info(f"Restarting service: {service_name}")
    subprocess.run(
        ["supervisorctl", "restart", service_name],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

def main():
    services = get_all_services()
    for service_name, status in services:
        if status.upper() != "RUNNING":
            logger.warning(f"Service '{service_name}' is '{status}', restarting...")
            restart_service(service_name)
        else:
            logger.info(f"Service '{service_name}' is running normally.")

if __name__ == "__main__":
    main()
