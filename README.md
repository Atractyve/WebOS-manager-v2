# WebOS Manager v2

A terminal UI for managing and controlling LG WebOS TVs over the network. Now powered by [bscpylgtv](https://github.com/chros73/bscpylgtv) for better screenshot support and more features.

---

## Requirements

- Python 3.11 or higher
- Git

---

## Installation

### Arch Linux

```bash
sudo pacman -S git python

git clone https://github.com/Atractyve/WebOS-Manager-v2.git
cd WebOS-Manager-v2

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
cd WebOS-Manager-v2

# bash/zsh:
source .venv/bin/activate
# fish:
source .venv/bin/activate.fish

python src/main.py
```

### Windows

```
git clone https://github.com/Atractyve/WebOS-Manager-v2.git
cd WebOS-Manager-v2

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

### Volume

| Command | Description |
| --- | --- |
| `client.volume_up()` | Raise volume by 1 |
| `client.volume_down()` | Lower volume by 1 |
| `client.set_volume(50)` | Set volume to a specific level (0-100) |
| `client.set_mute(True)` | Mute |
| `client.set_mute(False)` | Unmute |
| `client.get_volume()` | Get current volume level |

### Power

| Command | Description |
| --- | --- |
| `client.power_off()` | Turn off the TV |
| `client.screen_off()` | Turn off the screen (keep TV on) |
| `client.screen_on()` | Turn the screen back on |

### Screenshot

| Command | Description |
| --- | --- |
| `client.take_screenshot()` | Take a screenshot (returns imageUri) |

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
| `client.get_apps_all()` | List all installed apps |
| `client.get_current_app()` | Get the currently open app |
| `client.launch_app("app.id.here")` | Launch an app by ID |
| `client.close_app("app.id.here")` | Close an app by ID |

### Inputs

| Command | Description |
| --- | --- |
| `client.get_inputs()` | List all available inputs (HDMI etc.) |
| `client.set_input("HDMI_1")` | Switch to a specific input |

### Info & State

| Command | Description |
| --- | --- |
| `client.get_system_info()` | System info |
| `client.get_software_info()` | Firmware and software version |
| `client.get_power_state()` | Current power state |
| `client.get_sound_output()` | Current audio output |

### Notifications

| Command | Description |
| --- | --- |
| `client.send_message("Hello!")` | Show a toast notification on the TV |

### Raw SSAP Requests

| Command | Description |
| --- | --- |
| `client.request("ssap://uri/here")` | Send any SSAP request |
| `client.request("ssap://uri", {"key": "val"})` | SSAP request with payload |

---

## Config File

Rooms are stored at:

- **Linux/Mac:** `~/.webos-manager/rooms.json`
- **Windows:** `C:\Users\yourname\.webos-manager\rooms.json`

---

## Changes from v1

- Switched from `aiowebostv` to `bscpylgtv` for better API support
- Screenshot support via `client.take_screenshot()`
- More available commands (calibration, picture settings, etc.)
