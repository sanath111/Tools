#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psutil
import platform
import socket
import time
import mysql.connector
import subprocess
from datetime import datetime


# Database config
DB_HOST = '192.168.1.183'
DB_PORT = 3306
DB_USER = 'sensor_user'
DB_PASSWORD = ''
DB_NAME = 'sensor_db'
DB_TABLE = 'sensor_data'


# Function to get CPU temperature from various sources
def get_cpu_temp():
    try:
        # First try thermal_zone0
        paths = [
            "/sys/class/thermal/thermal_zone0/temp",
            "/sys/class/hwmon/hwmon0/temp1_input"
        ]
        for path in paths:
            try:
                with open(path, 'r') as f:
                    temp = int(f.read().strip()) / 1000.0
                    if temp > 0:
                        return round(temp, 2)
            except FileNotFoundError:
                continue

        # Fallback to psutil sensors_temperatures()
        temps = psutil.sensors_temperatures()
        for name, entries in temps.items():
            for entry in entries:
                if entry.current and entry.label.lower().startswith("core"):
                    return round(entry.current, 2)
                elif entry.current:
                    return round(entry.current, 2)
        return None
    except Exception:
        return None


# Function to get GPU temperature (NVIDIA or fallback)
def get_gpu_temp():
    try:
        result = subprocess.run(
            ['nvidia-smi', '--query-gpu=temperature.gpu', '--format=csv,noheader,nounits'],
            capture_output=True, text=True, check=True
        )
        return int(result.stdout.strip())
    except Exception:
        return None


# Get system uptime in seconds
def get_uptime():
    try:
        return int(time.time() - psutil.boot_time())
    except Exception:
        return None


def get_disk_partitions():
    partitions = []
    for part in psutil.disk_partitions(all=False):
        if not part.device.startswith('/dev'):
            continue
        try:
            usage = psutil.disk_usage(part.mountpoint)
            partitions.append({
                'mount_point': part.mountpoint,
                'fs_type': part.fstype,
                'device': part.device,
                'total': usage.total // (1024**3),
                'free': usage.free // (1024**3)
            })
        except PermissionError:
            continue
    return partitions


# Main function to collect and save stats
def collect_and_save_stats():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()

        # Collect system stats
        timestamp = datetime.now()
        hostname = socket.gethostname()
        memory = psutil.virtual_memory()
        total_ram = memory.total // 1024 // 1024  # MB
        free_ram = memory.available // 1024 // 1024  # MB
        load1, load5, load15 = psutil.getloadavg()
        cpu_cores = psutil.cpu_count(logical=True)
        cpu_temp = get_cpu_temp()
        gpu_temp = get_gpu_temp()
        uptime_seconds = get_uptime()

        # Insert stats into database
        insert_query = f"""
        INSERT INTO {DB_TABLE}
        (timestamp, host, total_ram, free_ram, load1, load5, load15, cpu_cores, cpu_temp, gpu_temp, uptime)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            timestamp, hostname, total_ram, free_ram,
            load1, load5, load15, cpu_cores,
            cpu_temp, gpu_temp, uptime_seconds
        )

        cursor.execute(insert_query, values)
        conn.commit()
        print(f"Stats saved at {timestamp}")

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


if __name__ == "__main__":
    collect_and_save_stats()
