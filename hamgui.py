import random
import PySimpleGUI as sg
button1 = sg.Button("Ok",expand_x=True)
button2 = sg.Button('Not OK',expand_x=True)
window = sg.Window("MyWindow",[[button1,button2]],no_titlebar=True,keep_on_top=True)
window.finalize()
window.maximize()
colors = [("black","red"),("black","yellow"),("black","green")]
while True:
    event,values = window.read()
    if event == sg.WIN_CLOSED or event == 'Ok':
        break
    if event == "Not OK":
        window['Ok'].update(button_color = random.choice(colors))

window.close()