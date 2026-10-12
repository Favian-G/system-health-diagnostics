import os
import sys

from datetime import datetime
from system_monitor import gather_all_info

def main():
  print("*" * 40)
  print("System Health Diagnostic Tool")
  print("*" * 40 + "\n")
  print(f"Scan started at: {datetime.now()}")
  
  print("Gathering system information...")
  system_data = gather_all_info()
  print("All system information gathered!\n")

  print("System Information")
  print("-" * 40)
  for key, value in system_data["System"].items():
    print(f"{key}: {value}")
  print()

  print("Memory Information")
  print("-" * 40)
  for key, value in system_data["Memory"].items():
    print(f"{key}: {value}")
  print()

  print("Disk information")
  print("-" * 40)
  for d, info in system_data["Disk"].items():
    print(f"Drive: {d}")
    for key, value in info.items():
      print(f" {key}: {value}")
    print()
  print()

  print("Top CPU Using Processes")
  print("-" * 40)
  for p in system_data["Processes"][:5]:
    #FIXME: not comparing "NONE" value correct 
    if p['cpu_percent'] == 'None':
      print(f"{p['name']}: {p['cpu_percent']}")
    else:
      print(f"{p['name']}: {p['cpu_percent']}%")
  print()

  print("Network status")
  print("-" * 40)
  # FIXME: There seems to be a error with speed readings
  for interface, stats in system_data["Network"].items():
    status = "Online" if stats["Upstate"] else "OfLine"
    print(f"Interface: {interface}")
    print(f"Status: {status}")
    print(f"Speed: {stats['Speed']} Mbps")
    print()

  print("-" * 40)
  print("Scan Fully Complete!")
  

if __name__ == "__main__":
  main()