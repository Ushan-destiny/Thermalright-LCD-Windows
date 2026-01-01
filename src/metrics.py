import time
import sys
import os
from collections import deque # Required for smoothing

# ==========================================
# DLL LOADING
# ==========================================
LHM_AVAILABLE = False
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Look for DLL in the same folder as this script
    dll_path = os.path.join(current_dir, "LibreHardwareMonitorLib.dll")
    
    if os.path.exists(dll_path):
        import clr # Requires 'pip install pythonnet'
        clr.AddReference(dll_path)
        from LibreHardwareMonitor.Hardware import Computer, HardwareType, SensorType
        LHM_AVAILABLE = True
    else:
        print("Error: LibreHardwareMonitorLib.dll missing from src folder.")
except Exception as e:
    print(f"Error loading DLL: {e}")

# ==========================================
# METRICS CLASS
# ==========================================
class Metrics:
    def __init__(self, update_interval=1.0):
        self.metrics = {'cpu_temp': 0, 'gpu_temp': 0, 'cpu_usage': 0, 'gpu_usage': 0}
        self.update_interval = update_interval
        self.last_update = 0
        
        # --- FIX: Initialize the Smoothing History ---
        # Stores the last 4 readings. 
        self.cpu_temp_history = deque(maxlen=4)
        
        self.computer = None
        self.cpu_hw = None
        self.gpu_hw = None
        
        if LHM_AVAILABLE:
            try:
                self.computer = Computer()
                self.computer.IsCpuEnabled = True
                self.computer.IsGpuEnabled = True
                self.computer.IsMemoryEnabled = False # CRITICAL: Prevents crash
                self.computer.IsMotherboardEnabled = False
                self.computer.IsControllerEnabled = False
                self.computer.IsNetworkEnabled = False
                self.computer.IsStorageEnabled = False
                self.computer.Open()
                
                print("Initializing Sensors...")
                for hardware in self.computer.Hardware:
                    # Save CPU Reference
                    if hardware.HardwareType == HardwareType.Cpu:
                        self.cpu_hw = hardware
                        print(f"  + Connected to CPU: {hardware.Name}")
                    
                    # Save GPU Reference
                    if hardware.HardwareType in [HardwareType.GpuNvidia, HardwareType.GpuAmd]:
                        self.gpu_hw = hardware
                        print(f"  + Connected to GPU: {hardware.Name}")
                        
            except Exception as e:
                print(f"Driver Init Failed: {e}")

    def get_metrics(self, temp_unit):
        # Don't update too fast
        if time.time() - self.last_update < self.update_interval:
            return self.metrics

        # 1. UPDATE CPU (With Tctl Targeting + Smoothing)
        if self.cpu_hw:
            try:
                self.cpu_hw.Update() # Force refresh
                raw_temp = 0
                
                # Search for the best sensor
                for sensor in self.cpu_hw.Sensors:
                    if sensor.SensorType == SensorType.Temperature:
                        name = sensor.Name.lower()
                        
                        # PRIORITY 1: Ryzen "Tctl" (The Standard Package Temp)
                        # Your debug logs confirmed this is called "Core (Tctl/Tdie)"
                        if "tctl" in name:
                            raw_temp = sensor.Value
                            break # Found the best one, stop searching!
                        
                        # PRIORITY 2: Intel "Package"
                        if "package" in name:
                            raw_temp = sensor.Value
                            break 
                        
                        # Fallback: Just take whatever we find first (e.g. CCD1)
                        if raw_temp == 0:
                            raw_temp = sensor.Value
                
                # Apply Smoothing
                if raw_temp > 0:
                    self.cpu_temp_history.append(raw_temp)
                    # Calculate average of the history buffer
                    avg_temp = sum(self.cpu_temp_history) / len(self.cpu_temp_history)
                    self.metrics['cpu_temp'] = int(avg_temp)
                    
            except Exception as e:
                print(f"Error reading CPU: {e}")

        # 2. UPDATE GPU
        if self.gpu_hw:
            try:
                self.gpu_hw.Update() # Force refresh
                for sensor in self.gpu_hw.Sensors:
                    if sensor.SensorType == SensorType.Temperature:
                        self.metrics['gpu_temp'] = int(sensor.Value)
                    if sensor.SensorType == SensorType.Load and "core" in sensor.Name.lower():
                        self.metrics['gpu_usage'] = int(sensor.Value)
            except Exception as e:
                pass

        # 3. CPU USAGE (Fallback to psutil)
        try:
            import psutil
            self.metrics['cpu_usage'] = int(psutil.cpu_percent(interval=None))
        except:
            pass

        self.last_update = time.time()
        
        # Unit Conversion
        for device in ["cpu", "gpu"]:
            if temp_unit.get(device) == "fahrenheit":
                c_temp = self.metrics.get(f"{device}_temp", 0)
                self.metrics[f"{device}_temp"] = int(c_temp * 9 / 5 + 32)
                
        return self.metrics