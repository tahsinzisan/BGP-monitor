# BGP Network Monitoring & Convergence Checker

This is a Python automation project to monitor a BGP network. It uses **ExaBGP** to make adjacency with a BGP-speaking router and listen for routing updates.

## ExaBGP Features

- Listens for BGP updates  
- Tracks route flaps  
- Detects bursts or unnatural frequency of route changes  
- Logs events with detailed information

## Convergence Checking

- Periodically checks iBGP routers for prefix consistency  
- Identifies routers missing specific prefixes  
- Flags potential iBGP convergence issues  
- Logs detailed results for further analysis

## Requirements

- Python 3  
- `pyyaml` (`pip install pyyaml`)  
- ExaBGP properly installed and configured  
- Logging directory must be writable
