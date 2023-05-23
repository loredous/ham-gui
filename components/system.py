from typing import Union
import PySimpleGUI
from components.componentbase import ComponentBase, ButtonColorPresets
from pystemd.systemd1 import Unit

defaults = {
    "button_color":ButtonColorPresets.NORMAL.value,
    "font":"monospace 18 normal",
    "expand_x":True,
    "auto_size_button":False,
    "size":(12,3)
}

class APToggle(ComponentBase):
    _name:str = "AP Toggle"
    _ui_key: str = "ap_toggle"

    def _set_ap_disabled(self):
        self._logger.info(f"Disabling AP")
        self._hostapdsvc.Unit.Stop('replace')
        self._dnsmasqsvc.Unit.Stop(b'replace')
        self.ui_control.update(text="Wifi AP - Off",button_color=ButtonColorPresets.UNKNOWN.value)

    def _set_ap_enabled(self):
        self._logger.info(f"Enabling AP")
        self._hostapdsvc.Unit.Start('replace')
        self._dnsmasqsvc.Unit.Start(b'replace')
        self.ui_control.update(text="Wifi AP - On",button_color=ButtonColorPresets.GOOD.value)

    def _setup(self):
        self._enabled = False
        self._hostapdsvc = Unit('hostapd.service', _autoload=True)
        self._dnsmasqsvc = Unit('dnsmasq.service', _autoload=True)
        self._service_issue = False
        if self._hostapdsvc.Unit.LoadError != (b'', b''):
            self._service_issue = True
            self._logger.error(f'Error loading hostapd service:\n{self._hostapdsvc.Unit.LoadError[0].decode()}\n{self._hostapdsvc.Unit.LoadError[1].decode()}')
        if self._dnsmasqsvc.Unit.LoadError != (b'', b''):
            self._service_issue = True
            self._logger.error(f'Error loading dnsmasq service:\n{self._hostapdsvc.Unit.LoadError[0].decode()}\n{self._hostapdsvc.Unit.LoadError[1].decode()}')
    
    def teardown(self):
        self._hostapdsvc.Unit.Stop(b'replace')
        self._dnsmasqsvc.Unit.Stop(b'replace')


    def _generate_ui_control(self) -> Union[PySimpleGUI.Button, PySimpleGUI.ButtonMenu]:
        return PySimpleGUI.Button(
            "Wifi AP",
            disabled = self._service_issue,
            **defaults
            )
    
    def update_state(self):
        if self._hostapdsvc.Unit.ActiveState == b'inactive':
            if self._enabled:
                self.ui_control.update(button_color=ButtonColorPresets.UNKNOWN.value)
            else:
                self.ui_control.update(button_color=ButtonColorPresets.NORMAL.value)
        else:
            if self._hostapdsvc.Unit.SubState == b'running':
                self.ui_control.update(button_color=ButtonColorPresets.GOOD.value)
            else:
                self.ui_control.update(button_color=ButtonColorPresets.BAD.value)

    def ui_control_interacted(self, value:str = ""):
        self._logger.debug(f"AP Toggle hit")
        self._enabled = not self._enabled
        if self._enabled:
            self._set_ap_enabled()
        else:
            self._set_ap_disabled()
        


class EthernetToggle(ComponentBase):
    _name:str = "EthernetToggle"
    _ui_key: str = "eth_toggle"

    def _generate_ui_control(self) -> Union[PySimpleGUI.Button, PySimpleGUI.ButtonMenu]:
        return PySimpleGUI.ButtonMenu(
            "Eth",
            ["menu",["Off","Private Network","Client Mode"]],
            **defaults
            )
    
    def update_state(self):
        pass

    def ui_control_interacted(self, value:str = ""):
        self._logger.info(f"Ethernet Toggle set to {value}")
        self._ui_control.update(button_text=f"Eth - {value.split(' ')[0]}")



components = [APToggle, EthernetToggle]
