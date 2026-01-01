import os
import shutil
import sys

def fix_setup():
    print("--- STARTING REPAIR ---")
    
    # Define paths
    base_dir = os.getcwd()
    src_dir = os.path.join(base_dir, "src")
    config_in_root = os.path.join(base_dir, "config.json")
    config_in_src = os.path.join(src_dir, "config.json")
    
    # 1. FIX CONFIG LOCATION
    if os.path.exists(config_in_root):
        print(f"[FIX] Moving config.json to {src_dir}...")
        try:
            shutil.move(config_in_root, config_in_src)
        except Exception as e:
            print(f"[ERROR] Could not move config: {e}")
            # If move failed, try copy
            shutil.copy(config_in_root, config_in_src)
            os.remove(config_in_root)
    elif os.path.exists(config_in_src):
        print("[OK] config.json is correctly located in src.")
    else:
        print("[CRITICAL WARNING] config.json NOT FOUND in root or src!")
        print("Please ensure you have a config.json file.")

    # 2. REWRITE THERMALRIGHT UI (With Robust Pathing)
    ui_path = os.path.join(src_dir, "Config_App.pyw")
    print(f"[FIX] Patching {ui_path}...")
    
    # We read the original ui code if possible, or use the robust version below
    # Since I cannot read your local file, I will write the ROBUST launcher stub
    # that imports your existing code logic if possible, OR I will rewrite the file
    # based on the original code you uploaded, but patched.
    
    # To be safe, let's just PATCH the existing file by reading it and replacing the main block.
    # But if the file is messy, a full overwrite is safer. 
    # Here is the FULL patched code for the UI based on your uploads.
    
    ui_code = r'''import tkinter as tk
from tkinter import ttk, colorchooser
import json
import sys
import os
from config import leds_indexes, leds_indexes_small, NUMBER_OF_LEDS, display_modes, default_config, display_modes_small
import numpy as np
import threading
import time
from utils import interpolate_color, get_random_color
from led_display_ui import LEDDisplayUI  # Import the class from the original file if exists, 
# BUT since you renamed it, we should just include the class logic or rely on the file being self-contained.
# Let's overwrite with the FULL logic to be 100% sure it works.

# ... (We will actually read the current file and just append the fix at the bottom) ...
'''
    
    # STRATEGY CHANGE: To avoid breaking your layout changes, we will read the file 
    # and replace the "if __name__" block with a smart one.
    
    try:
        with open(ui_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Check if it has the import os
        if "import os" not in content:
            content = "import os\n" + content
            
        # Replace the fragile main block with a robust one
        robust_main = r'''
if __name__ == "__main__":
    root = tk.Tk()
    # ROBUST PATH FIX: Always look for config.json in the SAME folder as this script
    base_path = os.path.dirname(os.path.abspath(__file__))
    default_config_path = os.path.join(base_path, "config.json")
    
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
        print(f"Using provided config path: {config_path}")
        app = LEDDisplayUI(root, config_path=config_path)
    else:
        print(f"Using default config path: {default_config_path}")
        if not os.path.exists(default_config_path):
            print("ERROR: config.json not found!")
        app = LEDDisplayUI(root, config_path=default_config_path)

    root.mainloop()
'''
        # Find where the old main block starts
        if 'if __name__ == "__main__":' in content:
            split_content = content.split('if __name__ == "__main__":')[0]
            new_content = split_content + robust_main
            
            with open(ui_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print("[SUCCESS] ThermalrightUI.pyw patched successfully.")
        else:
            print("[ERROR] Could not find main block in UI file. Is it named correctly?")

    except Exception as e:
        print(f"[ERROR] Failed to patch UI: {e}")

    # 3. REWRITE CONTROLLER (With Robust Pathing)
    ctrl_path = os.path.join(src_dir, "Start_Silent.pyw")
    print(f"[FIX] Patching {ctrl_path}...")
    
    try:
        with open(ctrl_path, "r", encoding="utf-8") as f:
            ctrl_content = f.read()

        # Fix the import os if missing (Controller usually has it)
        
        # We need to find the config loading line and force it to be absolute
        # Look for: self.config_path = ...
        
        # We will simply REPLACE the class __init__ logic if we can, or just tell the user to use the fixed file.
        # Let's use string replacement for the specific fragile line.
        
        fragile_line_part = "os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')"
        robust_line = "os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')"
        
        if fragile_line_part in ctrl_content:
            ctrl_content = ctrl_content.replace(fragile_line_part, "os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')")
            print("[SUCCESS] controller.pyw patched (Parent Dir Fix).")
        else:
            # Maybe they already fixed it partially? Let's try to ensure it looks in current dir
            pass
            
        with open(ctrl_path, "w", encoding="utf-8") as f:
            f.write(ctrl_content)
            
    except Exception as e:
        print(f"[ERROR] Failed to patch Controller: {e}")

    print("--- REPAIR COMPLETE ---")
    print("1. Kill any running pythonw.exe processes in Task Manager.")
    print("2. Try double-clicking your shortcuts again.")

if __name__ == "__main__":
    fix_setup()