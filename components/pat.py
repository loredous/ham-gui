from typing import Union
from components.componentbase import ComponentBase, ButtonColorPresets, BUTTON_DEFAULTS
import PySimpleGUI
from pystemd.systemd1 import Unit


class PatToggle(ComponentBase):
    _name:str = "Pat Toggle"
    _ui_key: str = "pat_toggle"

    def _set_pat_disabled(self):
        self._logger.info(f"Disabling Pat")
        self._patsvc.Unit.Stop('replace')
        self.ui_control.update(text="Pat - Off",button_color=ButtonColorPresets.UNKNOWN.value)

    def _set_pat_enabled(self):
        self._logger.info(f"Enabling Pat")
        self._patsvc.Unit.Start('replace')
        self.ui_control.update(text="Pat - On",button_color=ButtonColorPresets.GOOD.value)

    def _setup(self):
        self._enabled = False
        self._patsvc = Unit('pat@k0jlb.service', _autoload=True)
        if self._patsvc.Unit.LoadError != (b'', b''):
            self._service_issue = True
            self._logger.error(f'Error loading pat service:\n{self._patsvc.Unit.LoadError[0].decode()}\n{self._patsvc.Unit.LoadError[1].decode()}')
        else:
            self._service_issue = False

    def teardown(self):
        self._patsvc.Unit.Stop(b'replace')


    def _generate_ui_control(self) -> Union[PySimpleGUI.Button, PySimpleGUI.ButtonMenu]:
        return PySimpleGUI.Button(
            "Pat",
            disabled = self._service_issue,
            **BUTTON_DEFAULTS
            )
    
    def update_state(self):
        if self._patsvc.Unit.ActiveState == b'inactive':
            if self._enabled:
                self.ui_control.update(button_color=ButtonColorPresets.UNKNOWN.value)
            else:
                self.ui_control.update(button_color=ButtonColorPresets.NORMAL.value)
        else:
            if self._patsvc.Unit.SubState == b'running':
                self.ui_control.update(button_color=ButtonColorPresets.GOOD.value)
            else:
                self.ui_control.update(button_color=ButtonColorPresets.BAD.value)

    def ui_control_interacted(self, value:str = ""):
        self._logger.debug(f"Pat Toggle hit")
        self._enabled = not self._enabled
        if self._enabled:
            self._set_pat_enabled()
        else:
            self._set_pat_disabled()
        
components = [PatToggle]