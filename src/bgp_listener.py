#!/usr/bin/env python3
import sys
import time
import logging
from datetime import datetime
from collections import deque

# Set up flap logging
flap_logger = logging.getLogger('flap_logger')
flap_logger.setLevel(logging.INFO)
flap_handler = logging.FileHandler('../logs/bgp_flaps.log')
flap_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
flap_logger.addHandler(flap_handler)

# Flap detection parameters
FLAP_WINDOW_SECONDS = 60  # Time window to monitor for flaps
MIN_FLAPS_TO_ALERT = 3    # Minimum flaps in window to trigger alert
flap_history = deque(maxlen=20)  # Stores timestamps of recent flaps

def is_flapping_burst():
    
    if len(flap_history) < MIN_FLAPS_TO_ALERT:
        return False
    
    # Get flaps within our time window
    now = time.time()
    recent_flaps = [t for t in flap_history if now - t <= FLAP_WINDOW_SECONDS]
    
    return len(recent_flaps) >= MIN_FLAPS_TO_ALERT

def main():
    last_alert_time = 0
    alert_cooldown = 300  # Don't alert more than once every 5 minutes
    
    while True:
        try:
            line = sys.stdin.readline().strip()
            if not line:
                break
            
            if "withdrawn" in line or "announced" in line:
                current_time = time.time()
                flap_history.append(current_time)
                
                if is_flapping_burst() and (current_time - last_alert_time) > alert_cooldown:
                    prefix = line.split()[5] if "withdrawn" in line else line.split()[4]
                    flap_logger.info(f"FLAPPING BURST DETECTED! Prefix: {prefix} - {len(flap_history)} changes in last {FLAP_WINDOW_SECONDS} sec")
                    last_alert_time = current_time
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            flap_logger.error(f"Error processing line: {str(e)}")

if __name__ == '__main__':
    main()