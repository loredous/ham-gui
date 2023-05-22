from typing import Union
import PySimpleGUI
from components.componentbase import ComponentBase, ButtonColorPresets

class WifiToggle(ComponentBase):
    _name:str = "WifiToggle"
    _ui_key: str = "wifi_toggle"

    def _set_wifi_disabled(self):
        pass

    def _set_wifi_ap(self):
        pass

    def _set_wifi_client(self):
        pass

    def _setup(self):
        self._wifi = pywifi.PyWiFi()

    def _generate_ui_control(self) -> Union[PySimpleGUI.Button, PySimpleGUI.ButtonMenu]:
        return PySimpleGUI.ButtonMenu(
            "Wifi",
            ["menu",["Off","AP Mode","Client Mode"]],
            button_color=ButtonColorPresets.NORMAL,
            font=("monospace 22 normal"), 
            expand_x=True,
            auto_size_button=False
            )
    
    def update_state(self):
        pass

    def ui_control_interacted(self, value:str = ""):
        self._logger.info(f"Wifi Toggle set to {value}")
        match value:
            case "Off":
                self._set_wifi_disabled()
            case "AP Mode":
                self._set_wifi_ap()
            case "Client Mode":
                self._set_wifi_client()
        self._ui_control.update(button_text=f"Wifi - {value.split(' ')[0]}")


class EthernetToggle(ComponentBase):
    _name:str = "EthernetToggle"
    _ui_key: str = "eth_toggle"

    def _generate_ui_control(self) -> Union[PySimpleGUI.Button, PySimpleGUI.ButtonMenu]:
        return PySimpleGUI.ButtonMenu(
            "Eth",
            ["menu",["Off","Private Network","Client Mode"]],
            button_color=ButtonColorPresets.NORMAL,
            font=("monospace 22 normal"), 
            expand_x=True,
            auto_size_button=False
            )
    
    def update_state(self):
        pass

    def ui_control_interacted(self, value:str = ""):
        self._logger.info(f"Ethernet Toggle set to {value}")
        self._ui_control.update(button_text=f"Eth - {value.split(' ')[0]}")



components = [WifiToggle, EthernetToggle]
