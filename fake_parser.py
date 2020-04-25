from scanner import Scanner
import PySimpleGUI as sg
import sys

# Load file
sg.theme('DarkAmber')
fname = sg.popup_get_file('Open test file')

if not fname:
    raise SystemExit()

frame_layout_tokens =  [  [sg.Text('Tokens Found:')],
    [sg.MLine(size=(50,18), key='-OUTPUT1-'+sg.WRITE_ONLY_KEY)],
    [sg.Text('Non Tokens Found:')],
    [sg.MLine(size=(50,4), key='-OUTPUT2-'+sg.WRITE_ONLY_KEY)]]

frame_layout_summary =  [ [sg.Text('')],
    [sg.MLine(size=(50,24), key='-OUTPUT3-'+sg.WRITE_ONLY_KEY)] ]

# Layout
layout = [ [sg.Frame('Elements', frame_layout_tokens) ,sg.Frame('Summary', frame_layout_summary)],
    [sg.Button('Ok')] ]

# layout = [ [sg.Column(col) ]]

window = sg.Window('Parser', layout, finalize=True)

# Initialize scanner
sc = Scanner(fname)

# token variables
token = (None, None)
nontokens_found = []
nontokens_counter = 0
tokens_found = []
tokens_counter = []

# Scan simulation
while token[1] != "end_token":
    # scan
    token = sc.scan()

    # case of non token
    if token[1] == "not_a_token":
        nontokens_found.append(token[0])
        nontokens_counter += 1

    # case of token
    elif token[1] != "end_token":
        if token[1] in tokens_found:
            tokens_counter[tokens_found.index(token[1])] += 1
        else:
            tokens_found.append(token[1])
            tokens_counter.append(1)

        name = token[1]
        tok = token[0]

        tok = tok.replace("\n","\\n")
        tok = tok.replace("\r","\\r")
        tok = tok.replace("\t","\\t")
        window['-OUTPUT1-'+sg.WRITE_ONLY_KEY].print(name + " | \"" + tok + "\"")

    else:
        window['-OUTPUT1-'+sg.WRITE_ONLY_KEY].print("END reached at exit " + str(token[0]))

window['-OUTPUT2-'+sg.WRITE_ONLY_KEY].print("non tokens: " + str(nontokens_counter))
window['-OUTPUT2-'+sg.WRITE_ONLY_KEY].print(nontokens_found)

for i in range(len(tokens_found)):
    window['-OUTPUT3-'+sg.WRITE_ONLY_KEY].print(tokens_found[i] + ": " + str(tokens_counter[i]))


# Event display loop
while True: 
    event, values = window.read()
    if event in (None, 'Ok'):
        break

# Exit
window.close()

