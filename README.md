# Thermalright LCD Controller (Windows Edition)

A lightweight, resource-efficient Python driver for Thermalright CPU Cooler LCD screens.
**Optimized specifically for Windows** to replace proprietary bloatware.

## Features
* **Zero Background Usage:** Runs as a silent background process (`.pyw`).
* **No "Ghost" Temps:** Direct hardware access via LibreHardwareMonitor (bypasses broken Windows WMI).
* **Ryzen & Intel Support:** Custom sensor logic to find the *real* CPU package temp (Tctl/Package).
* **GUI Configurator:** Change colors and modes without editing code.

## Prerequisites
1.  Install [Python 3.10+](https://www.python.org/downloads/) (Check **"Add Python to PATH"** during install).
2.  Download this repository and extract it.

## Installation

1.  Open the folder in a terminal (PowerShell or CMD).
2.  Install dependencies:
    ```powershell
    pip install -r requirements.txt
    ```
3.  Run the setup script to finalize the package:
    ```powershell
    python fix_setup.py
    ```
    *This organizes files and ensures paths are correct.*

## Usage

### 1. Start the Driver
* Go to the `src` folder.
* Double-click **`Start_Silent.pyw`**.
* *Note: Nothing will appear on screen. The cooler screen should start updating immediately.*
* **To run on startup:** Right-click `Start_Silent.pyw` -> Create Shortcut -> Move shortcut to `shell:startup`.

### 2. Change Settings (Colors/Modes)
* Double-click **`Config_App.pyw`** (or the shortcut created on your desktop).
* Change your settings and click **Save**. The cooler will update instantly.

## 📂 File Structure Explained
* **`.py` files (`src/controller.py`)**: The actual source code. Edit these if you want to modify logic.
* **`.pyw` files (`src/Start_Silent.pyw`)**: Windows Launchers.
    * **Why?** On Windows, `.py` files open a black command console. `.pyw` files run silently.
    * **Usage:** Use `.pyw` for daily use. Use `.py` only for debugging errors.

## Troubleshooting
* **Screen not updating?** Kill `pythonw.exe` in Task Manager and restart `Start_Silent.pyw`.
* **Crash on startup?** Run `python src/controller.py` in a terminal to see the error message.

## Credits
Based on the original work by [MathieuxHugo](https://github.com/MathieuxHugo/digital_thermal_right_lcd).
Ported to Windows with direct DLL drivers by Ushan-destiny.