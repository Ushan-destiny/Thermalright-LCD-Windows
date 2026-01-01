import tkinter as tk
import os
import sys

# FIX: Import the class from your main UI file
from ThermalrightUI import LEDDisplayUI

if __name__ == "__main__":
    root = tk.Tk()
    
    # 1. Robust Path Logic (Finds config.json in the same folder)
    base_path = os.path.dirname(os.path.abspath(__file__))
    default_config_path = os.path.join(base_path, "config.json")
    
    # 2. Argument Handling (Optional, allows dragging config file onto script)
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
    else:
        config_path = default_config_path

    # 3. Launch the App
    if not os.path.exists(config_path):
        # Create a tiny popup if config is missing, instead of crashing silently
        tk.messagebox.showerror("Error", f"Config file not found at:\n{config_path}")
    else:
        app = LEDDisplayUI(root, config_path=config_path)
        root.mainloop()