from kivy.app import App
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem

from gui.credential_stuffing.credential_stuffing_view import CredentialStuffingView
from gui.global_variables import default_tab_width
from gui.utils.console_view import ConsoleView
from gui.csrf_grab_token.crsf_token_view import CSRFTokenView
from gui.global_variables import  default_tab_width
from gui.least_privilege.least_privilege_view import LeastPrivilegeTokenView

Window.size = (1600, 800)

class Gui(App):
    def build(self):
        self.window = GridLayout()
        self.window.cols = 1
        self.window.add_widget(MainView())

        return self.window


class MainView(GridLayout):
    def __init__(self, **kwargs):
        super(MainView, self).__init__(**kwargs)
        self.cols = 3

        console_view = ConsoleView("Console", "Clear Console")
        report_view = ConsoleView("Report", "Clear Report")

        self.add_widget(ParametersView(console_view, report_view))
        self.add_widget(console_view)
        self.add_widget(report_view)


class ParametersView(GridLayout):
        super(ParametersView, self).__init__(**kwargs)
        self.cols = 1
        self.rows = 2


class TabsView(TabbedPanel):
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
