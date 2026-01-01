import sys

print("--- DIAGNOSTIC START ---")

# TEST 1: WinTmp (The one we want to use)
print("\n[1] Testing WinTmp...")
try:
    import WinTmp
    temp = WinTmp.CPU_Temp()
    print(f"SUCCESS: WinTmp says CPU is {temp}°C")
except Exception as e:
    print(f"FAILURE: WinTmp crashed. Reason: {e}")
except ImportError:
    print("FAILURE: WinTmp library not installed.")

# TEST 2: Standard WMI (The one giving you 16°C)
print("\n[2] Testing Standard WMI (Ghost Readings)...")
try:
    import wmi
    w = wmi.WMI(namespace="root\\wmi")
    zones = w.MSAcpi_ThermalZoneTemperature()
    if len(zones) > 0:
        raw = zones[0].CurrentTemperature
        celsius = (raw / 10.0) - 273.15
        print(f"SUCCESS: WMI says CPU is {celsius:.1f}°C (Raw: {raw})")
    else:
        print("FAILURE: No Thermal Zones found.")
except Exception as e:
    print(f"FAILURE: WMI Error: {e}")

# TEST 3: OpenHardwareMonitor (The backup plan)
print("\n[3] Testing OpenHardwareMonitor...")
try:
    w = wmi.WMI(namespace="root\\OpenHardwareMonitor")
    sensors = w.Sensor()
    found = False
    for sensor in sensors:
        if sensor.SensorType == 'Temperature' and 'CPU' in sensor.Name:
            print(f"SUCCESS: Found '{sensor.Name}' = {sensor.Value}°C")
            found = True
    if not found:
        print("FAILURE: Namespace exists, but no CPU sensor found.")
except Exception as e:
    print(f"FAILURE: OpenHardwareMonitor not detected. ({e})")

print("\n--- DIAGNOSTIC END ---")
input("Press Enter to exit...")