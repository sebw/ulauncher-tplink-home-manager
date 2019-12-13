# TPLink Smart Plug Manager

## Supported models

- HS110 Smart Plug
- KL60 Smart Bulb

## If you want support for more device

Contact me! I will ask for some Python output from your device.

## Requirements

Install the `pyHS100` Python library:

`pip install pyHS100`

This extension only works for devices on the local network. You can't remotely control your switches.

## Screenshots

Calling the extension:

<img aligh="center" src="https://blog.wains.be/images/ulauncher_tplink_plug.png">

Smart Plug is off:

<img aligh="center" src="https://blog.wains.be/images/ulauncher_tplink_off.png">

Turning on Smart Plug:

<img aligh="center" src="https://blog.wains.be/images/ulauncher_tplink_turned_on.png">

Smart Plug is on:

<img aligh="center" src="https://blog.wains.be/images/ulauncher_tplink_on.png">

## Known Issues

- No support for HS100. Please provide me with the `plug.get_sysinfo()` output so I can support HS100.
- Limited to plugs with static IP.

## To Do

- Implement auto-discovery, but it doesn't work properly for me (maybe because my devices are in a large subnet).