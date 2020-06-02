# fake_parser.py
# By: Luis Diego Fernandez
# The program is used for making a scanner.py file. This is made by using a Cocol file
# that specified the compiler.
from cocol_reader import CocolReader as cr
from cocol_writer import CocolWriter as cw
import PySimpleGUI as sg
import sys
import os

# display(reader(), writer())
# The function is used to display the content in the reader and writer in a simply gui.
def display(reader, writer):
    # Layout
    layout = [  [sg.Text('Characters:')],
            [sg.MLine(size=(100,8), key='-OUTPUT1-'+sg.WRITE_ONLY_KEY)],
            [sg.Text('Keywords:')],
            [sg.MLine(size=(100,8), key='-OUTPUT2-'+sg.WRITE_ONLY_KEY)],
            [sg.Text('Tokens:')],
            [sg.MLine(size=(100,8), key='-OUTPUT3-'+sg.WRITE_ONLY_KEY)],
            [sg.Text('Productions:')],
            [sg.MLine(size=(100,8), key='-OUTPUT4-'+sg.WRITE_ONLY_KEY)],
            [sg.Button('Ok')]  ]

    # Main Window
    window = sg.Window('Scanner generado', layout, finalize=True)

    # Output from characters
    for i in reader.comp_chars:
        window['-OUTPUT1-'+sg.WRITE_ONLY_KEY].print(i[0] + " -> " + i[1])
        window['-OUTPUT1-'+sg.WRITE_ONLY_KEY].print(i[2])
    
    # Output from keywords
    for i in reader.comp_keywords:
        window['-OUTPUT2-'+sg.WRITE_ONLY_KEY].print(i[0])
        window['-OUTPUT2-'+sg.WRITE_ONLY_KEY].print(i[3])
    
    # Output from tokens
    for i in reader.comp_tokens:
        window['-OUTPUT3-'+sg.WRITE_ONLY_KEY].print(i[0])
        window['-OUTPUT3-'+sg.WRITE_ONLY_KEY].print(i[3])

     # Output from prodcutions
    for i in reader.comp_producs:
        window['-OUTPUT4-'+sg.WRITE_ONLY_KEY].print("Name: " + str(i[0]))
        window['-OUTPUT4-'+sg.WRITE_ONLY_KEY].print("   Arguments: " + str(i[1]))
        window['-OUTPUT4-'+sg.WRITE_ONLY_KEY].print("   Array:     " + str(i[2]) + "\n")

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
fname = sg.popup_get_file('Document to open',initial_folder=str(os.getcwd() + "/Pruebas_ATG"))

# Split Exit | Read File
if not fname:
    raise SystemExit()
else:
    # Read file
    reader = cr(fname)
    reader.startReading()
    
    try:
        # Write scanner & parser
        writer = cw(reader.comp_name)
        writer.setKeywords(reader.comp_keywords)
        writer.setTokens(reader.comp_tokens)
        writer.setProductionsTokens(reader.comp_producs_toks)
        writer.setIgnoreChars(reader.comp_ignore)
        writer.setProductions(reader.comp_producs)
        writer.startWritingScanner()
        writer.startWritingParser()

    except:
        # Caso de error en escritura
        sg.popup('Error en creacion de scanner (revisar definicion de compilador)')
        exit()
    
    # Popup de creacion correcta
    sg.popup('Scanner creado correctamente \nArchivo creado/modificado: scanner.py')

    # Display data
    display(reader, writer)