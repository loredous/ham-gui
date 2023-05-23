from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum, IntEnum
from queue import Queue
from typing import Tuple, Union
from pydantic import BaseModel
import PySimpleGUI

class ButtonColorPresets(Enum):
    NORMAL = ('black','grey')
    GOOD = ('black','green')
    UNKNOWN = ('black','yellow')
    BAD = ('black','red')

BUTTON_DEFAULTS = {
    "button_color":ButtonColorPresets.NORMAL.value,
    "font":"monospace 18 normal",
    "expand_x":True,
    "auto_size_button":False,
    "size":(12,3)
}

class ComponentLogMessage(BaseModel):
    class LogMessageLevel(IntEnum):
        DEBUG = 0
        INFO = 1
        WARNING = 2
        ERROR = 3
        FATAL = 4

    level: LogMessageLevel=LogMessageLevel.INFO
    time: datetime = datetime.utcnow()
    message: str
    source: str

class ComponentLogger():
    def send_message(self, message:str, level: ComponentLogMessage.LogMessageLevel = ComponentLogMessage.LogMessageLevel.INFO):
        self._queue.put_nowait(ComponentLogMessage(source=self._name, message=message, level=level))
    
    def info(self, message:str):
        self.send_message(message=message, level=ComponentLogMessage.LogMessageLevel.INFO)

    def warning(self, message:str):
        self.send_message(message=message, level=ComponentLogMessage.LogMessageLevel.WARNING)

    def error(self, message:str):
        self.send_message(message=message, level=ComponentLogMessage.LogMessageLevel.ERROR)

    def fatal(self, message:str):
        self.send_message(message=message, level=ComponentLogMessage.LogMessageLevel.FATAL)
    
    def debug(self, message:str):
        self.send_message(message=message, level=ComponentLogMessage.LogMessageLevel.DEBUG)

    def __init__(self, component_name: str, logging_queue: Queue):
        self._name = component_name
        self._queue = logging_queue

class ComponentBase(ABC):
    _name:str = "ComponentBase"
    _ui_key: str = "base"

    def __init__(self, log_queue: Queue):
        self._logger = ComponentLogger(self._name, log_queue)
        self._ui_control = None
        self._logger.debug(message=f"Component {self._name} initializing!")
        self._setup()

    def _setup(self):
        pass

    def teardown(self):
        pass

    @property
    def ui_control(self) -> Union[PySimpleGUI.Button, PySimpleGUI.ButtonMenu]:
        if not self._ui_control:
            self._logger.debug("Generating new UI control")
            self._ui_control = self._generate_ui_control()
            self._ui_control.Key = self.ui_key
        return self._ui_control

    @property
    def ui_key(self):
        return self._ui_key
    
    @abstractmethod
    def _generate_ui_control(self) -> Union[PySimpleGUI.Button, PySimpleGUI.ButtonMenu]:
        pass
    
    @abstractmethod
    def update_state(self):
        pass

    @abstractmethod
    def ui_control_interacted(self, value:str = ""):
        pass
