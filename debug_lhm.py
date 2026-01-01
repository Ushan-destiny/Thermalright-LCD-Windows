import os
import sys

print("--- DIAGNOSTIC: DIRECT DLL DRIVER ---")

# 1. Load the DLL
current_dir = os.path.dirname(os.path.abspath(__file__))
# Check src folder for the DLL
dll_path = os.path.join(current_dir, "src", "LibreHardwareMonitorLib.dll")

if not os.path.exists(dll_path):
    print(f"CRITICAL ERROR: DLL not found at: {dll_path}")
    print("Please make sure 'LibreHardwareMonitorLib.dll' is inside the 'src' folder.")
    sys.exit(1)

try:
    import clr # pythonnet
    clr.AddReference(dll_path)
    from LibreHardwareMonitor.Hardware import Computer, HardwareType, SensorType
    print("SUCCESS: DLL Loaded via pythonnet.")
except ImportError:
    print("CRITICAL ERROR: 'pythonnet' library is missing. Run: pip install pythonnet")
    sys.exit(1)
except Exception as e:
    print(f"CRITICAL ERROR: Could not load DLL: {e}")
    sys.exit(1)

# 2. Open the Computer
print("\nScanning Hardware...")
try:
    computer = Computer()
    computer.IsCpuEnabled = True
    computer.IsGpuEnabled = True
    computer.IsMemoryEnabled = False # Disabled to prevent crash
    computer.IsMotherboardEnabled = False
    computer.IsControllerEnabled = False
    computer.IsNetworkEnabled = False
    computer.IsStorageEnabled = False
    computer.Open()
except Exception as e:
    print(f"CRITICAL ERROR: Driver crashed during 'Open()': {e}")
    sys.exit(1)

# 3. List Everything
found_cpu_temp = False

for hardware in computer.Hardware:
    hardware.Update() # Force read
    print(f"\n[HARDWARE FOUND]: {hardware.Name} (Type: {hardware.HardwareType})")
    
    for sensor in hardware.Sensors:
        print(f"  - Sensor: '{sensor.Name}' | Type: {sensor.SensorType} | Value: {sensor.Value}")
        
        # Check if this is what we need
        if hardware.HardwareType == HardwareType.Cpu and sensor.SensorType == SensorType.Temperature:
            found_cpu_temp = True
            print("    ^^^ THIS IS A CPU TEMP CANDIDATE")

if not found_cpu_temp:
    print("\nWARNING: No CPU Temperature sensors found!")
    print("Possible reasons:")
    print("1. Your CPU (Ryzen?) might need 'IsMotherboardEnabled = True' to see temps.")
    print("2. You might need to run this script as ADMINISTRATOR.")

print("\n--- END ---")
input("Press Enter to exit...")