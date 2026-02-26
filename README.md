# WebOS Manager v2

A terminal UI for managing and controlling LG WebOS TVs over the network. Powered by [bscpylgtv](https://github.com/chros73/bscpylgtv) for screenshot support, picture settings, remote buttons, service menus, and more.

---

## Requirements

- Python 3.11 or higher
- Git

---

## Installation

### Arch Linux

```bash
sudo pacman -S git python

git clone https://github.com/Atractyve/webos-manager-v2.git
cd webos-manager-v2

python -m venv .venv

# bash/zsh:
source .venv/bin/activate
# fish:
source .venv/bin/activate.fish

pip install -r requirements.txt

python src/main.py
```

To run again later:

```bash
cd webos-manager-v2

# bash/zsh:
source .venv/bin/activate
# fish:
source .venv/bin/activate.fish

python src/main.py
```

### Windows

```
git clone https://github.com/Atractyve/webos-manager-v2.git
cd webos-manager-v2

python -m venv .venv
.venv\Scripts\activate

pip install -r requirements.txt

python src/main.py
```

---

## Pairing with a TV

The first time you connect to a TV, it will show a pairing prompt on the screen. Accept it, and the client key will be saved automatically for future connections.

If you already have a client key, you can add it manually to `~/.webos-manager/rooms.json`:

```json
{
  "Room 1": {
    "ip": "192.168.1.101",
    "key": "YOUR_CLIENT_KEY"
  }
}
```

---

## Controls

Once connected to a TV, type any command into the terminal input and press Enter. All commands are called on the `client` object.

### Volume & Audio

| Command | Description |
| --- | --- |
| `client.volume_up()` | Raise volume by 1 |
| `client.volume_down()` | Lower volume by 1 |
| `client.set_volume(50)` | Set volume to a specific level (0-100) |
| `client.set_mute(True)` | Mute |
| `client.set_mute(False)` | Unmute |
| `client.get_volume()` | Get current volume level |
| `client.get_audio_status()` | Get current audio status |
| `client.get_sound_output()` | Get current audio output |
| `client.change_sound_output("tv_speaker")` | Change audio output |

### Power & Screen

| Command | Description |
| --- | --- |
| `client.power_off()` | Turn off the TV (standby) |
| `client.turn_screen_off()` | Turn off the screen (keep TV on) |
| `client.turn_screen_on()` | Turn the screen back on |
| `client.get_power_state()` | Get current power state |
| `client.reboot()` | Full reboot the TV |

### Screenshot

| Command | Description |
| --- | --- |
| `client.take_screenshot()` | Take a screenshot (returns `imageUri` with HTTP link) |

### Playback

| Command | Description |
| --- | --- |
| `client.play()` | Play |
| `client.pause()` | Pause |
| `client.stop()` | Stop |
| `client.rewind()` | Rewind |
| `client.fast_forward()` | Fast forward |

### Channels

| Command | Description |
| --- | --- |
| `client.channel_up()` | Next channel |
| `client.channel_down()` | Previous channel |
| `client.get_current_channel()` | Get info on the current channel |
| `client.get_channels()` | List all available channels |
| `client.set_channel(channel)` | Switch to a specific channel |

### Apps

| Command | Description |
| --- | --- |
| `client.get_apps_all()` | List all installed apps (including hidden) |
| `client.get_current_app()` | Get the currently open app |
| `client.launch_app("app.id.here")` | Launch an app by ID |
| `client.close_app("app.id.here")` | Close an app by ID |
| `client.launch_app_with_params("app.id", {"key": "val"})` | Launch app with parameters |

### Inputs

| Command | Description |
| --- | --- |
| `client.get_inputs()` | List all available inputs (HDMI etc.) |
| `client.get_input()` | Get current input |
| `client.set_input("HDMI_2")` | Switch to a specific input |
| `client.set_device_info("HDMI_2", "pc", "PC")` | Set PC mode for an input |
| `client.set_device_info("HDMI_2", "hometheater", "Home Theatre")` | Set Home Theatre mode |

### Remote Buttons

| Command | Description |
| --- | --- |
| `client.button("INFO")` | Press INFO button |
| `client.button("HOME")` | Press HOME button |
| `client.button("BACK")` | Press BACK button |
| `client.button("LEFT")` | Press LEFT button |
| `client.button("RIGHT")` | Press RIGHT button |
| `client.button("UP")` | Press UP button |
| `client.button("DOWN")` | Press DOWN button |
| `client.button("ENTER")` | Press ENTER/OK button |
| `client.button("MENU")` | Press MENU button |
| `client.button("MUTE")` | Press MUTE button |
| `client.button("RED")` | Press RED button |
| `client.button("GREEN")` | Press GREEN button |
| `client.button("YELLOW")` | Press YELLOW button |
| `client.button("BLUE")` | Press BLUE button |

### Picture Settings

| Command | Description |
| --- | --- |
| `client.get_picture_settings(["backlight", "contrast"])` | Get specific picture settings |
| `client.set_current_picture_mode("expert2")` | Switch picture preset |
| `client.set_system_settings("picture", {"backlight": 0, "contrast": 85})` | Set picture values |
| `client.set_settings("picture", {"backlight": 0})` | Set picture values (alt) |

### System Settings

| Command | Description |
| --- | --- |
| `client.get_system_settings("option", ["country"])` | Get system settings |
| `client.get_system_info()` | Get system info |
| `client.get_software_info()` | Get firmware/software version |
| `client.get_configs(["tv.model.*"])` | Get config values |

### Notifications

| Command | Description |
| --- | --- |
| `client.send_message("Hello!")` | Show a toast notification on the TV |

### Raw SSAP Requests

| Command | Description |
| --- | --- |
| `client.request("ssap://uri/here")` | Send any SSAP request |
| `client.request("ssap://uri", {"key": "val"})` | SSAP request with payload |

### Hidden Menus & Advanced

| Command | Description |
| --- | --- |
| `client.launch_app("com.webos.app.installation")` | Installation menu (Hotel Mode, Set ID, etc.) |
| `client.launch_app("com.webos.app.screensaver")` | Launch screensaver |
| `client.launch_app_with_params("com.webos.app.tvhotkey", {"activateType": "mute-hidden-action"})` | 3x MUTE hidden menu |
| `client.launch_app_with_params("com.webos.app.tvhotkey", {"activateType": "freesync-info"})` | 7x GREEN FreeSync info |
| `client.launch_app_with_params("com.webos.app.factorywin", {"id": "executeFactory", "irKey": "inStart"})` | In-Start Service Menu (code: 0413) |
| `client.launch_app_with_params("com.webos.app.factorywin", {"id": "executeFactory", "irKey": "ezAdjust"})` | Ez-Adjust Service Menu (code: 0413) |
| `client.launch_app_with_params("com.palm.app.settings", {"target": "PictureMode"})` | Picture mode settings |

---

## Config File

Rooms are stored at:

- **Linux/Mac:** `~/.webos-manager/rooms.json`
- **Windows:** `C:\Users\yourname\.webos-manager\rooms.json`

---

## Changes from v1

- Switched from `aiowebostv` to `bscpylgtv` for better API support
- Screenshot support via `client.take_screenshot()`
- Remote button presses via `client.button()`
- Picture/system settings control
- Hidden menu access
- Service menu access
- Device info / PC mode toggling
