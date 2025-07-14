# GitHub Actions Usage Examples

## Creating a Release

### Method 1: Automatic Release (Recommended)
```bash
# Tag your commit with a version
git tag v1.0.0
git push origin v1.0.0

# The build-uf2.yml workflow will automatically:
# - Download CircuitPython UF2 files
# - Bundle all required libraries
# - Create release packages for all boards
# - Publish a GitHub release
```

### Method 2: Manual Build
1. Go to your repository's "Actions" tab
2. Select "Manual Build" workflow
3. Click "Run workflow"
4. Enter version (e.g., "v1.0.0")
5. Choose board type or "all"
6. Download artifacts when complete

## Release Contents

Each release includes bundles for all supported boards:
- `pico-ducky-v1.0.0-raspberry_pi_pico.zip`
- `pico-ducky-v1.0.0-raspberry_pi_pico_w.zip`
- `pico-ducky-v1.0.0-raspberry_pi_pico2.zip`
- `pico-ducky-v1.0.0-raspberry_pi_pico2_w.zip`

Each bundle contains:
```
pico-ducky-v1.0.0-raspberry_pi_pico_w/
├── adafruit-circuitpython-raspberry_pi_pico_w-en_US-9.2.1.uf2
├── boot.py
├── code.py
├── duckyinpython.py
├── webapp.py
├── wsgiserver.py
├── secrets.py
├── lib/
│   ├── adafruit_hid/
│   ├── adafruit_debouncer.mpy
│   ├── adafruit_ticks.mpy
│   ├── asyncio/
│   └── adafruit_wsgi/
├── examples/
├── README.md
├── WIFI_GUIDE.md
├── CHANGES.md
└── INSTALL.txt
```

## Installation from Release

1. **Download**: Get the appropriate bundle for your board
2. **Extract**: Unzip the bundle
3. **Flash**: Hold BOOTSEL, connect Pico, copy UF2 to RPI-RP2
4. **Install**: Copy Python files and lib folder to CIRCUITPY
5. **Configure**: Edit secrets.py with WiFi settings
6. **Run**: Safely eject and use

## WiFi Configuration Example

```python
# secrets.py
wifi_mode = 'client'  # or 'ap'

# For client mode (home network)
home_network = {
    'ssid': 'MyHomeWiFi',
    'password': 'MyPassword123'
}

# For AP mode (hotspot)
secrets = {
    'ssid': 'PicoDucky',
    'password': 'BadPassword123'
}
```

## Troubleshooting Builds

### Check Build Status
- Go to Actions tab to see workflow runs
- Click on failed runs to see error logs
- Red X indicates failure, green check indicates success

### Common Issues
- **Library download failures**: Usually temporary, re-run the workflow
- **UF2 download failures**: Check CircuitPython.org availability
- **Permission issues**: Ensure GITHUB_TOKEN has necessary permissions
- **Bundle creation errors**: Check file paths and permissions

### Manual Debugging
If automatic builds fail, you can run the Python scripts locally:
```bash
# Install dependencies
pip install requests

# Run the build script manually
python3 -c "
import requests
# ... (copy the Python code from the workflow)
"
```

## Customizing Workflows

### Adding New Boards
Edit the `BOARDS` dictionary in the workflow:
```python
BOARDS = {
    'new_board': 'https://downloads.circuitpython.org/bin/new_board/...',
    # existing boards...
}
```

### Adding Libraries
Update the `required_libs` list:
```python
required_libs = [
    'adafruit_hid',
    'new_library.mpy',
    # existing libraries...
]
```

### Changing CircuitPython Version
Update the `CP_VERSION` variable:
```python
CP_VERSION = "9.2.1"  # Change to desired version
```
