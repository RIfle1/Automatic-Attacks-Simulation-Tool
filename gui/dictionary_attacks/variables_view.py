from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

from dictionary_attacks.global_variables import USERNAME_KEY, PASSWORD_KEY, LOGIN_SUCCESS_KEY, username_variable, \
    password_variable, login_success_variable
from gui.dictionary_attacks.custom_layout import CustomDynamicLayout, CustomHeightLayout
from gui.global_variables import default_font_size, title_font_size


class VariablesView(GridLayout):
    def __init__(self, **kwargs):
        super(VariablesView, self).__init__(**kwargs)
        self.cols = 1
        self.rows = 2
        self.size_hint = (1, 0.3)

        label_layout = CustomHeightLayout()
        label = Label(
            text="Variables",
            font_size=title_font_size,
        )
        label_layout.add_widget(label)

        self.variables_scroll_view = VariablesScrollView()

        self.variables_scroll_view.add_variable(VariableView(variable=USERNAME_KEY, default_value=username_variable))
        self.variables_scroll_view.add_variable(VariableView(variable=PASSWORD_KEY, default_value=password_variable))
        self.variables_scroll_view.add_variable(VariableView(variable=LOGIN_SUCCESS_KEY, default_value=login_success_variable))

        self.add_widget(label_layout)
        self.add_widget(self.variables_scroll_view)

    def get_variable_values(self, variable):
        for variable_view in self.variables_scroll_view.variable_layout.children:
            if variable_view.get_variable_label() == variable:
                return variable_view.get_variable_value()


class VariablesScrollView(ScrollView):
    def __init__(self, **kwargs):
        super(VariablesScrollView, self).__init__(**kwargs)
        self.size_hint = (1, 1)
        self.variable_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.variable_layout.bind(minimum_height=self.variable_layout.setter('height'))

        self.add_widget(self.variable_layout)

    def add_variable(self, variable):
        self.variable_layout.add_widget(variable)


class VariableView(GridLayout):
    def __init__(self, variable, default_value, **kwargs):
        super(VariableView, self).__init__(**kwargs)

        self.cols = 2
        self.rows = 1
        self.size_hint_max_y = 35
        self.size_hint_min_y = 35

        variable_label_layout = CustomDynamicLayout(size_x=0.5, size_y=1, padding=1)
        self.variable_label = Label(
            text=variable,
            font_size=default_font_size,
        )
        variable_label_layout.add_widget(self.variable_label)

        variable_input_layout = CustomDynamicLayout(size_x=0.5, size_y=1, padding=1)
        self.variable_input = TextInput(
            text=default_value,
            hint_text="Value",
            multiline=False,
            font_size=default_font_size,
        )
        variable_input_layout.add_widget(self.variable_input)

        self.add_widget(variable_label_layout)
        self.add_widget(variable_input_layout)

    def get_variable_value(self):
        return self.variable_input.text

    def get_variable_label(self):
        return self.variable_label.text