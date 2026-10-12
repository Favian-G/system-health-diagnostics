import psutil
import platform
import time
import socket
from datetime import datetime

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
        }
      except (PermissionError, FileNotFoundError):
        continue
  except Exception as e:
    print(f"Error getting disk information: {e}")
  return disk_info

def get_memory_info():
  try:
    memory = psutil.virtual_memory()
    total_gb = round(memory.total / (1024**3), 2)
    available_gb = round(memory.available / (1024**3), 2)
    used_gb = round(total_gb - available_gb, 2)
    
    return {
      "Total": total_gb,
      "Used": used_gb,
      "Available": available_gb
    }
  except Exception as e:
    print(f"Error getting RAM information: {e}")
  return {}


def get_cpu_info():
  try:
    return {"Current usage": psutil.cpu_percent(interval=0.1)}
  except Exception as e:
    print(f"Error getting CPU information: {e}")
  return {"Current usage": 0.0}

def get_network_info():
    network_info = {"Internet_Connected": check_internet_connectivity()}
    try:
        interfaces = psutil.net_if_stats()
        adapter_stats = {}
        for interface, stats in interfaces.items():
            adapter_stats[interface] = {
                "Upstate": stats.isup,
                "Speed": stats.speed
            }
        network_info["Adapters"] = adapter_stats
    except Exception as e:
        print(f"Error getting network information: {e}")
        
    return network_info

def get_general_system_info():
  try:
    os_name = platform.system()
    if os_name == "Darwin":
      os_name = "macOS"
    return {
      
      "OS": os_name,
      "Version": platform.version(),
      "Release Date": platform.release(), 
      "Machine": platform.machine()
    }
  except Exception as e:
    print(f"Error getting General System Information: {e}")
  return {}

def get_processes():
  process_list = []
  try:
    num_of_cores = psutil.cpu_count(logical=True)

    psutil.cpu_percent(interval=None)
    
    for p in psutil.process_iter(attrs=["pid", "name"]):
      try:
        p.cpu_percent(interval=None)
        process_list.append(p)
      except (psutil.NoSuchProcess, psutil.AccessDenied):
        continue

    # Wait a moment to allow CPU percent to calculate accurately
    time.sleep(0.1)

    final_process_data = []

    for p in process_list:
      try:
        p_info = p.info
        p_info["cpu_percent"] = round(p.cpu_percent(interval=None) / num_of_cores, 2)
        final_process_data.append(p_info)
      except (psutil.NoSuchProcess, psutil.AccessDenied):
        continue
    
    top_processes = sorted(final_process_data, key=lambda x: x.get("cpu_percent") or 0.0, reverse=True)[:10]
    return top_processes
  
  except Exception as e:
    print(f"Error getting Process Information: {e}")
  return []
import socket

def check_internet_connectivity(host="8.8.8.8", port=53, timeout=3):
    """Tests if the machine has active internet access by connecting to a public DNS."""
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False

def gather_all_info():
  return {
    "timestamp": datetime.now().isoformat(),
    "System": get_general_system_info(),
    "CPU": get_cpu_info(),
    "Memory": get_memory_info(),
    "Disk": get_disk_info(),
    "Network": get_network_info(),
    "Internet": {"Connected": check_internet_connectivity()},
    "Processes": get_processes()
  }
