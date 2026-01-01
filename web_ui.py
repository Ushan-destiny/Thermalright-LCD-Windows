import json
import os
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
CONFIG_FILE = 'config.json'

def load_config():
    """Reads the current configuration safely."""
    if not os.path.exists(CONFIG_FILE):
        return {}
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def save_config(new_config):
    """Writes the new configuration."""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(new_config, f, indent=4)

@app.route('/')
def index():
    config = load_config()
    
    # Get current settings to pre-fill the form
    current_mode = config.get('display_mode', 'metrics')
    
    # Try to guess the current color from the first LED
    # The config stores an array of 84 colors. We just pick the first one to show in the picker.
    try:
        colors = config.get('metrics', {}).get('colors', [])
        current_color_hex = "#" + colors[0] if colors else "#ffffff"
        # Handle complex colors like 'random' or gradients by defaulting to white
        if "-" in current_color_hex or "random" in current_color_hex:
            current_color_hex = "#ffffff"
    except:
        current_color_hex = "#ffffff"

    return render_template('index.html', current_mode=current_mode, current_color=current_color_hex)

@app.route('/update', methods=['POST'])
def update_settings():
    config = load_config()
    
    # 1. Update Mode
    new_mode = request.form.get('display_mode')
    config['display_mode'] = new_mode
    
    # 2. Update Color
    # The device needs 84 individual color codes. We take the one picked color
    # and duplicate it 84 times to fill the whole screen.
    hex_color = request.form.get('led_color') # Returns #RRGGBB
    clean_color = hex_color.replace('#', '')  # Remove # for the config
    
    # Create array of 84 identical colors
    solid_color_array = [clean_color] * 84
    
    # Update both 'metrics' and 'time' colors so it applies everywhere
    if 'metrics' not in config: config['metrics'] = {}
    if 'time' not in config: config['time'] = {}
    
    config['metrics']['colors'] = solid_color_array
    config['time']['colors'] = solid_color_array

    save_config(config)
    
    return redirect('/')

if __name__ == '__main__':
    # accessible on network at port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)