from kivy.app import App
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem

from gui.credential_stuffing.credential_stuffing_view import CredentialStuffingView
from gui.csrf_grab_token.crsf_token_view import CSRFTokenView
from gui.global_variables import default_tab_width
from gui.jwt.jwt_attack_view import JwtAttackView
from gui.jwt.jwt_pentest_view import JwtPentestView
from gui.least_privilege.least_privilege_view import LeastPrivilegeTokenView
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

        # Tab 1: Credential Stuffing
        credential_stuffing_tab = TabbedPanelItem(text="Credential Stuffing")
        credential_stuffing_tab.add_widget(CredentialStuffingView(console_view, report_view))
        self.add_widget(credential_stuffing_tab)

        # Tab 2: CSRF Token
        crsf_token_grab_tab = TabbedPanelItem(text="CSRF Token Grab")
        crsf_token_grab_tab.add_widget(CSRFTokenView(console_view))
        self.add_widget(crsf_token_grab_tab)

        # Tab 3: Least Privilege
        least_privilege_tab = TabbedPanelItem(text="Least Privilege")
        least_privilege_tab.add_widget(LeastPrivilegeTokenView(console_view))
        self.add_widget(least_privilege_tab)

        # Tab 4: JWT Attack
        jwt_attack_tab = TabbedPanelItem(text="JWT Attack")
        jwt_attack_tab.add_widget(JwtAttackView(console_view))
        self.add_widget(jwt_attack_tab)

        # Tab 5: JWT Pentest
        jwt_pentest_tab = TabbedPanelItem(text="JWT Pentest")
        jwt_pentest_tab.add_widget(JwtPentestView(console_view))
        self.add_widget(jwt_pentest_tab)

        self.set_def_tab(credential_stuffing_tab)

        # Tab 5: Denial of Service
        tab4 = TabbedPanelItem(text="SQL")
        tab4.add_widget(SqlInjectionView(console_view))
        self.add_widget(tab4)
        # Tab 4: Denial of Service
        tab5 = TabbedPanelItem(text="DoS Attack")
        tab5.add_widget(DoSAttackView(console_view))
        self.add_widget(tab5)


if __name__ == "__main__":
    Gui().run()
