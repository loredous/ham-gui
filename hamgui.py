import itertools
from components.componentbase import ComponentBase, ComponentLogMessage
import pkgutil
from queue import Queue, Empty
import sys
import PySimpleGUI as sg

WIDTH = 480
HEIGHT = 800

log_queue = Queue()
modules = []
active_components = []

def load_components():
    dirname = "components"
    for importer, package_name, _ in pkgutil.iter_modules([dirname]):
        full_package_name = '%s.%s' % (dirname, package_name)
        if full_package_name not in sys.modules:
            module = importer.find_module(package_name
                        ).load_module(package_name)
            modules.append(module)


def setup_window() -> sg.Window:
    buttons = []
    for module in modules:
        if hasattr(module, "components"):
            for component in module.components:
                if issubclass(component,ComponentBase):
                    comp = component(log_queue=log_queue)
                    active_components.append(comp)
                    buttons.append(comp.ui_control)
    column1 = sg.Column([[]],expand_x=True)
    column2 = sg.Column([[]],expand_x=True)
    exit_button = sg.Button('Exit',key="--exit--",button_color=("black","white"), font=("monospace 22 normal"), expand_x=True)
    columns = [column1, column2]
    for button, col in zip(buttons, itertools.cycle(columns)):
        col.add_row(button)
    new_window = sg.Window("HamPi",[columns,[exit_button]],no_titlebar=True,keep_on_top=True,size=(WIDTH,HEIGHT)) # TODO: Make screen size auto-detect
    return new_window

def handle_pending_logs():
    try:
        while item := log_queue.get_nowait():
            print(f"{item.time} {item.source}[{item.level.name}] {item.message}")
    except Empty:
        return

def handle_window_event(event, values):
    if event == sg.WIN_CLOSED or event == "--exit--":
            return False
    for component in active_components:
        if event == component.ui_key:
            component.ui_control_interacted(values[event])
    return True

def handle_status_updates():
    for component in active_components:
        component.update_state()
    window.refresh()



def event_loop(window: sg.Window):
    continuing = True
    while continuing:
        handle_pending_logs()
        handle_status_updates()
        event, values = window.read(timeout=1000)
        if event != "timeout_key":
            continuing = handle_window_event(event,values)
    window.close()


if __name__ == "__main__":
    load_components()
    window = setup_window()
    event_loop(window=window)
    

