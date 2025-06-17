#!/usr/bin/env python3
from netmiko import ConnectHandler
import yaml
import time
import logging
from datetime import datetime

# Set up iBGP logging
ibgp_logger = logging.getLogger('ibgp_logger')
ibgp_logger.setLevel(logging.INFO)
ibgp_handler = logging.FileHandler('../logs/ibgp_checks.log')
ibgp_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
ibgp_logger.addHandler(ibgp_handler)

def check_ibgp_convergence():
    with open('devices.yaml') as f:
        devices = yaml.safe_load(f)
    
    while True:
        for device in devices['route_reflectors']:
            try:
                conn = ConnectHandler(**device)
                output = conn.send_command("show bgp summary")
                
                if "Established" not in output:
                    ibgp_logger.info(f"iBGP down on {device['host']}")
                
                conn.disconnect()
            except Exception as e:
                ibgp_logger.info(f"Connection failed to {device['host']}: {str(e)}")
        
        time.sleep(300)  # Check every 5 minutes

if __name__ == '__main__':
    check_ibgp_convergence()