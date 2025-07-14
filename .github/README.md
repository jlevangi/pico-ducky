# GitHub Actions for Pico-Ducky

This repository includes GitHub Actions workflows to automatically build and release Pico-Ducky packages with UF2 files.

## Available Workflows

### 1. Build UF2 Release (`build-uf2.yml`)
- **Trigger**: Automatically runs when you push a git tag starting with `v` (e.g., `v1.0.0`) **from any branch**
- **Purpose**: Creates a complete release with UF2 files for all supported boards
- **Output**: GitHub release with ZIP bundles and UF2 files

### 2. Test Build (`test-build.yml`)
- **Trigger**: Runs on pull requests to main/master branches, or manual trigger
- **Purpose**: Validates the build process without creating releases
- **Output**: Test results and validation

### 3. Manual Build (`manual-build.yml`)
- **Trigger**: Manual trigger from GitHub Actions tab
- **Purpose**: Build for specific board or all boards on demand
- **Options**: Choose version and board type
- **Output**: Build artifacts (downloadable from Actions tab)

### 4. Build and Release (`release.yml`)
- **Trigger**: Tag pushes or manual dispatch
- **Purpose**: Alternative release workflow with simplified build process
- **Output**: GitHub release with complete bundles

## How to Use

### Creating a Release
**Important**: Releases can be created from any branch by tagging a commit.

1. Tag your commit with a version number:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. The `build-uf2.yml` workflow will automatically:
   - Download CircuitPython UF2 files for all supported boards
   - Download required CircuitPython libraries
   - Create installation bundles for each board
   - Create a GitHub release with all files

**To ensure releases only from main branch:**
```bash
# Switch to main branch first
git checkout main
git pull origin main

# Then tag and push
git tag v1.0.0
git push origin v1.0.0
```

### Manual Build
1. Go to the "Actions" tab in your GitHub repository
2. Select "Manual Build" workflow
3. Click "Run workflow"
4. Choose your version and board type
5. Download the artifacts when complete

## What's Included in Each Release

Each release bundle contains:
- **CircuitPython UF2 file** - Flash this to your Pico first
- **Python source files** - All `.py` files including your WiFi modifications
- **Library files** - All required CircuitPython libraries in `lib/` folder
- **Documentation** - README, WiFi guide, and installation instructions
- **Examples** - Example payload files
- **Installation guide** - Step-by-step setup instructions

## Supported Boards

- Raspberry Pi Pico (`raspberry_pi_pico`)
- Raspberry Pi Pico W (`raspberry_pi_pico_w`)
- Raspberry Pi Pico 2 (`raspberry_pi_pico2`)
- Raspberry Pi Pico 2 W (`raspberry_pi_pico2_w`)

## Installation Process

1. **Flash CircuitPython**: Hold BOOTSEL button, connect Pico, copy UF2 file to RPI-RP2 drive
2. **Install Code**: Copy all Python files to CIRCUITPY root
3. **Install Libraries**: Copy `lib` folder to CIRCUITPY root
4. **Configure WiFi**: Edit `secrets.py` with your network settings
5. **Run**: Safely eject and the device will start

## WiFi Configuration

The release includes the enhanced WiFi functionality:

```python
# Client mode (connect to home network)
wifi_mode = 'client'
home_network = {
    'ssid': 'YourHomeNetwork',
    'password': 'YourPassword'
}

# AP mode (create hotspot)
wifi_mode = 'ap'
secrets = {
    'ssid': 'PicoDucky',
    'password': 'YourPassword'
}
```

## Troubleshooting

- **Build failures**: Check the Actions logs for detailed error messages
- **Missing libraries**: The workflow downloads the latest CircuitPython bundle
- **UF2 download issues**: Workflow includes retry logic and error handling
- **WiFi connection problems**: Device automatically falls back to AP mode

## Customization

You can modify the workflows to:
- Change CircuitPython version (update `CP_VERSION`)
- Add additional libraries (update `required_libs` list)
- Change bundle contents (modify file copying logic)
- Customize installation instructions (edit `install_txt` template)
