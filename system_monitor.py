
#Gathers RAM, CPU, DISK, and Network information

import psutil
import platform
from datetime import datetime


# Get disk information
def get_disk_info():
  disk_info = {}

  try:
    partitions = psutil.disk_partitions()

    for partition in partitions:
      try:
        usage = psutil.disk_usage(partition.mountpoint)
        disk_info[partition.mountpoint] = {
          "Total": round(usage.total / (1024**3), 2),
          "Used": round(usage.used / (1024**3), 2),
          "Free": round(usage.free / (1024**3), 2)
          # FIXME: might add more info about disk
        }

      except (PermissionError, FileExistsError):
        continue
  except Exception as e:
    print(f"Error getting disk information: {e}")

  return disk_info


# Get RAM information
def get_memory_info():
  try:
    memory = psutil.virtual_memory()
    memory_info = {
      "Total": round(memory.total / (1024**3), 2),
      "Used": round(memory.used / (1024**3), 2),
      "Free": round(memory.free / (1024**3), 2), 
      # FIXME: might add more info about RAM
    }
  except Exception as e:
    print(f"Error getting RAM information: {e}")

  return memory_info

# Get CPU information
def get_cpu_info():
  try:
    cpu_info = {
      "Current usage": psutil.cpu_percent(interval=0.1)
    }
  except Exception as e:
    print(f"Error getting CPU information: {e}")
  return cpu_info

# Get Network information
def get_network_info():
  network_info = {}
  try:
    interfaces = psutil.net_if_stats()
    for interface, stats in interfaces.items():
      network_info[interface] = {
        "Upstate": stats.isup,
        "Speed": stats.speed
      }
  except Exception as e:
    print(f"Error getting network information: {e}")

  return network_info

# Get General System Information
def get_general_system_info():
  try:
    system_info = {
      "OS": platform.system(),
      "Version": platform.version(),
      "Release Date": platform.release(), #ensure this output is formated correct 
      "Machine": platform.machine()
    }
  except Exception as e:
    print(f"Error getting General System Information: {e}")

  return system_info

# Get CPU usage processes
def get_processes():
  processess = []
  process_list = []
  try:
    for p in psutil.process_iter(["pid", "name", "cpu_percent"]):
      try:
        process_list.append(p.info)
      except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass

    top_processess = sorted(process_list, key=lambda x: x["cpu_percent"] or 0.0, reverse = True)[:10]
    processess = top_processess
  except Exception as e:
    print(f"Error getting Processe Information")

  return processess

def gather_all_info():
  all_info = {
    "timestamp": datetime.now().isoformat(),
    "System": get_general_system_info(),
    "CPU": get_cpu_info(),
    "Memory": get_memory_info(),
    "Disk": get_disk_info(),
    "Network": get_network_info(),
    "Processes": get_processes()
  }
  return all_info


