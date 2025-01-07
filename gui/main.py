from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem

from gui.credential_stuffing.console_view import ConsoleView
from gui.credential_stuffing.credential_stuffing_view import CredentialStuffingView
from gui.csrf_grab_token.crsf_token_view import CSRFTokenView
from gui.global_variables import  default_tab_width
from gui.least_privilege.least_privilege_view import LeastPrivilegeTokenView


class Gui(App):
    def build(self):
        self.window = GridLayout()
        self.window.cols = 1
        self.window.add_widget(MainView())

        return self.window


class MainView(GridLayout):
    def __init__(self, **kwargs):
        super(MainView, self).__init__(**kwargs)
        self.cols = 2

        console_view = ConsoleView()

        self.add_widget(ParametersView(console_view))
        self.add_widget(console_view)


class ParametersView(GridLayout):
    def __init__(self, console_view: ConsoleView, **kwargs):
        super(ParametersView, self).__init__(**kwargs)
        self.cols = 1
        self.rows = 2
        self.add_widget(TabsView(console_view))


class TabsView(TabbedPanel):
    def __init__(self, console_view: ConsoleView, **kwargs):
        super(TabsView, self).__init__(**kwargs)
        self.do_default_tab = False
        self.tab_width = default_tab_width

        # Tab 1: Credential Stuffing
        tab1 = TabbedPanelItem(text="Credential Stuffing")
        tab1.add_widget(CredentialStuffingView(console_view))
        self.add_widget(tab1)

        # Tab 2: CSRF Token
        tab2 = TabbedPanelItem(text="CSRF Token Grab")
        tab2.add_widget(CSRFTokenView(console_view))
        self.add_widget(tab2)

        # Tab 3: Least Privilege
        tab3 = TabbedPanelItem(text="Least Privilege")
        tab3.add_widget(LeastPrivilegeTokenView(console_view))
        self.add_widget(tab3)

        self.set_def_tab(tab1)


if __name__ == "__main__":
    Gui().run()
