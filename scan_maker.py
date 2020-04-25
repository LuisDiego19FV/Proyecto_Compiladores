from cocol_reader import CocolReader as cr
from cocol_writer import CocolWriter as cw
import PySimpleGUI as sg
import sys

def display(reader, writer):
    layout = [  [sg.Text('Characters:')],
            [sg.MLine(size=(100,8), key='-OUTPUT1-'+sg.WRITE_ONLY_KEY)],
            [sg.Text('Keywords:')],
            [sg.MLine(size=(100,8), key='-OUTPUT2-'+sg.WRITE_ONLY_KEY)],
            [sg.Text('Tokens:')],
            [sg.MLine(size=(100,8), key='-OUTPUT3-'+sg.WRITE_ONLY_KEY)],
            [sg.Button('Ok')]  ]

    window = sg.Window('Scanner generado', layout, finalize=True)

    for i in reader.comp_chars:
        window['-OUTPUT1-'+sg.WRITE_ONLY_KEY].print(i[0] + " -> " + i[1])
        window['-OUTPUT1-'+sg.WRITE_ONLY_KEY].print(i[2])
    
    for i in reader.comp_keywords:
        window['-OUTPUT2-'+sg.WRITE_ONLY_KEY].print(i[0] + " -> " + i[1])
        window['-OUTPUT2-'+sg.WRITE_ONLY_KEY].print(i[3])
    
    for i in reader.comp_tokens:
        window['-OUTPUT3-'+sg.WRITE_ONLY_KEY].print(i[0] + " -> " + i[1])
        window['-OUTPUT3-'+sg.WRITE_ONLY_KEY].print(i[3])

    # Event loop
    while True: 
        event, values = window.read()
        if event in (None, 'Ok'):
            break
    
    # Exit
    window.close()

# Theme
sg.theme('DarkAmber')

# Open doc
fname = sg.popup_get_file('Document to open')

# Split Exit | Read File
if not fname:
    raise SystemExit()
else:
    reader = cr(fname)
    reader.startReading()

    writer = cw("scanner.py")
    writer.setKeywords(reader.comp_keywords)
    writer.setTokens(reader.comp_tokens)
    writer.setIgnoreChars(reader.comp_ignore)
    writer.startWriting()

    sg.popup('Scanner creado correctamente \nArchivo creado/modificado: scanner.py')

    display(reader, writer)