import jwt
import datetime
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.switch import Switch
from kivy.uix.scrollview import ScrollView

from gui.global_variables import default_font_size, title_font_size


class JwtAttackView(GridLayout):
    def __init__(self, console_view, report_view, **kwargs):
        super(JwtAttackView, self).__init__(**kwargs)
        self.cols = 1
        self.rows = 15
        self.padding = 10
        self.spacing = 10

        self.console_view = console_view
        self.report_view = report_view
        self.fields = {}  # Store fields with their layouts

        self.add_widget(Label(text="JWT Secret", size_hint=(1, None), height=30, font_size=title_font_size))

        # Set default secret
        self.secret_input = TextInput(
            hint_text="Enter JWT Secret",
            text="AxNjIsInN1YiI6ImxkZWxhdHVsbGF5ZUBqdW5pb3Jpc2VwLmNvbSIsIn",
            multiline=False,
            size_hint=(1, None),
            height=30,
            font_size=default_font_size
        )
        self.add_widget(self.secret_input)

        self.add_widget(Label(text="Build Payload", size_hint=(1, None), height=30, font_size=title_font_size))

        self.build_switch = Switch(active=True, size_hint=(1, None), height=30)
        self.build_switch.bind(active=self.on_switch_active)
        self.add_widget(self.build_switch)

        # Add scrollable fields layout
        self.fields_layout = GridLayout(cols=1, size_hint_y=None)
        self.fields_layout.bind(minimum_height=self.fields_layout.setter('height'))

        # Add column labels
        self.add_column_labels()

        # Add static fields
        self.add_static_field("exp", "100000")
        self.add_static_field("sub", "ldelatullaye@juniorisep.com")
        self.add_static_field("roles", "ROLE_ADMIN", is_list=True)

        self.scroll_view = ScrollView(size_hint=(1, None), height=200)
        self.scroll_view.add_widget(self.fields_layout)
        self.add_widget(self.scroll_view)

        self.add_field_button = Button(text="Add Custom Field", size_hint=(1, None), height=30, font_size=default_font_size)
        self.add_field_button.bind(on_press=self.add_custom_field)
        self.add_widget(self.add_field_button)

        self.payload_input = TextInput(
            hint_text="Enter Payload as JSON",
            multiline=True,
            size_hint=(1, None),
            height=100,
            font_size=default_font_size
        )
        self.add_widget(self.payload_input)

        self.generate_button = Button(text="Generate JWT", size_hint=(1, None), height=30, font_size=default_font_size)
        self.generate_button.bind(on_press=self.generate_jwt)
        self.add_widget(self.generate_button)

        self.on_switch_active(self.build_switch, self.build_switch.active)

    def add_column_labels(self):
        """
        Add labels for the columns: Active, List.
        """
        header_layout = GridLayout(cols=2, size_hint_y=None, height=30)
        active_label = Label(text="Active", size_hint=(0.5, None), height=30, halign='left')
        list_label = Label(text="List", size_hint=(0.5, None), height=30, halign='right')
        active_label.bind(size=active_label.setter('text_size'))
        list_label.bind(size=list_label.setter('text_size'))
        header_layout.add_widget(active_label)
        header_layout.add_widget(list_label)
        self.fields_layout.add_widget(header_layout)

    def add_static_field(self, field_name, default_value="", is_list=False):
        """
        Add a static field that cannot be deleted or renamed.
        """
        layout = GridLayout(cols=4, size_hint_y=None, height=30)

        checkbox = CheckBox(active=True, size_hint=(None, None), size=(30, 30))
        list_checkbox = CheckBox(active=is_list, size_hint=(None, None), size=(30, 30))  # List toggle
        value_input = TextInput(
            hint_text=f"Enter Value for {field_name}",
            text=default_value,
            multiline=False,
            size_hint=(0.6, None),
            height=30,
            font_size=default_font_size
        )

        layout.add_widget(checkbox)
        layout.add_widget(value_input)
        layout.add_widget(list_checkbox)  # List toggle

        self.fields[field_name] = {
            "layout": layout,
            "checkbox": checkbox,
            "list_checkbox": list_checkbox,
            "value_input": value_input
        }
        self.fields_layout.add_widget(layout)

    def add_field(self, field_name, default_value="", is_custom=True, is_list=False):
        """
        Add a field with options to rename and delete.
        """
        layout = GridLayout(cols=5, size_hint_y=None, height=30)

        checkbox = CheckBox(active=True, size_hint=(None, None), size=(30, 30))
        name_input = TextInput(
            text=field_name if is_custom else "",
            hint_text="Field Name" if is_custom else "",
            multiline=False,
            size_hint=(0.2, None),
            height=30,
            font_size=default_font_size
        )
        name_input.disabled = not is_custom

        value_input = TextInput(
            hint_text=f"Enter Value for {field_name}",
            text=default_value,
            multiline=False,
            size_hint=(0.4, None),
            height=30,
            font_size=default_font_size
        )
        list_checkbox = CheckBox(active=is_list, size_hint=(None, None), size=(30, 30))  # List toggle

        delete_button = Button(text="Delete", size_hint=(None, None), size=(80, 30))
        delete_button.bind(on_press=lambda _: self.delete_field(field_name, layout))

        layout.add_widget(checkbox)
        layout.add_widget(name_input)
        layout.add_widget(value_input)
        layout.add_widget(list_checkbox)  # List toggle
        layout.add_widget(delete_button)

        self.fields[field_name] = {
            "layout": layout,
            "checkbox": checkbox,
            "name_input": name_input,
            "value_input": value_input,
            "list_checkbox": list_checkbox
        }
        self.fields_layout.add_widget(layout)

    def add_custom_field(self, _):
        """
        Add a new custom field with an editable name and value.
        """
        custom_field_name = f"CustomField{len(self.fields) + 1}"
        self.add_field(custom_field_name)

    def delete_field(self, field_name, layout):
        """
        Delete a field from the UI and dictionary.
        """
        if field_name in self.fields:
            self.fields_layout.remove_widget(layout)
            del self.fields[field_name]

    def on_switch_active(self, _, value):
        self.payload_input.disabled = value
        for field in self.fields.values():
            field["checkbox"].disabled = not value
            if "name_input" in field:
                field["name_input"].disabled = not value
            field["value_input"].disabled = not value
            field["list_checkbox"].disabled = not value
        self.add_field_button.disabled = not value

    def generate_jwt(self, _):
        secret = self.secret_input.text.strip()
        payload = {}

        print(f"[DEBUG] Secret: {secret}")

        if self.build_switch.active:
            # Build the payload from the fields
            for field_name, field_widgets in self.fields.items():
                checkbox = field_widgets["checkbox"]
                value_input = field_widgets["value_input"]
                list_checkbox = field_widgets["list_checkbox"]
                name = field_widgets.get("name_input", field_name).text.strip() if "name_input" in field_widgets else field_name

                if checkbox.active and value_input.text.strip():
                    value = value_input.text.strip()
                    if list_checkbox.active:  # Convert to list if list checkbox is checked
                        value = value.split(',')
                    if name == "exp":  # Special handling for exp
                        try:
                            value = int((datetime.datetime.now(datetime.timezone.utc) +
                                         datetime.timedelta(seconds=int(value))).timestamp())
                        except ValueError:
                            self.console_view.add_text_schedule("Invalid expiration time.")
                            return
                    payload[name] = value

        else:
            # Use custom JSON payload
            try:
                payload = eval(self.payload_input.text)
            except Exception as e:
                self.console_view.add_text_schedule(f"Error in payload: {e}")
                return

        print(f"[DEBUG] Final Payload: {payload}")

        # Generate JWT
        try:
            token = jwt.encode(payload, secret, algorithm="HS256")
            self.console_view.add_text_schedule(f"Generated JWT: {token}")
            self.report_view.add_text_schedule(f"Generated JWT: {token}")
        except Exception as e:
            self.console_view.add_text_schedule(f"Error: {e}")
            self.report_view.add_text_schedule(f"Error: {e}")