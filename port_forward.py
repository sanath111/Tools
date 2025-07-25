#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import sys
import os
import re
import logging

UPNPC = "/usr/bin/upnpc"
SCRIPT_NAME = os.path.splitext(os.path.basename(sys.argv[0]))[0]
if os.access("/var/log", os.W_OK):
    LOGFILE = f"/var/log/{SCRIPT_NAME}.log"
else:
    LOGFILE = os.path.expanduser(f"~/.{SCRIPT_NAME}.log")

logging.basicConfig(
    filename=LOGFILE,
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(SCRIPT_NAME)

# Port mappings: (EXTPORT, IN_IP, INPORT, PROTO, DESCRIPTION)
MAPPINGS = [
    (9090, "192.168.1.175", 22, "TCP", "SSH access for remoteaccess"),
    (9091, "192.168.1.183", 3000, "TCP", "Grafana on rfidsteampunk"),
    (9092, "192.168.1.39", 22, "TCP", "SSH access for blue0030"),
    (9094, "192.168.1.174", 4501, "TCP", "MYSQL server on mysqlserver"),
    (9096, "192.168.1.195", 5222, "TCP", "Pidgin on xmpp"),
    (9098, "192.168.1.170", 5901, "TCP", "VNC on stor6"),
]

def get_existing_mappings():
    """
    Run 'upnpc -l' once and parse the output to a set of tuples:
    (protocol, external_port, internal_ip, internal_port)
    """
    try:
        result = subprocess.run(
            [UPNPC, "-l"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=True,
            text=True
        )
        mappings = set()
        for line in result.stdout.splitlines():
            # Match pattern: protocol external_port->internal_ip:internal_port
            match = re.search(r"(?i)\b(TCP|UDP)\b\s+(\d+)->([\d\.]+):(\d+)", line)
            if match:
                proto = match.group(1).upper()
                ext_port = int(match.group(2))
                in_ip = match.group(3)
                in_port = int(match.group(4))
                mappings.add((proto, ext_port, in_ip, in_port))
        return mappings
    except subprocess.CalledProcessError:
        logger.error("upnpc command failed or no IGD found")
        return set()

def add_mapping(extport, in_ip, inport, proto, desc):
    """Add a UPnP port mapping."""
    try:
        subprocess.run([UPNPC, "-e", desc, "-a", in_ip, str(inport), str(extport), proto], check=True)
        logger.info(f"Successfully mapped port {extport}")
    except subprocess.CalledProcessError:
        logger.error(f"ERROR mapping port {extport}")

def main():
    logger.info("UPnP forward start")

    existing = get_existing_mappings()
    if not existing:
        sys.exit(1)

    logger.info(existing)

    for extport, in_ip, inport, proto, desc in MAPPINGS:
        key = (proto.upper(), extport, in_ip, inport)
        if key in existing:
            logger.info(f"Mapping exists: {extport} -> {in_ip}:{inport} ({proto}) [{desc}]")
        else:
            logger.info(f"Creating mapping: {extport} -> {in_ip}:{inport} ({proto}) [{desc}]")
            add_mapping(extport, in_ip, inport, proto, desc)

    logger.info("UPnP forward done.")

if __name__ == "__main__":
    main()

