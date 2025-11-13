# DecoyStorm

DecoyStorm is a safe, non-destructive distraction tool for academic red-team competitions. It creates harmless artifacts that look suspicious, increasing defender workload without damaging system availability or integrity.

## Features
- Creates harmless but suspicious files (e.g., `payload.enc`, `exfiltration.zip`)
- Generates fake Bash/PowerShell scripts
- Produces fake log activity
- Adds a benign scheduled task (Windows) or cron job (Linux)
- Logs all artifacts for cleanup

## Supported Systems
- Windows Server 2022  
- Ubuntu Jammy

## Usage
Run:
- python3 decoystorm.py

Or on Windows:
- py decoystorm.py

## Cleanup
If cleanup mode is added:
- python3 decoystorm.py --cleanup


## Requirements
- Python 3  
- Cron (Linux)

## Notes
- For competition/lab use only  
- All actions are fully reversible  

## Author
Pranav Natarajan
psn5263@rit.edu
