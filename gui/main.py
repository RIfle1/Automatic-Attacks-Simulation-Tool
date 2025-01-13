from kivy.app import App
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem

from gui.credential_stuffing.credential_stuffing_view import CredentialStuffingView
from gui.global_variables import default_tab_width
from gui.utils.console_view import ConsoleView

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
    def __init__(self, console_view: ConsoleView, report_view: ConsoleView, **kwargs):
        super(ParametersView, self).__init__(**kwargs)
        self.cols = 1
        self.rows = 2
        self.add_widget(TabsView(console_view, report_view))


class TabsView(TabbedPanel):
    def __init__(self, console_view: ConsoleView, report_view: ConsoleView, **kwargs):
        super(TabsView, self).__init__(**kwargs)
        self.do_default_tab = False
        self.tab_width = default_tab_width

        tab1 = TabbedPanelItem(text="Credential Stuffing")
        tab1.add_widget(CredentialStuffingView(console_view, report_view))
        self.add_widget(tab1)

        tab2 = TabbedPanelItem(text="Tab 2")
        tab2.add_widget(Label(text="Tab 2"))
        self.add_widget(tab2)

        self.set_def_tab(tab1)


if __name__ == "__main__":
    Gui().run()
