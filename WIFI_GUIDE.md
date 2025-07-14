# WiFi Configuration Guide

The Pico-Ducky now supports two WiFi modes:

## 1. Access Point Mode (Original Behavior)
Creates its own WiFi hotspot that you connect to directly.

## 2. Client Mode (New Feature)
Connects to your existing home network for easier control of local devices.

## Configuration

Edit the `secrets.py` file to configure your WiFi settings:

### For Home Network Connection (Client Mode):
```python
wifi_mode = 'client'

home_network = {
    'ssid': 'YourHomeNetworkName',
    'password': 'YourHomeNetworkPassword'
}
```

### For Hotspot Mode (AP Mode):
```python
wifi_mode = 'ap'

secrets = {
    'ssid': 'PicoDucky',
    'password': 'BadPassword123'
}
```

## Usage

### Client Mode (Home Network):
1. Set `wifi_mode = 'client'` in `secrets.py`
2. Update `home_network` with your WiFi credentials
3. Connect the Pico-Ducky to power
4. The device will connect to your home network
5. Check the serial output for the assigned IP address
6. Access the web interface at `http://<IP_ADDRESS>:80`

### AP Mode (Hotspot):
1. Set `wifi_mode = 'ap'` in `secrets.py`
2. Update `secrets` with your desired hotspot name and password
3. Connect the Pico-Ducky to power
4. Connect your device to the "PicoDucky" WiFi network
5. Access the web interface at `http://192.168.4.1:80`

## Advantages of Client Mode

- **Easier Access**: No need to switch WiFi networks on your device
- **Better Range**: Uses your existing WiFi infrastructure
- **Multiple Devices**: Multiple devices can access the interface simultaneously
- **Network Integration**: Can be accessed from anywhere on your network
- **Persistent Connection**: Maintains connection even when not actively using

## Troubleshooting

1. **Connection Issues**: Verify your WiFi credentials are correct
2. **IP Address**: Check serial output for the assigned IP address
3. **Network Access**: Ensure your device is on the same network
4. **Firewall**: Check if your router's firewall is blocking access
