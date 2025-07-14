#!/usr/bin/env python3
"""
Script to create INSTALL.txt file for pico-ducky releases
"""
import sys
import os

def create_install_txt(bundle_dir, is_test=False):
    """Create INSTALL.txt file in the bundle directory"""
    
    test_header = """Pico-Ducky Test Installation
====================================

This is a test build. For production use, download from GitHub releases.

""" if is_test else ""
    
    install_content = test_header + """Pico-Ducky Installation Instructions
====================================

IMPORTANT: Read all instructions before starting!

Quick Setup (5 minutes):
1. Connect your Raspberry Pi Pico while holding the BOOTSEL button
2. Device appears as USB drive "RPI-RP2"
3. Copy the .uf2 file to RPI-RP2 (device will reboot)
4. Device reappears as "CIRCUITPY"
5. Copy all .py files to CIRCUITPY root
6. Copy lib folder to CIRCUITPY root
7. Create your payload.dd file (see below)
8. For Pico W: Edit secrets.py for WiFi settings
9. Safely eject and test

SETUP MODE (IMPORTANT FOR SAFETY):
Before first use, enter setup mode to prevent accidental payload execution:
- Connect pin 1 (GP0) to pin 3 (GND) with a jumper wire
- This prevents the payload from running on your development machine
- Remove jumper when ready to deploy

CREATING PAYLOADS:
- Create a file called "payload.dd" in the root of CIRCUITPY
- Use Ducky Script syntax (see examples folder or README.md)
- Example: 
  GUI r
  DELAY 500
  STRING notepad
  ENTER
  STRING Hello World!

WIFI CONFIGURATION (Pico W only):
Edit secrets.py to configure WiFi:

For Home Network (recommended):
  wifi_mode = 'client'
  home_network = {'ssid': 'YourNetwork', 'password': 'YourPassword'}

For Hotspot Mode:
  wifi_mode = 'ap'
  secrets = {'ssid': 'PicoDucky', 'password': 'BadPassword123'}

MULTIPLE PAYLOADS:
Ground these pins to select different payloads:
- GP4: payload.dd
- GP5: payload2.dd  
- GP10: payload3.dd
- GP11: payload4.dd

USB STEALTH MODE:
To hide USB drive when deployed:
- Enter setup mode
- Connect jumper between pin 18 (GND) and pin 20 (GPIO15)
- Note: Pico W defaults to USB disabled, Pico defaults to USB enabled

WEB INTERFACE (Pico W only):
- Access Point Mode: http://192.168.4.1:80
- Client Mode: Check serial output for IP address

TROUBLESHOOTING:
- Device not recognized: Try different USB cable/port
- Payload not running: Check setup mode jumper
- WiFi issues: Verify credentials in secrets.py
- Corrupted device: See RESET.md for recovery

For detailed instructions, examples, and troubleshooting:
See README.md and WIFI_GUIDE.md

WARNING: Test payloads safely! Use setup mode and test on your own devices only.
"""
    
    install_path = os.path.join(bundle_dir, 'INSTALL.txt')
    with open(install_path, 'w') as f:
        f.write(install_content)
    
    print(f"Created INSTALL.txt in {bundle_dir}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python create_install.py <bundle_directory>")
        sys.exit(1)
    
    bundle_dir = sys.argv[1]
    is_test = len(sys.argv) > 2 and sys.argv[2] == "--test"
    create_install_txt(bundle_dir, is_test)
