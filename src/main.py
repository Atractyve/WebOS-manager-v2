import json
import os
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, DataTable, Input, Label, RichLog
from textual.screen import Screen
from textual.binding import Binding
from bscpylgtv import WebOsClient

CONFIG_FILE = os.path.expanduser("~/.webos-manager/rooms.json")


def load_rooms():
    if not os.path.exists(CONFIG_FILE):
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        return {}
    with open(CONFIG_FILE) as f:
        return json.load(f)


def save_rooms(rooms):
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(rooms, f, indent=2)


def save_client_key(name: str, key: str):
    rooms = load_rooms()
    if name in rooms:
        if isinstance(rooms[name], dict):
            rooms[name]["key"] = key
        else:
            rooms[name] = {"ip": rooms[name], "key": key}
        save_rooms(rooms)


def get_room_ip(room):
    if isinstance(room, dict):
        return room["ip"]
    return room


def get_room_key(room):
    if isinstance(room, dict):
        return room.get("key")
    return None


class RoomTable(DataTable):
    BINDINGS = [
        Binding("space", "select_room", "Connect"),
    ]

    def action_select_room(self):
        self.screen.action_connect()


class MainScreen(Screen):
    BINDINGS = [
        Binding("e", "edit", "Edit Rooms"),
        Binding("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield RoomTable()
        yield Footer()

    def on_mount(self):
        table = self.query_one(RoomTable)
        table.cursor_type = "row"
        table.add_columns("Room", "IP Address")
        self.refresh_table()
        table.focus()

    def refresh_table(self):
        table = self.query_one(RoomTable)
        table.clear()
        rooms = load_rooms()
        for name, room in rooms.items():
            ip = get_room_ip(room)
            table.add_row(name, ip)

    def on_screen_resume(self):
        self.refresh_table()
        self.query_one(RoomTable).focus()

    def action_edit(self):
        self.app.push_screen(EditScreen())

    def action_connect(self):
        table = self.query_one(RoomTable)
        rooms = load_rooms()
        keys = list(rooms.keys())
        if keys and table.cursor_row is not None:
            name = keys[table.cursor_row]
            ip = get_room_ip(rooms[name])
            self.app.push_screen(ConnectScreen(name, ip))


class EditScreen(Screen):
    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back"),
        Binding("a", "add", "Add Room"),
        Binding("d", "delete", "Delete Room"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Edit Rooms - Press A to add, D to delete, ESC to go back")
        yield DataTable()
        yield Footer()

    def on_mount(self):
        table = self.query_one(DataTable)
        table.cursor_type = "row"
        table.add_columns("Room", "IP Address")
        self.refresh_table()
        table.focus()

    def refresh_table(self):
        table = self.query_one(DataTable)
        table.clear()
        rooms = load_rooms()
        for name, room in rooms.items():
            ip = get_room_ip(room)
            table.add_row(name, ip)

    def action_add(self):
        self.app.push_screen(AddRoomScreen())

    def action_delete(self):
        table = self.query_one(DataTable)
        rooms = load_rooms()
        keys = list(rooms.keys())
        if keys and table.cursor_row is not None:
            del rooms[keys[table.cursor_row]]
            save_rooms(rooms)
            self.refresh_table()


class AddRoomScreen(Screen):
    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Room Name:")
        yield Input(placeholder="e.g. Room 1", id="name")
        yield Label("IP Address:")
        yield Input(placeholder="e.g. 192.168.1.101", id="ip")
        yield Footer()

    def on_mount(self):
        self.query_one("#name", Input).focus()

    def on_input_submitted(self, event: Input.Submitted):
        if event.input.id == "name":
            self.query_one("#ip", Input).focus()
        elif event.input.id == "ip":
            name = self.query_one("#name", Input).value
            ip = self.query_one("#ip", Input).value
            if name and ip:
                rooms = load_rooms()
                rooms[name] = {"ip": ip, "key": None}
                save_rooms(rooms)
                self.app.pop_screen()


class ConnectScreen(Screen):
    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back"),
    ]

    def __init__(self, name: str, ip: str):
        super().__init__()
        self.room_name = name
        self.ip = ip

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label(f"Connecting to {self.room_name} ({self.ip})...")
        yield Footer()

    def on_mount(self):
        self.run_worker(self.connect())

    async def connect(self):
        try:
            rooms = load_rooms()
            room = rooms.get(self.room_name)
            client_key = get_room_key(room)

            client = await WebOsClient.create(
                self.ip,
                client_key=client_key,
                ping_interval=None,
                states=[],
            )
            await client.connect()

            if client.client_key and client.client_key != client_key:
                save_client_key(self.room_name, client.client_key)

            self.app.push_screen(ControlScreen(self.room_name, self.ip, client))
        except Exception as e:
            self.query_one(Label).update(f"Failed to connect: {e}")


class TerminalInput(Input):
    def _on_key(self, event) -> None:
        if event.key == "up":
            event.prevent_default()
            self.screen.action_history_up()
        elif event.key == "down":
            event.prevent_default()
            self.screen.action_history_down()
        else:
            super()._on_key(event)


class ControlScreen(Screen):
    BINDINGS = [
        Binding("escape", "app.pop_screen", "Disconnect"),
    ]

    def __init__(self, name: str, ip: str, client: WebOsClient):
        super().__init__()
        self.room_name = name
        self.ip = ip
        self.client = client
        self.history = []
        self.history_index = -1

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label(f"Connected to {self.room_name} ({self.ip})  |  ESC to disconnect")
        yield RichLog(id="output", wrap=True, highlight=True, markup=True)
        yield TerminalInput(placeholder=">>> ", id="cmd")
        yield Footer()

    def on_mount(self):
        self.query_one("#cmd", TerminalInput).focus()
        self.query_one(RichLog).write(
            "Type any command e.g: client.power_off()  |  client.volume_up()  |  client.take_screenshot()"
        )

    def action_history_up(self):
        if self.history and self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.query_one("#cmd", TerminalInput).value = self.history[-(self.history_index + 1)]

    def action_history_down(self):
        cmd_input = self.query_one("#cmd", TerminalInput)
        if self.history_index > 0:
            self.history_index -= 1
            cmd_input.value = self.history[-(self.history_index + 1)]
        elif self.history_index == 0:
            self.history_index = -1
            cmd_input.value = ""

    def on_input_submitted(self, event: Input.Submitted):
        cmd = event.value
        if not cmd:
            return
        self.history.append(cmd)
        self.history_index = -1
        self.query_one("#cmd", TerminalInput).clear()
        self.query_one(RichLog).write(f"[bold cyan]>>> {cmd}[/bold cyan]")
        self.run_worker(self.run_command(cmd))

    async def run_command(self, cmd: str):
        log = self.query_one(RichLog)
        try:
            client = self.client
            result = await eval(cmd)
            if result is None:
                log.write("[green]OK[/green]")
            elif isinstance(result, (dict, list)):
                log.write(json.dumps(result, indent=2, default=str))
            else:
                log.write(str(result))
        except Exception as e:
            log.write(f"[red]Error: {e}[/red]")


class WebOSManager(App):
    def on_mount(self):
        self.push_screen(MainScreen())


if __name__ == "__main__":
    app = WebOSManager()
    app.run()
