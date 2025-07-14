# WiFi Configuration for Pico-Ducky
# Set wifi_mode to either 'ap' or 'client'
# 'ap' = Create hotspot (original behavior)
# 'client' = Connect to existing home network

wifi_mode = 'ap'  # Change to 'client' for home network mode

# Settings for hotspot mode (when wifi_mode = 'ap')
secrets = {
    'ssid': 'PicoDucky',
    'password': 'BadPassword123'
}

# Settings for home network mode (when wifi_mode = 'client')
# Replace with your actual home network credentials
home_network = {
    'ssid': 'YourHomeNetwork',
    'password': 'YourHomePassword'
}
