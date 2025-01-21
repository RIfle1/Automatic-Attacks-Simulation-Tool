from kivy.app import App
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.clock import Clock

from gui.credential_stuffing.credential_stuffing_view import CredentialStuffingView
from gui.csrf_grab_token.crsf_token_view import CSRFTokenView
from gui.dos_attack.dos_attack_view import DoSAttackView
from gui.global_variables import default_tab_width
from gui.jwt.jwt_attack_view import JwtAttackView
from gui.jwt.jwt_pentest_view import JwtPentestView
from gui.least_privilege.least_privilege_view import LeastPrivilegeTokenView
from gui.sql_injection.sql_injection_view import SqlInjectionView
from gui.utils.console_view import ConsoleView
from gui.cors_exploitation.cors_exploitation_view import CORSExploitationView
from gui.docker_trojan.docker_trojan_view import DockerTrojanView, app # DO NOT REMOVE app FROM IMPORT

class Gui(App):
    def build(self):
        Clock.schedule_once(self.set_window_size, 0)
        self.window = GridLayout()
        self.window.cols = 1
        self.window.add_widget(MainView())
        return self.window

    def set_window_size(self, dt):
        Window.size = (1600, 800)

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
        crsf_token_grab_tab.add_widget(CSRFTokenView(console_view,report_view))
        self.add_widget(crsf_token_grab_tab)

        # Tab 3: Least Privilege
        least_privilege_tab = TabbedPanelItem(text="Least Privilege")
        least_privilege_tab.add_widget(LeastPrivilegeTokenView(console_view,report_view))
        self.add_widget(least_privilege_tab)

        # Tab 4: JWT Attack
        jwt_attack_tab = TabbedPanelItem(text="JWT Attack")
        jwt_attack_tab.add_widget(JwtAttackView(console_view, report_view))
        self.add_widget(jwt_attack_tab)

        # Tab 5: JWT Pentest
        jwt_pentest_tab = TabbedPanelItem(text="JWT Pentest")
        jwt_pentest_tab.add_widget(JwtPentestView(console_view, report_view))
        self.add_widget(jwt_pentest_tab)

        self.set_def_tab(credential_stuffing_tab)

        # Tab 6: SQL Injection Tab
        sql_injection_tab = TabbedPanelItem(text="SQL")
        sql_injection_tab.add_widget(SqlInjectionView(console_view, report_view))
        self.add_widget(sql_injection_tab)

        # Tab 7: Denial of Service
        dos_tab = TabbedPanelItem(text="DoS Attack")
        dos_tab.add_widget(DoSAttackView(console_view, report_view))
        self.add_widget(dos_tab)

        # Tab 8: Docker Trojan
        docker_trojan_tab = TabbedPanelItem(text="Docker Trojan")
        docker_trojan_tab.add_widget(DockerTrojanView(console_view, report_view))
        self.add_widget(docker_trojan_tab)

        # Tab 9: CORS Exploitation
        cors_exploitation_tab = TabbedPanelItem(text="CORS Exploitation")
        cors_exploitation_tab.add_widget(CORSExploitationView(console_view,report_view))
        self.add_widget(cors_exploitation_tab)

if __name__ == "__main__":
    Gui().run()