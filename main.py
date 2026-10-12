import os
import sys
from datetime import datetime


from system_monitor import gather_all_info
from report_generator import create_html_report

def main():
  print("*" * 40)
  print("System Health Diagnostic Tool")
  print("*" * 40 + "\n")
  print(f"Scan started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
  
  print("Gathering system information...")
  system_data = gather_all_info()
  print("All system information gathered!\n")

  print("System Information")
  print("-" * 40)
  for key, value in system_data.get("System", {}).items():
    print(f"{key}: {value}")
  print()

  print("Memory Information")
  print("-" * 40)
  memory = system_data.get("Memory", {})
  print(f"Total Ram: {memory.get('Total')} GB")
  print(f"Memory Used: {memory.get('Used')} GB")
  print(f"Memory Available: {memory.get('Available')} GB")
  print()

  print("Disk information")
  print("-" * 40)
  for d, info in system_data.get("Disk", {}).items():
    print(f"Drive: {d}")
    for key, value in info.items():
      print(f"  {key}: {value} GB")
    print()
  print()

  print("Top CPU Using Processes")
  print("-" * 40)

  for p in system_data.get("Processes", [])[:5]:
    p_name = p.get('name', 'Unknown')
    p_cpu = p.get('cpu_percent')
    
    if p_cpu is None:
      print(f"{p_name}: 0.0%")
    else:
      print(f"{p_name}: {p_cpu}%")
  print()

  print("Network status")
  print("-" * 40)
  for interface, stats in system_data.get("Network", {}).items():
    status = "Online" if stats.get("Upstate") else "Offline"
    print(f"Interface: {interface}")
    print(f"Status: {status}")
    
    speed = stats.get('Speed', 0)
    if speed <= 0:
      print(f"Speed: undetermined")
    else:
      print(f"Speed: {speed} Mbps")
    print()

  print("-" * 40)
  print("Scan Fully Complete!")
  
  # HTML report generation
  report_file = create_html_report(system_data)

  if report_file:
    print("\nHTML report generated successfully!")
  else:
    print("\nFailed to generate HTML report.")

if __name__ == "__main__":
  main()
