# fake_parser.py
# By: Luis Diego Fernandez
# The program uses a scanner class to look for tokens in a certain text file.
from my_parser import Parser
import PySimpleGUI as sg
import sys
import os

# Load file to test parser.py
sg.theme('DarkAmber')
fname = sg.popup_get_file('Open test file',initial_folder=str(os.getcwd() + "/Pruebas_prog"))

# Exit in case of no file load
if not fname:
    raise SystemExit()

ps = Parser(fname)

