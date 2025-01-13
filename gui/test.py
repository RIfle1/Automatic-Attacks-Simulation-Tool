import threading
import time

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


class MyApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        # Create a button that starts the thread
        self.button = Button(text="Start Background Task")
        self.button.bind(on_press=self.start_thread)

        # Create a label to show status
        self.status_label = Label(text="Status: Not Started")

        # Add widgets to layout
        self.layout.add_widget(self.button)
        self.layout.add_widget(self.status_label)

        return self.layout

    def start_thread(self, instance):
        # Disable the button after it's pressed
        self.button.disabled = True

        # Start the background thread
        threading.Thread(target=self.background_task).start()

    def background_task(self):
        # Simulate a long-running task
        for i in range(5):
            time.sleep(1)  # Simulate some work
            print(f"Background task running: {i + 1} seconds")

            # Use Clock to schedule the update of the UI from the main thread
            # Clock.schedule_once(self.update_label, 0)
            self.update_label(str(i))

        # Re-enable the button after task is done
        Clock.schedule_once(self.enable_button, 0)

    def update_label(self, text):
        # This method updates the label from the main thread
        self.status_label.text = text

    def enable_button(self, dt):
        # Re-enable the button after the task
        self.button.disabled = False


if __name__ == "__main__":
    MyApp().run()